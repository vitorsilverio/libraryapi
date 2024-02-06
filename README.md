# libraryapi

![deploy](https://github.com/vitorsilverio/libraryapi/actions/workflows/deploy.yml/badge.svg)
![lint](https://github.com/vitorsilverio/libraryapi/actions/workflows/lint.yml/badge.svg)
![Snyk](https://github.com/vitorsilverio/libraryapi/actions/workflows/snyk.yml/badge.svg)
![CodeQL Analysis](https://github.com/vitorsilverio/libraryapi/actions/workflows/codeql-analysis.yml/badge.svg)
![Tests](https://github.com/vitorsilverio/libraryapi/actions/workflows/tests.yml/badge.svg)
[![Dockerhub](https://img.shields.io/docker/pulls/vitorsilverio/libraryapi.svg)](https://hub.docker.com/r/vitorsilverio/libraryapi)

An API to get [MARC (Machine-Readable Cataloging)](https://en.wikipedia.org/wiki/MARC_standards) data in many formats (MARC ISO, MARCXML, mnemonic MARC, JSON) from ILS like Pergamum.

## Update
If you use an instance of Pergamum version 10 or you want to use a JavaScript tool that uses API, see the [Get Pergamum Marc Records](https://github.com/jaideraf/getPergamumMarcRecords) tool.

## Running

### Using [Docker](https://hub.docker.com/r/vitorsilverio/libraryapi)

- `docker pull vitorsilverio/libraryapi:main`
- `docker run -d --name libraryapi -p 8000:80 vitorsilverio/libraryapi:main`

### Locally

- Make sure you have Python 3.12+ installed. You may have to prefix `pip` and `uvicorn` commands with `python3.12 -m` if you have more than one Python interpreter.
- Install [Pipenv](https://pipenv.pypa.io/) with pip: `pip install --user pipenv`
- In Ubuntu 22.04: `export SETUPTOOLS_USE_DISTUTILS=stdlib`
- `pipenv install --deploy`
- `pipenv shell`
- `uvicorn app.main:app --port 80` append `--reload` if you are developing and change the port

## Endpoints and services

Check the endpoints in documentation page at http://**deploy-ip**:**port**/docs

## Demo

See a working demo instance at Heroku:

- <https://libraryapi.sites.ufsc.br/docs>

### Examples (version 2)

Using query params:

- A MARC ISO 2709 record from Pergamum:

<https://libraryapi.sites.ufsc.br/api/v2/pergamum/676009?url=https://catalogobiblioteca.ufmg.br/pergamum/web_service/servidor_ws.php&media_type=application/marc>

- A MARCXML record from Pergamum:

<https://libraryapi.sites.ufsc.br/api/v2/pergamum/676009?url=https://catalogobiblioteca.ufmg.br/pergamum/web_service/servidor_ws.php&media_type=application/xml>

- A mnemonic MARC record (MARCMaker/MarcEdit format) from Pergamum:

<https://libraryapi.sites.ufsc.br/api/v2/pergamum/676009?url=https://catalogobiblioteca.ufmg.br/pergamum/web_service/servidor_ws.php&media_type=text/plain>

- A JSON MARC record from Pergamum (default, if no "media_type" is specified or if it is "application/json"):

<https://libraryapi.sites.ufsc.br/api/v2/pergamum/676009?url=https://catalogobiblioteca.ufmg.br/pergamum/web_service/servidor_ws.php&media_type=application/json>

Using headers:

- A MARC ISO 2709 record from Pergamum:

```console
curl "https://libraryapi.sites.ufsc.br/api/v2/pergamum/676009" \
-H "Server: https://catalogobiblioteca.ufmg.br/pergamum/web_service/servidor_ws.php" \
-H "Accept: application/marc"
```

- A MARCXML record from Pergamum:

```console
curl "https://libraryapi.sites.ufsc.br/api/v2/pergamum/676009" \
-H "Server: https://catalogobiblioteca.ufmg.br/pergamum/web_service/servidor_ws.php" \
-H "Accept: application/xml"
```

- A mnemonic MARC record (MARCMaker/MarcEdit format) from Pergamum:

```console
curl "https://libraryapi.sites.ufsc.br/api/v2/pergamum/676009" \
-H "Server: https://catalogobiblioteca.ufmg.br/pergamum/web_service/servidor_ws.php" \
-H "Accept: text/plain"
```

- A JSON MARC record from Pergamum (default, if no "media_type" is specified or if it is "application/json"):

```console
curl "https://libraryapi.sites.ufsc.br/api/v2/pergamum/676009" \
-H "Server: https://catalogobiblioteca.ufmg.br/pergamum/web_service/servidor_ws.php" \
-H "Accept: application/json"
```

#### Version 1 style (deprecated)

- A MARC ISO 2709 record from Pergamum: <https://libraryapi.sites.ufsc.br/pergamum/mrc?url=https://catalogobiblioteca.ufmg.br/pergamum&id=676009>
- A MARCXML record from Pergamum: <https://libraryapi.sites.ufsc.br/pergamum/xml?url=https://catalogobiblioteca.ufmg.br/pergamum&id=676009>
- A mnemonic MARC record (MARCMaker/MarcEdit format) from Pergamum: <https://libraryapi.sites.ufsc.br/pergamum/mrk?url=https://catalogobiblioteca.ufmg.br/pergamum&id=676009>

## Contributing

Please read [Contibution.md](CONTRIBUTING.md) to know how to contribute code or [buy me a ☕](https://www.buymeacoffee.com/vitorsilverio)
