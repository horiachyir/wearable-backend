"""
iFRS™ Layer - Intelligent Frequency Response System
Proprietary frequency domain analysis for biosignals
"""

import numpy as np
from typing import Dict
import random

from app.models.schemas import (
    BiosignalData, iFRSLayerResult, FrequencyBands,
    HRVFeatures, RhythmClassification
)


class iFRSLayer:
    """
    iFRS™ - Intelligent Frequency Response System

    Features:
    - Fast Fourier Transform (FFT) for frequency analysis
    - Heart Rate Variability (HRV) feature extraction
    - Frequency band power analysis (VLF, LF, HF)
    - Rhythm classification
    - Respiratory rate estimation
    - Frequency stability assessment
    """

    def __init__(self):
        self.sample_rate = 100  # Hz
        self.buffer_size = 256  # FFT window size
        self.hr_buffer = []
        self.rr_intervals = []  # R-R intervals for HRV

    def process(self, data: BiosignalData) -> Dict:
        """
        Process biosignal data through iFRS™ layer

        Args:
            data: Clarity-enhanced biosignal data

        Returns:
            iFRS layer processing results
        """
        # Add to heart rate buffer
        self.hr_buffer.append(data.heart_rate)
        if len(self.hr_buffer) > self.buffer_size:
            self.hr_buffer.pop(0)

        # Simulate R-R intervals from heart rate
        self._update_rr_intervals(data.heart_rate)

        # Perform frequency analysis
        dominant_freq, frequency_stability = self._analyze_frequency()

        # Calculate frequency band powers
        frequency_bands = self._calculate_frequency_bands()

        # Extract HRV features
        hrv_features = self._extract_hrv_features()

        # Classify rhythm
        rhythm_classification = self._classify_rhythm(
            data.heart_rate, hrv_features, frequency_bands
        )

        # Estimate respiratory rate
        respiratory_rate = self._estimate_respiratory_rate(frequency_bands)

        # Apply frequency-based enhancement (simulate)
        enhanced_data = self._enhance_signals(data)

        # Generate processing notes
        notes = self._generate_processing_notes(
            dominant_freq, rhythm_classification, hrv_features
        )

        return {
            'enhanced_data': enhanced_data,
            'dominant_frequency': dominant_freq,
            'frequency_bands': frequency_bands,
            'hrv_features': hrv_features,
            'rhythm_classification': rhythm_classification,
            'respiratory_rate': respiratory_rate,
            'frequency_stability': frequency_stability,
            'processing_notes': notes
        }

    def _update_rr_intervals(self, heart_rate: float):
        """
        Update R-R intervals buffer from heart rate
        R-R interval = 60,000ms / heart_rate
        """
        if heart_rate > 0:
            rr_interval = 60000.0 / heart_rate  # in milliseconds
            self.rr_intervals.append(rr_interval)

            # Keep only recent intervals
            if len(self.rr_intervals) > 100:
                self.rr_intervals.pop(0)

    def _analyze_frequency(self) -> tuple[float, float]:
        """
        Analyze frequency content using FFT

        Returns:
            (dominant_frequency, frequency_stability)
        """
        if len(self.hr_buffer) < 32:
            return 1.25, 0.85  # Default values

        # Apply FFT
        signal = np.array(self.hr_buffer[-128:])  # Use recent samples
        signal = signal - np.mean(signal)  # Remove DC component

        # Apply Hanning window to reduce spectral leakage
        window = np.hanning(len(signal))
        signal_windowed = signal * window

        # Compute FFT
        fft_result = np.fft.fft(signal_windowed)
        fft_magnitude = np.abs(fft_result[:len(fft_result)//2])

        # Frequency bins
        freqs = np.fft.fftfreq(len(signal), 1.0/self.sample_rate)
        freqs = freqs[:len(freqs)//2]

        # Find dominant frequency (exclude DC component)
        if len(fft_magnitude) > 1:
            dominant_idx = np.argmax(fft_magnitude[1:]) + 1
            dominant_freq = abs(float(freqs[dominant_idx]))
        else:
            dominant_freq = 1.25

        # Calculate frequency stability (how concentrated is power)
        total_power = np.sum(fft_magnitude ** 2)
        dominant_power = fft_magnitude[dominant_idx] ** 2 if len(fft_magnitude) > 1 else total_power

        if total_power > 0:
            frequency_stability = dominant_power / total_power
        else:
            frequency_stability = 0.5

        frequency_stability = min(1.0, max(0.3, frequency_stability))

        return round(dominant_freq, 2), round(float(frequency_stability), 2)

    def _calculate_frequency_bands(self) -> FrequencyBands:
        """
        Calculate power in standard HRV frequency bands

        VLF: Very Low Frequency (0.003-0.04 Hz)
        LF: Low Frequency (0.04-0.15 Hz) - sympathetic + parasympathetic
        HF: High Frequency (0.15-0.4 Hz) - parasympathetic (respiratory)
        """
        if len(self.rr_intervals) < 10:
            # Return default values
            return FrequencyBands(
                vlf=45.0,
                lf=35.0,
                hf=20.0,
                lf_hf_ratio=1.75
            )

        # Simulate frequency band powers
        # In real implementation, this would use Welch's method or Lomb-Scargle
        vlf_power = random.uniform(30, 60)
        lf_power = random.uniform(25, 50)
        hf_power = random.uniform(15, 35)

        # Normalize to percentages
        total_power = vlf_power + lf_power + hf_power
        vlf_pct = (vlf_power / total_power) * 100
        lf_pct = (lf_power / total_power) * 100
        hf_pct = (hf_power / total_power) * 100

        # Calculate LF/HF ratio (autonomic balance indicator)
        lf_hf_ratio = lf_power / hf_power if hf_power > 0 else 1.5

        return FrequencyBands(
            vlf=round(vlf_pct, 1),
            lf=round(lf_pct, 1),
            hf=round(hf_pct, 1),
            lf_hf_ratio=round(lf_hf_ratio, 2)
        )

    def _extract_hrv_features(self) -> HRVFeatures:
        """
        Extract Heart Rate Variability features

        RMSSD: Root Mean Square of Successive Differences
        SDNN: Standard Deviation of NN intervals
        pNN50: Percentage of successive NN intervals that differ by > 50ms
        """
        if len(self.rr_intervals) < 5:
            return HRVFeatures(
                rmssd=42.0,
                sdnn=65.0,
                pnn50=25.0,
                hrv_score=75.0
            )

        rr_array = np.array(self.rr_intervals[-50:])  # Use recent data

        # SDNN: Standard deviation of NN intervals
        sdnn = float(np.std(rr_array))

        # RMSSD: Root mean square of successive differences
        successive_diffs = np.diff(rr_array)
        rmssd = float(np.sqrt(np.mean(successive_diffs ** 2)))

        # pNN50: Percentage of intervals > 50ms different from previous
        nn50_count = np.sum(np.abs(successive_diffs) > 50)
        pnn50 = (nn50_count / len(successive_diffs)) * 100 if len(successive_diffs) > 0 else 0

        # Calculate HRV score (0-100)
        # Higher RMSSD and SDNN generally indicate better HRV
        hrv_score = min(100, (rmssd / 2 + sdnn / 2))

        return HRVFeatures(
            rmssd=round(rmssd, 1),
            sdnn=round(sdnn, 1),
            pnn50=round(float(pnn50), 1),
            hrv_score=round(hrv_score, 1)
        )

    def _classify_rhythm(
        self, heart_rate: float, hrv: HRVFeatures, freq_bands: FrequencyBands
    ) -> RhythmClassification:
        """
        Classify heart rhythm based on rate, variability, and frequency analysis
        """
        # Normal sinus rhythm: HR 60-100, good HRV
        if 60 <= heart_rate <= 100 and hrv.hrv_score >= 60:
            return RhythmClassification.NORMAL_SINUS

        # Athletic: Low HR, high HRV
        if heart_rate < 60 and hrv.hrv_score >= 70:
            return RhythmClassification.ATHLETIC

        # Elevated: High HR
        if heart_rate > 100:
            return RhythmClassification.ELEVATED

        # Low: Low HR without high HRV
        if heart_rate < 60:
            return RhythmClassification.LOW

        # Irregular: Low HRV or abnormal frequency patterns
        if hrv.hrv_score < 40 or freq_bands.lf_hf_ratio > 3.0:
            return RhythmClassification.IRREGULAR

        return RhythmClassification.NORMAL_SINUS

    def _estimate_respiratory_rate(self, freq_bands: FrequencyBands) -> float:
        """
        Estimate respiratory rate from HF band (respiratory sinus arrhythmia)

        HF band (0.15-0.4 Hz) corresponds to respiratory frequency
        Typical respiratory rate: 12-20 breaths/min (0.2-0.33 Hz)
        """
        # Simulate respiratory rate based on HF power
        # Higher HF power suggests stronger respiratory influence
        base_rr = 16.0  # breaths per minute

        # Add variation based on HF component
        variation = (freq_bands.hf - 25) * 0.1

        respiratory_rate = base_rr + variation
        respiratory_rate = np.clip(respiratory_rate, 10, 25)

        return round(float(respiratory_rate), 1)

    def _enhance_signals(self, data: BiosignalData) -> BiosignalData:
        """
        Apply frequency-based signal enhancement

        In real implementation, this would:
        - Apply band-pass filtering
        - Remove specific frequency artifacts
        - Enhance signal features in specific bands
        """
        # For simulation, apply slight smoothing
        enhanced_dict = data.dict()

        if len(self.hr_buffer) >= 3:
            # Smooth heart rate using frequency domain knowledge
            recent_hr = self.hr_buffer[-3:]
            enhanced_dict['heart_rate'] = round(float(np.mean(recent_hr)), 2)

        return BiosignalData(**enhanced_dict)

    def _generate_processing_notes(
        self, dominant_freq: float, rhythm: RhythmClassification, hrv: HRVFeatures
    ) -> str:
        """Generate human-readable processing notes"""
        notes = []

        notes.append(f"Dominant frequency: {dominant_freq:.2f} Hz")
        notes.append(f"Rhythm: {rhythm.value.replace('_', ' ').title()}")
        notes.append(f"HRV Score: {hrv.hrv_score:.1f}/100")
        notes.append(f"RMSSD: {hrv.rmssd:.1f}ms, SDNN: {hrv.sdnn:.1f}ms")
        notes.append("FFT analysis completed with Hanning window")

        return " | ".join(notes)
