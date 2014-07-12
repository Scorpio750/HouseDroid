#!/bin/bash
if [ $# -ne 1 ]; then
  echo "./client.sh [port]"
  exit 1
fi
gst-launch-0.10 -v udpsrc port=${1} ! \
  jpegdec ! \
  autovideosink
