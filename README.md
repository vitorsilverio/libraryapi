# libraryapi
![deploy](https://github.com/vitorsilverio/libraryapi/actions/workflows/deploy.yml/badge.svg)
![lint](https://github.com/vitorsilverio/libraryapi/actions/workflows/lint.yml/badge.svg)
![Snyk](https://github.com/vitorsilverio/libraryapi/actions/workflows/snyk.yml/badge.svg)
![CodeQL Analysis](https://github.com/vitorsilverio/libraryapi/actions/workflows/codeql-analysis.yml/badge.svg)
![Tests](https://github.com/vitorsilverio/libraryapi/actions/workflows/tests.yml/badge.svg)
[![Dockerhub](https://img.shields.io/docker/pulls/vitorsilverio/libraryapi.svg)](https://hub.docker.com/r/vitorsilverio/libraryapi)
[![Known Vulnerabilities](https://snyk.io/test/github/vitorsilverio/libraryapi/badge.svg)](https://snyk.io/test/github/vitorsilverio/libraryapi)

An API to get [MARC (Machine-Readable Cataloging)](https://en.wikipedia.org/wiki/MARC_standards) data in many formats (MARC ISO, MARCXML, mnemonic MARC) from ILS like Pergamum.

## Running
### Using [docker](https://hub.docker.com/r/vitorsilverio/libraryapi)
- `docker pull vitorsilverio/libraryapi:main`
- `docker run -d --name libraryapi -p 80:80 vitorsilverio/libraryapi:main`

### Locally
- Make sure you have Python 3.9+ installed. You may have to prefix `pip` and `uvicorn` commands with `python3.9 -m` if you have more than one Python interpreter.
- You can create a [virtualenv](https://virtualenv.pypa.io/) before
- `pip install -r requirements.txt`
- `uvicorn app.main:app --port 80`

## Endpoints and services
Check the endpoints in documentation page at http://**deploy-ip**:**port**/docs

## Demo
See a working demo instance at Heroku:
 - https://libraryapi-demo.herokuapp.com/docs

### Examples
 - A MARC ISO 2709 record from Pergamum: https://libraryapi-demo.herokuapp.com/pergamum/mrc?url=https://pergamum.ufsc.br/pergamum&id=339742
 - A MARCXML record from Pergamum: https://libraryapi-demo.herokuapp.com/pergamum/xml?url=https://pergamum.ufsc.br/pergamum&id=339742
 - A mnemonic MARC record (MARCMaker/MarcEdit format) from Pergamum: https://libraryapi-demo.herokuapp.com/pergamum/mrk?url=https://pergamum.ufsc.br/pergamum&id=339742

## Contributing
Please read [Contibution.md](CONTRIBUTING.md) to know how to contribute code or [buy me a ☕](https://www.buymeacoffee.com/vitorsilverio)
