#!/bin/bash

if [ -z "$SERVER_HOST" ]
then
  export SERVER_HOST="localhost"
fi

if [ -z "$SERVER_PORT" ]
then
  export SERVER_PORT="5000"
fi

if [ -z "$RATE_LIMIT" ]
then
  export RATE_LIMIT="10"
fi

if [ -z "$GRID_MAX_X" ]
then
  export GRID_MAX_X="100"
fi

if [ -z "$GRID_MAX_Y" ]
then
  export GRID_MAX_Y="100"
fi

if [ -z "$SCAN_DISTANCE_X" ]
then
  export SCAN_DISTANCE_X="5"
fi

if [ -z "$SCAN_DISTANCE_Y" ]
then
  export SCAN_DISTANCE_Y="5"
fi

if [ -z "$MAX_CLAIMS" ]
then
  export MAX_CLAIMS="3"
fi

if [ -z "$SHOW_IMAGE" ]
then
  export SHOW_IMAGE="0"
fi

python3 bot.py