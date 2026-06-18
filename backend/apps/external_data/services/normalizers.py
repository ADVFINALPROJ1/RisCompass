"""
Normalizers for converting economic indicators to risk scores (0-100).
Higher risk scores indicate higher risk.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def normalize_inflation_to_risk(inflation_rate: Optional[float]) -> int:
    """
    Convert inflation rate to a risk score (0-100).
    
    Higher inflation is generally riskier for economic stability.
    Deflation (negative inflation) is also risky.
    
    Args:
        inflation_rate: Annual inflation rate as percentage (e.g., 5.2 for 5.2%)
    
    Returns:
        Risk score from 0 (low risk) to 100 (high risk)
    """
    if inflation_rate is None:
        logger.warning("Inflation rate is None, returning medium risk")
        return 50
    
    try:
        inflation_rate = float(inflation_rate)
    except (ValueError, TypeError):
        logger.warning(f"Invalid inflation rate: {inflation_rate}, returning medium risk")
        return 50
    
    # Deflation (negative inflation) is risky
    if inflation_rate < 0:
        # Scale deflation risk: -10% or worse = 100 risk, 0% = 50 risk
        risk_score = min(100, 50 + abs(inflation_rate) * 5)
        return int(risk_score)
    
    # Low inflation (0-2%): Low risk
    if inflation_rate <= 2:
        risk_score = inflation_rate * 10  # 0% = 0, 2% = 20
        return int(risk_score)
    
    # Moderate inflation (2-4%): Low to moderate risk
    if inflation_rate <= 4:
        risk_score = 20 + (inflation_rate - 2) * 10  # 2% = 20, 4% = 40
        return int(risk_score)
    
    # Medium-high inflation (4-7%): Moderate to high risk
    if inflation_rate <= 7:
        risk_score = 40 + (inflation_rate - 4) * 6.67  # 4% = 40, 7% = 60
        return int(risk_score)
    
    # High inflation (7-10%): High risk
    if inflation_rate <= 10:
        risk_score = 60 + (inflation_rate - 7) * 6.67  # 7% = 60, 10% = 80
        return int(risk_score)
    
    # Very high inflation (10%+): Very high risk
    # Cap at 100 for 20%+ inflation
    risk_score = min(100, 80 + (inflation_rate - 10) * 10)
    return int(risk_score)


def normalize_unemployment_to_risk(unemployment_rate: Optional[float]) -> int:
    """
    Convert unemployment rate to a risk score (0-100).
    
    Higher unemployment is riskier for social and economic stability.
    
    Args:
        unemployment_rate: Unemployment rate as percentage (e.g., 5.5 for 5.5%)
    
    Returns:
        Risk score from 0 (low risk) to 100 (high risk)
    """
    if unemployment_rate is None:
        logger.warning("Unemployment rate is None, returning medium risk")
        return 50
    
    try:
        unemployment_rate = float(unemployment_rate)
    except (ValueError, TypeError):
        logger.warning(f"Invalid unemployment rate: {unemployment_rate}, returning medium risk")
        return 50
    
    # Negative values are invalid, treat as high risk
    if unemployment_rate < 0:
        logger.warning(f"Negative unemployment rate: {unemployment_rate}, returning high risk")
        return 80
    
    # Very low unemployment (0-3%): Very low risk
    if unemployment_rate <= 3:
        risk_score = unemployment_rate * 6.67  # 0% = 0, 3% = 20
        return int(risk_score)
    
    # Low unemployment (3-5%): Low risk
    if unemployment_rate <= 5:
        risk_score = 20 + (unemployment_rate - 3) * 10  # 3% = 20, 5% = 40
        return int(risk_score)
    
    # Moderate unemployment (5-7%): Moderate risk
    if unemployment_rate <= 7:
        risk_score = 40 + (unemployment_rate - 5) * 10  # 5% = 40, 7% = 60
        return int(risk_score)
    
    # High unemployment (7-10%): High risk
    if unemployment_rate <= 10:
        risk_score = 60 + (unemployment_rate - 7) * 6.67  # 7% = 60, 10% = 80
        return int(risk_score)
    
    # Very high unemployment (10%+): Very high risk
    # Cap at 100 for 20%+ unemployment
    risk_score = min(100, 80 + (unemployment_rate - 10) * 5)
    return int(risk_score)


def normalize_internet_usage_to_risk(internet_usage: Optional[float]) -> int:
    """
    Convert internet usage rate to a risk score (0-100).
    
    Higher internet usage is generally less risky (better connectivity, 
    information access, digital infrastructure).
    
    Args:
        internet_usage: Internet usage as percentage of population (e.g., 75.5 for 75.5%)
    
    Returns:
        Risk score from 0 (low risk) to 100 (high risk)
    """
    if internet_usage is None:
        logger.warning("Internet usage is None, returning medium risk")
        return 50
    
    try:
        internet_usage = float(internet_usage)
    except (ValueError, TypeError):
        logger.warning(f"Invalid internet usage: {internet_usage}, returning medium risk")
        return 50
    
    # Clamp to valid range 0-100
    internet_usage = max(0, min(100, internet_usage))
    
    # Very high internet usage (80-100%): Very low risk
    if internet_usage >= 80:
        risk_score = (100 - internet_usage) * 1  # 100% = 0, 80% = 20
        return int(risk_score)
    
    # High internet usage (60-80%): Low risk
    if internet_usage >= 60:
        risk_score = 20 + (80 - internet_usage)  # 80% = 20, 60% = 40
        return int(risk_score)
    
    # Moderate internet usage (40-60%): Moderate risk
    if internet_usage >= 40:
        risk_score = 40 + (60 - internet_usage)  # 60% = 40, 40% = 60
        return int(risk_score)
    
    # Low internet usage (20-40%): High risk
    if internet_usage >= 20:
        risk_score = 60 + (40 - internet_usage) * 1.5  # 40% = 60, 20% = 90
        return int(risk_score)
    
    # Very low internet usage (0-20%): Very high risk
    risk_score = 90 + (20 - internet_usage) * 0.5  # 20% = 90, 0% = 100
    return int(risk_score)


def normalize_gdp_growth_to_risk(gdp_growth: Optional[float]) -> int:
    """
    Convert GDP growth rate to a risk score (0-100).
    
    Higher GDP growth is generally less risky (stronger economy).
    Negative growth (recession) is very risky.
    
    Args:
        gdp_growth: Annual GDP growth rate as percentage (e.g., 3.5 for 3.5%)
    
    Returns:
        Risk score from 0 (low risk) to 100 (high risk)
    """
    if gdp_growth is None:
        logger.warning("GDP growth is None, returning medium risk")
        return 50
    
    try:
        gdp_growth = float(gdp_growth)
    except (ValueError, TypeError):
        logger.warning(f"Invalid GDP growth: {gdp_growth}, returning medium risk")
        return 50
    
    # Negative growth (recession): Very high risk
    if gdp_growth < 0:
        # Scale: -10% or worse = 100 risk, 0% = 80 risk
        risk_score = min(100, 80 + abs(gdp_growth) * 2)
        return int(risk_score)
    
    # Very low growth (0-1%): High risk
    if gdp_growth <= 1:
        risk_score = 80 - gdp_growth * 20  # 0% = 80, 1% = 60
        return int(risk_score)
    
    # Low growth (1-3%): Moderate to high risk
    if gdp_growth <= 3:
        risk_score = 60 - (gdp_growth - 1) * 10  # 1% = 60, 3% = 40
        return int(risk_score)
    
    # Moderate growth (3-5%): Low to moderate risk
    if gdp_growth <= 5:
        risk_score = 40 - (gdp_growth - 3) * 10  # 3% = 40, 5% = 20
        return int(risk_score)
    
    # High growth (5%+): Very low risk
    # Cap at 0 for 10%+ growth
    risk_score = max(0, 20 - (gdp_growth - 5) * 4)
    return int(risk_score)
