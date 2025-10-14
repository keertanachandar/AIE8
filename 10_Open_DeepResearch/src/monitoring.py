# monitoring.py - Health checks and monitoring

from typing import Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

@dataclass
class HealthStatus:
    """Health check status"""
    healthy: bool
    status: str
    checks: Dict[str, bool]
    warnings: List[str]
    errors: List[str]
    timestamp: datetime

class SystemMonitor:
    """Monitor system health and performance"""
    
    def __init__(self, logger, error_handler, rate_limiter):
        self.logger = logger
        self.error_handler = error_handler
        self.rate_limiter = rate_limiter
        self.start_time = datetime.now()
    
    def check_health(self) -> HealthStatus:
        """Perform comprehensive health check"""
        checks = {}
        warnings = []
        errors = []
        
        # Check error rate
        error_summary = self.error_handler.get_error_summary()
        total_errors = error_summary["total_errors"]
        checks["errors_acceptable"] = total_errors < 10
        
        if total_errors >= 10:
            warnings.append(f"High error count: {total_errors}")
        if total_errors >= 50:
            errors.append(f"Critical error count: {total_errors}")
        
        # Check rate limiter
        rl_metrics = self.rate_limiter.get_metrics()
        rate_limited = rl_metrics["rate_limited"]
        cost_limited = rl_metrics["cost_limited"]
        
        checks["rate_limits_ok"] = rate_limited < 20
        checks["cost_limits_ok"] = cost_limited == 0
        
        if rate_limited >= 20:
            warnings.append(f"Frequent rate limiting: {rate_limited} times")
        if cost_limited > 0:
            errors.append(f"Cost limits hit: {cost_limited} times")
        
        # Check costs
        hourly_cost = rl_metrics["current_hourly_cost"]
        hourly_limit = rl_metrics["hourly_limit"]
        hourly_usage_pct = (hourly_cost / hourly_limit) * 100 if hourly_limit > 0 else 0
        
        checks["cost_under_control"] = hourly_usage_pct < 80
        
        if hourly_usage_pct >= 80:
            warnings.append(f"High hourly cost usage: {hourly_usage_pct:.1f}%")
        if hourly_usage_pct >= 95:
            errors.append(f"Critical hourly cost usage: {hourly_usage_pct:.1f}%")
        
        # Overall health
        healthy = all(checks.values()) and len(errors) == 0
        
        if healthy:
            status = "HEALTHY"
        elif len(errors) > 0:
            status = "CRITICAL"
        elif len(warnings) > 0:
            status = "WARNING"
        else:
            status = "DEGRADED"
        
        return HealthStatus(
            healthy=healthy,
            status=status,
            checks=checks,
            warnings=warnings,
            errors=errors,
            timestamp=datetime.now()
        )
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report"""
        runtime = datetime.now() - self.start_time
        logger_metrics = self.logger.get_metrics()
        rl_metrics = self.rate_limiter.get_metrics()
        error_summary = self.error_handler.get_error_summary()
        
        return {
            "runtime": {
                "seconds": runtime.total_seconds(),
                "formatted": str(runtime)
            },
            "api_performance": {
                "total_calls": logger_metrics["api_calls"],
                "successful_calls": logger_metrics["successful_requests"],
                "success_rate": logger_metrics["success_rate"],
                "tokens_used": logger_metrics["tokens_used"],
                "total_cost": logger_metrics["total_cost"],
                "avg_cost_per_call": logger_metrics["average_cost_per_call"]
            },
            "rate_limiting": {
                "rate_limited_count": rl_metrics["rate_limited"],
                "cost_limited_count": rl_metrics["cost_limited"],
                "retries": rl_metrics["retries"]
            },
            "errors": {
                "total": error_summary["total_errors"],
                "by_category": error_summary["by_category"],
                "by_severity": error_summary["by_severity"]
            },
            "cost_tracking": {
                "hourly_cost": rl_metrics["current_hourly_cost"],
                "hourly_limit": rl_metrics["hourly_limit"],
                "daily_cost": rl_metrics["current_daily_cost"],
                "daily_limit": rl_metrics["daily_limit"]
            }
        }
    
    def print_health_check(self):
        """Print health check results"""
        health = self.check_health()
        
        status_emoji = {
            "HEALTHY": "✅",
            "WARNING": "⚠️",
            "DEGRADED": "🔶",
            "CRITICAL": "🚨"
        }
        
        print("\n" + "="*60)
        print(f"SYSTEM HEALTH CHECK {status_emoji.get(health.status, '❓')}")
        print("="*60)
        print(f"Status: {health.status}")
        print(f"Time: {health.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nChecks:")
        for check, passed in health.checks.items():
            icon = "✓" if passed else "✗"
            print(f"  {icon} {check}")
        
        if health.warnings:
            print(f"\n⚠️  Warnings ({len(health.warnings)}):")
            for warning in health.warnings:
                print(f"  - {warning}")
        
        if health.errors:
            print(f"\n🚨 Errors ({len(health.errors)}):")
            for error in health.errors:
                print(f"  - {error}")
        
        print("="*60 + "\n")
    
    def print_performance_report(self):
        """Print performance report"""
        report = self.get_performance_report()
        
        print("\n" + "="*60)
        print("PERFORMANCE REPORT")
        print("="*60)
        
        print(f"\n⏱️  Runtime: {report['runtime']['formatted']}")
        
        print(f"\n🔧 API Performance:")
        api = report['api_performance']
        print(f"  Total Calls:     {api['total_calls']}")
        print(f"  Success Rate:    {api['success_rate']*100:.1f}%")
        print(f"  Tokens Used:     {api['tokens_used']:,}")
        print(f"  Total Cost:      ${api['total_cost']:.4f}")
        print(f"  Avg Cost/Call:   ${api['avg_cost_per_call']:.4f}")
        
        print(f"\n🛡️  Rate Limiting:")
        rl = report['rate_limiting']
        print(f"  Rate Limited:    {rl['rate_limited_count']} times")
        print(f"  Cost Limited:    {rl['cost_limited_count']} times")
        print(f"  Retries:         {rl['retries']}")
        
        print(f"\n💰 Cost Tracking:")
        cost = report['cost_tracking']
        hourly_pct = (cost['hourly_cost'] / cost['hourly_limit'] * 100) if cost['hourly_limit'] > 0 else 0
        daily_pct = (cost['daily_cost'] / cost['daily_limit'] * 100) if cost['daily_limit'] > 0 else 0
        print(f"  Hourly:  ${cost['hourly_cost']:.2f} / ${cost['hourly_limit']:.2f} ({hourly_pct:.1f}%)")
        print(f"  Daily:   ${cost['daily_cost']:.2f} / ${cost['daily_limit']:.2f} ({daily_pct:.1f}%)")
        
        print(f"\n⚠️  Errors:")
        errors = report['errors']
        print(f"  Total:           {errors['total']}")
        if errors['by_category']:
            print(f"  By Category:")
            for cat, count in errors['by_category'].items():
                if count > 0:
                    print(f"    - {cat}: {count}")
        
        print("="*60 + "\n")
    
    def export_metrics(self, filepath: str = "metrics_export.json"):
        """Export metrics to JSON file"""
        metrics = {
            "health": self.check_health().__dict__,
            "performance": self.get_performance_report(),
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filepath, "w") as f:
            json.dump(metrics, f, indent=2, default=str)
        
        print(f"✓ Metrics exported to {filepath}")