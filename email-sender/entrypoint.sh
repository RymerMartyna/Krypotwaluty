#!/bin/sh

celery -A main worker --pool=prefork -l info