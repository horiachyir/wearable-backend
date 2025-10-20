"""
BLE Device Simulator
Simulates Bluetooth Low Energy wearable device data streaming
"""

import asyncio
import numpy as np
from datetime import datetime
from typing import Dict, Optional
import random

from app.models.schemas import BiosignalData, DeviceStatus


class BLESimulator:
    """
    Simulates a BLE wearable device generating realistic biosignal data
    """

    def __init__(self):
        self.is_running = False
        self.device_id = "WEARABLE_SIM_001"
        self.firmware_version = "2.1.4"
        self.battery_level = 87.0
        self.signal_strength = random.randint(-70, -40)  # RSSI in dBm

        # Signal generation parameters
        self.time_offset = 0
        self.base_values = {
            'heart_rate': 75.0,
            'spo2': 98.0,
            'temperature': 36.8,
            'activity': 30.0
        }

        # Oscillation patterns for realistic variation
        self.patterns = {
            'heart_rate': {'freq': 0.1, 'amplitude': 10},
            'spo2': {'freq': 0.05, 'amplitude': 2},
            'temperature': {'freq': 0.02, 'amplitude': 0.3},
            'activity': {'freq': 0.15, 'amplitude': 40}
        }

        # Current data cache
        self.current_data = None
        self.last_update = None

        # Background update task
        self.update_task = None

    async def start(self):
        """Start the BLE simulator"""
        self.is_running = True
        self.update_task = asyncio.create_task(self._update_loop())

    async def stop(self):
        """Stop the BLE simulator"""
        self.is_running = False
        if self.update_task:
            self.update_task.cancel()
            try:
                await self.update_task
            except asyncio.CancelledError:
                pass

    async def _update_loop(self):
        """Background task to continuously update biosignal data"""
        while self.is_running:
            try:
                self.current_data = self._generate_biosignal_data()
                self.last_update = datetime.now()

                # Slowly drain battery
                self.battery_level = max(0, self.battery_level - 0.0001)

                # Vary signal strength slightly
                self.signal_strength = random.randint(-70, -40)

                # Wait 100ms (10Hz update rate)
                await asyncio.sleep(0.1)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in BLE simulator update loop: {e}")
                await asyncio.sleep(1)

    def _generate_biosignal_data(self) -> Dict[str, float]:
        """
        Generate realistic biosignal data using sinusoidal patterns with noise
        """
        data = {}

        for signal_type, base_value in self.base_values.items():
            pattern = self.patterns[signal_type]

            # Generate sinusoidal wave
            sine_wave = pattern['amplitude'] * np.sin(
                2 * np.pi * pattern['freq'] * self.time_offset
            )

            # Add realistic noise
            noise = np.random.normal(0, pattern['amplitude'] * 0.2)

            # Calculate value
            value = base_value + sine_wave + noise

            # Apply realistic constraints
            if signal_type == 'heart_rate':
                value = np.clip(value, 45, 180)
            elif signal_type == 'spo2':
                value = np.clip(value, 90, 100)
            elif signal_type == 'temperature':
                value = np.clip(value, 35.5, 38.5)
            elif signal_type == 'activity':
                value = np.clip(value, 0, 150)

            data[signal_type] = round(float(value), 2)

        self.time_offset += 0.01

        return data

    async def get_current_data(self) -> BiosignalData:
        """Get current biosignal data"""
        if self.current_data is None:
            self.current_data = self._generate_biosignal_data()

        return BiosignalData(**self.current_data)

    async def get_device_status(self) -> DeviceStatus:
        """Get current device status"""
        return DeviceStatus(
            device_id=self.device_id,
            is_connected=self.is_running,
            battery_level=round(self.battery_level, 1),
            signal_strength=self.signal_strength,
            firmware_version=self.firmware_version,
            last_updated=datetime.now()
        )

    def inject_anomaly(self, signal_type: str, anomaly_type: str = 'spike'):
        """
        Inject an anomaly into a specific signal for testing

        Args:
            signal_type: One of 'heart_rate', 'spo2', 'temperature', 'activity'
            anomaly_type: 'spike' or 'drop'
        """
        if signal_type in self.base_values:
            if anomaly_type == 'spike':
                self.base_values[signal_type] *= random.uniform(1.3, 1.5)
            elif anomaly_type == 'drop':
                self.base_values[signal_type] *= random.uniform(0.6, 0.8)

    def reset_to_normal(self):
        """Reset all signals to normal baseline values"""
        self.base_values = {
            'heart_rate': 75.0,
            'spo2': 98.0,
            'temperature': 36.8,
            'activity': 30.0
        }

    def simulate_exercise(self):
        """Simulate exercise scenario"""
        self.base_values['heart_rate'] = 140.0
        self.base_values['activity'] = 120.0
        self.base_values['temperature'] = 37.5

    def simulate_rest(self):
        """Simulate resting scenario"""
        self.base_values['heart_rate'] = 60.0
        self.base_values['activity'] = 5.0
        self.base_values['temperature'] = 36.5

    def simulate_sleep(self):
        """Simulate sleep scenario"""
        self.base_values['heart_rate'] = 55.0
        self.base_values['activity'] = 0.0
        self.base_values['temperature'] = 36.3
        self.base_values['spo2'] = 97.0
