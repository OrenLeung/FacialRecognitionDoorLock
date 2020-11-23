FROM jjanzic/docker-python3-opencv

RUN pip install face_recognition

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY . .

COPY ./creds.json /app/creds.json

CMD python main.py