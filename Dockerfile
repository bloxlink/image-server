FROM python:3.8.0

WORKDIR /usr/src/bloxlink-image-server

ADD . /usr/src/bloxlink-image-server

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
RUN apt install dumb-init

EXPOSE 8000

ENTRYPOINT ["dumb-init", "-v", "--", "python3", "src/main.py"]