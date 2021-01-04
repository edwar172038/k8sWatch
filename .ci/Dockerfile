FROM nexus-docker.test.cyclone.com/testdev/python-base:latest

WORKDIR /data/app

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python3","watchEvent.py" ]
