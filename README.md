# libraryapi

An API to get [MARC (Machine-Readable Cataloging)](https://en.wikipedia.org/wiki/MARC_standards) data in many formats (MARC ISO, MARCXML) from ILS like Pergamum.

## Running
### Using docker
- `docker pull vitorsilverio/libraryapi:main` 
- `docker run -d --name libraryapi -p 80:80 vitorsilverio/libraryapi:main`

### Locally
- Make sure you have python 3.9+ installed. You may have to prefix `pip` and `uvicorn` commands with `python3.9 -m` if you has more than one python interpreter.
- You can create a virtualenv before
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
