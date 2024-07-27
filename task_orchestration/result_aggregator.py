import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict


class ResultAggregator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.results = defaultdict(list)

    def add_result(self, task_id, result):
        self.results[task_id].append(result)
        self.logger.info(f"Added result for task {task_id}")

    def get_results(self, task_id):
        return self.results.get(task_id, [])

    def clear_results(self, task_id):
        if task_id in self.results:
            del self.results[task_id]
            self.logger.info(f"Cleared results for task {task_id}")

    def aggregate_results(self, task_id, aggregation_func):
        results = self.get_results(task_id)
        if not results:
            self.logger.warning(f"No results found for task {task_id}")
            return None

        try:
            aggregated_result = aggregation_func(results)
            self.logger.info(f"Aggregated results for task {task_id}")
            return aggregated_result
        except Exception as e:
            self.logger.error(f"Error aggregating results for task {task_id}: {str(e)}")
            return None

    def parallel_aggregate(self, tasks, aggregation_func, max_workers=5):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(self.aggregate_results, task_id, aggregation_func): task_id for task_id in
                              tasks}
            aggregated_results = {}
            for future in as_completed(future_to_task):
                task_id = future_to_task[future]
                try:
                    aggregated_results[task_id] = future.result()
                except Exception as e:
                    self.logger.error(f"Error in parallel aggregation for task {task_id}: {str(e)}")

        return aggregated_results