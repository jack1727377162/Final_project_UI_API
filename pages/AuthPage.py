from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import allure


class Authorization:

    def __init__(self, driver: WebDriver):
        self._driver = driver

    @allure.step(
        "Открытие страницы сервиса 'Кинопоиск'. Авторизация.\
              Ожидание возвращения на главную страницу\
                  сервиса. Логин - {login}, пароль - {password}"
    )
    def user_auth(self, login: str, password: str):
        """Метод для авторизации на сервисе, с использованием\
              электронной почты и пароля

        Args:
            login (str): электронная почта
            password (str): пароль
        """
        with allure.step(
            "Нажатие на 'CAPTCHA', в случаее появления"
        ):
            try:
                self._driver.find_element(
                    By.CSS_SELECTOR, ".CheckboxCaptcha-Button"
                ).click()
            except NoSuchElementException:
                pass

        with allure.step("Нажатие на кнопку 'Войти' на"
                         " главной странице севиса"):
            self._driver.find_element(
                By.CSS_SELECTOR, ".styles_loginButton__LWZQp"
            ).click()

        with allure.step("Ввод электронной почты"):
            self._driver.find_element(
                By.CSS_SELECTOR, "#passp-field-login"
                ).send_keys(
                login
            )

        with allure.step(
            "Нажатие на кнопку 'Войти' на странице для ввода логина"
        ):
            self._driver.find_element(
                By.CSS_SELECTOR, ".passp-button.passp-sign-in-button"
            ).click()

        with allure.step("Ввод пароля"):
            self._driver.find_element(
                By.CSS_SELECTOR, "#passp-field-passwd"
                ).send_keys(
                password
            )

        with allure.step(
            "Нажатие на кнопку 'Войти' на странице для ввода пароля"
        ):
            self._driver.find_element(
                By.CSS_SELECTOR, ".passp-button.passp-sign-in-button"
            ).click()

        with allure.step("Ожидание возвращения на главную страницу сервиса"):
            WebDriverWait(self._driver, 5).until(
                EC.url_contains("https://www.kinopoisk.ru/")
            )
