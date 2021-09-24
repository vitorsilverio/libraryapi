FROM python:3.7

RUN apt-get update && apt-get install -y libsaxonb-java yaz openjdk-11-jre

COPY ./app /app
COPY ./libraryapi /libraryapi
COPY ./* /

RUN pip install -r /requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]