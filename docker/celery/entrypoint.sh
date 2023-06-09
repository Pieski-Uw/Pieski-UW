#!/bin/bash

pushd django
celery -A pieskiUW worker --loglevel=info --concurrency 1 -E