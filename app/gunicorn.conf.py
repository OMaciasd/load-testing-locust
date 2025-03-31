#gunicorn.conf.py
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
timeout = 30
