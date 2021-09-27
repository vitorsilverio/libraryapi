# libraryapi

It's an API for get marc data in many formats (Marc xml, Marc binary) from ILS like Pergamum.

## Running
### Using docker
- `docker pull vitorsilverio/libraryapi` 
- `docker run -d --name libraryapi -p 80:80 libraryapi`

### Locally
- Make sure you have python 3.9+ installed
- You can create a virtualenv before
- `pip install -r requirements.txt`
- `uvicorn app.main:app --port 80`

## Endpoints and services
Check the endpoints in documentation page at http://**deploy-ip**:**port**/docs
