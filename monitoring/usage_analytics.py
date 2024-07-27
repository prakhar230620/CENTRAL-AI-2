import json
from datetime import datetime, timedelta
from collections import defaultdict

class UsageAnalytics:
    def __init__(self, storage_file='usage_analytics.json'):
        self.storage_file = storage_file
        self.usage_data = defaultdict(lambda: defaultdict(int))
        self.load_data()

    def load_data(self):
        try:
            with open(self.storage_file, 'r') as f:
                self.usage_data = json.load(f)
        except FileNotFoundError:
            self.usage_data = {}

    def save_data(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.usage_data, f)

    def record_event(self, event_type, user_id=None):
        date = datetime.now().strftime("%Y-%m-%d")
        self.usage_data[date][event_type] += 1
        if user_id:
            self.usage_data[date][f"user_{user_id}_{event_type}"] += 1
        self.save_data()

    def get_daily_stats(self, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        return self.usage_data.get(date, {})

    def get_weekly_stats(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        stats = defaultdict(int)
        for i in range(7):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for event, count in self.usage_data.get(date, {}).items():
                stats[event] += count
        return dict(stats)

    def get_user_stats(self, user_id, days=30):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        stats = defaultdict(int)
        for i in range(days):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for event, count in self.usage_data.get(date, {}).items():
                if event.startswith(f"user_{user_id}_"):
                    stats[event.split('_')[-1]] += count
        return dict(stats)