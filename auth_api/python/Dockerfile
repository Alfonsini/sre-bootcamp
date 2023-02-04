FROM python:3-alpine

# Add your instructions to dockerize the application
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

ENV FLASK_APP=app/__init__.py
ENV DATABASE_URI="mysql+pymysql://secret:jOdznoyH6swQB9sTGdLUeeSrtejWkcw@sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com:3306/bootcamp_tht"
ENV JWT_SECRET_KEY='my2w7wjd7yXF64FIADfJxNs1oupTGAuW'

# App must run on port 8000
EXPOSE 5000

CMD [ "python -m flask run --host=0.0.0.0" ]
