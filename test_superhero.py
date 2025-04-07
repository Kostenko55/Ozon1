import pytest
import requests
from unittest.mock import Mock, patch
from superhero import get_tallest_hero

##1. Тест на отсутствие подходящих героев
##Проверка, когда нет героев с заданными критериями.
@patch('requests.get')
def test_no_matching_heroes(mock_get):
    mock_get.return_value = Mock(json=Mock(return_value=[
        {
            "appearance": {"gender": "Female", "height": ["5'9", "175 cm"]},
            "work": {"occupation": "Engineer"}
        }
    ]))
    result = get_tallest_hero("male", True)
    assert result is None
##2. Тест на некорректный формат роста
##Проверка обработки героев с невалидным значением роста.
@patch('requests.get')
def test_invalid_height_format(mock_get):
    mock_get.return_value = Mock(json=Mock(return_value=[
        {
            "appearance": {"gender": "Male", "height": ["unknown", "invalid"]},
            "work": {"occupation": "Hero"}
        }
    ]))
    result = get_tallest_hero("male", True)
    assert result is None  # Герой с невалидным ростом должен игнорироваться

##3. Тест на несколько героев с одинаковым максимальным ростом
##Проверка, что возвращается первый герой при совпадении роста.
@patch('requests.get')
def test_multiple_tallest_heroes(mock_get):
    mock_get.return_value = Mock(json=Mock(return_value=[
        {
            "name": "HeroA",
            "appearance": {"gender": "Male", "height": ["6'5", "195 cm"]},
            "work": {"occupation": "Hero"}
        },
        {
            "name": "HeroB",
            "appearance": {"gender": "Male", "height": ["6'5", "195 cm"]},
            "work": {"occupation": "Hero"}
        }
    ]))
    result = get_tallest_hero("male", True)
    assert result["name"] == "HeroA"  # Первый в списке

##4. Тест на регистр в поле gender
##Проверка, что функция нечувствительна к регистру.
@patch('requests.get')
def test_gender_case_insensitive(mock_get):
    mock_get.return_value = Mock(json=Mock(return_value=[
        {
            "name": "HeroX",
            "appearance": {"gender": "MALE", "height": ["6'2", "188 cm"]},
            "work": {"occupation": "Detective"}
        }
    ]))
    result = get_tallest_hero("male", True)
    assert result["name"] == "HeroX"

##5. Тест на работу (work=False)
##Проверка фильтрации героев без работы.
@patch('requests.get')
def test_hero_without_work(mock_get):
    mock_get.return_value = Mock(json=Mock(return_value=[
        {
            "name": "Hero1",
            "appearance": {"gender": "Female", "height": ["5'10", "178 cm"]},
            "work": {"occupation": "-"}  # Нет работы
        },
        {
            "name": "Hero2",
            "appearance": {"gender": "Female", "height": ["5'8", "173 cm"]},
            "work": {"occupation": "Teacher"}
        }
    ]))
    result = get_tallest_hero("female", False)
    assert result["name"] == "Hero1"  # Тот, у кого occupation == "-"

##6. Тест на обработку ошибки API
##Проверка, что функция возвращает None при ошибке запроса.
@patch('requests.get')
def test_api_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("API недоступно")
    result = get_tallest_hero("male", True)
    assert result is None

##7. Тест на отсутствие поля work
##Проверка обработки героев без информации о работе.
@patch('requests.get')
def test_missing_work_field(mock_get):
    mock_get.return_value = Mock(json=Mock(return_value=[
        {
            "name": "HeroY",
            "appearance": {"gender": "Male", "height": ["6'1", "185 cm"]},
            # Нет секции "work"
        }
    ]))
    result = get_tallest_hero("male", True)
    assert result is None  # Поле work отсутствует → не подходит под work=True



##8. Тест на частично заполненные данные
##Проверка, что герой с неполными данными (например, отсутствует height) игнорируется.
@patch('requests.get')
def test_incomplete_data(mock_get):
    mock_get.return_value = Mock(json=Mock(return_value=[
        {
            "appearance": {"gender": "Male"},  # Нет height
            "work": {"occupation": "Hero"}
        }
    ]))
    result = get_tallest_hero("male", True)
    assert result is None

