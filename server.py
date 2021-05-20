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
import select
import sys
from socket import socket, AF_INET, SOCK_STREAM
from log.server_log_config import logger
from dec import logs
from service import info_log, main


def server_to_accept(sock_cli):
    client, address = sock_cli.accept()
    return client, address


def server_to_accept_message(cli_add):
    data = cli_add.recv(1024)
    data_message = pickle.loads(data)
    try:
        logger.info(f'Сообщение от клиента {cli_add.getpeername()}: {data_message}')
    except Exception as e:
        logger.info(f'Произошел сбой: {e}')
    return f'Сообщение от клиента {cli_add.getpeername()}: {data_message}'


def server_connect(ip_start="", tcp_start=7777):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ip_start, tcp_start))
    sock.listen(5)
    sock.settimeout(0.2)
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


def read_requests(r_clients, all_clients):
    """Чтение запросов из списка клиентов"""
    responses = {}

    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except OSError:
            print(f'Клиент {sock.getpeername()} отключился.')
            all_clients.remove(sock)

    return responses


def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """

    for sock in w_clients:
        if sock in requests:
            try:
                resp = requests[sock]
                for cli in w_clients:
                    cli.send(resp)
            except OSError:
                print(f'Клиент {sock.getpeername()} отключился.')
                all_clients.remove(sock)


def write_responses_main(requests, w_clients, all_clients):
    for sock in w_clients:
        if sock in requests:
            try:
                resp = requests[sock]
                print(f"{resp}")
            except OSError:
                print(f'Клиент {sock.getpeername()} отключился.')
                all_clients.remove(sock)


def echo_server(ip_go="", tcp_go=7777):
    """ Основной цикл обработки запросов клиентов
    """
    clients = []
    sock = server_connect(ip_go, tcp_go)
    while True:
        try:
            cli, adr = server_to_accept(sock)
        except OSError as e:
            pass  # timeout вышел
        else:
            print(f"Получен запрос на соединение от {adr}")
            clients.append(cli)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 10
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except Exception as e:
                print(f"Клиент отключился{e}")

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                write_responses(requests, w, clients)  # Выполним отправку ответов клиентам


def echo_server_main(ip_go="", tcp_go=7777):
    """ Основной цикл обработки запросов клиентов
    """
    clients = []
    sock = server_connect(ip_go, tcp_go)
    while True:
        try:
            cli, adr = server_to_accept(sock)
        except OSError as e:
            pass  # timeout вышел
        else:
            print(f"Получен запрос на соединение от {adr}")
            clients.append(cli)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 10
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except Exception as e:
                print(f"Клиент отключился{e}")

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                write_responses_main(requests, w, clients)  # Выполним отправку ответов клиентам


if __name__ == "__main__":
    echo_server_main()
