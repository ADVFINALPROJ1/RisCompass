"""
Service for generating risk reports from business snapshots.
"""
import logging
from typing import Dict
from apps.snapshots.models import BusinessSnapshot
from apps.industries.models import IndustryRiskWeight
from .models import RiskReport, RiskFactor
from .calculator import RiskCalculator
from .mappings import get_confidence_label, RISK_CATEGORIES

logger = logging.getLogger(__name__)


def generate_risk_report(snapshot: BusinessSnapshot) -> RiskReport:
    """
    Generate a risk report for a business snapshot.
    
    Logic:
    1. Fetch World Bank data for inflation, unemployment, internet usage, and GDP growth.
    2. Normalize values into risk scores.
    3. Calculate:
       - financial_risk from inflation and unemployment
       - market_risk from GDP growth and unemployment
       - operational_risk from internet usage
       - legal_risk default 50
       - cultural_risk default 50
    4. Apply IndustryRiskWeight.
    5. Save RiskReport.
    6. Save RiskFactors.
    7. Return report.
    
    Args:
        snapshot: BusinessSnapshot instance
    
    Returns:
        RiskReport instance
    """
    logger.info(f"Generating risk report for snapshot: {snapshot.title}")
    
    # Get country code from region
    country_code = snapshot.region.country_code
    
    # Initialize calculator
    calculator = RiskCalculator(country_code)
    
    # Fetch economic data from World Bank
    economic_data = calculator.fetch_economic_data()
    
    # Calculate individual risk scores
    financial_risk = calculator.calculate_financial_risk()
    market_risk = calculator.calculate_market_risk()
    operational_risk = calculator.calculate_operational_risk()
    legal_risk = calculator.calculate_legal_risk()
    cultural_risk = calculator.calculate_cultural_risk()
    
    # Apply industry weights if available
    try:
        industry_weight = IndustryRiskWeight.objects.get(industry=snapshot.industry)
        weights = {
            'financial_weight': float(industry_weight.financial_weight),
            'market_weight': float(industry_weight.market_weight),
            'legal_weight': float(industry_weight.legal_weight),
            'cultural_weight': float(industry_weight.cultural_weight),
            'operational_weight': float(industry_weight.operational_weight),
        }
        financial_risk, market_risk, legal_risk, cultural_risk, operational_risk = \
            calculator.apply_industry_weights(
                financial_risk, market_risk, legal_risk, cultural_risk, operational_risk, weights
            )
    except IndustryRiskWeight.DoesNotExist:
        logger.warning(f"No industry risk weight found for {snapshot.industry.name}, using unweighted scores")
    
    # Calculate overall risk score
    overall_risk_score = calculator.calculate_overall_risk(
        financial_risk, market_risk, legal_risk, cultural_risk, operational_risk
    )
    
    # Calculate confidence score
    confidence_score = calculator.calculate_confidence_score()
    confidence_label = get_confidence_label(confidence_score)
    
    # Generate summary and recommendation based on overall risk
    summary, recommendation = _generate_summary_and_recommendation(
        overall_risk_score,
        financial_risk,
        market_risk,
        legal_risk,
        cultural_risk,
        operational_risk
    )
    
    # Create RiskReport
    risk_report = RiskReport.objects.create(
        snapshot=snapshot,
        overall_risk_score=overall_risk_score,
        confidence_score=confidence_score,
        confidence_label=confidence_label,
        financial_risk=financial_risk,
        market_risk=market_risk,
        legal_risk=legal_risk,
        cultural_risk=cultural_risk,
        operational_risk=operational_risk,
        summary=summary,
        recommendation=recommendation,
        data_sources_used=calculator.data_sources
    )
    
    # Create RiskFactors
    _create_risk_factors(risk_report, economic_data)
    
    logger.info(f"Risk report generated successfully with ID: {risk_report.id}")
    return risk_report


def _generate_summary_and_recommendation(
    overall_risk: int,
    financial_risk: int,
    market_risk: int,
    legal_risk: int,
    cultural_risk: int,
    operational_risk: int
) -> tuple:
    """
    Generate summary and recommendation based on risk scores.
    """
    # Determine overall risk level
    if overall_risk < 20:
        risk_level = "Very Low"
        summary = f"Overall risk level is very low ({overall_risk}/100). "
    elif overall_risk < 40:
        risk_level = "Low"
        summary = f"Overall risk level is low ({overall_risk}/100). "
    elif overall_risk < 60:
        risk_level = "Medium"
        summary = f"Overall risk level is medium ({overall_risk}/100). "
    elif overall_risk < 80:
        risk_level = "High"
        summary = f"Overall risk level is high ({overall_risk}/100). "
    else:
        risk_level = "Very High"
        summary = f"Overall risk level is very high ({overall_risk}/100). "
    
    # Add category-specific information
    summary += f"Financial risk: {financial_risk}, Market risk: {market_risk}, "
    summary += f"Legal risk: {legal_risk}, Cultural risk: {cultural_risk}, Operational risk: {operational_risk}."
    
    # Generate recommendation based on highest risk category
    risk_categories = {
        'Financial': financial_risk,
        'Market': market_risk,
        'Legal': legal_risk,
        'Cultural': cultural_risk,
        'Operational': operational_risk,
    }
    highest_risk_category = max(risk_categories, key=risk_categories.get)
    highest_risk_score = risk_categories[highest_risk_category]
    
    if highest_risk_score >= 70:
        recommendation = f"High {highest_risk_category.lower()} risk detected ({highest_risk_score}/100). "
        recommendation += f"Consider conducting a detailed analysis of {highest_risk_category.lower()} factors "
        recommendation += "and developing mitigation strategies before proceeding."
    elif highest_risk_score >= 50:
        recommendation = f"Moderate {highest_risk_category.lower()} risk detected ({highest_risk_score}/100). "
        recommendation += f"Monitor {highest_risk_category.lower()} conditions closely and "
        recommendation += "be prepared to adjust plans if conditions worsen."
    else:
        recommendation = f"{highest_risk_category.lower()} risk is within acceptable range ({highest_risk_score}/100). "
        recommendation += "Continue monitoring but no immediate action required."
    
    return summary, recommendation


def _create_risk_factors(risk_report: RiskReport, economic_data: Dict[str, float]):
    """
    Create RiskFactor instances for each risk category.
    """
    # Financial risk factors
    RiskFactor.objects.create(
        report=risk_report,
        category=RiskFactor.CATEGORY_FINANCIAL,
        name='Inflation Risk',
        score=risk_report.financial_risk,
        explanation=f"Based on inflation rate: {economic_data.get('inflation', 'N/A')}%",
        source_type=RiskFactor.SOURCE_TYPE_EXTERNAL_API if economic_data.get('inflation') else RiskFactor.SOURCE_TYPE_SYSTEM_DEFAULT
    )
    
    RiskFactor.objects.create(
        report=risk_report,
        category=RiskFactor.CATEGORY_FINANCIAL,
        name='Unemployment Risk',
        score=risk_report.financial_risk,
        explanation=f"Based on unemployment rate: {economic_data.get('unemployment', 'N/A')}%",
        source_type=RiskFactor.SOURCE_TYPE_EXTERNAL_API if economic_data.get('unemployment') else RiskFactor.SOURCE_TYPE_SYSTEM_DEFAULT
    )
    
    # Market risk factors
    RiskFactor.objects.create(
        report=risk_report,
        category=RiskFactor.CATEGORY_MARKET,
        name='GDP Growth Risk',
        score=risk_report.market_risk,
        explanation=f"Based on GDP growth rate: {economic_data.get('gdp_growth', 'N/A')}%",
        source_type=RiskFactor.SOURCE_TYPE_EXTERNAL_API if economic_data.get('gdp_growth') else RiskFactor.SOURCE_TYPE_SYSTEM_DEFAULT
    )
    
    RiskFactor.objects.create(
        report=risk_report,
        category=RiskFactor.CATEGORY_MARKET,
        name='Market Conditions',
        score=risk_report.market_risk,
        explanation="Based on unemployment and GDP growth indicators",
        source_type=RiskFactor.SOURCE_TYPE_EXTERNAL_API if economic_data.get('gdp_growth') or economic_data.get('unemployment') else RiskFactor.SOURCE_TYPE_SYSTEM_DEFAULT
    )
    
    # Operational risk factors
    RiskFactor.objects.create(
        report=risk_report,
        category=RiskFactor.CATEGORY_OPERATIONAL,
        name='Internet Infrastructure',
        score=risk_report.operational_risk,
        explanation=f"Based on internet usage: {economic_data.get('internet_usage', 'N/A')}%",
        source_type=RiskFactor.SOURCE_TYPE_EXTERNAL_API if economic_data.get('internet_usage') else RiskFactor.SOURCE_TYPE_SYSTEM_DEFAULT
    )
    
    # Legal risk factors
    RiskFactor.objects.create(
        report=risk_report,
        category=RiskFactor.CATEGORY_LEGAL,
        name='Legal Environment',
        score=risk_report.legal_risk,
        explanation="Default risk score - requires local legal assessment",
        source_type=RiskFactor.SOURCE_TYPE_SYSTEM_DEFAULT
    )
    
    # Cultural risk factors
    RiskFactor.objects.create(
        report=risk_report,
        category=RiskFactor.CATEGORY_CULTURAL,
        name='Cultural Fit',
        score=risk_report.cultural_risk,
        explanation="Default risk score - requires cultural assessment",
        source_type=RiskFactor.SOURCE_TYPE_SYSTEM_DEFAULT
    )
