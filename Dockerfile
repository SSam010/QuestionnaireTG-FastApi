FROM python:3.11

WORKDIR /usr/src/quest

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
