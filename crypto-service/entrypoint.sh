#!/bin/sh

celery -A main worker -B -l info