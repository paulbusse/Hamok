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

    def execute_alljob(self):
        self._queue.put({JOBID: JobID.ALL})

    def execute_updatejob(self, ent, payload):
        self._queue.put({
            JOBID: JobID.UPDATE,
            ENTITY: ent,
            PAYLOAD: payload,
        })

    def job_handler(self, i):
        while True:
            job = self._queue.get()
            llog.debug(f"Worker {i} is executing {job}")

            # PYTHON 3.10 use switch statement
            if job[JOBID] == JobID.ALL:
                from oekofen import oekofenc
                import parse
                fdata = oekofenc.load()
                if fdata:
                    parse.parser(fdata)
                else:
                    llog.error("Could not retrieve information from Ökofen system.")

            elif job[JOBID] == JobID.UPDATE:
                entity = job[ENTITY]
                value = job[PAYLOAD]
                entity.set_haval(value)

            elif job[JOBID] == JobID.SCHEDULE:
                job[CALLBACK](*job[ARGUMENTS])

            self._queue.task_done()


jobhandler = Jobs()