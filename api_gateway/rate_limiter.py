import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_times = deque()

    def allow_request(self):
        current_time = time.time()

        # Remove old requests
        while self.request_times and current_time - self.request_times[0] > self.time_window:
            self.request_times.popleft()

        # Check if we're within the rate limit
        if len(self.request_times) < self.max_requests:
            self.request_times.append(current_time)
            return True

        return False