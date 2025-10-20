# Wearable Biosignal Analysis System - Technical Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Proprietary Layers](#proprietary-layers)
4. [API Reference](#api-reference)
5. [Data Flow](#data-flow)
6. [Mobile App Integration](#mobile-app-integration)
7. [Deployment](#deployment)
8. [Testing](#testing)

---

## System Overview

The Wearable Biosignal Analysis System is a comprehensive health monitoring platform that processes biosignals from wearable devices through three proprietary processing layers before generating Lifestyle Intelligence Analysis (LIA) insights.

### Key Features
- **Real-time biosignal streaming** via BLE simulation
- **Three proprietary processing layers**: Clarity™, iFRS™, Timesystems™
- **LIA integration** for comprehensive health insights
- **FastAPI backend** with RESTful and WebSocket APIs
- **React Native mobile app** integration
- **Session management** and data persistence
- **Comprehensive logging** for demonstration and debugging

### Technology Stack
- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Data Processing**: NumPy, SciPy
- **API**: REST + WebSocket
- **Mobile**: React Native with Expo
- **Deployment**: Docker-ready

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Mobile Application                         │
│                    (React Native + Expo)                         │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTP/WebSocket
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ REST API     │  │ WebSocket    │  │ Session Manager     │   │
│  │ Endpoints    │  │ Streaming    │  │                     │   │
│  └──────────────┘  └──────────────┘  └─────────────────────┘   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Processing Pipeline                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────┐          │
│  │ Step 1: BLE Simulator                              │          │
│  │ - Generates realistic biosignal data               │          │
│  │ - Simulates: HR, SpO2, Temperature, Activity       │          │
│  └────────────────┬───────────────────────────────────┘          │
│                   ▼                                               │
│  ┌────────────────────────────────────────────────────┐          │
│  │ Step 2: Clarity™ Layer                             │          │
│  │ - Signal quality assessment                        │          │
│  │ - Adaptive noise reduction                         │          │
│  │ - SNR calculation                                  │          │
│  │ - Artifact detection                               │          │
│  └────────────────┬───────────────────────────────────┘          │
│                   ▼                                               │
│  ┌────────────────────────────────────────────────────┐          │
│  │ Step 3: iFRS™ Layer                                │          │
│  │ - Frequency domain analysis (FFT)                  │          │
│  │ - HRV feature extraction                           │          │
│  │ - Rhythm classification                            │          │
│  │ - Respiratory rate estimation                      │          │
│  └────────────────┬───────────────────────────────────┘          │
│                   ▼                                               │
│  ┌────────────────────────────────────────────────────┐          │
│  │ Step 4: Timesystems™ Layer                         │          │
│  │ - Temporal pattern recognition                     │          │
│  │ - Circadian rhythm detection                       │          │
│  │ - Trend analysis                                   │          │
│  │ - Rhythm coherence scoring                         │          │
│  └────────────────┬───────────────────────────────────┘          │
│                   ▼                                               │
│  ┌────────────────────────────────────────────────────┐          │
│  │ Step 5: LIA Engine                                 │          │
│  │ - Condition classification                         │          │
│  │ - Wellness assessment                              │          │
│  │ - Risk factor identification                       │          │
│  │ - Personalized recommendations                     │          │
│  └────────────────────────────────────────────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
backend/
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── models/
│   ├── __init__.py
│   └── schemas.py              # Pydantic models for API
├── services/
│   ├── __init__.py
│   ├── ble_simulator.py        # BLE device simulation
│   ├── clarity.py              # Clarity™ layer implementation
│   ├── ifrs.py                 # iFRS™ layer implementation
│   ├── timesystems.py          # Timesystems™ layer implementation
│   ├── lia_integration.py      # LIA engine
│   └── session_manager.py      # Session management
└── utils/
    ├── __init__.py
    └── logger.py               # Logging utilities
```

---

## Proprietary Layers

### 1. Clarity™ Layer - Signal Quality and Noise Reduction

**Purpose**: Enhance biosignal quality through adaptive filtering and quality assessment.

**Key Features**:
- **Adaptive Noise Reduction**: Wavelet-inspired smoothing based on signal quality
- **Quality Metrics**: Per-channel quality scoring (Heart Rate, SpO2, Temperature, Activity)
- **SNR Calculation**: Signal-to-noise ratio in dB
- **Artifact Detection**: Motion artifacts, electrode noise, saturation, dropouts
- **Quality Assessment**: Categorical rating (Excellent, Good, Fair, Poor)

**Algorithms**:
- Weighted moving average with exponential decay
- Historical consistency analysis
- Coefficient of variation for stability assessment
- Multi-factor quality scoring

**Input**: Raw biosignal data from BLE simulator
**Output**: Enhanced signals + quality metrics + processing notes

**Key Metrics**:
- Quality Score: 0.0 - 1.0
- SNR: 15 - 60 dB (typical: 20-50 dB)
- Individual channel quality scores

---

### 2. iFRS™ Layer - Intelligent Frequency Response System

**Purpose**: Frequency domain analysis for physiological rhythm assessment.

**Key Features**:
- **FFT Analysis**: Fast Fourier Transform for frequency content
- **HRV Extraction**: RMSSD, SDNN, pNN50, HRV Score
- **Frequency Bands**: VLF, LF, HF power distribution
- **Rhythm Classification**: Normal Sinus, Athletic, Elevated, Low, Irregular
- **Respiratory Rate**: Estimation from HF band

**Algorithms**:
- Hanning window for spectral leakage reduction
- R-R interval computation from heart rate
- LF/HF ratio for autonomic balance
- Dominant frequency detection

**Input**: Clarity-enhanced biosignal data
**Output**: Frequency features + HRV metrics + rhythm classification

**Key Metrics**:
- Dominant Frequency: Hz
- HRV Score: 0 - 100
- RMSSD: milliseconds
- SDNN: milliseconds
- LF/HF Ratio: autonomic balance indicator
- Respiratory Rate: breaths per minute

---

### 3. Timesystems™ Layer - Temporal Analysis and Circadian Rhythm

**Purpose**: Time-domain pattern recognition and circadian alignment assessment.

**Key Features**:
- **Circadian Phase Identification**: Morning, Afternoon, Evening, Night
- **Pattern Recognition**: Stable, Increasing, Decreasing, Oscillating, Irregular
- **Temporal Consistency**: Signal stability over time
- **Circadian Alignment**: Comparison with expected physiological rhythms
- **Rhythm Scoring**: Overall rhythm health score (0-100)

**Algorithms**:
- Linear regression for trend detection
- Autocorrelation for periodicity
- Time-of-day physiological expectations
- Pattern confidence scoring

**Input**: iFRS-enhanced biosignal data
**Output**: Temporal patterns + circadian analysis + rhythm scores

**Key Metrics**:
- Temporal Consistency: 0.0 - 1.0
- Circadian Alignment Score: 0.0 - 1.0
- Rhythm Score: 0 - 100
- Phase Shift: minutes from expected

---

### 4. LIA Engine - Lifestyle Intelligence Analysis

**Purpose**: Comprehensive health insights through multi-layer data fusion.

**Key Features**:
- **Condition Classification**: 10 health states (Normal Resting, Exercise, Sleep, Stress, etc.)
- **Wellness Assessment**: Multi-dimensional scoring
  - Cardiovascular Health (0-100)
  - Respiratory Health (0-100)
  - Activity Level (0-100)
  - Stress Level (0-100)
  - Overall Wellness (0-100)
- **Risk Factor Identification**: Automatic detection of concerning patterns
- **Positive Indicators**: Recognition of healthy signs
- **Personalized Recommendations**: Context-aware health advice

**Input**: Outputs from all three proprietary layers
**Output**: Condition, wellness scores, recommendations

**Condition Types**:
1. Normal Resting
2. Light Activity
3. Moderate Exercise
4. Intense Exercise
5. Deep Rest
6. Sleep State
7. Elevated Stress
8. Relaxation
9. Recovery Mode
10. Optimal Wellness

---

## API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. System Endpoints

##### GET `/`
**Description**: Root endpoint with API information

**Response**:
```json
{
  "service": "Wearable Biosignal Analysis API",
  "version": "1.0.0",
  "status": "operational",
  "features": [...],
  "endpoints": {...}
}
```

##### GET `/api/v1/health`
**Description**: Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "services": {
    "ble_simulator": true,
    "timesystems": true,
    "ifrs": true,
    "clarity": true,
    "lia": true
  },
  "connected_clients": 2,
  "active_sessions": 1
}
```

---

#### 2. Connection Endpoints

##### POST `/api/v1/connect`
**Description**: Connect a mobile client to the backend

**Request Body**:
```json
{
  "device_id": "MOBILE_APP_001",
  "device_type": "mobile_app",
  "app_version": "1.0.0",
  "user_id": "user_123"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Connected successfully to biosignal backend",
  "session_id": "session_abc123def456",
  "device_status": {
    "device_id": "WEARABLE_SIM_001",
    "is_connected": true,
    "battery_level": 87.5,
    "signal_strength": -55,
    "firmware_version": "2.1.4",
    "last_updated": "2024-01-15T10:30:00"
  },
  "available_features": [
    "real_time_streaming",
    "timesystems_analysis",
    "ifrs_processing",
    "clarity_enhancement",
    "lia_insights"
  ]
}
```

---

#### 3. Data Endpoints

##### GET `/api/v1/stream`
**Description**: Get current biosignal data processed through all layers

**Response**: (See detailed schema below)
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "raw_signals": {
    "heart_rate": 75.2,
    "spo2": 98.1,
    "temperature": 36.8,
    "activity": 32.5
  },
  "clarity_layer": {
    "processed_data": {...},
    "quality_score": 0.92,
    "signal_to_noise_ratio": 38.5,
    "quality_assessment": "excellent",
    ...
  },
  "ifrs_layer": {
    "enhanced_data": {...},
    "dominant_frequency": 1.25,
    "hrv_features": {
      "rmssd": 42.3,
      "sdnn": 68.1,
      "pnn50": 28.5,
      "hrv_score": 75.2
    },
    "rhythm_classification": "normal_sinus",
    ...
  },
  "timesystems_layer": {
    "pattern_type": "stable",
    "temporal_consistency": 0.88,
    "circadian_phase": "afternoon",
    "rhythm_score": 82.5,
    ...
  },
  "lia_insights": {
    "condition": "Normal Resting",
    "confidence": 0.92,
    "wellness_score": 85.3,
    "probabilities": {...},
    "recommendation": "Maintain current activity levels and hydration",
    "wellness_assessment": {
      "cardiovascular_health": 88.5,
      "respiratory_health": 92.1,
      "activity_level": 78.3,
      "stress_level": 82.0,
      "overall_wellness": 85.3
    },
    "risk_factors": [],
    "positive_indicators": [
      "Excellent heart rate variability",
      "Optimal blood oxygen saturation",
      "Strong circadian rhythm alignment"
    ]
  }
}
```

##### GET `/api/v1/predict`
**Description**: Get latest prediction from LIA engine

**Response**:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "condition": "Normal Resting",
  "confidence": 0.92,
  "wellness_score": 85.3,
  "probabilities": {
    "Normal Resting": 0.78,
    "Light Activity": 0.10,
    "Optimal Wellness": 0.05,
    ...
  },
  "signal_quality": "excellent",
  "recommendation": "Maintain current activity levels and hydration",
  "metrics": {
    "heart_rate": 75.2,
    "spo2": 98.1,
    "temperature": 36.8,
    "activity": 32.5
  }
}
```

---

#### 4. Session Endpoints

##### POST `/api/v1/sessions`
**Description**: Create a new monitoring session

**Request Body**:
```json
{
  "device_id": "MOBILE_APP_001",
  "user_id": "user_123",
  "session_type": "workout"
}
```

**Response**:
```json
{
  "session_id": "session_xyz789",
  "device_id": "MOBILE_APP_001",
  "user_id": "user_123",
  "session_type": "workout",
  "start_time": "2024-01-15T10:30:00",
  "end_time": null,
  "status": "active",
  "data_points_collected": 0,
  "average_wellness_score": null,
  "summary": null,
  "metadata": {...}
}
```

##### GET `/api/v1/sessions/{session_id}`
**Description**: Get session details

**Response**: Same as session creation response

---

#### 5. Demonstration Endpoints

##### GET `/api/v1/demo/layers`
**Description**: Detailed demonstration of data flow through all layers

**Response**: Comprehensive step-by-step breakdown showing:
- Raw input data
- Clarity™ processing details
- iFRS™ processing details
- Timesystems™ processing details
- LIA final output
- Processing algorithms used
- Detailed metrics at each stage

##### GET `/api/v1/logs/processing`
**Description**: Get recent processing logs

**Query Parameters**:
- `limit` (optional): Number of logs to return (default: 100)

**Response**:
```json
{
  "total": 100,
  "logs": [
    {
      "timestamp": "2024-01-15T10:30:00.123",
      "level": "INFO",
      "message": "CLARITY_LAYER | quality=0.92 | snr=38.5dB | noise_reduced=false",
      "data": {}
    },
    ...
  ]
}
```

---

#### 6. WebSocket Endpoint

##### WS `/ws/stream`
**Description**: Real-time biosignal streaming via WebSocket

**Connection**:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/stream');
```

**Message Format**:
```json
{
  "type": "stream_data",
  "data": {
    "timestamp": "2024-01-15T10:30:00",
    "raw_signals": {...},
    "clarity_layer": {...},
    "ifrs_layer": {...},
    "timesystems_layer": {...},
    "lia_insights": {...}
  }
}
```

**Update Rate**: 10 Hz (100ms interval)

---

## Data Flow

### Complete Processing Pipeline

```
1. BLE Simulator
   ↓
   Generates: {heart_rate, spo2, temperature, activity}
   Rate: 10 Hz

2. Clarity™ Layer
   ↓
   Input: Raw biosignals
   Processing:
   - Calculate quality metrics for each channel
   - Assess signal stability from history
   - Apply adaptive noise reduction if quality < 0.7
   - Calculate SNR
   - Detect artifacts
   Output: Enhanced signals + quality assessment

3. iFRS™ Layer
   ↓
   Input: Clarity-enhanced signals
   Processing:
   - Apply FFT with Hanning window
   - Extract R-R intervals from heart rate
   - Calculate HRV features (RMSSD, SDNN, pNN50)
   - Analyze frequency bands (VLF, LF, HF)
   - Classify cardiac rhythm
   - Estimate respiratory rate
   Output: Frequency features + HRV metrics

4. Timesystems™ Layer
   ↓
   Input: iFRS-enhanced signals
   Processing:
   - Identify circadian phase (time of day)
   - Analyze temporal patterns
   - Detect trends (linear regression)
   - Calculate temporal consistency
   - Assess circadian alignment
   - Score rhythm health
   Output: Temporal analysis + circadian metrics

5. LIA Engine
   ↓
   Input: All layer outputs
   Processing:
   - Multi-factor condition classification
   - Calculate wellness dimensions
   - Identify risk factors
   - Identify positive indicators
   - Generate personalized recommendation
   Output: Health insights + wellness scores
```

### Data Update Cycle

1. **BLE Simulator** generates new data every 100ms
2. **Each request** triggers complete pipeline processing
3. **WebSocket** streams continuous updates at 10 Hz
4. **Logs** capture each layer's processing in real-time

---

## Mobile App Integration

### React Native Configuration

Update the API base URL in your mobile app:

**File**: `BLE-wearable-App/src/services/api.ts` (create if doesn't exist)

```typescript
// API Configuration
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',  // For iOS Simulator
  // BASE_URL: 'http://10.0.2.2:8000',  // For Android Emulator
  // BASE_URL: 'http://YOUR_IP:8000',   // For physical device
  WS_URL: 'ws://localhost:8000/ws/stream',
  TIMEOUT: 10000,
};
```

### Example Integration Code

```typescript
// Connect to backend
async function connectToBackend(deviceId: string) {
  const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/connect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      device_id: deviceId,
      device_type: 'mobile_app',
      app_version: '1.0.0',
    }),
  });

  return await response.json();
}

// Get stream data
async function getStreamData() {
  const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/stream`);
  return await response.json();
}

// WebSocket streaming
const ws = new WebSocket(API_CONFIG.WS_URL);

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'stream_data') {
    // Update UI with message.data
    console.log('Wellness Score:', message.data.lia_insights.wellness_score);
  }
};
```

---

## Deployment

### Local Development

1. **Install Dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Run Server**:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. **Access API Documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Production Deployment

**Using Docker**:

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t wearable-backend .
docker run -p 8000:8000 wearable-backend
```

---

## Testing

### Manual Testing with cURL

**Health Check**:
```bash
curl http://localhost:8000/api/v1/health
```

**Connect**:
```bash
curl -X POST http://localhost:8000/api/v1/connect \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "TEST_DEVICE_001",
    "device_type": "mobile_app",
    "app_version": "1.0.0"
  }'
```

**Get Stream**:
```bash
curl http://localhost:8000/api/v1/stream
```

**Layer Demonstration**:
```bash
curl http://localhost:8000/api/v1/demo/layers
```

### Testing with Postman

Import the provided Postman collection (see POSTMAN_COLLECTION.json) for comprehensive API testing.

### Automated Testing

Run pytest:
```bash
pytest tests/ -v
```

---

## Performance Metrics

- **API Response Time**: < 50ms (average)
- **WebSocket Update Rate**: 10 Hz (100ms interval)
- **Processing Latency**: < 20ms per layer
- **Total Pipeline Latency**: < 50ms (real-time capable)
- **Concurrent Clients**: Supports 100+ simultaneous connections

---

## Troubleshooting

### Common Issues

1. **Port Already in Use**:
   - Change port: `uvicorn main:app --port 8001`

2. **CORS Errors**:
   - Ensure CORS middleware is configured
   - Check mobile app uses correct IP address

3. **Import Errors**:
   - Verify all `__init__.py` files exist
   - Check Python path includes backend directory

4. **WebSocket Connection Fails**:
   - Use `ws://` not `wss://` for local development
   - Check firewall settings

---

## Support

For issues or questions:
- Check API documentation: http://localhost:8000/docs
- Review processing logs: http://localhost:8000/api/v1/logs/processing
- Examine layer demonstration: http://localhost:8000/api/v1/demo/layers

---

## Version History

- **v1.0.0** (2024-01-15): Initial release
  - Complete FastAPI backend implementation
  - Three proprietary layers (Clarity™, iFRS™, Timesystems™)
  - LIA integration
  - REST + WebSocket APIs
  - Comprehensive logging and documentation
