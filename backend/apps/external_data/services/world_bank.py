import requests
import logging
from django.conf import settings
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def fetch_world_bank_indicator(country_code: str, indicator_code: str) -> Optional[Dict]:
    """
    Fetch data from World Bank API for a specific country and indicator.
    
    Args:
        country_code: ISO country code (e.g., 'US', 'GB', 'FR')
        indicator_code: World Bank indicator code (e.g., 'FP.CPI.TOTL.ZG' for inflation)
    
    Returns:
        Dictionary with keys: country_code, indicator_code, year, value, source
        Returns None if fetch fails or no valid data found
    """
    try:
        base_url = getattr(settings, 'WORLD_BANK_API_BASE_URL', 'https://api.worldbank.org/v2')
        url = f"{base_url}/country/{country_code}/indicator/{indicator_code}?format=json"
        
        logger.info(f"Fetching World Bank data: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # World Bank API returns [metadata, data] or [error] structure
        if not data or len(data) < 2:
            logger.warning(f"No data returned from World Bank API for {country_code}/{indicator_code}")
            return None
        
        # Check if the first element contains error information
        if isinstance(data[0], dict) and data[0].get('message'):
            logger.error(f"World Bank API error: {data[0].get('message')}")
            return None
        
        records = data[1]
        
        if not records:
            logger.warning(f"No records found for {country_code}/{indicator_code}")
            return None
        
        # Find the latest non-null value
        latest_record = None
        for record in records:
            if record.get('value') is not None:
                latest_record = record
                break  # Records are already sorted by date descending
        
        if not latest_record:
            logger.warning(f"No non-null values found for {country_code}/{indicator_code}")
            return None
        
        result = {
            'country_code': country_code,
            'indicator_code': indicator_code,
            'year': latest_record.get('date'),
            'value': latest_record.get('value'),
            'source': 'World Bank'
        }
        
        logger.info(f"Successfully fetched data for {country_code}/{indicator_code}: {result}")
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error fetching World Bank data for {country_code}/{indicator_code}: {e}")
        return None
    except (ValueError, KeyError, IndexError) as e:
        logger.error(f"Data parsing error for {country_code}/{indicator_code}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching World Bank data for {country_code}/{indicator_code}: {e}")
        return None
