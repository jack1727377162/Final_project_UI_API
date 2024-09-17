from typing import Tuple, List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import allure


class Main:

    def __init__(self, driver: WebDriver):
        self._driver = driver

    @allure.step("Проходение 'CAPTCHA', в случаее появления")
    def captcha(self):
        """
        Метод для прохождения капчи
        """
        try:
            self._driver.find_element(
                By.CSS_SELECTOR, ".CheckboxCaptcha-Button"
            ).click()
        except NoSuchElementException:
            pass

    @allure.step("Ввод данных в поле поиска: {info_to_search}")
    def enter_search_info(self, info_to_search: str):
        """
        Метод для ввода данных в поле поиска
        Args:
            info_to_search (str): данные для поиска
        """
        search_field = self._driver.find_element(
            By.CSS_SELECTOR,
            ".kinopoisk-header-search-form-input"
            "__input[aria-label='Фильмы, сериалы, персоны']",
        )
        search_field.click()
        search_field.send_keys(info_to_search)

    @allure.step("Получение текста элементов в подсказках к полю для поиска")
    def get_search_field_list(self, selector: str) -> List[str]:
        """Метод для сбора списка элементов в подсказках к полю для поиска
        Args:
            selector (str): селектор веб элемента
        Returns:
            list: возвращает список элементов
        """
        elements = self._driver.find_elements(By.CSS_SELECTOR, selector)
        return [element.text for element in elements]

    @allure.step("Нажатие на кнопку поиска")
    def click_search_button(self):
        """
        Метод для нажатия на кнопку поиска в поисковике сервиса
        """
        self._driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

    @allure.step("Ожидание и возврат элемента на странице результата поиска")
    def get_element_from_search_result_page(
        self, css_selector: str
    ) -> Tuple[WebElement, str]:
        """Метод для ожидания появление элемента на странице.
        Возвращает данный веб элемент и текст ссылки
        Args:
            css_selector (str): селектор элемента
        Returns:
            Tuple[WebElement, str]: веб элемент и текст ссылки
        """
        element = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        div_info = element.find_element(By.CSS_SELECTOR, "div.info")
        p_name_result_search_page = div_info.find_element(
            By.CSS_SELECTOR, "p.name")
        a_link = p_name_result_search_page.find_element(By.CSS_SELECTOR, "a")
        text_link = a_link.text
        return a_link, text_link

    @allure.step(
        "Переход на сервис 'Кинопоиск'. Осуществление\
              поиска фильма/сериала. Название - {info_to_search}."
    )
    def search_film_or_tv_series(self, info_to_search: str) -> str:
        """Метод для осуществления поиска фильма/сериала с
        использованием информации полученной на вход
        Открыть индивидуальную страницу фильма/сериала
        Args:
            info_to_search (str): название фильма или сериала
        Returns:
            str: возвращает название фильма/сериала из подсказки\
                  к полю для поиска, страницы результата поиска,\
                      индивидуальной страницы фильма/сериала
        """
        self.captcha()
        self.enter_search_info(info_to_search)
        found_movie_titles = self.get_search_field_list("[id^='suggest-item']")
        self.click_search_button()
        a_film_link, film_text_link = self.get_element_from_search_result_page(
            "div.element.most_wanted"
        )
        a_film_link.click()

        with allure.step("Получение названия фильма/сериала"):
            name_film_personal_page = WebDriverWait(self._driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "h1[itemprop='name']")
                )
            )

        with allure.step(
            "Возврат списка с 1 фильмом/сериалом из подсказки к полю\
                  для поиска, название фильма/сериала на странице\
                      результата поиска, название с индивидуальной страницы"
        ):
            return (
                found_movie_titles,
                film_text_link,
                name_film_personal_page.text,
            )

    @allure.step(
        "Переход на сервис 'Кинопоиск'. Осуществление поиска персоны.\
              Фамилия и имя персоны - {info_to_search}."
    )
    def search_person(self, info_to_search: str) -> str:
        """Метод для поиска персоны с использованием информации\
              полученной на вход.Отрыть индивидуальную страницу персоны

        Args:
            info_to_search (str): фамилия и имя персоны
        Returns:
            str: возвращает список с 1 персоной из подсказки к полю\
                  для поиска, фамилию и имя персоны на странице результата\
                      поиска, фамилию и имя с индивидуальной странице персоны
        """
        self.captcha()
        self.enter_search_info(info_to_search)
        found_person_titles = self.get_search_field_list(
            "[id^='suggest-item-person']")
        self.click_search_button()
        a_person_link, person_text_link = self.get_element_from_search_result_page(
            "div.element.most_wanted"
        )
        a_person_link.click()

        with allure.step("Получение фамилии и имени"
                         " индивидуальной странице персоны"):
            name_surname_person_page = WebDriverWait(self._driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "[class^='styles_primaryName']",
                    )
                )
            )

        with allure.step(
            "Возврат списока с 1 персоной из подсказки к полю для поиска,\
                  фамилию и имя персоны на странице результата поиска, фамилию\
                      и имя с индивидуальной страницы персоны"
        ):
            return (
                found_person_titles,
                person_text_link,
                name_surname_person_page.text,
            )

    @allure.step(
        "Переход на сервис 'Кинопоиск'. Осуществление поиска по"
        " невалидному названию. Проверка информационного сообщения"
    )
    def empty_search(self, info_to_search: str) -> str:
        """Метод для поиска данных по невалидному названию,
        проверка наличия сообщения об отсутствии результатов\
              поиска на странице результата поиска.
        Args:
            info_to_search (str): ввести невалидые данные
        Returns:
            str: текст информационного сообщения
        """
        self.captcha()
        self.enter_search_info(info_to_search)
        self.click_search_button()

        with allure.step("Считывание текста сообщения и его возврат"):
            message_empty_result = self._driver.find_element(
                By.CSS_SELECTOR, "h2.textorangebig"
            ).text
            return message_empty_result
