FROM python:3.12

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app" ,"--port", "8000", "--host", "0.0.0.0" ]