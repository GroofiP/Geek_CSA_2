# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
# в байтовое и выполнить обратное преобразование (используя методы encode и decode).

list_a = ["разработка", "сокет", "декоратор", "standard"]

for a in list_a:
    a = a.encode(encoding="UTF-8")
    print(a)
    a = a.decode(encoding="UTF-8")
    print(a)
