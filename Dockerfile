FROM python:latest

COPY . /

RUN pip install -r /requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]