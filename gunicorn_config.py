import multiprocessing
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

name = "portfolio_dimitri"
bind = "unix:/run/gunicorn/portfolio.sock"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30

accesslog = "/var/log/gunicorn/portfolio_access.log"
errorlog = "/var/log/gunicorn/portfolio_error.log"
loglevel = "info"

proc_name = "portfolio_dimitri"
daemon = False

raw_env = [
    "DJANGO_SETTINGS_MODULE=portfolio_dimitri.settings",
]

