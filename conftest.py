from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.AuthPage import Authorization
from pages.MainPage import Main
from pages.FilmSeriesPage import PersonalPage
from api.FilmSeriesApi import FilmSeriesApi
from api.PersonApi import PersonApi
import pytest
import json


with open("config.json", "r") as config_file:
    config = json.load(config_file)

base_url_api = config.get("base_url_api")
token_info = config.get("token_info")


@pytest.fixture
def browser():
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))
    driver.get("https://www.kinopoisk.ru")
    driver.implicitly_wait(4)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def auth_page(browser):
    return Authorization(browser)


@pytest.fixture
def main_page(browser):
    return Main(browser)


@pytest.fixture
def personal_page(browser):
    return PersonalPage(browser)


@pytest.fixture
def api():
    return FilmSeriesApi(base_url_api)


@pytest.fixture
def film_api():
    return FilmSeriesApi(base_url_api)


@pytest.fixture
def person_api():
    return PersonApi(base_url_api)
