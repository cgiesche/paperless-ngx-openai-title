#!/bin/bash

# Start cron in background
cron -f &


exec python ./find_documents_with_tag_id.py
