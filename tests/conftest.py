import os
import pytest
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_file, override=True)


@pytest.fixture(scope="session")
def app():
    from scheduler.__init__ import create_app

    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "DEBUG": True,
        }
    )

    yield app


@pytest.fixture(scope="session")
def client(app):
    yield app.test_client()


@pytest.fixture
def schedule_get_mock(requests_mock):
    from scheduler.config import Config

    yield requests_mock.get(f"{Config.TARANIS_CORE_URL}/config/schedule", json={"items": [], "total_count": 0})
