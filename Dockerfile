FROM python:3-slim-bullseye as builder
# This stage installs gcc to compile all python modules that requires it.
# We don't need gcc in final stage

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential

COPY Pipfile .
RUN pip install pipenv
RUN python -m venv /venv
RUN . /venv/bin/activate && pipenv install --deploy

FROM python:3-slim-bullseye
# this stage contains the final code

WORKDIR /app

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

USER app

COPY --from=builder --chown=app:app /venv /venv
ENV PATH="/venv/bin/:${PATH}"

COPY . /app/

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
