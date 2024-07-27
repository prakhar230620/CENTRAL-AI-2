import logging
from queue import PriorityQueue
from threading import Thread, Event
import time

class Task:
    def __init__(self, func, args=(), kwargs={}, priority=0):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

class TaskScheduler:
    def __init__(self, max_workers=10):
        self.logger = logging.getLogger(__name__)
        self.task_queue = PriorityQueue()
        self.max_workers = max_workers
        self.workers = []
        self.stop_event = Event()

    def start(self):
        self.logger.info("Starting TaskScheduler")
        for _ in range(self.max_workers):
            worker = Thread(target=self._worker_loop)
            worker.start()
            self.workers.append(worker)

    def stop(self):
        self.logger.info("Stopping TaskScheduler")
        self.stop_event.set()
        for worker in self.workers:
            worker.join()
        self.workers.clear()

    def schedule_task(self, func, args=(), kwargs={}, priority=0):
        task = Task(func, args, kwargs, priority)
        self.task_queue.put(task)
        self.logger.info(f"Scheduled task: {func.__name__} with priority {priority}")

    def _worker_loop(self):
        while not self.stop_event.is_set():
            try:
                task = self.task_queue.get(timeout=1)
                self.logger.info(f"Executing task: {task.func.__name__}")
                task.func(*task.args, **task.kwargs)
                self.task_queue.task_done()
            except Exception as e:
                if not isinstance(e, TimeoutError):
                    self.logger.error(f"Error executing task: {str(e)}")

    def get_queue_size(self):
        return self.task_queue.qsize()

    def clear_queue(self):
        with self.task_queue.mutex:
            self.task_queue.queue.clear()
        self.logger.info("Task queue cleared")