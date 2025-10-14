# research_logger.py - Comprehensive logging system

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json
from logging.handlers import RotatingFileHandler

class ResearchLogger:
    """Centralized logging for research workflow"""
    
    def __init__(
        self,
        name: str = "research",
        log_dir: str = "logs",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        max_bytes: int = 10_000_000,  # 10MB
        backup_count: int = 5
    ):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []  # Clear existing handlers
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_level)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (rotating)
        log_file = self.log_dir / f"{name}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(file_level)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Cost tracking log
        cost_log_file = self.log_dir / f"{name}_costs.log"
        self.cost_handler = RotatingFileHandler(
            cost_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        cost_formatter = logging.Formatter(
            '%(asctime)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.cost_handler.setFormatter(cost_formatter)
        
        # Metrics
        self.metrics = {
            "api_calls": 0,
            "tokens_used": 0,
            "errors": 0,
            "successful_requests": 0,
            "total_cost": 0.0
        }
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.metrics["errors"] += 1
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.metrics["errors"] += 1
        self.logger.critical(message, extra=kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)
    
    def log_api_call(
        self,
        model: str,
        tokens_used: int,
        cost: float,
        duration: float,
        success: bool = True,
        metadata: Optional[Dict] = None
    ):
        """Log API call with cost tracking"""
        self.metrics["api_calls"] += 1
        self.metrics["tokens_used"] += tokens_used
        self.metrics["total_cost"] += cost
        
        if success:
            self.metrics["successful_requests"] += 1
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "tokens": tokens_used,
            "cost_usd": cost,
            "duration_seconds": duration,
            "success": success,
            "metadata": metadata or {}
        }
        
        self.cost_handler.handle(
            logging.LogRecord(
                name=self.name,
                level=logging.INFO,
                pathname="",
                lineno=0,
                msg=json.dumps(log_entry),
                args=(),
                exc_info=None
            )
        )
        
        self.logger.info(
            f"API Call | Model: {model} | Tokens: {tokens_used} | Cost: ${cost:.4f} | Duration: {duration:.2f}s"
        )
    
    def log_tool_usage(self, tool_name: str, success: bool, duration: float, result: Any = None):
        """Log tool usage"""
        status = "✓" if success else "✗"
        self.logger.info(
            f"Tool {status} | {tool_name} | Duration: {duration:.2f}s"
        )
    
    def log_research_stage(self, stage: str, status: str, metadata: Optional[Dict] = None):
        """Log research workflow stage"""
        self.logger.info(
            f"Stage: {stage} | Status: {status}",
            extra={"stage": stage, "status": status, "metadata": metadata or {}}
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return {
            **self.metrics,
            "average_cost_per_call": (
                self.metrics["total_cost"] / self.metrics["api_calls"]
                if self.metrics["api_calls"] > 0 else 0
            ),
            "success_rate": (
                self.metrics["successful_requests"] / self.metrics["api_calls"]
                if self.metrics["api_calls"] > 0 else 0
            )
        }
    
    def print_summary(self):
        """Print metrics summary"""
        metrics = self.get_metrics()
        print("\n" + "="*60)
        print("RESEARCH SESSION SUMMARY")
        print("="*60)
        print(f"API Calls:        {metrics['api_calls']}")
        print(f"Tokens Used:      {metrics['tokens_used']:,}")
        print(f"Total Cost:       ${metrics['total_cost']:.4f}")
        print(f"Avg Cost/Call:    ${metrics['average_cost_per_call']:.4f}")
        print(f"Success Rate:     {metrics['success_rate']*100:.1f}%")
        print(f"Errors:           {metrics['errors']}")
        print("="*60 + "\n")