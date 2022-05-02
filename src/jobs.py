import threading
from queue import Queue

import llog
from const import (
    ARGUMENTS,
    CALLBACK,
)


class Jobs:
    def __init__(self):
        self._queue = Queue()
        for i in range(3):
            worker = threading.Thread(target=self.job_handler, args=(i,), daemon=True)
            worker.start()

    def schedule(self, job):
        self._queue.put(job)


    def wait(self):
        self._queue.join()


    def job_handler(self, i):
        while True:
            job = self._queue.get()

            llog.debug(f"Worker {i} is executing <{job[CALLBACK].__name__}>.")
            job[CALLBACK](*job[ARGUMENTS])

            self._queue.task_done()


jobhandler = Jobs()