FROM python:3.8-alpine

COPY requirements.txt /app/

RUN pip install opencv-python

RUN apt-get build-dep python-imaging
RUN apt-get install libjpeg62 libjpeg62-dev
RUN pip install PIL

RUN pip install face_recognition

RUN pip install -r /app/requirements.txt

COPY . /app