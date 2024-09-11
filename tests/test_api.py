from scheduler.config import Config


def test_jobindex(client):
    response = client.get(f"{Config.APPLICATION_ROOT}/")
    assert response.status_code == 200
