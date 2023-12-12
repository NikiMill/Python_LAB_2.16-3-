#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Индивидуальное задание из работы 2.6
#Использовать словарь, содержащий следующиек лючи: название пунктa аназначения; номерпоезда; времяотправления.
#Написать программу, выполняющую следующие действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры; записи должны быть упорядочены по номерам поездов;
#вывод на экран информации о поезде, номер которого введен с клавиатуры; если таких поездов нет, выдать на дисплей соответствующее сообщение
import json
import sys
import time


def get_train():
    # запросить данные о поезде
    name = input("Название пункта назначения? ")
    no = input("Номер поезда? ")
    time_str = input("Введите время отправления (чч:мм)\n")
    t = time.asctime(time.strptime(time_str, "%H:%M"))[11:-5]
    return {
        "name": name,
        "no": no,
        "t": t,
    }


def list(train):
    # Проверить, что список работников не пуст.
    if train:
        line = "+-{}-+-{}-+-{}-+".format(
            "-" * 10,
            "-" * 20,
            "-" * 8,
        )
        print(line)
        print("| {:^10} | {:^20} | {:^8} |".format(" No ", "Название", "Время"))
        print(line)

        for idx, po in enumerate(train, 1):
            print(
                "| {:>10} | {:<20} | {"
                "} |".format(po.get("no", ""), po.get("name", ""), po.get("t", ""))
            )
        print(line)
    else:
        print("Список поездов пуст.")


def select(train, nom):
    result = [po for po in train if po.get("no", "") == nom]
    return result


def save_train(file_name, train):
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(train, fout, ensure_ascii=False, indent=4)


def load_train(file_name):
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def help():
    print("Список команд:\n")
    print("add - добавить поезд;")
    print("list - вывести список поездов;")
    print("select - запросить поезд по номеру;")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


def main():
    train = []

    while True:
        command = input(">>> ").lower()

        if command == "exit":
            break

        elif command == "add":
            po = get_train()
            train.append(po)
            if len(train) > 1:
                train.sort(key=lambda item: item.get("no", ""))

        elif command == "list":
            list(train)

        elif command.startswith("select"):
            print("Введите номер поезда: ")
            nom = input()
            selected = select(train, nom)
            list(selected)

        elif command == "help":
            # Вывести справку о работе с программой.
            help()

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_train(file_name, train)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            train = load_train(file_name)

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == "__main__":
    main()
