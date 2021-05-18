# Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
# клиент отправляет запрос серверу;
# сервер отвечает соответствующим кодом результата.
# Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.
# Функции сервера:
# принимает сообщение клиента;
# формирует ответ клиенту;
# отправляет ответ клиенту;
# имеет параметры командной строки:
# -p <port> — TCP-порт для работы (по умолчанию использует 7777);
# -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
import pickle
import sys
from socket import socket, AF_INET, SOCK_STREAM
from log.server_log_config import logger
from dec import logs
from service import info_log, main


def server_to_accept(sock_cli):
    client, address = sock_cli.accept()
    return client, address


def server_to_accept_message(sock_cli):
    data = sock_cli.recv(1024)
    data_message = pickle.loads(data)
    try:
        logger.info(f'Сообщение от клиента {sock_cli.getsockname()}: {data_message}')
    except Exception as e:
        logger.info(f'Произошел сбой: {e}')
    return f'Сообщение от клиента {sock_cli.getpeername()}: {data_message}'


def server_connect(ip_start="", tcp_start=7777):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ip_start, tcp_start))
    sock.listen(5)
    return sock


def server_send(cli_add, message):
    cli_add.send(pickle.dumps(message))


@logs
def server_start(ip_go="", tcp_go=7777):
    sock = server_connect(ip_go, tcp_go)
    while True:
        client, address = server_to_accept(sock)
        message = server_to_accept_message(client)
        server_send(client, message)
        info_log("server")
        client.close()


def start_script():
    if len(sys.argv) <= 1:
        main(server_start)
    elif len(sys.argv) >= 4:
        argv_1 = sys.argv[4]
        argv_2 = int(sys.argv[2])
        server_start(argv_1, argv_2)
    else:
        for param in sys.argv:
            if param == "-p":
                argv_1 = int(sys.argv[2])
                server_start(tcp_go=argv_1)
            elif param == "-a":
                argv_1 = sys.argv[2]
                server_start(ip_go=argv_1)


if __name__ == "__main__":
    start_script()
