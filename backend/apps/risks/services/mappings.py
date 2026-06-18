"""
Mappings for risk categories, World Bank indicators, and risk formulas.
"""

# World Bank indicator codes for economic data
WORLD_BANK_INDICATORS = {
    'inflation': 'FP.CPI.TOTL.ZG',  # Inflation, consumer prices (annual %)
    'unemployment': 'SL.UEM.TOTL.ZS',  # Unemployment, total (% of total labor force)
    'internet_usage': 'IT.NET.USER.ZS',  # Internet users (% of population)
    'gdp_growth': 'NY.GDP.MKTP.KD.ZG',  # GDP growth (annual %)
}

# Risk category mappings
RISK_CATEGORIES = {
    'financial': {
        'name': 'Financial Risk',
        'indicators': ['inflation', 'unemployment'],
        'default_score': 50,
    },
    'market': {
        'name': 'Market Risk',
        'indicators': ['gdp_growth', 'unemployment'],
        'default_score': 50,
    },
    'operational': {
        'name': 'Operational Risk',
        'indicators': ['internet_usage'],
        'default_score': 50,
    },
    'legal': {
        'name': 'Legal Risk',
        'indicators': [],
        'default_score': 50,
    },
    'cultural': {
        'name': 'Cultural Risk',
        'indicators': [],
        'default_score': 50,
    },
}

# Confidence label mappings based on confidence score
CONFIDENCE_LABELS = {
    (0, 20): 'Very Low',
    (21, 40): 'Low',
    (41, 60): 'Medium',
    (61, 80): 'High',
    (81, 100): 'Very High',
}

def get_confidence_label(confidence_score):
    """
    Get confidence label based on confidence score.
    """
    for (min_score, max_score), label in CONFIDENCE_LABELS.items():
        if min_score <= confidence_score <= max_score:
            return label
    return 'Unknown'
