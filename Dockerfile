FROM python:3.10

WORKDIR /deployment

COPY ./api/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY ./api /deployment/api

CMD ["python3", "./api/script.py"]
