FROM python:3.10-slim as builder
# This stage installs gcc to compile all python modules that requires it.
# We don't need gcc in final stage

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential

COPY Pipfile .
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM python:3.10-slim
# this stage contains the final code

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

USER app

COPY . /app/

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
