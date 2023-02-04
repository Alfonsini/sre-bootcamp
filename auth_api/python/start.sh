#!/bin/bash

app_name="wize-alfonso-ramirez:latest"

sudo docker build -t ${app_name} .

sudo docker run -d -p 8000:5000 ${app_name}