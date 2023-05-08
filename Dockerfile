FROM python:3.11

RUN mkdir /questionnaire

WORKDIR /questionnaire

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
