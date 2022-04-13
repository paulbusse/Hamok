import threading
from queue import Queue

import llog
from const import (
    ARGUMENTS,
    JOBID,
    PAYLOAD,
    JobID,
    ENTITY,
    CALLBACK,
)


class Jobs:
    def __init__(self):
        self._queue = Queue()
        for i in range(3):
            worker = threading.Thread(target=self.job_handler, args=(i,), daemon=True)
            worker.start()

    def schedule(self, job):
        job[JOBID] = JobID.SCHEDULE
        self._queue.put(job)


    def wait(self):
        self._queue.join()


    def execute_updatejob(self, ent, payload):
        self._queue.put({
            JOBID: JobID.UPDATE,
            ENTITY: ent,
            PAYLOAD: payload,
        })

    def job_handler(self, i):
        while True:
            job = self._queue.get()

            if job[JOBID] == JobID.UPDATE:
                entity = job[ENTITY]
                value = job[PAYLOAD]
                llog.debug(f"Worker {i} is executing <Updating HA>")
                entity.set_haval(value)

            elif job[JOBID] == JobID.SCHEDULE:
                llog.debug(f"Worker {i} is executing <{job[CALLBACK].__name__}>.")
                job[CALLBACK](*job[ARGUMENTS])

            self._queue.task_done()


jobhandler = Jobs()