FROM python:3.10.9

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "server:app", "--host=0.0.0.0", "--port=80"]

#docker image build --tag fastapi_mine .
#docker container run --publish 5000:80 --name fastapi_mine fastapi_mine
#uvicorn server:app --host=0.0.0.0 --port=80