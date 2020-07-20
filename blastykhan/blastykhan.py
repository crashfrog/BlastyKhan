from flask import Flask, appcontext_tearing_down, g
from multiprocessing.managers import BaseManager
from werkzeug.utils import secure_filename

import click

import tempfile
import subprocess
import uuid
import pathlib
import shutil

app = Flask(__name__)


def jobs_manager():
    if not hasattr(g, 'jobs_server'):
        manager = BaseManager(('', 37844), b'')
        manager.register('get_jobs')
        manager.connect()
        g.jobs_manager = manager
    return g.jobs_manager

@app.route('/')
def index():
    return """
<html>
<head>
<title>BlastyKhan</title>
</head>
<body>
</body>
</html>
"""

@app.route('/api/submit', method=['POST',])
def start():
    "Kick off BLAST job"

    blast_cmd = """
        blastn
        --opt
        --opt2
        --0pt3 {arg}
""".replace('\t', '').replace('\n', ' ')

    job_dir = pathlib.Path(tempfile.mkdtemp())
    fa = request.files['file_a']
    file_a = job_dir / secure_filename(fa.filename)
    fa.save(file_a)
    fb = request.files['file_b']
    file_b = job_dir / secure_filename(fb.filename)
    fb.save(file_b)

    # start a job

    proc = subprocess.Popen(blast_cmd.format(**locals()).split())

    jobs_manager().newJob(job_dir, proc)

    return job_id



@app.route('/api/poll/<job_id>')
def poll(job_id):
    job, job_dir = jobs_manager().getJob(job_id)
    if job.poll():
        if job.returncode:
            return dict(job_id=job_id,
                        status="failed")
        # else
        jobs_manager().rmJob(job_id)
        shutil.rmtree(job_dir)
        return dict() # alignment from BLAST
    return dict(job_id=job_id,
                status="running")

@appcontext_tearing_down.connect_via(app)
def teardown(*args, **kwargs):
    for job, job_dir in jobs_manager().items():
        job.terminate()
        job.wait()
        shutil.rmtree(job_dir)
    