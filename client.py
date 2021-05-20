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
    data_message = pickle.loads(data)
    try:
        logger.info(f'{data_message}')
    except Exception as e:
        logger.info(f'Произошел сбой: {e}')
    print(f'{data_message}')


def client_connect(ip_start="", tcp_start=7777, sock=()):
    sock.connect((ip_start, tcp_start))
    return sock


def client_send(sock_cli):
    message = {f"{sock_cli.getsockname()}": input("Введите сообщение от клиента: ")}
    if message == "":
        return False
    sock_cli.send(pickle.dumps(message))


@logs
def client_start(ip_go="", tcp_go=7777):
    sock = client_connect(ip_go, tcp_go)
    while True:
        client_send(sock)
        client_to_accept_message(sock)
        info_log("client")


def start_client_script():
    if len(sys.argv) <= 1:
        main(client_start)
    else:
        argv_1 = sys.argv[1]
        argv_2 = int(sys.argv[2])
        client_start(argv_1, argv_2)


ADDRESS = ('localhost', 7777)


def echo_client():
    # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
    # При выходе из оператора with сокет будет автоматически закрыт
    with socket(AF_INET, SOCK_STREAM) as s:  # Создать сокет TCP
        client_connect(sock=s)
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


def echo_client_main():
    # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
    # При выходе из оператора with сокет будет автоматически закрыт
    with socket(AF_INET, SOCK_STREAM) as s:  # Создать сокет TCP
        client_connect(sock=s)
        while True:
            msg = input('Введите сообщение: ')
            if msg == 'exit':
                break
            msg = f"Сообщение от {s.getsockname()}: {msg}\n"
            s.send(msg.encode('utf-8'))  # Отправить!


if __name__ == '__main__':
    echo_client_main()
