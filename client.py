# Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
# клиент отправляет запрос серверу;
# сервер отвечает соответствующим кодом результата.
# Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.
# Функции клиента:
# сформировать presence-сообщение;
# отправить сообщение серверу;
# получить ответ сервера;
# разобрать сообщение сервера;
# параметры командной строки скрипта client.py <adr> [<port>]:
# adr — ip-адрес сервера;
# port — tcp-порт на сервере, по умолчанию 7777.
import argparse
import pickle
from socket import socket, AF_INET, SOCK_STREAM
from log.server_log_config import logger
from dec import logs
from service import info_log


def client_connect(ip_start="", tcp_start=7777):
    """Подключение клиента на определнном ip и tcp"""
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip_start, tcp_start))
    return sock


def client_to_accept_message(sock_cli):
    """Прием сообщения от сервера и просмотр этого сообщения """
    data = sock_cli.recv(1024)
    data_message = pickle.loads(data)
    try:
        logger.info(f'{data_message}')
    except Exception as e:
        logger.info(f'Произошел сбой: {e}')
    print(f'{data_message}')


def client_send(sock_cli):
    """Отправка сообщения"""
    message = {f"{sock_cli.getsockname()}": input("Введите сообщение от клиента: ")}
    if message == "":
        return False
    sock_cli.send(pickle.dumps(message))


@logs
def client_start(ip_go="", tcp_go=7777):
    """Функция для настройки клиента под ключ"""
    sock = client_connect(ip_go, tcp_go)
    while True:
        client_send(sock)
        client_to_accept_message(sock)
        info_log("client")


def start_client_parser(func_start):
    """Сценарий для терминала"""
    parser = argparse.ArgumentParser(description='Запуск клиента')
    parser.add_argument("a", type=str, help='Выбор ip', nargs='?')
    parser.add_argument("p", type=int, help='Выбор tcp', nargs='?')
    args = parser.parse_args()
    if args.a and args.p is not None:
        func_start(args.a, args.p)
    else:
        func_start()


def echo_client(ip_go="", tcp_go=7777):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((ip_go, tcp_go))
        while True:
            msg = input('Введите сообщение: ')
            if msg == 'exit':
                break
            elif msg == "":
                data = s.recv(1024).decode('utf-8')
                print(f'{data}')
            else:
                massage = f"Сообщение от {s.getsockname()}: {msg}\n"
                s.send(massage.encode('utf-8'))  # Отправить!
                data = s.recv(1024).decode('utf-8')
                print(f'{data}')


def echo_client_main(ip_go="", tcp_go=7777):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((ip_go, tcp_go))
        print(s)
        while True:
            msg = input('Введите сообщение: ')
            if msg == 'exit':
                break
            msg = f"Сообщение от {s.getsockname()}: {msg}\n"
            s.send(msg.encode('utf-8'))


########################################################################################################################
def cli_start(sock):
    msg = input(
        'Введите, что вы хотите сделать (П/Отправить сообщение пользователю, '
        'Г/Отправить группе, ВГ/Вступить в группу)? '
    )
    sock.send(pickle.dumps(msg))
    return msg


def cli_send_p(sock):
    print(pickle.loads(sock.recv(1024)))
    msg_a = input("Введите номер пользователя с #0 до #99 с которым хотите начать беседу: ")
    msg_b = input(f'Введите сообщение пользователю {msg_a}:')
    sock.send(pickle.dumps([msg_a, msg_b]))
    print(pickle.loads(sock.recv(1024)))


def cli_send_g(sock):
    print(pickle.loads(sock.recv(1024)))
    msg_a = input("Введите номер пользователя с #0 до #99 с которым хотите начать беседу: ")
    msg_b = input(f'Введите сообщение пользователю {msg_a}:')
    sock.send(pickle.dumps([msg_a, msg_b]))
    print(pickle.loads(sock.recv(1024)))


def cli_add_g(sock):
    print(pickle.loads(sock.recv(1024)))
    msg_a = input("Введите номер группы # которую хотите создать или подключится: ")
    sock.send(pickle.dumps(msg_a))
    print(pickle.loads(sock.recv(1024)))


def client_original(ip_go="", tcp_go=7777):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((ip_go, tcp_go))
        while True:
            msg_1 = cli_start(s)
            if msg_1 == 'П':
                cli_send_p(s)
            elif msg_1 == 'Г':
                cli_send_g(s)
            elif msg_1 == 'ВГ':
                cli_add_g(s)
            else:
                pass


if __name__ == '__main__':
    start_client_parser(client_original)
