FROM python:3.7

RUN mkdir /usr/app
WORKDIR /usr/app

COPY . .

EXPOSE 5000

RUN pip install -r requirements.txt
CMD python app.py