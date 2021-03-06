from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_is_running():
    response = client.get("/docs")
    assert response.status_code == 200


def test_download_marc_xml_from_pergamum():
    response = client.get(
        "/pergamum/xml?url=https://pergamum.ufsc.br/pergamum&id=339742"
    )
    assert response.headers["content-type"] == "application/xml; charset=utf-8"
    assert response.status_code == 200


def test_api_v2():
    response = client.get(
        "/api/v2/pergamum/339742",
        headers={
            "Accept": "application/xml",
            "Server": "https://pergamum.ufsc.br/pergamum/web_service/servidor_ws.php",
        },
    )
    assert response.headers["content-type"] == "application/xml; charset=utf-8"
    assert response.status_code == 200
