#!/bin/bash
while ! python api_request.py
do
    sleep 1
    echo "Relaunch the program..."
done
