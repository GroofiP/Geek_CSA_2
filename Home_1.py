# Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
# info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
# В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы»,  «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
# соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
# os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data —
# и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
# «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить
# в файл main_data (также для каждого файла);
import csv

file_info_all = ["info_1.txt", "info_2.txt", "info_3.txt"]

os_prod_list = []

os_name_list = []

os_code_list = []

os_type_list = []


def get_data():
    main_data = [["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]]
    for file in file_info_all:
        with open(f"{file}", encoding="utf-8") as f:
            read_f = csv.reader(f)
            for row in read_f:
                row_value = "".join(row)
                row_value = row_value.split(":")
                if main_data[0][0] in row_value:
                    os_prod_list.append(row_value[1].strip())
                if main_data[0][1] in row_value:
                    os_name_list.append(row_value[1].strip())
                if main_data[0][2] in row_value:
                    os_code_list.append(row_value[1].strip())
                if main_data[0][3] in row_value:
                    os_type_list.append(row_value[1].strip())
    main_data.append(
        [
            os_prod_list,
            os_name_list,
            os_code_list,
            os_type_list
        ]
    )
    return main_data


def write_csv(file):
    with open(file, "w") as f:
        csv_write = csv.writer(f)
        csv_write.writerows(get_data())


write_csv("main_data.csv")
