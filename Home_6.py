# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
from pip._vendor import chardet

with open("test_file.txt", 'r', encoding="UTF-8") as f:
    b = f.read()
    print(b)
    f.close()

a = "сетевое программирование"
b = "сокет"
c = "декоратор"

with open("Test_File_2.txt", "w", encoding="UTF-8") as f:
    f.write(f"{a}\n{b}\n{c}")
    f.close()

with open("Test_File_2.txt", 'r', encoding="UTF-8") as f:
    b = f.read()
    print(b)
    f.close()
