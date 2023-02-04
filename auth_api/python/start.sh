#!/bin/bash

app_name='wize-alfonso-ramirez:latest'
database_user=''
database_password=''
database_url=''
database_port='3306'
database_name=''
jwt_secret_key=''

database_uri="mysql+pymysql://${database_user}:${database_password}@${database_url}/${database_name}"


sudo docker build -t ${app_name} .

sudo docker run -d \
	-e DATABASE_URI=${database_uri} \
	-e JWT_SECRET_KEY=${jwt_secret_key} \
	-p 8000:5000 \
	${app_name}