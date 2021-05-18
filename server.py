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
from log.server_log_config import logger
import pickle
import sys
from socket import socket, AF_INET, SOCK_STREAM
from dec import logs
from service import info_log, main


def server_to_accept_message(sock_cli):
    client, address = sock_cli.accept()
    data = client.recv(1024)
    data_message = pickle.loads(data)
    try:
        logger.info(f'Сообщение от клиента серверу: {data_message["message"]}')
    except Exception as e:
        logger.info(f'Произошел сбой: {e}')
    return client, address


def server_connect(ip_start="", tcp_start=7777):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ip_start, tcp_start))
    sock.listen(5)
    return sock


def server_send(cli_add):
    massage = {
        "message": input("Введите сообщение от сервера: "),
    }
    cli_add.send(pickle.dumps(massage))


@logs
def server_start(ip_go="", tcp_go=7777):
    sock = server_connect(ip_go, tcp_go)

    while True:
        client, address = server_to_accept_message(sock)
        server_send(client)
        info_log("server")
        client.close()


if __name__ == "__main__":
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
