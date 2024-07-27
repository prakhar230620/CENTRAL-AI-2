import psutil
import time
import logging
from threading import Thread, Event

class PerformanceMonitor:
    def __init__(self, interval=5):
        self.interval = interval
        self.stop_event = Event()
        self.logger = logging.getLogger(__name__)
        self.thread = Thread(target=self._monitor, daemon=True)
        self.metrics = {}

    def start(self):
        self.logger.info("Starting Performance Monitor")
        self.thread.start()

    def stop(self):
        self.logger.info("Stopping Performance Monitor")
        self.stop_event.set()
        self.thread.join()

    def _monitor(self):
        while not self.stop_event.is_set():
            self.metrics['cpu'] = psutil.cpu_percent(interval=1)
            self.metrics['memory'] = psutil.virtual_memory().percent
            self.metrics['disk'] = psutil.disk_usage('/').percent
            self.metrics['network'] = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

            self.logger.info(f"Current metrics: {self.metrics}")

            # Check for threshold violations
            if self.metrics['cpu'] > 80:
                self.logger.warning(f"High CPU usage detected: {self.metrics['cpu']}%")
            if self.metrics['memory'] > 80:
                self.logger.warning(f"High memory usage detected: {self.metrics['memory']}%")

            time.sleep(self.interval)

    def get_metrics(self):
        return self.metrics

    def set_interval(self, interval):
        self.interval = interval
        self.logger.info(f"Monitoring interval updated to {interval} seconds")