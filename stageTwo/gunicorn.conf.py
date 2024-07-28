# gunicorn.conf.py

import multiprocessing
import os

bind = f"0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
