# Contributing

Please install Pipenv and run `pipenv install --dev` before starting your branch.
libraryapi is a free and open-source project that welcomes contributions from everyone. Make sure to run `pre-commit install` before commit, so code will be ok to be reviewed.

## Using Docker

If you don't want to install all the Python dependencies, you can use a Docker container and edit the Python files directly, checking the changes on the browser at http://0.0.0.0:8000/docs. To do this you need to use the `docker-compose.yml` and to run:

`docker-compose up --build`
