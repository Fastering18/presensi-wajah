FROM python:3.9.13

WORKDIR /presensi-wajah

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "web.py"]