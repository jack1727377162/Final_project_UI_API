import allure
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

base_url_ui = config.get("base_url_ui")
auth_credentials = config.get("auth_credentials")


@allure.feature("Авторизация на сервисе")
@allure.title("Тест авторизации зарегестрированного пользователя")
@allure.description("Авторизация пользователя"
                    " с использованием логина и пароля")
@allure.id(1)
@allure.severity("Blocker")
def test_auth(auth_page):
    auth_page.user_auth(
        auth_credentials["username"], auth_credentials["password"]
        )
    with allure.step(
        "Проверка возвтарта на главную страницу севиса после авторизации"
    ):
        expected_url = base_url_ui
        actual_url = auth_page._driver.current_url
        assert actual_url.startswith(expected_url)


@allure.feature("Поисковик сервиса")
@allure.title("Тест поиска фильма/сериала")
@allure.description("Поиск фильма/сериала по полученным данным")
@allure.id(2)
@allure.severity("Blocker")
def test_search_film_tv_series(main_page):
    film_tv_series = "Сонная Лощина"
    film_name_search_list, film_name_result_search, film_name_personal_page = (
        main_page.search_film_or_tv_series(film_tv_series)
    )
    with allure.step(
        "Проверка совпадения введенного названия фильма/сериала с названием"
        " предлагаемым поисковиком сервиса в подсказках, на странице"
        " результата поиска, на индивидуальной странице фильма/сериала"
    ):
        assert film_tv_series in film_name_search_list[0]
        assert film_name_result_search.startswith(film_tv_series)
        assert film_name_personal_page.startswith(
            film_tv_series
            )


@allure.feature("Поисковик сервиса")
@allure.title("Тест поиска персоны")
@allure.description("Осуществление поиска персоны согласно полученным данным")
@allure.id(3)
@allure.severity("Blocker")
def test_search_person(main_page):
    person_info = "Джонни Депп"
    person_info_search_list, person_info_search, person_info_private_page = (
        main_page.search_person(person_info)
    )
    with allure.step(
        "Проверка совпадения введенных данных персоны с данными предлагаемыми"
        "поисковиком сервиса в подсказках, на странице"
        "результата поиска, на индивидуальной станице персоны"
    ):
        assert person_info in person_info_search_list[0]
        assert person_info_search == person_info
        assert person_info_private_page == person_info


@allure.feature("Поисковик сервиса")
@allure.title("Тест поиска фильма/сериала/персоны с невалидынми данными")
@allure.description(
    "Осуществление поиска фильма/сериала/персоны при вводе невалидынх данных."
    "Проверка наличия сообщения об отсутствии результатов"
    " поиска на странице результата поиска"
)
@allure.id(4)
@allure.severity("Normal")
def test_empty_search_info_message(main_page):
    search_info = "A non-existent film"
    message = "К сожалению, по вашему запросу ничего не найдено..."
    get_message = main_page.empty_search(search_info)
    with allure.step(
        "Проверка корректности сообщения об отсутствии результатов поиска"
    ):
        assert get_message == message


@allure.feature("Присвоение оценки фильму/сериалу")
@allure.title("Тест присвоения оценки фильму/сериалу")
@allure.description(
    "Осуществление авторизации, осуществление поиска фильма/сериала,"
    " присвоение оценки фильму/сериалу"
)
@allure.id(5)
@allure.severity("Critical")
def test_set_rating_for_film_or_tv_series(auth_page, main_page, personal_page):
    auth_page.user_auth(
        auth_credentials["username"], auth_credentials["password"]
        )
    film_tv_series = "Тайное окно"
    film_name_search_list, film_name_result_search, film_name_personal_page = (
        main_page.search_film_or_tv_series(film_tv_series)
    )
    first_value = 2
    second_value = 10
    button_text = "Оценить фильм"
    personal_page.set_rating(first_value)
    control_first = personal_page.control_vote()
    assert str(first_value) == control_first
    personal_page.change_rating(second_value)
    control_second = personal_page.control_vote()
    assert str(second_value) == control_second
    deleted_rating_button_text = personal_page.delete_rating()
    assert deleted_rating_button_text == button_text
