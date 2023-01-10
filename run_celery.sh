#!/bin/bash
export PATH=$PATH:/usr/local/python3/bin
celery -A celery_tasks.main beat -l info &
celery -A celery_tasks.main worker -l info -c 1 -Q task_queue &
celery -A celery_tasks.main worker -l info -c 2
