# error_handler_simple.py - Minimal working version

from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    API_ERROR = "api_error"
    RATE_LIMIT = "rate_limit"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"
    DATA_ERROR = "data_error"
    TOOL_ERROR = "tool_error"
    TIMEOUT_ERROR = "timeout_error"

class ResearchError(Exception):
    def __init__(self, message: str, category=None, severity=None, **kwargs):
        super().__init__(message)
        self.message = message
        self.category = category or ErrorCategory.API_ERROR
        self.severity = severity or ErrorSeverity.MEDIUM
        self.timestamp = datetime.now()
        self.recoverable = kwargs.get('recoverable', True)
        self.metadata = kwargs.get('metadata', {})

class ErrorHandler:
    def __init__(self, logger=None):
        self.logger = logger
        self.error_history = []
        self.error_counts = {}
    
    def log_error(self, error, context=None):
        """Log an error"""
        self.error_history.append({
            'message': str(error),
            'timestamp': datetime.now(),
            'context': context or {}
        })
        
        if self.logger:
            if hasattr(self.logger, 'error'):
                self.logger.error(str(error))
            else:
                print(f"ERROR: {error}")
    
    def handle_error(self, error, context=None, raise_on_critical=True):
        """Handle an error"""
        self.log_error(error, context)
        
        if isinstance(error, ResearchError):
            return error.recoverable
        return False
    
    def get_error_summary(self):
        """Get error summary"""
        return {
            'total_errors': len(self.error_history),
            'by_category': {},
            'by_severity': {},
            'recent_errors': [
                {
                    'message': e['message'],
                    'timestamp': e['timestamp'].isoformat(),
                    'category': 'unknown',
                    'severity': 'unknown'
                }
                for e in self.error_history[-5:]
            ]
        }

# Export the class
__all__ = ['ErrorHandler', 'ResearchError', 'ErrorSeverity', 'ErrorCategory']