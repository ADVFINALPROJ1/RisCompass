"""
Gemini API service for generating AI insights from interview data.
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from google import genai
from django.conf import settings

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client with API key from settings."""
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set in environment variables")
        try:
            self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.client = None
    
    def _build_prompt(
        self,
        snapshot: Dict[str, Any],
        questions: List[Dict[str, Any]],
        answers: List[Dict[str, Any]]
    ) -> str:
        """
        Build a structured prompt for Gemini API.
        
        Args:
            snapshot: Business snapshot data
            questions: List of interview questions
            answers: List of interview answers
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
You are a risk assessment assistant for RisCompass. Analyze the following business information and interview responses to provide risk insights.

IMPORTANT:
- Return ONLY valid JSON. No markdown formatting, no code blocks, no additional text.
- Do NOT provide legal advice. This is for informational purposes only.
- Risk signals should be integers from 0 (low risk) to 100 (high risk).
- Base your assessment on the provided data and interview answers.

BUSINESS SNAPSHOT:
- Company Name: {snapshot.get('company_name', 'N/A')}
- Industry: {snapshot.get('industry', 'N/A')}
- Region: {snapshot.get('region', 'N/A')}
- Description: {snapshot.get('description', 'N/A')}

INTERVIEW QUESTIONS AND ANSWERS:
"""
        
        # Map answers to questions
        answer_map = {ans.get('question_id'): ans for ans in answers}
        
        for question in questions:
            q_id = question.get('id')
            q_text = question.get('question_text', '')
            q_category = question.get('risk_category', '')
            
            answer = answer_map.get(q_id, {})
            ans_text = answer.get('answer_text', '')
            ans_value = answer.get('answer_value', '')
            
            prompt += f"\n[Category: {q_category}]\n"
            prompt += f"Question: {q_text}\n"
            prompt += f"Answer: {ans_text or ans_value or 'No answer'}\n"
        
        prompt += """

REQUIRED JSON OUTPUT FORMAT:
{
  "summary": "Brief summary of the business risk profile based on the interview",
  "financial_risk_signal": 0-100,
  "market_risk_signal": 0-100,
  "legal_risk_signal": 0-100,
  "cultural_risk_signal": 0-100,
  "operational_risk_signal": 0-100,
  "recommended_warnings": ["Warning 1", "Warning 2", ...]
}

Return ONLY the JSON object, nothing else.
"""
        return prompt
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Safely parse JSON response from Gemini.
        
        Args:
            response_text: Raw response text from Gemini
            
        Returns:
            Parsed JSON dict or fallback values if parsing fails
        """
        fallback_values = {
            "summary": "Unable to generate summary due to parsing error",
            "financial_risk_signal": 50,
            "market_risk_signal": 50,
            "legal_risk_signal": 50,
            "cultural_risk_signal": 50,
            "operational_risk_signal": 50,
            "recommended_warnings": []
        }
        
        if not response_text:
            logger.error("Empty response from Gemini API")
            return fallback_values
        
        # Try to extract JSON from response (in case it's wrapped in markdown)
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks if present
        if cleaned_text.startswith("```"):
            lines = cleaned_text.split("\n")
            json_lines = []
            in_json = False
            for line in lines:
                if line.strip().startswith("```"):
                    if in_json:
                        break
                    in_json = True
                    continue
                if in_json:
                    json_lines.append(line)
            cleaned_text = "\n".join(json_lines)
        
        # Remove any leading/trailing whitespace
        cleaned_text = cleaned_text.strip()
        
        try:
            parsed = json.loads(cleaned_text)
            
            # Validate required fields
            required_fields = [
                "summary",
                "financial_risk_signal",
                "market_risk_signal",
                "legal_risk_signal",
                "cultural_risk_signal",
                "operational_risk_signal",
                "recommended_warnings"
            ]
            
            for field in required_fields:
                if field not in parsed:
                    logger.warning(f"Missing required field '{field}' in Gemini response")
                    if field.endswith("_signal"):
                        parsed[field] = 50
                    elif field == "recommended_warnings":
                        parsed[field] = []
                    else:
                        parsed[field] = ""
            
            # Ensure risk signals are integers between 0 and 100
            signal_fields = [
                "financial_risk_signal",
                "market_risk_signal",
                "legal_risk_signal",
                "cultural_risk_signal",
                "operational_risk_signal"
            ]
            
            for field in signal_fields:
                try:
                    value = int(parsed[field])
                    parsed[field] = max(0, min(100, value))
                except (ValueError, TypeError):
                    logger.warning(f"Invalid value for {field}: {parsed[field]}")
                    parsed[field] = 50
            
            # Ensure recommended_warnings is a list
            if not isinstance(parsed["recommended_warnings"], list):
                logger.warning("recommended_warnings is not a list, converting")
                parsed["recommended_warnings"] = []
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Gemini response: {e}")
            logger.debug(f"Response text: {response_text[:500]}")
            return fallback_values
        except Exception as e:
            logger.error(f"Unexpected error parsing Gemini response: {e}")
            return fallback_values
    
    def generate_insights(
        self,
        snapshot: Dict[str, Any],
        questions: List[Dict[str, Any]],
        answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate AI insights using Gemini API.
        
        Args:
            snapshot: Business snapshot data
            questions: List of interview questions
            answers: List of interview answers
            
        Returns:
            Dict containing risk signals and recommendations
        """
        if not self.client:
            logger.error("Gemini client not initialized. Check GEMINI_API_KEY.")
            return self._parse_json_response("")
        
        try:
            # Build the prompt
            prompt = self._build_prompt(snapshot, questions, answers)
            
            # Call Gemini API
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt
            )
            
            # Extract response text
            response_text = response.text if response else ""
            
            if not response_text:
                logger.error("Empty response from Gemini API")
                return self._parse_json_response("")
            
            # Parse and validate JSON response
            insights = self._parse_json_response(response_text)
            
            logger.info("Successfully generated insights from Gemini API")
            return insights
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return self._parse_json_response("")
