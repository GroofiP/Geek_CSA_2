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


def client_start(ip_start="", tcp_start=7777):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip_start, tcp_start))
    massage = {
        "message": "Привет, сервер",
    }
    sock.send(pickle.dumps(massage))
    data = sock.recv(1024)
    data_message = pickle.loads(data)
    print(f'Сообщение: {data_message["message"]}')
    sock.close()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        client_start()
    else:
        argv_1 = sys.argv[1]
        argv_2 = int(sys.argv[2][1:5])
        client_start(argv_1, argv_2)
