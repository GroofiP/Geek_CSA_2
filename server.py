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
# -a <adr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
import argparse
import pickle
import select
from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM
from log.server_log_config import logger
from dec import logs
from service import info_log


def server_connect(ip_start="", tcp_start=7777):
    """Развертывание сервера на определнном ip и tcp"""
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ip_start, tcp_start))
    sock.listen(5)
    return sock


def server_to_accept(sock_cli):
    """Поставить сервер на ожидание клиента"""
    client, address = sock_cli.accept()
    return client, address


def server_to_accept_message(cli_add):
    """Прием сообщения от клиента и просмотр этого сообщения """
    data = cli_add.recv(1024)
    data_message = pickle.loads(data)
    try:
        logger.info(f'Сообщение от клиента {cli_add.getpeername()}: {data_message}')
    except Exception as err:
        logger.info(f'Произошел сбой: {err}')
    return f'Сообщение от клиента {cli_add.getpeername()}: {data_message}'


def server_send(cli_add, message):
    """Отправка сообщения"""
    cli_add.send(pickle.dumps(message))


@logs
def server_start(ip_go="", tcp_go=7777):
    """Функция для настройки сервера под ключ"""
    sock = server_connect(ip_go, tcp_go)
    while True:
        client, address = server_to_accept(sock)
        message = server_to_accept_message(client)
        server_send(client, message)
        info_log("server")
        client.close()


def start_parser(func_start):
    """Сценарий для терминала"""
    parser = argparse.ArgumentParser(description='Запуск сервера')
    parser.add_argument("-a", type=str, help='Выбор ip')
    parser.add_argument("-p", type=int, help='Выбор tcp')
    args = parser.parse_args()
    if args.a and args.p is not None:
        func_start(ip_go=args.a, tcp_go=args.p)
    elif args.a is None:
        func_start(tcp_go=args.p)
    elif args.p is None:
        func_start(ip_go=args.a)
    else:
        func_start()


def read_requests(r_clients, all_clients):
    """Чтение запросов из списка клиентов для эхо сервера"""
    responses = {}
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except OSError:
            print(f'Клиент {sock.getpeername()} отключился.')
            all_clients.remove(sock)
    return responses


def write_responses(requests, w_clients, all_clients, func_proc_res):
    """ Эхо-ответ сервера клиентам, от которых были запросы"""
    for sock in w_clients:
        if sock in requests:
            try:
                func_proc_res(requests, sock, w_clients)
            except OSError:
                print(f'Клиент {sock.getpeername()} отключился.')
                all_clients.remove(sock)


def write_responses_ver_1(*args):
    resp = args[0][args[1]].encode('utf-8')
    for cli in args[2]:
        cli.send(resp)


def write_responses_ver_2(*args):
    resp = args[0][args[1]]
    print(f"{resp}")


def echo_server_select(x_socket, x_cli, func_proc_select):
    while True:
        try:
            cli, adr = server_to_accept(x_socket)
        except OSError:
            pass
        else:
            print(f"Получен запрос на соединение от {adr}")
            x_cli.append(cli)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 10
            r = []
            w = []
            try:
                r, w, er = select.select(x_cli, x_cli, [], wait)
            except Exception as err:
                print(f"Клиент отключился{err}")

            requests = read_requests(r, x_cli)  # Сохраним запросы клиентов
            if requests:
                write_responses(requests, w, x_cli, func_proc_select)  # Выполним отправку ответов клиентам


def echo_server(ip_go="", tcp_go=7777, func_proc=write_responses_ver_1):
    """Функция для настройки эхо сервера под ключ"""
    clients = []
    sock = server_connect(ip_go, tcp_go)
    print(sock)
    echo_server_select(sock, clients, func_proc)


def client_client(sock_cli, base_cli, base_gro):
    data_message = pickle.loads(sock_cli.recv(1024))
    if data_message == "П":
        sock_cli.send(pickle.dumps(str(base_cli)))
        data = sock_cli.recv(1024)
        data_message = pickle.loads(data)
        for k, v in data_message.items():
            base_cli[int(k)].send(pickle.dumps(v))
    elif data_message == "Г":
        sock_cli.send(pickle.dumps(str(base_gro)))
        data = sock_cli.recv(1024)
        data_message = pickle.loads(data)
        try:
            for k, v in data_message.items():
                sock_base_gro = base_gro[int(k)]
                for i in sock_base_gro:
                    i.send(pickle.dumps(v))
        except Exception as exp:
            print(exp)
            sock_cli.send(pickle.dumps("Группы ещё не созданы"))
    elif data_message == "ВГ":
        sock_cli.send(pickle.dumps(str(base_gro)))
        data = sock_cli.recv(1024)
        data_message = pickle.loads(data)
        gro = {data_message: []}
        print(gro)
        for k, v in gro.items():
            print(len(base_gro))
            if len(base_gro) > 0:
                for a, b in base_gro.items():
                    print(a)
                    if a == k:
                        base_gro[gro[k]].append(sock_cli)
                        sock_cli.send(pickle.dumps("Вы вступили в группу"))
            else:
                base_gro.update({k: [sock_cli]})
                print(base_gro)
                sock_cli.send(pickle.dumps("Вы создали группу"))


def server_original(ip_go="", tcp_go=7777):
    sock = server_connect(ip_go, tcp_go)
    clients = []
    base_all_groups = {}
    while True:
        try:
            cli, adr = server_to_accept(sock)
        except OSError:
            pass
        else:
            print(f"Получен запрос на соединение от {adr}")
            clients.append(cli)
        finally:
            wait = 10
            r = []
            w = []
            try:
                r, w, er = select.select(clients, clients, [], wait)
            except Exception as err:
                print(f"Клиент отключился{err}")

            base_all_client = {a: clients[a] for a in range(len(clients))}

            for s in w:
                proc = Process(target=client_client, args=(s, base_all_client, base_all_groups))
                proc.start()


if __name__ == "__main__":
    try:
        start_parser(server_original)
    except Exception as e:
        print(e)
        start_parser(server_original())
