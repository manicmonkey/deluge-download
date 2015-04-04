#!/bin/bash
set -e
while true; do
  ./deluge_download.py
  echo "Sleeping for 2 minutes"
  sleep 120
done
