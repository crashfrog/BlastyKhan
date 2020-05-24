from multiprocessing.managers import BaseManager
from collections import UserDict
import uuid()


jobs = {}

def newJob(job_dir, running_process):
    job_id = uuid.uuid4()
    jobs[job_id] = (job_dir, running_process)
    return job_id

def getJob(job_id):
    return self.jobs[job_id]

def rmJob(job_id):
    del self.jobs[job_id]

def items():
    return jobs.items()

if __name__ == '__main__':
    mngr =  BaseManager(('', 37844), b'')
    mngr.register('newJob', newJob)
    mngr.register('getJob', getJob)
    mngr.register('rmJob', rmJob)
    mngr.register('items', items)
    svr = mngr.get_server()
    svr.serve_forever()