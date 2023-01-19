#!/bin/bash
export PATH=$PATH:/usr/local/python3/bin
ln -s /app/client/exploit /app/exploit
ln -s /app/client/core /app/core
nginx;
gunicorn app:myscan_app -c gunicorn_config.py

