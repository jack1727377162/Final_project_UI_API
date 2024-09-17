import allure


@allure.feature("Поиск фильма/сериала")
@allure.title("Тест получения информации о фильме/сериале по названию")
@allure.description("Получение информации о\
                     фильме/сериале согласно введенным данным")
@allure.id(1)
@allure.severity("Blocker")
def test_get_film_tv_series_by_name(api):

    film_tv_series = "Сонная Лощина"

    result_search_by_name, status_code = api.search_film_tv_series_by_name(
        film_tv_series
    )
    assert status_code == 200
    assert result_search_by_name["docs"][1]["name"] == "Сонная Лощина"


@allure.feature("Поиск фильма/сериала")
@allure.title("Тест получения информации о фильме/сериале по id")
@allure.description("Получение информации\
                     о фильме/сериале согласно введенным данным")
@allure.id(2)
@allure.severity("Blocker")
def test_get_film_tv_series_by_id(film_api):

    film_id = "5622"

    result_search_by_id, status_code = film_api.search_film_tv_series_by_id(
        film_id
        )
    assert status_code == 200
    assert result_search_by_id["id"] == int(film_id)
    assert result_search_by_id["name"] == "Сонная Лощина"


@allure.feature("Поиск персоны.")
@allure.title("Тест получение информации о персоне по имени и фамилии")
@allure.description("Получение информации согласно введенным данным")
@allure.id(4)
@allure.severity("Blocker")
def test_search_person_by_name(person_api):
    person_name = "Джонни Депп"
    result_serch_person_name, status_code = person_api.search_person_by_name(
        person_name
    )
    assert status_code == 200
    assert result_serch_person_name["docs"][0]["name"] == person_name
    assert result_serch_person_name["docs"][0]["id"] == 6245


@allure.feature("Поиск персоны.")
@allure.title("Тест получения информации о персоне по id")
@allure.description("Получение информации согласно введенным данным")
@allure.id(5)
@allure.severity("Blocker")
def test_search_person_by_id(person_api):

    person_id = "6245"
    result_search_person_by_id, status_code = person_api.search_person_by_id(
        person_id
        )
    assert status_code == 200
    assert result_search_person_by_id["id"] == int(person_id)
    assert result_search_person_by_id["name"] == "Джонни Депп"


@allure.feature("Поиск фильма/сериала")
@allure.title("Тест на получение информации о фильме/сериале по полям")
@allure.description("Получение информации согласно введенным данным")
@allure.id(3)
@allure.severity("Critical")
def test_get_film_tv_series_by_field(api):
    film_tv_series_field = "genres.name"
    result_search_by_field, status_code = api.search_by_fields(
        film_tv_series_field
        )
    assert status_code == 200
    assert "ужасы" in [genre["name"] for genre in result_search_by_field]
