FROM python:3.12

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD [ "uvicorn", "main:app" ,"--port", "80", "--host", "0.0.0.0" ]