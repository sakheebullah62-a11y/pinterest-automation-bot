from datetime import datetime, timedelta
from collections import Counter

class AnalyticsAgent:
    """Analytics and reporting agent"""
    
    def __init__(self):
        self.pins_history = []
    
    def track_pin(self, pin_data):
        """Track generated pin"""
        pin_data["tracked_at"] = datetime.now().isoformat()
        self.pins_history.append(pin_data)
    
    def get_performance_report(self):
        """Generate performance report"""
        if not self.pins_history:
            return {
                "total_pins": 0,
                "message": "No data yet"
            }
        
        total = len(self.pins_history)
        
        # Count by niche
        niches = Counter(p.get("niche") for p in self.pins_history)
        
        # Count by status
        statuses = Counter(p.get("status") for p in self.pins_history)
        
        # Count by platform
        platforms = Counter(p.get("link_platform") for p in self.pins_history if p.get("link_platform"))
        
        return {
            "total_pins": total,
            "by_niche": dict(niches),
            "by_status": dict(statuses),
            "by_platform": dict(platforms),
            "last_updated": datetime.now().isoformat()
        }
    
    def get_trending_niches(self):
        """Get most used niches"""
        niches = [p.get("niche") for p in self.pins_history]
        counter = Counter(niches)
        return counter.most_common(5)
    
    def get_daily_stats(self, days=7):
        """Get last N days statistics"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_pins = [
            p for p in self.pins_history 
            if datetime.fromisoformat(p.get("tracked_at", "2000-01-01")) > cutoff_date
        ]
        
        return {
            "total_pins_last_days": len(recent_pins),
            "days": days,
            "average_per_day": len(recent_pins) / days if days > 0 else 0
        }
