FROM jjanzic/docker-python3-opencv

COPY requirements.txt /app/

# RUN pip install opencv-python

# RUN apt-get build-dep 
# RUN apt-get install libjpeg
# RUN pip install PIL

RUN pip install face_recognition

RUN pip install -r /app/requirements.txt

COPY . .

COPY ./creds.json /app/creds.json

CMD python main.py