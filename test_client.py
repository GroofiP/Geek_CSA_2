# 1. Для всех функций из урока 3 написать тесты
# с использованием unittest. Они должны быть оформлены
# в отдельных скриптах
# с префиксом test_ в имени файла (например, test_client.py).
# * Использовал pytest
from client import client_start


def test_client_start():
    assert client_start('127.0.0.1', 7777) != ('localhost', 7777), "Неправильный тип данных"
