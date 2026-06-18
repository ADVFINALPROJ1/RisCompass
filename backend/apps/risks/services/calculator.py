"""
Risk calculator for computing risk scores from economic indicators.
"""
import logging
from typing import Dict, Optional, Tuple
from apps.external_data.services.normalizers import (
    normalize_inflation_to_risk,
    normalize_unemployment_to_risk,
    normalize_internet_usage_to_risk,
    normalize_gdp_growth_to_risk,
)
from apps.external_data.services.world_bank import fetch_world_bank_indicator
from .mappings import WORLD_BANK_INDICATORS, RISK_CATEGORIES, get_confidence_label

logger = logging.getLogger(__name__)


class RiskCalculator:
    """
    Calculator for computing risk scores from economic indicators.
    """

    def __init__(self, country_code: str):
        self.country_code = country_code
        self.economic_data = {}
        self.data_sources = []

    def fetch_economic_data(self) -> Dict[str, Optional[float]]:
        """
        Fetch economic data from World Bank API.
        
        Returns:
            Dictionary with indicator names as keys and values as values
        """
        data = {}
        
        for indicator_name, indicator_code in WORLD_BANK_INDICATORS.items():
            try:
                result = fetch_world_bank_indicator(self.country_code, indicator_code)
                if result and 'value' in result:
                    data[indicator_name] = result['value']
                    self.data_sources.append(f"World Bank: {indicator_code}")
                    logger.info(f"Fetched {indicator_name}: {result['value']}")
                else:
                    data[indicator_name] = None
                    logger.warning(f"No data available for {indicator_name} ({indicator_code})")
            except Exception as e:
                logger.error(f"Error fetching {indicator_name}: {e}")
                data[indicator_name] = None
        
        self.economic_data = data
        return data

    def calculate_financial_risk(self) -> int:
        """
        Calculate financial risk from inflation and unemployment.
        
        Formula: Average of inflation risk and unemployment risk
        """
        inflation = self.economic_data.get('inflation')
        unemployment = self.economic_data.get('unemployment')
        
        inflation_risk = normalize_inflation_to_risk(inflation)
        unemployment_risk = normalize_unemployment_to_risk(unemployment)
        
        financial_risk = (inflation_risk + unemployment_risk) // 2
        logger.info(f"Financial risk: {financial_risk} (inflation: {inflation_risk}, unemployment: {unemployment_risk})")
        
        return financial_risk

    def calculate_market_risk(self) -> int:
        """
        Calculate market risk from GDP growth and unemployment.
        
        Formula: Average of GDP growth risk and unemployment risk
        """
        gdp_growth = self.economic_data.get('gdp_growth')
        unemployment = self.economic_data.get('unemployment')
        
        gdp_risk = normalize_gdp_growth_to_risk(gdp_growth)
        unemployment_risk = normalize_unemployment_to_risk(unemployment)
        
        market_risk = (gdp_risk + unemployment_risk) // 2
        logger.info(f"Market risk: {market_risk} (GDP: {gdp_risk}, unemployment: {unemployment_risk})")
        
        return market_risk

    def calculate_operational_risk(self) -> int:
        """
        Calculate operational risk from internet usage.
        
        Formula: Internet usage risk directly
        """
        internet_usage = self.economic_data.get('internet_usage')
        
        operational_risk = normalize_internet_usage_to_risk(internet_usage)
        logger.info(f"Operational risk: {operational_risk} (internet usage: {internet_usage})")
        
        return operational_risk

    def calculate_legal_risk(self) -> int:
        """
        Calculate legal risk (default value).
        
        Formula: Default to 50 (medium risk)
        """
        legal_risk = 50
        logger.info(f"Legal risk: {legal_risk} (default)")
        return legal_risk

    def calculate_cultural_risk(self) -> int:
        """
        Calculate cultural risk (default value).
        
        Formula: Default to 50 (medium risk)
        """
        cultural_risk = 50
        logger.info(f"Cultural risk: {cultural_risk} (default)")
        return cultural_risk

    def apply_industry_weights(
        self,
        financial_risk: int,
        market_risk: int,
        legal_risk: int,
        cultural_risk: int,
        operational_risk: int,
        industry_weights: Dict[str, float]
    ) -> Tuple[int, int, int, int, int]:
        """
        Apply industry-specific risk weights to risk scores.
        
        Args:
            financial_risk: Raw financial risk score
            market_risk: Raw market risk score
            legal_risk: Raw legal risk score
            cultural_risk: Raw cultural risk score
            operational_risk: Raw operational risk score
            industry_weights: Dictionary with weight values for each category
        
        Returns:
            Tuple of weighted risk scores (financial, market, legal, cultural, operational)
        """
        weighted_financial = int(financial_risk * industry_weights.get('financial_weight', 0.2))
        weighted_market = int(market_risk * industry_weights.get('market_weight', 0.2))
        weighted_legal = int(legal_risk * industry_weights.get('legal_weight', 0.2))
        weighted_cultural = int(cultural_risk * industry_weights.get('cultural_weight', 0.2))
        weighted_operational = int(operational_risk * industry_weights.get('operational_weight', 0.2))
        
        logger.info(f"Weighted risks - Financial: {weighted_financial}, Market: {weighted_market}, "
                   f"Legal: {weighted_legal}, Cultural: {weighted_cultural}, Operational: {weighted_operational}")
        
        return (
            weighted_financial,
            weighted_market,
            weighted_legal,
            weighted_cultural,
            weighted_operational,
        )

    def calculate_overall_risk(
        self,
        financial_risk: int,
        market_risk: int,
        legal_risk: int,
        cultural_risk: int,
        operational_risk: int
    ) -> int:
        """
        Calculate overall risk score from individual risk categories.
        
        Formula: Average of all risk categories
        """
        overall = (financial_risk + market_risk + legal_risk + cultural_risk + operational_risk) // 5
        logger.info(f"Overall risk: {overall}")
        return overall

    def calculate_confidence_score(self) -> int:
        """
        Calculate confidence score based on data availability.
        
        Formula: Percentage of indicators that have data
        """
        total_indicators = len(WORLD_BANK_INDICATORS)
        available_indicators = sum(1 for value in self.economic_data.values() if value is not None)
        
        confidence = int((available_indicators / total_indicators) * 100)
        logger.info(f"Confidence score: {confidence} ({available_indicators}/{total_indicators} indicators available)")
        
        return confidence
