from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class PersonalPage:

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def find_element_and_click(self, css_selector: str):
        """
        Метод для нахождения элемента на\
              странице по селектору, нажатие на элемент
        Args:
            css_selector (str): css_selector элемента
        """
        element = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        element.click()

    def find_element_and_return_text(
        self, element: WebElement, css_selector: str
    ) -> str:
        """
        Метод для нахождения элемента на странице\
              по селектору, возврат текста элемента
        Args:
            element: WebElement.
            css_selector (str): css_selector элемента
        Returns:
            str: текст элемента
        """
        element = WebDriverWait(element, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        return element.text

    def find_button_change_delete_by_text(self, button_text: str) -> WebElement:
        """
        Метод для поиска кнопки по тексту.\
              Подкнопки: 'Изменить оценку' и 'Удалить оценку'
        Args:
            button_text (str): текст кнопки для поиска
        Returns:
            WebElement: найденная кнопка
        """
        buttons = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button[class^='style_root']")
            )
        )
        for button in buttons:
            if button.text == button_text:
                return button

    @allure.step(
        "Проверка отображения оценки на странице, возвращение её значения"
    )
    def control_vote(self) -> str:
        """
        Метод для считывания выставленной фильму или сериалу оценки
        Returns:
            str: выставленная оценка
        """
        div_with_vote = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[class^='styles_valueContainer']")
            )
        )
        return self.find_element_and_return_text(div_with_vote, "span[class^='styles']")

    @allure.step("Выставление оценки фильму/сериалу. Оценка - {value}.")
    def set_rating(self, value: int):
        """Метод для выставления оценки фильму/сериалу
        Args:
            value (int): значение от 1 до 10
        """
        with allure.step("На странице нажать кнопку 'Оценить фильм/сериал'"):
            self.find_element_and_click(
                "[class^='styles_kinopoiskRatingSnippet']")

        with allure.step("Выставить оценку согласно переданному значению"):
            rating_button_selector = f"button[aria-label='Оценка {value}']"
            self.find_element_and_click(rating_button_selector)

    @allure.step(
        "Изменение выставленной ранее оценки\
              фильму/сериалу. Новая оценка - {new_value}"
    )
    def change_rating(self, new_value: int):
        """Метод для изменения оценки фильму/сериалу
        Args:
            value (int): значение от 1 до 10
        """
        with allure.step("На странице нажать на кнопку 'Изменить оценку'"):
            self.find_element_and_click(
                "[class^='styles_kinopoiskRatingSnippet']")
            self.find_button_change_delete_by_text("Изменить оценку").click()

        with allure.step("Выставить оценку согласно"
                         " новому переданному значению"):
            rating_button_selector = f"button[aria-label='Оценка {new_value}']"
            self.find_element_and_click(rating_button_selector)

    @allure.step(
        "Удаление ранее выставленной оценки"
        " фильму/сериалу. Нажать на кнопку"
        " 'Изменить оценку', затем нажать на кнопку 'Удалить оценку'"
    )
    def delete_rating(self):
        """
        Метод для удаления оценки фильму/сериалу
        """
        div = self._driver.find_element(
            By.CSS_SELECTOR, "[class^='styles_kinopoiskRatingSnippet']"
        )
        div.click()
        delete_button = self.find_button_change_delete_by_text(
            "Удалить оценку")
        delete_button.click()
        self._driver.refresh()
        div1 = self._driver.find_element(
            By.CSS_SELECTOR, "[class^='styles_kinopoiskRatingSnippet']"
        )
        result = self.find_element_and_return_text(
            div1, "button[class^='style_button']"
        )

        return result
