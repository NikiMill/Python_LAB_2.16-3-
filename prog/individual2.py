#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Для своего варианта лабораторной работы 2.8 -> (2.6) необходимо дополнительно  реализовать  сохранение  и  чтение  данных  из  файла формата  JSON.
# Необходимо  также  проследить  за  тем,  чтобы  файлы генерируемый   этой   программой   не   попадали   в   репозиторий лабораторной работы.
import json
import jsonschema
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
    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "poezd": {
                    "name": {"type": "string"},
                    "no": {"type": "string"},
                    "t": {"type": "string"},
                },
                "required": ["name", "no", "t"],
            }
        ],
    }
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
        validator = jsonschema.Draft7Validator(schema)
        try:
            if not validator.validate(loadfile):
                print("Валидация прошла успешно")
        except jsonschema.exceptions.ValidationError:
            print("Ошибка валидации", file=sys.stderr)
            exit()
    return loadfile


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
            help()

        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save_train(file_name, train)

        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            train = load_train(file_name)

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == "__main__":
    main()
