#!/bin/bash

if [ "${YOLO_ENV}" = "development" ]; then
  exec fastapi dev --port=80 yolo/main.py
else
  exec fastapi run --host=0.0.0.0 --port=80 yolo/main.py
fi