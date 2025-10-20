# Wearable Biosignal Analysis Backend

FastAPI-based backend for processing biosignals through proprietary Reconnect layers: **Timesystems™**, **iFRS™**, and **Clarity™**, integrated with **LIA** (Lifestyle Intelligence Analysis).

## Quick Start

### Local Development

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Run the Server

From the project root:

```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or using the Python module directly:

```bash
python3 -m app.main
```

### 3. Access the API

- **API Base**: http://localhost:8000
- **Swagger UI** (Interactive Docs): http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Run Demo Client

```bash
python3 app/demo_client.py
```

This will demonstrate:
- Device connection
- Real-time data streaming
- Processing through all three proprietary layers
- LIA health insights
- Continuous streaming mode

## Deployment to Render.com

### Quick Deploy (5 Minutes)

See [QUICKSTART_RENDER.md](QUICKSTART_RENDER.md) for step-by-step deployment instructions.

**TL;DR:**
1. Push code to GitHub
2. Create new Blueprint on Render.com
3. Connect repository (render.yaml auto-detected)
4. Deploy!

### Detailed Deployment Guide

For comprehensive deployment instructions, troubleshooting, and best practices, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md).

## Key Features

### Proprietary Processing Layers

1. **Clarity™** - Signal Quality & Noise Reduction
   - Adaptive wavelet-based noise reduction
   - Multi-channel quality assessment
   - SNR calculation and artifact detection
   - Quality scores: Excellent, Good, Fair, Poor

2. **iFRS™** - Intelligent Frequency Response System
   - FFT-based frequency analysis
   - Heart Rate Variability (HRV) extraction
   - Rhythm classification
   - Respiratory rate estimation
   - Frequency band analysis (VLF, LF, HF)

3. **Timesystems™** - Temporal Analysis & Circadian Rhythm
   - Pattern recognition (stable, increasing, decreasing, oscillating, irregular)
   - Circadian phase detection
   - Temporal consistency scoring
   - Rhythm health assessment

4. **LIA Engine** - Lifestyle Intelligence Analysis
   - 10 health condition classifications
   - Multi-dimensional wellness scoring
   - Risk factor identification
   - Personalized recommendations

### API Endpoints

#### Core Endpoints
- `GET /` - API information
- `GET /api/v1/health` - Health check
- `POST /api/v1/connect` - Connect device
- `GET /api/v1/stream` - Get processed biosignal data
- `GET /api/v1/predict` - Get health prediction
- `WS /ws/stream` - WebSocket real-time streaming

#### Session Management
- `POST /api/v1/sessions` - Create session
- `GET /api/v1/sessions/{id}` - Get session details

#### Demonstration
- `GET /api/v1/demo/layers` - Complete layer processing demo
- `GET /api/v1/logs/processing` - Processing logs

## Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Connect device
curl -X POST http://localhost:8000/api/v1/connect \
  -H "Content-Type: application/json" \
  -d '{"device_id":"TEST_001","device_type":"mobile_app","app_version":"1.0.0"}'

# Get stream data
curl http://localhost:8000/api/v1/stream

# Layer demonstration
curl http://localhost:8000/api/v1/demo/layers
```

### Using Postman

Import `POSTMAN_COLLECTION.json` for a complete test suite with:
- All endpoints pre-configured
- Example requests
- Automatic session ID extraction

### Using Python Demo Client

```bash
python demo_client.py
```

Runs comprehensive demonstration of all features.

## Data Flow

```
BLE Simulator
    ↓ (Heart Rate, SpO2, Temperature, Activity)
Clarity™ Layer
    ↓ (Enhanced signals + Quality metrics)
iFRS™ Layer
    ↓ (Frequency features + HRV)
Timesystems™ Layer
    ↓ (Temporal patterns + Circadian analysis)
LIA Engine
    ↓ (Health insights + Wellness scores)
API Response
```

## Project Structure

```
backend/
├── main.py                    # FastAPI application
├── requirements.txt           # Dependencies
├── demo_client.py            # Demo script
├── TECHNICAL_DOCUMENTATION.md # Full technical docs
├── POSTMAN_COLLECTION.json   # Postman test collection
├── models/
│   └── schemas.py            # Pydantic models
├── services/
│   ├── ble_simulator.py      # BLE device simulation
│   ├── clarity.py            # Clarity™ layer
│   ├── ifrs.py               # iFRS™ layer
│   ├── timesystems.py        # Timesystems™ layer
│   ├── lia_integration.py    # LIA engine
│   └── session_manager.py    # Session management
└── utils/
    └── logger.py             # Logging utilities
```

## Mobile App Integration

### Configuration

In your React Native app, update the API configuration:

```typescript
// src/services/api.ts
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',  // iOS Simulator
  // BASE_URL: 'http://10.0.2.2:8000', // Android Emulator
  // BASE_URL: 'http://YOUR_IP:8000',  // Physical device
  WS_URL: 'ws://localhost:8000/ws/stream',
};
```

### Example Usage

```typescript
// Connect to backend
const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/connect`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    device_id: 'MOBILE_APP_001',
    device_type: 'mobile_app',
    app_version: '1.0.0',
  }),
});

// Get stream data
const streamData = await fetch(`${API_CONFIG.BASE_URL}/api/v1/stream`);
const data = await streamData.json();

console.log('Wellness Score:', data.lia_insights.wellness_score);
console.log('Condition:', data.lia_insights.condition);
```

## Biosignal Data Format

### Raw Signals
- **Heart Rate**: 45-180 BPM
- **SpO2**: 90-100%
- **Temperature**: 35.5-38.5°C
- **Activity**: 0-150 steps/min

### Processing Output

Each `/api/v1/stream` request returns:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "raw_signals": {...},
  "clarity_layer": {
    "quality_score": 0.92,
    "signal_to_noise_ratio": 38.5,
    "quality_assessment": "excellent",
    ...
  },
  "ifrs_layer": {
    "dominant_frequency": 1.25,
    "hrv_features": {...},
    "rhythm_classification": "normal_sinus",
    ...
  },
  "timesystems_layer": {
    "pattern_type": "stable",
    "circadian_phase": "afternoon",
    "rhythm_score": 82.5,
    ...
  },
  "lia_insights": {
    "condition": "Normal Resting",
    "confidence": 0.92,
    "wellness_score": 85.3,
    "wellness_assessment": {...},
    "recommendation": "Maintain current activity levels",
    ...
  }
}
```

## Demonstration Features

### Real-Time Streaming
- 10 Hz update rate (100ms intervals)
- WebSocket support for continuous streaming
- REST API for polling

### Layer Processing Logs
View detailed processing at each layer:

```bash
curl http://localhost:8000/api/v1/logs/processing?limit=50
```

Example log:
```
CLARITY_LAYER | quality=0.92 | snr=38.5dB | noise_reduced=false
IFRS_LAYER | dominant_freq=1.25Hz | hrv_score=75.2 | rhythm=normal_sinus
TIMESYSTEMS_LAYER | pattern=stable | circadian_phase=afternoon | temporal_consistency=0.88
LIA_ENGINE | condition=Normal Resting | confidence=0.920 | wellness_score=85.3
```

### Complete Layer Demo
```bash
curl http://localhost:8000/api/v1/demo/layers
```

Returns step-by-step breakdown showing:
- Raw input at each stage
- Processing algorithms used
- Output at each stage
- Detailed metrics and parameters

## Performance

- **Response Time**: < 50ms average
- **Processing Latency**: < 20ms per layer
- **Total Pipeline**: < 50ms (real-time capable)
- **WebSocket Rate**: 10 Hz (100ms intervals)
- **Concurrent Clients**: 100+ supported

## Development

### Code Style
```bash
# Format code
black backend/

# Lint code
flake8 backend/
```

### Running Tests
```bash
pytest tests/ -v
```

## Troubleshooting

### Port in use
```bash
# Change port
uvicorn main:app --port 8001
```

### Import errors
```bash
# Ensure you're in the backend directory
cd backend
python main.py
```

### CORS issues
CORS is configured to allow all origins. For production, update `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://yourapp.com"],  # Specific origins
    ...
)
```

## Documentation

- **Technical Documentation**: `TECHNICAL_DOCUMENTATION.md`
- **API Documentation**: http://localhost:8000/docs
- **Postman Collection**: `POSTMAN_COLLECTION.json`

## Support

For detailed information about:
- **Architecture**: See TECHNICAL_DOCUMENTATION.md
- **API Reference**: Open http://localhost:8000/docs
- **Data Models**: Check `models/schemas.py`
- **Processing Layers**: See individual service files in `services/`

## License

Proprietary - All Rights Reserved

**Reconnect™ Proprietary Layers**:
- Clarity™
- iFRS™ (Intelligent Frequency Response System)
- Timesystems™
