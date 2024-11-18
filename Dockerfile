FROM python:3.9.13

WORKDIR /presensi-wajah

RUN apt-get -y update
# for dlib
RUN apt-get install -y build-essential cmake
# for opencv
RUN apt-get install -y libopencv-dev

RUN pip install dlib -vvv

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "web:app"]