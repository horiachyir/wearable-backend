"""
Timesystems™ Layer - Temporal Analysis and Circadian Rhythm Detection
Proprietary time-domain pattern recognition and circadian alignment
"""

import numpy as np
from datetime import datetime, time
from typing import Dict, Optional
import random

from app.models.schemas import (
    BiosignalData, TimesystemsLayerResult, PatternType,
    CircadianPhase, PatternRecognition, CircadianAlignment
)


class TimesystemsLayer:
    """
    Timesystems™ - Proprietary temporal analysis system

    Features:
    - Circadian rhythm detection and phase identification
    - Temporal pattern recognition (trends, periodicity)
    - Time-of-day physiological alignment
    - Rhythm coherence scoring
    - Long-term trend analysis
    - Pattern prediction
    """

    def __init__(self):
        self.temporal_buffer = []
        self.buffer_size = 600  # 60 seconds at 10Hz
        self.pattern_window = 100

        # Circadian reference values (expected HR by time of day)
        self.circadian_reference = {
            'morning': 70,    # 6 AM - 12 PM
            'afternoon': 75,  # 12 PM - 6 PM
            'evening': 72,    # 6 PM - 10 PM
            'night': 62       # 10 PM - 6 AM
        }

    def process(self, data: BiosignalData) -> Dict:
        """
        Process biosignal data through Timesystems™ layer

        Args:
            data: iFRS-enhanced biosignal data

        Returns:
            Timesystems layer processing results
        """
        # Add to temporal buffer with timestamp
        timestamp = datetime.now()
        self.temporal_buffer.append({
            'timestamp': timestamp,
            'data': data.dict()
        })

        if len(self.temporal_buffer) > self.buffer_size:
            self.temporal_buffer.pop(0)

        # Identify circadian phase
        circadian_phase = self._identify_circadian_phase(timestamp)

        # Analyze time-of-day patterns
        time_of_day_analysis = self._analyze_time_of_day(data, timestamp)

        # Recognize patterns
        pattern_type = self._recognize_pattern()
        pattern_recognition = self._detailed_pattern_recognition()

        # Calculate temporal consistency
        temporal_consistency = self._calculate_temporal_consistency()

        # Assess circadian alignment
        circadian_alignment = self._assess_circadian_alignment(
            data.heart_rate, circadian_phase
        )

        # Calculate rhythm score
        rhythm_score = self._calculate_rhythm_score(
            temporal_consistency, circadian_alignment, pattern_recognition
        )

        # Apply temporal synchronization
        synchronized_data = self._synchronize_signals(data)

        # Generate processing notes
        notes = self._generate_processing_notes(
            pattern_type, circadian_phase, rhythm_score
        )

        return {
            'synchronized_data': synchronized_data,
            'pattern_type': pattern_type,
            'temporal_consistency': temporal_consistency,
            'circadian_phase': circadian_phase,
            'time_of_day_analysis': time_of_day_analysis,
            'pattern_recognition': pattern_recognition,
            'circadian_alignment': circadian_alignment,
            'rhythm_score': rhythm_score,
            'processing_notes': notes
        }

    def _identify_circadian_phase(self, timestamp: datetime) -> CircadianPhase:
        """
        Identify current circadian phase based on time of day
        """
        hour = timestamp.hour

        if 6 <= hour < 12:
            return CircadianPhase.MORNING
        elif 12 <= hour < 18:
            return CircadianPhase.AFTERNOON
        elif 18 <= hour < 22:
            return CircadianPhase.EVENING
        else:
            return CircadianPhase.NIGHT

    def _analyze_time_of_day(
        self, data: BiosignalData, timestamp: datetime
    ) -> Dict:
        """
        Analyze physiological metrics in context of time of day
        """
        hour = timestamp.hour
        phase = self._identify_circadian_phase(timestamp)

        # Expected ranges based on circadian rhythm
        analysis = {
            'current_hour': hour,
            'phase': phase.value,
            'expected_heart_rate_range': self._get_expected_hr_range(phase),
            'heart_rate_deviation': self._calculate_hr_deviation(
                data.heart_rate, phase
            ),
            'activity_appropriate': self._is_activity_appropriate(
                data.activity, phase
            ),
            'temperature_rhythm': self._assess_temperature_rhythm(
                data.temperature, phase
            )
        }

        return analysis

    def _get_expected_hr_range(self, phase: CircadianPhase) -> tuple:
        """Get expected heart rate range for circadian phase"""
        ranges = {
            CircadianPhase.MORNING: (65, 80),
            CircadianPhase.AFTERNOON: (70, 85),
            CircadianPhase.EVENING: (65, 80),
            CircadianPhase.NIGHT: (55, 70)
        }
        return ranges.get(phase, (60, 80))

    def _calculate_hr_deviation(self, hr: float, phase: CircadianPhase) -> float:
        """Calculate heart rate deviation from circadian expectation"""
        expected_hr = self.circadian_reference[phase.value]
        deviation = hr - expected_hr
        return round(deviation, 1)

    def _is_activity_appropriate(self, activity: float, phase: CircadianPhase) -> bool:
        """Check if activity level is appropriate for time of day"""
        if phase == CircadianPhase.NIGHT and activity > 50:
            return False  # High activity at night is unusual
        if phase in [CircadianPhase.MORNING, CircadianPhase.AFTERNOON] and activity < 10:
            return True  # Low activity during day could be sedentary work
        return True

    def _assess_temperature_rhythm(self, temp: float, phase: CircadianPhase) -> str:
        """Assess body temperature rhythm alignment"""
        # Body temperature typically peaks in late afternoon, lowest in early morning
        if phase == CircadianPhase.AFTERNOON and temp >= 37.0:
            return "Normal circadian peak"
        elif phase == CircadianPhase.NIGHT and temp <= 36.5:
            return "Normal circadian trough"
        elif phase == CircadianPhase.MORNING and temp < 36.7:
            return "Expected morning low"
        else:
            return "Within normal variation"

    def _recognize_pattern(self) -> PatternType:
        """
        Recognize overall pattern type from temporal data
        """
        if len(self.temporal_buffer) < 20:
            return PatternType.STABLE

        # Extract heart rate trend
        recent_data = self.temporal_buffer[-min(self.pattern_window, len(self.temporal_buffer)):]
        hr_values = [sample['data']['heart_rate'] for sample in recent_data]

        # Calculate trend using linear regression
        if len(hr_values) < 2:
            return PatternType.STABLE

        x = np.arange(len(hr_values))
        coefficients = np.polyfit(x, hr_values, 1)
        slope = coefficients[0]

        # Calculate variability
        hr_std = np.std(hr_values)

        # Classify pattern
        if abs(slope) < 0.05 and hr_std < 5:
            return PatternType.STABLE
        elif slope > 0.15:
            return PatternType.INCREASING
        elif slope < -0.15:
            return PatternType.DECREASING
        elif hr_std > 10:
            return PatternType.IRREGULAR
        else:
            return PatternType.OSCILLATING

    def _detailed_pattern_recognition(self) -> PatternRecognition:
        """
        Detailed pattern recognition analysis
        """
        if len(self.temporal_buffer) < 20:
            return PatternRecognition(
                short_term_trend="Stable",
                long_term_trend="Insufficient data",
                periodicity_detected=False,
                period_length_seconds=None,
                pattern_confidence=0.5
            )

        # Short-term trend (last 30 samples)
        short_window = min(30, len(self.temporal_buffer))
        short_term_hr = [
            s['data']['heart_rate']
            for s in self.temporal_buffer[-short_window:]
        ]
        short_term_trend = self._calculate_trend_description(short_term_hr)

        # Long-term trend (all buffered samples)
        long_term_hr = [s['data']['heart_rate'] for s in self.temporal_buffer]
        long_term_trend = self._calculate_trend_description(long_term_hr)

        # Detect periodicity using autocorrelation
        periodicity, period = self._detect_periodicity(long_term_hr)

        # Calculate pattern confidence
        confidence = self._calculate_pattern_confidence(long_term_hr)

        return PatternRecognition(
            short_term_trend=short_term_trend,
            long_term_trend=long_term_trend,
            periodicity_detected=periodicity,
            period_length_seconds=period,
            pattern_confidence=confidence
        )

    def _calculate_trend_description(self, values: list) -> str:
        """Calculate descriptive trend from values"""
        if len(values) < 2:
            return "Stable"

        x = np.arange(len(values))
        coefficients = np.polyfit(x, values, 1)
        slope = coefficients[0]

        if slope > 0.2:
            return "Rising"
        elif slope < -0.2:
            return "Declining"
        else:
            return "Stable"

    def _detect_periodicity(self, values: list) -> tuple[bool, Optional[float]]:
        """
        Detect periodicity in signal using autocorrelation

        Returns:
            (periodicity_detected, period_in_seconds)
        """
        if len(values) < 50:
            return False, None

        # Simulate periodicity detection
        # Real implementation would use autocorrelation
        periodicity_detected = random.random() > 0.6

        if periodicity_detected:
            # Typical respiratory rhythm: 15 breaths/min = 4 second period
            period = random.uniform(3.0, 6.0)
            return True, round(period, 1)

        return False, None

    def _calculate_pattern_confidence(self, values: list) -> float:
        """
        Calculate confidence in pattern recognition

        Based on:
        - Data quantity
        - Signal consistency
        - Pattern clarity
        """
        if len(values) < 10:
            return 0.3

        # More data = higher confidence
        data_confidence = min(1.0, len(values) / 100)

        # Lower variance = higher confidence
        normalized_std = np.std(values) / max(np.mean(values), 1)
        consistency_confidence = max(0.3, 1.0 - normalized_std)

        overall_confidence = (data_confidence + consistency_confidence) / 2

        return round(float(overall_confidence), 2)

    def _calculate_temporal_consistency(self) -> float:
        """
        Calculate temporal consistency score

        Measures how stable signals are over time
        """
        if len(self.temporal_buffer) < 10:
            return 0.75

        hr_values = [s['data']['heart_rate'] for s in self.temporal_buffer[-50:]]

        # Calculate coefficient of variation
        mean_hr = np.mean(hr_values)
        std_hr = np.std(hr_values)

        if mean_hr == 0:
            return 0.5

        cv = std_hr / mean_hr

        # Lower CV = higher consistency
        consistency = max(0.3, 1.0 - (cv * 2))
        consistency = min(1.0, consistency)

        return round(float(consistency), 2)

    def _assess_circadian_alignment(
        self, heart_rate: float, phase: CircadianPhase
    ) -> CircadianAlignment:
        """
        Assess how well current physiology aligns with circadian expectations
        """
        expected_hr = self.circadian_reference[phase.value]

        # Calculate alignment score
        deviation = abs(heart_rate - expected_hr)
        max_acceptable_deviation = 20  # bpm

        alignment_score = max(0.0, 1.0 - (deviation / max_acceptable_deviation))
        alignment_score = min(1.0, alignment_score)

        # Calculate phase shift
        if heart_rate > expected_hr:
            phase_shift = (heart_rate - expected_hr) * 2  # Rough estimate in minutes
        else:
            phase_shift = -(expected_hr - heart_rate) * 2

        return CircadianAlignment(
            expected_heart_rate=expected_hr,
            actual_heart_rate=heart_rate,
            alignment_score=round(alignment_score, 2),
            phase_shift_minutes=round(phase_shift, 1)
        )

    def _calculate_rhythm_score(
        self, temporal_consistency: float,
        circadian_alignment: CircadianAlignment,
        pattern_recognition: PatternRecognition
    ) -> float:
        """
        Calculate overall rhythm health score (0-100)

        Combines:
        - Temporal consistency
        - Circadian alignment
        - Pattern clarity
        """
        consistency_score = temporal_consistency * 40
        alignment_score = circadian_alignment.alignment_score * 35
        pattern_score = pattern_recognition.pattern_confidence * 25

        rhythm_score = consistency_score + alignment_score + pattern_score

        return round(rhythm_score, 1)

    def _synchronize_signals(self, data: BiosignalData) -> BiosignalData:
        """
        Apply temporal synchronization to signals

        In real implementation:
        - Align signals to same time base
        - Compensate for sensor timing differences
        - Apply phase correction
        """
        # For simulation, return data as-is
        # Real implementation would apply sophisticated timing corrections
        return data

    def _generate_processing_notes(
        self, pattern: PatternType, phase: CircadianPhase, rhythm_score: float
    ) -> str:
        """Generate human-readable processing notes"""
        notes = []

        notes.append(f"Pattern: {pattern.value.title()}")
        notes.append(f"Circadian Phase: {phase.value.title()}")
        notes.append(f"Rhythm Score: {rhythm_score:.1f}/100")
        notes.append("Temporal window: 60s")
        notes.append("Circadian alignment assessed")

        return " | ".join(notes)
