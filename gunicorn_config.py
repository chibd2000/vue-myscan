# gunicorn.conf
# gunicorn app:myscan_app -c gunicorn_config.py
bind = "0.0.0.0:5000"
workers = 4
backlog = 2048
pidfile = "log/gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/debug.log"
timeout = 600
debug = True
capture_output = True
