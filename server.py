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


def server_start(ip_start="", tcp_start=7777):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ip_start, tcp_start))
    sock.listen(5)

    while True:
        client, address = sock.accept()
        data = client.recv(1024)
        data_message = pickle.loads(data)
        print(f'Сообщение: {data_message["Hello"]}. {data_message["End"]}.\nБыло отправлено клиентом: {address}.')
        massage = {
            "Hello": "Привет, клиент",
            "End": f"Ваши данные длинной в {len(data)} байт"
        }
        client.send(pickle.dumps(massage))
        client.close()
        print(sys.argv[1])

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) <= 1:
        server_start()
    elif len(sys.argv) >= 4:
        argv_1 = sys.argv[4]
        argv_2 = int(sys.argv[2])
        server_start(argv_1, argv_2)
    else:
        for param in sys.argv:
            if param == "-p":
                argv_1 = int(sys.argv[2])
                server_start(tcp_start=argv_1)
            elif param == "-a":
                argv_1 = sys.argv[2]
                server_start(ip_start=argv_1)
