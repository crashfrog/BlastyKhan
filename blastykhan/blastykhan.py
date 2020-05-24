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

blast_cmd = """
    blastn
    --opt
    --opt2
    --0pt3 {arg}
""".replace('\t', '').replace('\n', ' ')

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

@app.route('/api/submit', method=['POST', 'GET'])
def start():
    "Kick off BLAST job"
    job_dir = pathlib.Path(tempfile.mkdtemp())
    if 'query' in request.form:
        q_string = request.form['query']
        # start a job

        proc = subprocess.Popen()

        jobs_manager().newJob(job_dir, proc)

        return job_id
    elif request.method == 'POST':
        fi = request.files['query_file']
        fi.save(job_dir / secure_filename(fi.filename))
        # start a job

        proc = subprocess.Popen()

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
        return dict()
    return dict(job_id=job_id,
                status="running")

@appcontext_tearing_down.connect_via(app)
def teardown(*args, **kwargs):
    for job, job_dir in jobs_manager().items():
        job.terminate()
        job.wait()
        shutil.rmtree(job_dir)
    