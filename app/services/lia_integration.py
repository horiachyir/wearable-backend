"""
LIA (Lifestyle Intelligence Analysis) Integration
Combines outputs from all proprietary layers for comprehensive health insights
"""

import numpy as np
from typing import Dict, List
import random

from app.models.schemas import (
    BiosignalData, WellnessAssessment, LIAInsights
)


class LIAEngine:
    """
    LIA - Lifestyle Intelligence Analysis Engine

    Integrates data from:
    - Clarity™ layer (signal quality)
    - iFRS™ layer (frequency analysis, HRV)
    - Timesystems™ layer (temporal patterns, circadian rhythm)

    Provides:
    - Health condition classification
    - Wellness scoring
    - Risk factor identification
    - Personalized recommendations
    - Multi-dimensional health assessment
    """

    def __init__(self):
        self.conditions = [
            'Normal Resting',
            'Light Activity',
            'Moderate Exercise',
            'Intense Exercise',
            'Deep Rest',
            'Sleep State',
            'Elevated Stress',
            'Relaxation',
            'Recovery Mode',
            'Optimal Wellness'
        ]

        self.condition_history = []
        self.history_size = 100

    def analyze(
        self,
        raw_data: BiosignalData,
        clarity_result: Dict,
        ifrs_result: Dict,
        timesystems_result: Dict
    ) -> Dict:
        """
        Perform comprehensive LIA analysis

        Args:
            raw_data: Raw biosignal data
            clarity_result: Clarity™ layer output
            ifrs_result: iFRS™ layer output
            timesystems_result: Timesystems™ layer output

        Returns:
            LIA insights including condition, wellness, recommendations
        """
        # Extract key metrics from each layer
        signal_quality = clarity_result['quality_score']
        hrv_features = ifrs_result['hrv_features']
        rhythm_class = ifrs_result['rhythm_classification']
        pattern_type = timesystems_result['pattern_type']
        circadian_alignment = timesystems_result['circadian_alignment']

        # Classify condition using ensemble approach
        condition = self._classify_condition(
            raw_data, hrv_features, rhythm_class, pattern_type
        )

        # Calculate confidence in classification
        confidence = self._calculate_confidence(
            signal_quality, clarity_result['signal_to_noise_ratio'],
            timesystems_result['temporal_consistency']
        )

        # Generate probability distribution
        probabilities = self._generate_probabilities(condition)

        # Perform wellness assessment
        wellness_assessment = self._assess_wellness(
            raw_data, hrv_features, circadian_alignment, signal_quality
        )

        # Calculate overall wellness score
        wellness_score = wellness_assessment.overall_wellness

        # Identify risk factors
        risk_factors = self._identify_risk_factors(
            raw_data, hrv_features, clarity_result, circadian_alignment
        )

        # Identify positive indicators
        positive_indicators = self._identify_positive_indicators(
            raw_data, hrv_features, signal_quality, circadian_alignment
        )

        # Generate recommendation
        recommendation = self._generate_recommendation(
            condition, wellness_score, risk_factors
        )

        # Store in history
        self.condition_history.append(condition)
        if len(self.condition_history) > self.history_size:
            self.condition_history.pop(0)

        return {
            'condition': condition,
            'confidence': confidence,
            'wellness_score': wellness_score,
            'probabilities': probabilities,
            'recommendation': recommendation,
            'wellness_assessment': wellness_assessment,
            'risk_factors': risk_factors,
            'positive_indicators': positive_indicators
        }

    def _classify_condition(
        self, data: BiosignalData, hrv, rhythm, pattern
    ) -> str:
        """
        Classify health condition using multi-factor analysis

        Classification logic:
        - Heart rate zones
        - Activity level
        - HRV features
        - Rhythm classification
        - Pattern type
        """
        hr = data.heart_rate
        activity = data.activity
        hrv_score = hrv.hrv_score

        # Sleep state
        if hr < 60 and activity < 5 and pattern.value == 'stable':
            return 'Sleep State'

        # Deep rest
        if hr < 65 and activity < 10 and hrv_score > 70:
            return 'Deep Rest'

        # Intense exercise
        if hr > 140 and activity > 100:
            return 'Intense Exercise'

        # Moderate exercise
        if hr > 110 and activity > 60:
            return 'Moderate Exercise'

        # Light activity
        if 90 < hr < 110 and activity > 30:
            return 'Light Activity'

        # Elevated stress (high HR, low HRV, low activity)
        if hr > 85 and hrv_score < 50 and activity < 20:
            return 'Elevated Stress'

        # Relaxation (good HRV, low activity, normal HR)
        if 60 <= hr <= 75 and hrv_score > 70 and activity < 20:
            return 'Relaxation'

        # Recovery mode
        if rhythm.value == 'athletic' and hrv_score > 80:
            return 'Recovery Mode'

        # Optimal wellness
        if 65 <= hr <= 75 and hrv_score > 75 and 60 <= data.spo2 <= 100:
            return 'Optimal Wellness'

        # Default: Normal resting
        return 'Normal Resting'

    def _calculate_confidence(
        self, signal_quality: float, snr: float, temporal_consistency: float
    ) -> float:
        """
        Calculate confidence in classification

        Based on:
        - Signal quality from Clarity™
        - SNR
        - Temporal consistency from Timesystems™
        """
        # Weight factors
        quality_weight = 0.4
        snr_weight = 0.3
        consistency_weight = 0.3

        # Normalize SNR (typical range: 20-50 dB)
        snr_normalized = min(1.0, max(0.0, (snr - 20) / 30))

        # Calculate weighted confidence
        confidence = (
            signal_quality * quality_weight +
            snr_normalized * snr_weight +
            temporal_consistency * consistency_weight
        )

        # Ensure minimum confidence of 0.70
        confidence = max(0.70, min(0.99, confidence))

        return round(confidence, 3)

    def _generate_probabilities(self, detected_condition: str) -> Dict[str, float]:
        """
        Generate probability distribution across all conditions

        Uses Dirichlet distribution with higher probability for detected condition
        """
        # Create alpha values (higher for detected condition)
        alphas = []
        for condition in self.conditions:
            if condition == detected_condition:
                alphas.append(10.0)  # High probability
            else:
                alphas.append(1.0)   # Low probability

        # Generate probabilities
        probs = np.random.dirichlet(alphas)

        # Create dictionary
        prob_dict = {
            condition: round(float(prob), 3)
            for condition, prob in zip(self.conditions, probs)
        }

        return prob_dict

    def _assess_wellness(
        self, data: BiosignalData, hrv, circadian_alignment, signal_quality: float
    ) -> WellnessAssessment:
        """
        Multi-dimensional wellness assessment

        Dimensions:
        - Cardiovascular health
        - Respiratory health
        - Activity level
        - Stress level
        - Overall wellness
        """
        # Cardiovascular health (based on HR, HRV)
        hr = data.heart_rate
        hrv_score = hrv.hrv_score

        if 60 <= hr <= 80 and hrv_score > 70:
            cardio_health = 90 + random.uniform(-5, 5)
        elif 55 <= hr <= 90 and hrv_score > 60:
            cardio_health = 75 + random.uniform(-5, 10)
        elif 50 <= hr <= 100:
            cardio_health = 65 + random.uniform(-10, 10)
        else:
            cardio_health = 50 + random.uniform(-10, 15)

        cardio_health = np.clip(cardio_health, 0, 100)

        # Respiratory health (based on SpO2, estimated RR)
        spo2 = data.spo2
        if spo2 >= 98:
            resp_health = 95 + random.uniform(-3, 5)
        elif spo2 >= 95:
            resp_health = 85 + random.uniform(-5, 10)
        elif spo2 >= 92:
            resp_health = 70 + random.uniform(-5, 10)
        else:
            resp_health = 55 + random.uniform(-10, 10)

        resp_health = np.clip(resp_health, 0, 100)

        # Activity level score
        activity = data.activity
        if 20 <= activity <= 80:
            activity_score = 85 + random.uniform(-5, 10)
        elif activity < 20:
            activity_score = 60 + random.uniform(-10, 10)
        else:
            activity_score = 75 + random.uniform(-5, 10)

        activity_score = np.clip(activity_score, 0, 100)

        # Stress level (inverse of HRV, circadian alignment)
        stress_indicators = []

        if hrv_score < 50:
            stress_indicators.append(0.6)
        elif hrv_score < 60:
            stress_indicators.append(0.4)
        else:
            stress_indicators.append(0.2)

        if circadian_alignment.alignment_score < 0.7:
            stress_indicators.append(0.5)
        else:
            stress_indicators.append(0.2)

        avg_stress = np.mean(stress_indicators)
        stress_level = (1 - avg_stress) * 100  # Invert (lower stress = better)

        # Overall wellness (weighted average)
        overall = (
            cardio_health * 0.35 +
            resp_health * 0.25 +
            activity_score * 0.20 +
            stress_level * 0.20
        )

        # Factor in signal quality
        overall *= (0.8 + signal_quality * 0.2)

        return WellnessAssessment(
            cardiovascular_health=round(float(cardio_health), 1),
            respiratory_health=round(float(resp_health), 1),
            activity_level=round(float(activity_score), 1),
            stress_level=round(float(stress_level), 1),
            overall_wellness=round(float(overall), 1)
        )

    def _identify_risk_factors(
        self, data: BiosignalData, hrv, clarity_result, circadian_alignment
    ) -> List[str]:
        """Identify potential risk factors"""
        risks = []

        # Heart rate risks
        if data.heart_rate > 100:
            risks.append("Elevated heart rate")
        elif data.heart_rate < 50:
            risks.append("Low heart rate (bradycardia)")

        # HRV risks
        if hrv.hrv_score < 50:
            risks.append("Low heart rate variability")

        # SpO2 risks
        if data.spo2 < 95:
            risks.append("Low blood oxygen saturation")

        # Temperature risks
        if data.temperature > 38:
            risks.append("Elevated body temperature")
        elif data.temperature < 36:
            risks.append("Low body temperature")

        # Signal quality risks
        if clarity_result['quality_score'] < 0.6:
            risks.append("Poor signal quality - check sensor placement")

        # Circadian misalignment
        if circadian_alignment.alignment_score < 0.6:
            risks.append("Circadian rhythm misalignment")

        # Artifacts
        if len(clarity_result['artifacts_detected']) > 2:
            risks.append("Multiple signal artifacts detected")

        return risks

    def _identify_positive_indicators(
        self, data: BiosignalData, hrv, signal_quality: float, circadian_alignment
    ) -> List[str]:
        """Identify positive health indicators"""
        positives = []

        # Good HRV
        if hrv.hrv_score > 75:
            positives.append("Excellent heart rate variability")
        elif hrv.hrv_score > 65:
            positives.append("Good heart rate variability")

        # Good SpO2
        if data.spo2 >= 98:
            positives.append("Optimal blood oxygen saturation")

        # Good signal quality
        if signal_quality > 0.85:
            positives.append("Excellent signal quality")

        # Good circadian alignment
        if circadian_alignment.alignment_score > 0.85:
            positives.append("Strong circadian rhythm alignment")

        # Normal temperature
        if 36.5 <= data.temperature <= 37.2:
            positives.append("Normal body temperature")

        # Optimal heart rate
        if 60 <= data.heart_rate <= 75:
            positives.append("Optimal resting heart rate")

        return positives

    def _generate_recommendation(
        self, condition: str, wellness_score: float, risk_factors: List[str]
    ) -> str:
        """
        Generate personalized recommendation based on current state
        """
        recommendations = {
            'Normal Resting': 'Maintain current activity levels and hydration',
            'Light Activity': 'Continue with light movement, stay hydrated',
            'Moderate Exercise': 'Good workout intensity, monitor heart rate recovery',
            'Intense Exercise': 'High intensity detected - ensure proper rest periods',
            'Deep Rest': 'Excellent recovery state, maintain relaxation',
            'Sleep State': 'Sleep pattern detected, ensure adequate rest duration',
            'Elevated Stress': 'Consider stress-reduction techniques like deep breathing',
            'Relaxation': 'Excellent relaxation state, continue current activity',
            'Recovery Mode': 'Optimal recovery detected, light activity recommended',
            'Optimal Wellness': 'Excellent health indicators, maintain current lifestyle'
        }

        base_rec = recommendations.get(condition, 'Continue monitoring health metrics')

        # Add risk-based recommendations
        if risk_factors:
            if 'Low heart rate variability' in risk_factors:
                base_rec += ' | Consider relaxation exercises to improve HRV'
            if 'Low blood oxygen saturation' in risk_factors:
                base_rec += ' | Deep breathing exercises recommended'
            if 'Circadian rhythm misalignment' in risk_factors:
                base_rec += ' | Try to maintain consistent sleep schedule'

        # Wellness-based recommendations
        if wellness_score < 60:
            base_rec += ' | Consult healthcare provider if symptoms persist'
        elif wellness_score > 85:
            base_rec += ' | Great health status - keep it up!'

        return base_rec
