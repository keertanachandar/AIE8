# error_handler.py - Complete error handling system

from typing import Optional, Dict, Any, Callable
from enum import Enum
import traceback
from dataclasses import dataclass
from datetime import datetime
import functools
import asyncio

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Categories of errors"""
    API_ERROR = "api_error"
    RATE_LIMIT = "rate_limit"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"
    DATA_ERROR = "data_error"
    TOOL_ERROR = "tool_error"
    TIMEOUT_ERROR = "timeout_error"
    AUTHENTICATION_ERROR = "authentication_error"
    CONFIGURATION_ERROR = "configuration_error"

@dataclass
class ErrorContext:
    """Context information for an error"""
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    timestamp: datetime
    component: str
    traceback_info: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    retry_count: int = 0
    recoverable: bool = True

class ResearchError(Exception):
    """Base exception for research workflow"""
    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.API_ERROR,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None,
        recoverable: bool = True
    ):
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.metadata = metadata or {}
        self.recoverable = recoverable
        self.timestamp = datetime.now()

class RateLimitError(ResearchError):
    """Raised when rate limit is hit"""
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.RATE_LIMIT,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        self.retry_after = retry_after

class ToolExecutionError(ResearchError):
    """Raised when tool execution fails"""
    def __init__(self, tool_name: str, message: str, **kwargs):
        super().__init__(
            f"Tool '{tool_name}' failed: {message}",
            category=ErrorCategory.TOOL_ERROR,
            **kwargs
        )
        self.tool_name = tool_name

class ValidationError(ResearchError):
    """Raised when input validation fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.VALIDATION_ERROR,
            severity=ErrorSeverity.LOW,
            **kwargs
        )

class ErrorHandler:
    """Central error handler for research workflow"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.error_history = []
        self.error_counts = {cat: 0 for cat in ErrorCategory}
    
    def log_error(self, error: ResearchError, context: Optional[Dict] = None):
        """Log an error with context"""
        error_ctx = ErrorContext(
            category=error.category,
            severity=error.severity,
            message=error.message,
            timestamp=error.timestamp,
            component=context.get("component", "unknown") if context else "unknown",
            traceback_info=traceback.format_exc(),
            metadata={**error.metadata, **(context or {})}
        )
        
        self.error_history.append(error_ctx)
        self.error_counts[error.category] += 1
        
        if self.logger:
            log_method = self._get_log_method(error.severity)
            log_message = f"[{error.category.value}] {error.message}"
            
            # Handle different logger types
            if hasattr(self.logger, 'log'):
                # Standard Python logger
                level_map = {
                    ErrorSeverity.LOW: 20,      # INFO
                    ErrorSeverity.MEDIUM: 30,   # WARNING
                    ErrorSeverity.HIGH: 40,     # ERROR
                    ErrorSeverity.CRITICAL: 50  # CRITICAL
                }
                self.logger.log(level_map.get(error.severity, 40), log_message)
            elif callable(log_method):
                log_method(log_message)
            else:
                print(log_message)
    
    def _get_log_method(self, severity: ErrorSeverity):
        """Get appropriate logging method based on severity"""
        if not self.logger:
            return print
        
        severity_map = {
            ErrorSeverity.LOW: getattr(self.logger, 'info', print),
            ErrorSeverity.MEDIUM: getattr(self.logger, 'warning', print),
            ErrorSeverity.HIGH: getattr(self.logger, 'error', print),
            ErrorSeverity.CRITICAL: getattr(self.logger, 'critical', print)
        }
        return severity_map.get(severity, getattr(self.logger, 'error', print))
    
    def handle_error(
        self,
        error: Exception,
        context: Optional[Dict] = None,
        raise_on_critical: bool = True
    ) -> bool:
        """
        Handle an error and determine if execution should continue
        
        Returns:
            bool: True if execution can continue, False otherwise
        """
        if isinstance(error, ResearchError):
            self.log_error(error, context)
            
            if error.severity == ErrorSeverity.CRITICAL and raise_on_critical:
                raise error
            
            return error.recoverable
        else:
            # Wrap unknown errors
            wrapped_error = ResearchError(
                str(error),
                category=ErrorCategory.API_ERROR,
                severity=ErrorSeverity.HIGH,
                metadata={"original_type": type(error).__name__}
            )
            self.log_error(wrapped_error, context)
            return False
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors"""
        return {
            "total_errors": len(self.error_history),
            "by_category": {cat.value: count for cat, count in self.error_counts.items()},
            "by_severity": {
                severity.value: sum(
                    1 for e in self.error_history 
                    if e.severity == severity
                )
                for severity in ErrorSeverity
            },
            "recent_errors": [
                {
                    "category": e.category.value,
                    "severity": e.severity.value,
                    "message": e.message,
                    "timestamp": e.timestamp.isoformat()
                }
                for e in self.error_history[-5:]
            ]
        }

def with_error_handling(
    component: str,
    error_handler: Optional[ErrorHandler] = None,
    fallback_value: Any = None
):
    """Decorator for functions that need error handling"""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if error_handler:
                    context = {"component": component, "function": func.__name__}
                    can_continue = error_handler.handle_error(e, context, raise_on_critical=False)
                    if not can_continue and fallback_value is not None:
                        return fallback_value
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if error_handler:
                    context = {"component": component, "function": func.__name__}
                    can_continue = error_handler.handle_error(e, context, raise_on_critical=False)
                    if not can_continue and fallback_value is not None:
                        return fallback_value
                raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator