"""
Demo Client Script for Wearable Biosignal Analysis System
Demonstrates the complete data flow through all proprietary layers
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any


class DemoClient:
    """
    Demonstration client for the Wearable Biosignal Analysis API
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None

    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)

    def print_section(self, title: str):
        """Print section divider"""
        print(f"\n--- {title} ---")

    def print_json(self, data: Dict[Any, Any], indent: int = 2):
        """Pretty print JSON data"""
        print(json.dumps(data, indent=indent, default=str))

    def test_health(self):
        """Test health endpoint"""
        self.print_header("1. HEALTH CHECK")

        response = requests.get(f"{self.base_url}/api/v1/health")
        data = response.json()

        print(f"Status: {data['status']}")
        print(f"Services:")
        for service, status in data['services'].items():
            status_icon = "✓" if status else "✗"
            print(f"  {status_icon} {service}: {status}")
        print(f"Connected clients: {data['connected_clients']}")
        print(f"Active sessions: {data['active_sessions']}")

    def test_connection(self):
        """Test device connection"""
        self.print_header("2. DEVICE CONNECTION")

        payload = {
            "device_id": "DEMO_CLIENT_001",
            "device_type": "mobile_app",
            "app_version": "1.0.0",
            "user_id": "demo_user"
        }

        print("Connecting to backend...")
        print(f"Request: POST {self.base_url}/api/v1/connect")
        print(f"Payload:")
        self.print_json(payload)

        response = requests.post(f"{self.base_url}/api/v1/connect", json=payload)
        data = response.json()

        if data['success']:
            self.session_id = data['session_id']
            print(f"\n✓ Connection successful!")
            print(f"Session ID: {self.session_id}")
            print(f"Device Status:")
            print(f"  - Device ID: {data['device_status']['device_id']}")
            print(f"  - Battery: {data['device_status']['battery_level']}%")
            print(f"  - Signal Strength: {data['device_status']['signal_strength']} dBm")
            print(f"  - Firmware: {data['device_status']['firmware_version']}")
            print(f"\nAvailable Features:")
            for feature in data['available_features']:
                print(f"  ✓ {feature}")
        else:
            print("✗ Connection failed!")

    def test_stream_data(self):
        """Test stream data endpoint"""
        self.print_header("3. BIOSIGNAL DATA STREAMING")

        print(f"Request: GET {self.base_url}/api/v1/stream")
        print("Retrieving real-time biosignal data processed through all layers...\n")

        response = requests.get(f"{self.base_url}/api/v1/stream")
        data = response.json()

        # Raw signals
        self.print_section("Raw Biosignals")
        raw = data['raw_signals']
        print(f"Heart Rate:    {raw['heart_rate']:.1f} BPM")
        print(f"SpO2:          {raw['spo2']:.1f} %")
        print(f"Temperature:   {raw['temperature']:.1f} °C")
        print(f"Activity:      {raw['activity']:.1f} steps/min")

        # Clarity layer
        self.print_section("Clarity™ Layer - Signal Quality & Noise Reduction")
        clarity = data['clarity_layer']
        print(f"Quality Score:        {clarity['quality_score']:.2f}/1.00")
        print(f"Signal-to-Noise:      {clarity['signal_to_noise_ratio']:.1f} dB")
        print(f"Quality Assessment:   {clarity['quality_assessment'].upper()}")
        print(f"Noise Reduction:      {'Applied' if clarity['noise_reduction_applied'] else 'Not needed'}")
        if clarity['artifacts_detected']:
            print(f"Artifacts Detected:   {', '.join(clarity['artifacts_detected'])}")
        else:
            print(f"Artifacts Detected:   None")

        # iFRS layer
        self.print_section("iFRS™ Layer - Intelligent Frequency Response")
        ifrs = data['ifrs_layer']
        print(f"Dominant Frequency:   {ifrs['dominant_frequency']:.2f} Hz")
        print(f"Rhythm:               {ifrs['rhythm_classification'].replace('_', ' ').title()}")
        print(f"Respiratory Rate:     {ifrs['respiratory_rate']:.1f} breaths/min")
        print(f"\nHeart Rate Variability:")
        hrv = ifrs['hrv_features']
        print(f"  HRV Score:          {hrv['hrv_score']:.1f}/100")
        print(f"  RMSSD:              {hrv['rmssd']:.1f} ms")
        print(f"  SDNN:               {hrv['sdnn']:.1f} ms")
        print(f"  pNN50:              {hrv['pnn50']:.1f}%")
        print(f"\nFrequency Bands:")
        fb = ifrs['frequency_bands']
        print(f"  VLF:                {fb['vlf']:.1f}%")
        print(f"  LF:                 {fb['lf']:.1f}%")
        print(f"  HF:                 {fb['hf']:.1f}%")
        print(f"  LF/HF Ratio:        {fb['lf_hf_ratio']:.2f}")

        # Timesystems layer
        self.print_section("Timesystems™ Layer - Temporal Analysis & Circadian Rhythm")
        timesys = data['timesystems_layer']
        print(f"Pattern Type:          {timesys['pattern_type'].title()}")
        print(f"Circadian Phase:       {timesys['circadian_phase'].title()}")
        print(f"Temporal Consistency:  {timesys['temporal_consistency']:.2f}/1.00")
        print(f"Rhythm Score:          {timesys['rhythm_score']:.1f}/100")
        print(f"\nCircadian Alignment:")
        ca = timesys['circadian_alignment']
        print(f"  Expected HR:         {ca['expected_heart_rate']:.1f} BPM")
        print(f"  Actual HR:           {ca['actual_heart_rate']:.1f} BPM")
        print(f"  Alignment Score:     {ca['alignment_score']:.2f}/1.00")
        print(f"  Phase Shift:         {ca['phase_shift_minutes']:.1f} minutes")

        # LIA insights
        self.print_section("LIA Engine - Lifestyle Intelligence Analysis")
        lia = data['lia_insights']
        print(f"Condition:            {lia['condition']}")
        print(f"Confidence:           {lia['confidence']:.1%}")
        print(f"Wellness Score:       {lia['wellness_score']:.1f}/100")
        print(f"\nWellness Assessment:")
        wa = lia['wellness_assessment']
        print(f"  Cardiovascular:     {wa['cardiovascular_health']:.1f}/100")
        print(f"  Respiratory:        {wa['respiratory_health']:.1f}/100")
        print(f"  Activity Level:     {wa['activity_level']:.1f}/100")
        print(f"  Stress Level:       {wa['stress_level']:.1f}/100")
        print(f"  Overall:            {wa['overall_wellness']:.1f}/100")

        if lia['positive_indicators']:
            print(f"\nPositive Indicators:")
            for indicator in lia['positive_indicators']:
                print(f"  ✓ {indicator}")

        if lia['risk_factors']:
            print(f"\nRisk Factors:")
            for risk in lia['risk_factors']:
                print(f"  ⚠ {risk}")

        print(f"\nRecommendation: {lia['recommendation']}")

    def test_prediction(self):
        """Test prediction endpoint"""
        self.print_header("4. HEALTH CONDITION PREDICTION")

        print(f"Request: GET {self.base_url}/api/v1/predict")

        response = requests.get(f"{self.base_url}/api/v1/predict")
        data = response.json()

        print(f"\nCondition:     {data['condition']}")
        print(f"Confidence:    {data['confidence']:.1%}")
        print(f"Wellness:      {data['wellness_score']:.1f}/100")
        print(f"Quality:       {data['signal_quality'].upper()}")
        print(f"\nTop Probabilities:")
        sorted_probs = sorted(
            data['probabilities'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for condition, prob in sorted_probs:
            bar = "█" * int(prob * 50)
            print(f"  {condition:25s} {prob:.1%} {bar}")

    def test_layer_demo(self):
        """Test comprehensive layer demonstration"""
        self.print_header("5. LAYER PROCESSING DEMONSTRATION")

        print(f"Request: GET {self.base_url}/api/v1/demo/layers")
        print("This shows the complete data flow through all processing layers...\n")

        response = requests.get(f"{self.base_url}/api/v1/demo/layers")
        data = response.json()

        print(f"Total Layers: {data['total_layers']}")
        print(f"Processing Pipeline: {' → '.join(data['summary']['layers_applied'])}")
        print(f"Processing Time: {data['summary']['total_processing_time_ms']}")

        # Show each step
        pipeline = data['processing_pipeline']

        for key in sorted(pipeline.keys()):
            step = pipeline[key]
            print(f"\n{'-' * 80}")
            print(f"{step['description']}")
            if 'layer' in step:
                print(f"Layer: {step['layer']}")
            if 'processing_details' in step:
                print(f"Processing Details:")
                for detail_key, detail_value in step['processing_details'].items():
                    print(f"  • {detail_key}: {detail_value}")

    def test_logs(self):
        """Test processing logs endpoint"""
        self.print_header("6. PROCESSING LOGS")

        print(f"Request: GET {self.base_url}/api/v1/logs/processing?limit=10")

        response = requests.get(f"{self.base_url}/api/v1/logs/processing", params={"limit": 10})
        data = response.json()

        print(f"\nShowing last {min(10, data['total'])} of {data['total']} log entries:\n")

        for log in data['logs'][-10:]:
            timestamp = log['timestamp'].split('T')[1][:12]
            level = log['level']
            message = log['message']
            print(f"[{timestamp}] {level:8s} | {message}")

    def test_continuous_stream(self, duration: int = 10):
        """Test continuous streaming"""
        self.print_header("7. CONTINUOUS STREAMING TEST")

        print(f"Streaming data for {duration} seconds...")
        print("Press Ctrl+C to stop\n")

        try:
            for i in range(duration):
                response = requests.get(f"{self.base_url}/api/v1/stream")
                data = response.json()

                # Extract key metrics
                hr = data['raw_signals']['heart_rate']
                wellness = data['lia_insights']['wellness_score']
                condition = data['lia_insights']['condition']

                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] HR: {hr:5.1f} BPM | Wellness: {wellness:5.1f}/100 | {condition}")

                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\nStreaming stopped by user")

    def run_all_tests(self):
        """Run all demonstration tests"""
        print("\n")
        print("█" * 80)
        print("█" + " " * 78 + "█")
        print("█" + "  Wearable Biosignal Analysis System - Demonstration Client".center(78) + "█")
        print("█" + " " * 78 + "█")
        print("█" * 80)
        print("\nBackend URL:", self.base_url)
        print("Demonstrating: Clarity™, iFRS™, Timesystems™ layers + LIA integration")

        try:
            # Run tests
            self.test_health()
            time.sleep(1)

            self.test_connection()
            time.sleep(1)

            self.test_stream_data()
            time.sleep(1)

            self.test_prediction()
            time.sleep(1)

            self.test_layer_demo()
            time.sleep(1)

            self.test_logs()
            time.sleep(1)

            # Optional continuous streaming
            print("\n\nWould you like to see continuous streaming? (This will stream for 10 seconds)")
            print("Starting continuous stream in 3 seconds... (Ctrl+C to skip)")
            try:
                time.sleep(3)
                self.test_continuous_stream(10)
            except KeyboardInterrupt:
                print("\nSkipped continuous streaming")

            # Summary
            self.print_header("DEMONSTRATION COMPLETE")
            print("\n✓ All tests completed successfully!")
            print("\nNext steps:")
            print("  1. Open Swagger UI: http://localhost:8000/docs")
            print("  2. Import Postman collection: POSTMAN_COLLECTION.json")
            print("  3. Review technical documentation: TECHNICAL_DOCUMENTATION.md")
            print("  4. Connect mobile app to test full integration")
            print("\n")

        except requests.exceptions.ConnectionError:
            print("\n❌ ERROR: Cannot connect to backend!")
            print("Please ensure the backend is running:")
            print("  cd backend && python main.py")
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    client = DemoClient()
    client.run_all_tests()
