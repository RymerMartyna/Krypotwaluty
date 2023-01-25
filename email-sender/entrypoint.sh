#!/bin/sh

celery -A process_email worker -l info -Q email_queue