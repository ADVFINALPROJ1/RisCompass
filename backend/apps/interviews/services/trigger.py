"""
Interview trigger service for determining when to trigger an interview session.
"""
from typing import Tuple, Optional
from apps.snapshots.models import BusinessSnapshot


def should_trigger_interview(snapshot: BusinessSnapshot, api_data_completeness: Optional[float] = None) -> Tuple[bool, str]:
    """
    Determine whether an interview should be triggered for a given business snapshot.
    
    Args:
        snapshot: BusinessSnapshot instance containing region and industry information
        api_data_completeness: Optional float representing API data completeness (0.0 to 1.0)
    
    Returns:
        Tuple of (should_trigger: bool, trigger_reason: str)
    
    Trigger Rules:
        - Trigger if region.data_availability_level is low or very_low
        - Trigger if region.region_type is rural or remote
        - Trigger if api_data_completeness is below 0.60
        - Trigger for Agriculture in remote regions
    """
    region = snapshot.region
    industry = snapshot.industry
    
    trigger_reasons = []
    
    # Rule 1: Trigger if region.data_availability_level is low or very_low
    if region.data_availability_level in ['low', 'very_low']:
        trigger_reasons.append(f"Region data availability is {region.data_availability_level}")
    
    # Rule 2: Trigger if region.region_type is rural or remote
    if region.region_type in ['rural', 'remote']:
        trigger_reasons.append(f"Region type is {region.region_type}")
    
    # Rule 3: Trigger if api_data_completeness is below 0.60
    if api_data_completeness is not None and api_data_completeness < 0.60:
        trigger_reasons.append(f"API data completeness ({api_data_completeness:.2f}) is below 0.60")
    
    # Rule 4: Trigger for Agriculture in remote regions
    if industry.name.lower() == 'agriculture' and region.region_type == 'remote':
        trigger_reasons.append("Agriculture industry in remote region")
    
    # Determine if interview should be triggered
    should_trigger = len(trigger_reasons) > 0
    
    # Format trigger reason
    if should_trigger:
        trigger_reason = "; ".join(trigger_reasons)
    else:
        trigger_reason = "No trigger conditions met"
    
    return should_trigger, trigger_reason
