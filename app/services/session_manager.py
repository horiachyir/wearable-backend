"""
Session Manager - Handle monitoring sessions
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid

from app.models.schemas import SessionResponse, SessionType


class SessionManager:
    """
    Manages monitoring sessions for users/devices
    """

    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.active_sessions: List[str] = []

    async def create_session(
        self,
        device_id: str,
        user_id: Optional[str] = None,
        session_type: SessionType = SessionType.DAILY_MONITORING
    ) -> SessionResponse:
        """
        Create a new monitoring session

        Args:
            device_id: Device identifier
            user_id: Optional user identifier
            session_type: Type of session

        Returns:
            Session details
        """
        session_id = f"session_{uuid.uuid4().hex[:12]}"

        session_data = {
            'session_id': session_id,
            'device_id': device_id,
            'user_id': user_id,
            'session_type': session_type,
            'start_time': datetime.now(),
            'end_time': None,
            'status': 'active',
            'data_points_collected': 0,
            'average_wellness_score': None,
            'summary': None,
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        }

        self.sessions[session_id] = session_data
        self.active_sessions.append(session_id)

        return SessionResponse(**session_data)

    async def get_session(self, session_id: str) -> Optional[SessionResponse]:
        """Get session by ID"""
        session_data = self.sessions.get(session_id)
        if session_data:
            return SessionResponse(**session_data)
        return None

    async def end_session(self, session_id: str, summary: Optional[str] = None):
        """End a monitoring session"""
        if session_id in self.sessions:
            self.sessions[session_id]['end_time'] = datetime.now()
            self.sessions[session_id]['status'] = 'completed'
            self.sessions[session_id]['summary'] = summary

            if session_id in self.active_sessions:
                self.active_sessions.remove(session_id)

    async def add_data_point(self, session_id: str):
        """Increment data points counter"""
        if session_id in self.sessions:
            self.sessions[session_id]['data_points_collected'] += 1

    async def update_wellness_score(self, session_id: str, wellness_score: float):
        """Update average wellness score"""
        if session_id in self.sessions:
            current_avg = self.sessions[session_id]['average_wellness_score']
            count = self.sessions[session_id]['data_points_collected']

            if current_avg is None:
                self.sessions[session_id]['average_wellness_score'] = wellness_score
            else:
                # Running average
                new_avg = ((current_avg * (count - 1)) + wellness_score) / count
                self.sessions[session_id]['average_wellness_score'] = round(new_avg, 1)

    def get_active_session_count(self) -> int:
        """Get count of active sessions"""
        return len(self.active_sessions)

    def get_all_sessions(self) -> List[SessionResponse]:
        """Get all sessions"""
        return [SessionResponse(**data) for data in self.sessions.values()]
