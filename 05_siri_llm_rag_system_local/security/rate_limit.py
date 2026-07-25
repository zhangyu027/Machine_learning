from __future__ import annotations

import time
from collections import defaultdict, deque
from threading import Lock


class InMemoryRateLimiter:
    def __init__(self, requests_per_minute: int):
        self.limit = requests_per_minute
        self.events = defaultdict(deque)
        self.lock = Lock()

    def allow(self, key: str) -> bool:
        now = time.time()
        cutoff = now - 60
        with self.lock:
            bucket = self.events[key]
            while bucket and bucket[0] < cutoff:
                bucket.popleft()
            if len(bucket) >= self.limit:
                return False
            bucket.append(now)
            return True
