import concurrent.futures
import threading


class TaskIteration:
    def __init__(self, functions):
        self.functions = functions
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.future = None
        self.start_index = 0
        self.lock = threading.Lock()

    def iterate_task_list(self, start_index):
        with self.lock:
            for i, function in enumerate(self.functions[start_index:]):
                function()
            return i + start_index

    def start_tasks(self):
        with self.lock:
            self.future = self.executor.submit(self.iterate_task_list, self.start_index)

    def pause_tasks(self):
        with self.lock:
            if self.future:
                self.future.cancel()
                self.start_index = self.future.result()
                self.future = None

    def resume_tasks(self):
        with self.lock:
            if not self.future:
                self.future = self.executor.submit(self.iterate_task_list, self.start_index)