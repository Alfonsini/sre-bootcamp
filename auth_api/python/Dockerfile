FROM python:3-alpine

# Add your instructions to dockerize the application
RUN mkdir -p /usr/src/api
WORKDIR /usr/src/api

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=true
ENV DATABASE_URI="mysql+pymysql://secret:jOdznoyH6swQB9sTGdLUeeSrtejWkcw@sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com:3306/bootcamp_tht"
ENV JWT_SECRET_KEY='my2w7wjd7yXF64FIADfJxNs1oupTGAuW'

# App must run on port 8000
# EXPOSE 8000

CMD ["sh", "-c", "sleep 5 && python -m flask run --port 5000 --host=0.0.0.0" ]