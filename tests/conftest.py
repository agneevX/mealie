from tests.pre_test import DB_URL, settings  # isort:skip

import json

import requests
from fastapi.testclient import TestClient
from mealie.app import app
from mealie.db.db_setup import SessionLocal, generate_session
from mealie.db.init_db import main
from pytest import fixture

from tests.app_routes import AppRoutes
from tests.test_config import TEST_DATA
from tests.utils.recipe_data import get_raw_no_image, get_raw_recipe, get_recipe_test_cases

main()


def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@fixture(scope="session")
def api_client():

    app.dependency_overrides[generate_session] = override_get_db

    yield TestClient(app)

    DB_URL.unlink(missing_ok=True)


@fixture(scope="session")
def api_routes():
    return AppRoutes()


@fixture(scope="session")
def test_image_jpg():
    return TEST_DATA.joinpath("images", "test_image.jpg")


@fixture(scope="session")
def test_image_png():
    return TEST_DATA.joinpath("images", "test_image.png")


@fixture(scope="session")
def token(api_client: requests, api_routes: AppRoutes):
    form_data = {"username": "changeme@email.com", "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(api_routes.auth_token, form_data)

    token = json.loads(response.text).get("access_token")

    return {"Authorization": f"Bearer {token}"}


@fixture(scope="session")
def raw_recipe():
    return get_raw_recipe()


@fixture(scope="session")
def raw_recipe_no_image():
    return get_raw_no_image()


@fixture(scope="session")
def recipe_store():
    return get_recipe_test_cases()
