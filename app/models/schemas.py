"""
Pydantic models and schemas for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class DeviceType(str, Enum):
    BRACELET = "bracelet"
    CLIP = "clip"
    WATCH = "watch"
    BAND = "band"
    MOBILE_APP = "mobile_app"


class SessionType(str, Enum):
    WORKOUT = "workout"
    MEDITATION = "meditation"
    SLEEP = "sleep"
    DAILY_MONITORING = "daily_monitoring"
    CLINICAL = "clinical"


class SignalQuality(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class PatternType(str, Enum):
    STABLE = "stable"
    INCREASING = "increasing"
    DECREASING = "decreasing"
    OSCILLATING = "oscillating"
    IRREGULAR = "irregular"


class CircadianPhase(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"


class RhythmClassification(str, Enum):
    NORMAL_SINUS = "normal_sinus"
    ELEVATED = "elevated"
    LOW = "low"
    IRREGULAR = "irregular"
    ATHLETIC = "athletic"


# ============================================================================
# REQUEST MODELS
# ============================================================================

class ConnectionRequest(BaseModel):
    device_id: str = Field(..., description="Unique device identifier")
    device_type: DeviceType = Field(..., description="Type of wearable device")
    app_version: Optional[str] = Field("1.0.0", description="Mobile app version")
    user_id: Optional[str] = Field(None, description="User identifier")


class SessionCreateRequest(BaseModel):
    device_id: str = Field(..., description="Device ID for the session")
    user_id: Optional[str] = Field(None, description="User ID")
    session_type: SessionType = Field(SessionType.DAILY_MONITORING, description="Type of session")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class DeviceStatus(BaseModel):
    device_id: str
    is_connected: bool
    battery_level: float = Field(..., ge=0, le=100, description="Battery percentage")
    signal_strength: int = Field(..., ge=-100, le=0, description="RSSI in dBm")
    firmware_version: str
    last_updated: datetime


class ConnectionResponse(BaseModel):
    success: bool
    message: str
    session_id: str
    device_status: DeviceStatus
    available_features: List[str]


class BiosignalData(BaseModel):
    heart_rate: float = Field(..., description="Heart rate in BPM")
    spo2: float = Field(..., description="Blood oxygen saturation (%)")
    temperature: float = Field(..., description="Body temperature (°C)")
    activity: float = Field(..., description="Activity level (steps/min)")


class QualityMetrics(BaseModel):
    heart_rate_quality: float = Field(..., ge=0, le=1)
    spo2_quality: float = Field(..., ge=0, le=1)
    temperature_quality: float = Field(..., ge=0, le=1)
    activity_quality: float = Field(..., ge=0, le=1)
    overall_quality: float = Field(..., ge=0, le=1)


class ClarityLayerResult(BaseModel):
    processed_data: BiosignalData
    quality_score: float = Field(..., ge=0, le=1, description="Overall signal quality score")
    signal_to_noise_ratio: float = Field(..., description="SNR in dB")
    noise_reduction_applied: bool
    quality_metrics: QualityMetrics
    quality_assessment: SignalQuality
    artifacts_detected: List[str] = Field(default_factory=list)
    processing_notes: str


class FrequencyBands(BaseModel):
    vlf: float = Field(..., description="Very Low Frequency (0.003-0.04 Hz)")
    lf: float = Field(..., description="Low Frequency (0.04-0.15 Hz)")
    hf: float = Field(..., description="High Frequency (0.15-0.4 Hz)")
    lf_hf_ratio: float = Field(..., description="LF/HF ratio")


class HRVFeatures(BaseModel):
    rmssd: float = Field(..., description="Root Mean Square of Successive Differences")
    sdnn: float = Field(..., description="Standard Deviation of NN intervals")
    pnn50: float = Field(..., description="Percentage of successive NN intervals > 50ms")
    hrv_score: float = Field(..., ge=0, le=100, description="Overall HRV health score")


class iFRSLayerResult(BaseModel):
    enhanced_data: BiosignalData
    dominant_frequency: float = Field(..., description="Dominant frequency in Hz")
    frequency_bands: FrequencyBands
    hrv_features: HRVFeatures
    rhythm_classification: RhythmClassification
    respiratory_rate: float = Field(..., description="Estimated respiratory rate")
    frequency_stability: float = Field(..., ge=0, le=1)
    processing_notes: str


class PatternRecognition(BaseModel):
    short_term_trend: str
    long_term_trend: str
    periodicity_detected: bool
    period_length_seconds: Optional[float]
    pattern_confidence: float = Field(..., ge=0, le=1)


class CircadianAlignment(BaseModel):
    expected_heart_rate: float
    actual_heart_rate: float
    alignment_score: float = Field(..., ge=0, le=1)
    phase_shift_minutes: float


class TimesystemsLayerResult(BaseModel):
    synchronized_data: BiosignalData
    pattern_type: PatternType
    temporal_consistency: float = Field(..., ge=0, le=1)
    circadian_phase: CircadianPhase
    time_of_day_analysis: Dict[str, Any]
    pattern_recognition: PatternRecognition
    circadian_alignment: CircadianAlignment
    rhythm_score: float = Field(..., ge=0, le=100)
    processing_notes: str


class WellnessAssessment(BaseModel):
    cardiovascular_health: float = Field(..., ge=0, le=100)
    respiratory_health: float = Field(..., ge=0, le=100)
    activity_level: float = Field(..., ge=0, le=100)
    stress_level: float = Field(..., ge=0, le=100)
    overall_wellness: float = Field(..., ge=0, le=100)


class LIAInsights(BaseModel):
    condition: str = Field(..., description="Detected health condition")
    confidence: float = Field(..., ge=0, le=1)
    wellness_score: float = Field(..., ge=0, le=100)
    probabilities: Dict[str, float] = Field(..., description="Probability for each condition")
    recommendation: str
    wellness_assessment: WellnessAssessment
    risk_factors: List[str] = Field(default_factory=list)
    positive_indicators: List[str] = Field(default_factory=list)


class StreamDataResponse(BaseModel):
    timestamp: datetime
    raw_signals: BiosignalData
    clarity_layer: ClarityLayerResult
    ifrs_layer: iFRSLayerResult
    timesystems_layer: TimesystemsLayerResult
    lia_insights: LIAInsights


class PredictionResponse(BaseModel):
    timestamp: datetime
    condition: str
    confidence: float = Field(..., ge=0, le=1)
    wellness_score: float = Field(..., ge=0, le=100)
    probabilities: Dict[str, float]
    signal_quality: SignalQuality
    recommendation: str
    metrics: Dict[str, float]


class SessionResponse(BaseModel):
    session_id: str
    device_id: str
    user_id: Optional[str]
    session_type: SessionType
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    data_points_collected: int
    average_wellness_score: Optional[float]
    summary: Optional[str]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SystemStatus(BaseModel):
    status: str
    timestamp: datetime
    services: Dict[str, bool]
    connected_clients: int
    active_sessions: int


class LayerProcessingLog(BaseModel):
    timestamp: datetime
    layer: str
    level: str
    message: str
    data: Optional[Dict[str, Any]] = None


# ============================================================================
# CONFIGURATION MODELS
# ============================================================================

class SignalConfig(BaseModel):
    name: str
    unit: str
    color: str
    min_value: float
    max_value: float
    normal_range: tuple[float, float]


class ProcessingConfig(BaseModel):
    sampling_rate: int = 100  # Hz
    buffer_size: int = 500
    update_interval_ms: int = 50
    noise_threshold: float = 0.3
    quality_threshold: float = 0.7
