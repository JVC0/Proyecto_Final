import os

import django
from rq import Worker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()


class BaseDeathPenalty:
    def __init__(self, timeout, exception_class, **kwargs):
        self.timeout = timeout
        self.exception_class = exception_class
        self.job_id = kwargs.get("job_id")

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class SimpleWorker(Worker):
    death_penalty_class = BaseDeathPenalty

    def main_work_horse(self, *args, **kwargs):
        raise NotImplementedError("Test worker does not implement this method")

    def execute_job(self, *args, **kwargs):
        """Execute job in same thread/process"""
        return self.perform_job(*args, **kwargs)
