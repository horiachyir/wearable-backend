"""
Logging utilities for the backend
"""

import logging
import sys
from datetime import datetime
from typing import List, Dict, Any
from collections import deque


class ProcessingLogger:
    """
    Special logger for tracking layer processing
    Stores logs in memory for demonstration purposes
    """

    def __init__(self, max_logs: int = 1000):
        self.logs = deque(maxlen=max_logs)
        self.max_logs = max_logs

    def info(self, message: str, data: Dict[str, Any] = None):
        """Log info level message"""
        self._log('INFO', message, data)

    def warning(self, message: str, data: Dict[str, Any] = None):
        """Log warning level message"""
        self._log('WARNING', message, data)

    def error(self, message: str, data: Dict[str, Any] = None):
        """Log error level message"""
        self._log('ERROR', message, data)

    def _log(self, level: str, message: str, data: Dict[str, Any] = None):
        """Internal log method"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'data': data or {}
        }
        self.logs.append(log_entry)

    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent logs"""
        logs_list = list(self.logs)
        return logs_list[-limit:]

    def clear(self):
        """Clear all logs"""
        self.logs.clear()


# Global processing logger instance
_processing_logger = ProcessingLogger()


def get_processing_logger() -> ProcessingLogger:
    """Get the global processing logger instance"""
    return _processing_logger


def setup_logger(name: str) -> logging.Logger:
    """
    Setup standard Python logger with formatting

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Console handler with formatting
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    # Format: [TIME] LEVEL - Message
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
