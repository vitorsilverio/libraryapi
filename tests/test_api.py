import warnings

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
    if response.status_code == 400:
        warnings.warn("Test ignored")
        warnings.warn(response.content)
        return
    assert response.headers["content-type"] == "application/xml; charset=utf-8"
    assert response.status_code == 200


def test_api_v2_ufsc():
    response = client.get(
        "/api/v2/pergamum/339742",
        headers={
            "Accept": "application/xml",
            "Server": "https://pergamum.ufsc.br/pergamum/web_service/servidor_ws.php",
        },
    )
    if response.status_code == 400:
        warnings.warn("Test ignored")
        warnings.warn(response.content)
        return

    assert response.headers["content-type"] == "application/xml; charset=utf-8"
    assert response.status_code == 200


def test_api_v2_ufpa():
    response = client.get(
        "/api/v2/pergamum/181408",
        headers={
            "Accept": "application/xml",
            "Server": "https://bibcentral.ufpa.br/pergamum/web_service/servidor_ws.php",
        },
    )
    if response.status_code == 400:
        warnings.warn("Test ignored")
        warnings.warn(response.content)
        return

    assert response.headers["content-type"] == "application/xml; charset=utf-8"
    assert response.status_code == 200
