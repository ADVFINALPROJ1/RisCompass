"""
Confidence score calculator for business risk assessments.
"""
import logging
from typing import Dict, Tuple
from apps.snapshots.models import BusinessSnapshot
from apps.regions.models import Region

logger = logging.getLogger(__name__)


class ConfidenceScoreCalculator:
    """
    Calculator for computing confidence scores based on data availability,
    region support, and interview completion.
    """

    # Region support scores based on region type and data availability
    REGION_SUPPORT_SCORES = {
        # Supported major urban region
        ('urban', 'high'): 100,
        ('urban', 'medium'): 100,
        # Supported medium-data region
        ('suburban', 'high'): 70,
        ('suburban', 'medium'): 70,
        ('urban', 'low'): 70,
        # Rural or remote
        ('rural', 'high'): 45,
        ('rural', 'medium'): 45,
        ('rural', 'low'): 45,
        ('remote', 'high'): 45,
        ('remote', 'medium'): 45,
        ('remote', 'low'): 45,
        # Unsupported/manual region
        ('suburban', 'low'): 25,
        ('urban', 'very_low'): 25,
        ('suburban', 'very_low'): 25,
        ('rural', 'very_low'): 25,
        ('remote', 'very_low'): 25,
    }

    # Confidence labels based on score ranges
    CONFIDENCE_LABELS = {
        (85, 100): 'High Confidence',
        (70, 84): 'Good Confidence',
        (50, 69): 'Informed Guess',
        (30, 49): 'Low Confidence',
        (0, 29): 'Very Low Confidence',
    }

    @staticmethod
    def get_region_support_score(region: Region) -> int:
        """
        Get region support score based on region type and data availability.

        Args:
            region: Region model instance

        Returns:
            Region support score (0-100)
        """
        region_type = region.region_type
        data_availability = region.data_availability_level

        # Look up score in mapping
        score = ConfidenceScoreCalculator.REGION_SUPPORT_SCORES.get(
            (region_type, data_availability)
        )

        if score is None:
            # Default to very low confidence for unknown combinations
            logger.warning(
                f"Unknown region combination: {region_type}, {data_availability}. "
                f"Defaulting to score of 25."
            )
            return 25

        logger.info(f"Region support score: {score} (type: {region_type}, data: {data_availability})")
        return score

    @staticmethod
    def get_confidence_label(score: int) -> str:
        """
        Get confidence label based on score.

        Args:
            score: Confidence score (0-100)

        Returns:
            Confidence label string
        """
        for (min_score, max_score), label in ConfidenceScoreCalculator.CONFIDENCE_LABELS.items():
            if min_score <= score <= max_score:
                return label

        # Fallback for edge cases
        if score > 100:
            return 'High Confidence'
        if score < 0:
            return 'Very Low Confidence'

        return 'Unknown'

    @staticmethod
    def calculate_interview_completion_score(
        interview_required: bool,
        interview_completed: bool
    ) -> int:
        """
        Calculate interview completion score.

        Args:
            interview_required: Whether an interview was required
            interview_completed: Whether the interview was completed

        Returns:
            Interview completion score (0-100)
        """
        if not interview_required:
            # If interview not required, this factor doesn't apply
            return 100

        if interview_completed:
            return 100
        else:
            return 0

    @classmethod
    def calculate_confidence_score(
        cls,
        snapshot: BusinessSnapshot,
        external_data_score: int,
        interview_required: bool,
        interview_completed: bool,
        answer_quality_score: int
    ) -> Dict[str, any]:
        """
        Calculate confidence score based on multiple factors.

        Args:
            snapshot: BusinessSnapshot instance
            external_data_score: External data quality score (0-100)
            interview_required: Whether an interview was required
            interview_completed: Whether the interview was completed
            answer_quality_score: Quality of interview answers (0-100)

        Returns:
            Dictionary with:
                - score: Overall confidence score (0-100)
                - label: Confidence label string
                - breakdown: Dictionary with individual component scores
        """
        # Validate inputs
        if not isinstance(external_data_score, (int, float)) or not (0 <= external_data_score <= 100):
            logger.error(f"Invalid external_data_score: {external_data_score}. Must be between 0 and 100.")
            raise ValueError("external_data_score must be between 0 and 100")

        if not isinstance(answer_quality_score, (int, float)) or not (0 <= answer_quality_score <= 100):
            logger.error(f"Invalid answer_quality_score: {answer_quality_score}. Must be between 0 and 100.")
            raise ValueError("answer_quality_score must be between 0 and 100")

        # Get region support score
        region_support_score = cls.get_region_support_score(snapshot.region)

        # Calculate interview completion score
        interview_completion_score = cls.calculate_interview_completion_score(
            interview_required,
            interview_completed
        )

        # Calculate overall confidence based on interview requirement
        if not interview_required:
            # Formula: external_data_score * 0.70 + region_support_score * 0.30
            confidence = (
                external_data_score * 0.70 +
                region_support_score * 0.30
            )
            logger.info(
                f"Confidence calculation (no interview): "
                f"external_data={external_data_score} * 0.70 + "
                f"region_support={region_support_score} * 0.30 = {confidence}"
            )
        else:
            # Formula: external_data_score * 0.35 + region_support_score * 0.15 +
            #          interview_completion_score * 0.30 + answer_quality_score * 0.20
            # Note: answer_quality_score only applies if interview is completed
            if interview_completed:
                confidence = (
                    external_data_score * 0.35 +
                    region_support_score * 0.15 +
                    interview_completion_score * 0.30 +
                    answer_quality_score * 0.20
                )
                logger.info(
                    f"Confidence calculation (with interview completed): "
                    f"external_data={external_data_score} * 0.35 + "
                    f"region_support={region_support_score} * 0.15 + "
                    f"interview_completion={interview_completion_score} * 0.30 + "
                    f"answer_quality={answer_quality_score} * 0.20 = {confidence}"
                )
            else:
                # When interview not completed, redistribute weights:
                # external_data_score * 0.50 + region_support_score * 0.20 + interview_completion_score * 0.30
                confidence = (
                    external_data_score * 0.50 +
                    region_support_score * 0.20 +
                    interview_completion_score * 0.30
                )
                logger.info(
                    f"Confidence calculation (interview not completed): "
                    f"external_data={external_data_score} * 0.50 + "
                    f"region_support={region_support_score} * 0.20 + "
                    f"interview_completion={interview_completion_score} * 0.30 = {confidence}"
                )

        # Ensure score is within valid range
        confidence = max(0, min(100, int(confidence)))

        # Get confidence label
        label = cls.get_confidence_label(confidence)

        # Build breakdown for transparency
        breakdown = {
            'external_data_score': external_data_score,
            'region_support_score': region_support_score,
            'interview_required': interview_required,
            'interview_completed': interview_completed,
            'interview_completion_score': interview_completion_score,
            'answer_quality_score': answer_quality_score if interview_required else None,
        }

        result = {
            'score': confidence,
            'label': label,
            'breakdown': breakdown
        }

        logger.info(f"Final confidence score: {confidence} ({label})")
        return result
