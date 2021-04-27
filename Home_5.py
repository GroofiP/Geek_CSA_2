# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового
# в строковый тип на кириллице.
import subprocess

from pip._vendor import chardet

# args = ["ping","yandex.ru"]
# sub_ping = subprocess.Popen(args,stdout=subprocess.PIPE)
# for line in sub_ping.stdout:
#     result = chardet.detect(line)
#     line = line.decode(result["encoding"]).encode("utf-8")
#     print(line.decode("utf-8"))



args = ["ping","youtube.com"]
sub_ping = subprocess.Popen(args,stdout=subprocess.PIPE)
for line in sub_ping.stdout:
    result = chardet.detect(line)
    line = line.decode(result["encoding"]).encode("utf-8")
    print(line.decode("utf-8"))


