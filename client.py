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
from log.server_log_config import logger
from dec import logs
from service import info_log, main


def client_to_accept_message(sock_cli):
    data = sock_cli.recv(1024)
    dict_message = pickle.loads(data)
    try:
        logger.info(f'Сообщение от сервера клиенту: {dict_message["message"]}')
    except Exception as e:
        logger.info(f'Произошел сбой: {e}')


def client_connect(ip_start="", tcp_start=7777):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip_start, tcp_start))
    return sock


def client_send(sock_cli):
    message = {
        "message": input("Введите сообщение от клиента: "),
    }
    sock_cli.send(pickle.dumps(message))


@logs
def client_start(ip_go="", tcp_go=7777):
    sock = client_connect(ip_go, tcp_go)
    client_send(sock)
    client_to_accept_message(sock)
    info_log("client")
    sock.close()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        main(client_start)
    else:
        argv_1 = sys.argv[1]
        argv_2 = int(sys.argv[2][1:5])
        client_start(argv_1, argv_2)
