FROM python:3.8.1

WORKDIR /usr/src/bloxlink-image-server

ADD . /usr/src/bloxlink-image-server

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8001

ENTRYPOINT ["python3", "src/main.py"]