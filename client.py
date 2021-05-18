# Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
# клиент отправляет запрос серверу;
# сервер отвечает соответствующим кодом результата.
# Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.
# Функции клиента:
# сформировать presence-сообщение;
# отправить сообщение серверу;
# получить ответ сервера;
# разобрать сообщение сервера;
# параметры командной строки скрипта client.py <addr> [<port>]:
# addr — ip-адрес сервера;
# port — tcp-порт на сервере, по умолчанию 7777.
import pickle
import sys
from socket import socket, AF_INET, SOCK_STREAM


def client_to_accept_message(sock_cli):
    data = sock_cli.recv(1024)
    dict_message = pickle.loads(data)
    print(f'{dict_message}')


def client_connect(ip_start="", tcp_start=7777):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip_start, tcp_start))
    return sock


def client_send(sock_cli):
    message = input("Введите сообщение от клиента: ")
    sock_cli.send(pickle.dumps(message))


def client_start(ip_go="", tcp_go=7777):
    sock = client_connect(ip_go, tcp_go)
    client_send(sock)
    client_to_accept_message(sock)
    sock.close()


def start_client_script():
    if len(sys.argv) <= 1:
        client_start()
    else:
        argv_1 = sys.argv[1]
        argv_2 = int(sys.argv[2])
        client_start(argv_1, argv_2)


if __name__ == "__main__":
    start_client_script()
