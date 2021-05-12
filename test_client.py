# 1. Для всех функций из урока 3 написать тесты
# с использованием unittest. Они должны быть оформлены
# в отдельных скриптах
# с префиксом test_ в имени файла (например, test_client.py).
# * Использовал pytest
from client import client_start

tcp_one = 8888
tcp_two = 8888

ip_one = "127.0.0.1"
ip_two = "127.0.0.1"


def test_server_tcp():
    assert tcp_one == tcp_two, "Неправильный тип данных или проброс другого порта"
    client_start(tcp_start=tcp_one)


def test_server_ip():
    assert ip_two == ip_one, "Неправильный тип данныхили проброс другого ip"
    client_start(ip_one)
