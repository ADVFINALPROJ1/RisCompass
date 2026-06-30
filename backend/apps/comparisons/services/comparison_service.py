from apps.risks.models import RiskReport
from apps.comparisons.models import Comparison


def create_comparison(user, snapshot_a, snapshot_b, filter_focus):
    """
    Create a comparison between two business snapshots based on their risk reports.
    
    Args:
        user: The user creating the comparison
        snapshot_a: First BusinessSnapshot to compare
        snapshot_b: Second BusinessSnapshot to compare
        filter_focus: The risk category to focus on (overall, financial, market, legal, cultural, operational)
    
    Returns:
        Comparison: The created comparison object
    
    Raises:
        ValueError: If risk reports are not found for either snapshot
    """
    # Get latest RiskReport for both snapshots
    try:
        report_a = RiskReport.objects.filter(snapshot=snapshot_a).latest('created_at')
    except RiskReport.DoesNotExist:
        raise ValueError(f"No risk report found for snapshot: {snapshot_a.title}")
    
    try:
        report_b = RiskReport.objects.filter(snapshot=snapshot_b).latest('created_at')
    except RiskReport.DoesNotExist:
        raise ValueError(f"No risk report found for snapshot: {snapshot_b.title}")
    
    # Map filter_focus to the appropriate risk score field
    score_field_map = {
        Comparison.FILTER_FOCUS_OVERALL: 'overall_risk_score',
        Comparison.FILTER_FOCUS_FINANCIAL: 'financial_risk',
        Comparison.FILTER_FOCUS_MARKET: 'market_risk',
        Comparison.FILTER_FOCUS_LEGAL: 'legal_risk',
        Comparison.FILTER_FOCUS_CULTURAL: 'cultural_risk',
        Comparison.FILTER_FOCUS_OPERATIONAL: 'operational_risk',
    }
    
    score_field = score_field_map.get(filter_focus, 'overall_risk_score')
    
    # Get the scores for comparison
    score_a = getattr(report_a, score_field)
    score_b = getattr(report_b, score_field)
    
    # Determine winner (lower risk score wins)
    winner_snapshot = None
    summary_parts = []
    
    if score_a < score_b:
        winner_snapshot = snapshot_a
        summary_parts.append(
            f"Snapshot A ({snapshot_a.title}) wins with a {filter_focus} risk score of {score_a}, "
            f"compared to Snapshot B's ({snapshot_b.title}) score of {score_b}."
        )
    elif score_b < score_a:
        winner_snapshot = snapshot_b
        summary_parts.append(
            f"Snapshot B ({snapshot_b.title}) wins with a {filter_focus} risk score of {score_b}, "
            f"compared to Snapshot A's ({snapshot_a.title}) score of {score_a}."
        )
    else:
        summary_parts.append(
            f"Both snapshots have the same {filter_focus} risk score of {score_a}. "
            f"It's a tie between Snapshot A ({snapshot_a.title}) and Snapshot B ({snapshot_b.title})."
        )
    
    # Add additional context to summary
    summary_parts.append(
        f"\n\nComparison based on {filter_focus} risk category. "
        f"Lower risk scores indicate lower risk."
    )
    
    summary = ''.join(summary_parts)
    
    # Create and save the comparison
    comparison = Comparison.objects.create(
        user=user,
        snapshot_a=snapshot_a,
        snapshot_b=snapshot_b,
        title=f"Comparison: {snapshot_a.title} vs {snapshot_b.title}",
        filter_focus=filter_focus,
        winner_snapshot=winner_snapshot,
        summary=summary
    )
    
    return comparison
