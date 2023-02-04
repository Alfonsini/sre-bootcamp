FROM python:3-alpine

# Add your instructions to dockerize the application
RUN mkdir -p /usr/src/api
WORKDIR /usr/src/api

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=true

# App must run on port 8000
# EXPOSE 8000

CMD ["sh", "-c", "sleep 5 && python -m flask run --port 5000 --host=0.0.0.0" ]