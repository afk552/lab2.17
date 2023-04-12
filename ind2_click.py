#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import os
import json
import copy
import click


@click.group()
def cli():
    pass


@cli.command("display")
@click.argument("filename")
def display_data(filename):
    """
    Вывести людей из списка
    """
    if os.path.exists(filename):
        people = load_workers(filename)
    else:
        people = []
    display_people(people)


@cli.command("select")
@click.argument("filename")
@click.option(
    "--month",
    help="Запросить людей, чьи дни рождения приходятся на месяц (число)",
)
def select_data(filename, month):
    """
    Выбрать людей по заданному месяцу рождения
    """
    if os.path.exists(filename):
        people = load_workers(filename)
    else:
        people = []
    select_people(f"select {month}", people)


@cli.command("add")
@click.argument("filename")
@click.option("--name", help="Имя человека")
@click.option("--surname", help="Фамилия человека")
@click.option(
    "--pnumber",
    help="Номер телефона",
)
@click.option("--birth", help="Дата рождения человека (01.01.2077)")
def add_data(filename, name, surname, pnumber, birth):
    """
    Добавить людей
    """
    if os.path.exists(filename):
        people = load_workers(filename)
    else:
        people = []
    full_name = f"{name} {surname}"
    birth = birth.split(".")
    birth_dt = datetime(int(birth[2]), int(birth[1]), int(birth[0]))
    people.append({"name": full_name, "pnumber": pnumber, "birth": birth_dt})
    save_workers(filename, people)


def load_workers(file_name):
    """
    Загрузка списка людей из json
    """
    if file_name.split(".", maxsplit=1)[-1] != "json":
        print("Несоответствующий формат файла", file=sys.stderr)
        return []

    if not os.path.exists(f"{os.getcwd()}/{file_name}"):
        print("Заданного файла не существует!", file=sys.stderr)
        return []

    with open(file_name, "r", encoding="utf-8") as f_in:
        data = json.load(f_in)
        flag = True
        if flag:
            for i in data:
                i["birth"] = datetime.strptime(i["birth"], "%d.%m.%Y").date()
            return data
        else:
            return []


def save_workers(file_name, people_list):
    """
    Сохранение списка людей в json
    """
    # Проверка заданного имени файла
    if file_name.split(".", maxsplit=1)[-1] != "json":
        print("Заданный формат файла не .json", file=sys.stderr)
        return False

    # Делаем копию списка, чтобы его не затронуть
    lst = copy.deepcopy(people_list)
    # Сериализация даты в строку для записи в файл
    list(lst)
    print(lst)
    for i in lst:
        i["birth"] = i["birth"].strftime("%d.%m.%Y")

    # Дамп в json списка
    with open(file_name, "w", encoding="utf-8") as f_out:
        json.dump(lst, f_out, ensure_ascii=False, indent=4)
    lst.clear()


def display_people(people_list):
    """
    Вывести людей из списка
    """
    if people_list:
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 14, "-" * 19
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^14} | {:^19} |".format(
                "№п/п", "Фамилия Имя", "Номер телефона", "Дата рождения"
            )
        )
        print(line)
        for nmbr, person in enumerate(people_list, 1):
            print(
                "| {:>4} | {:<30} | {:<14} | {:>19} |".format(
                    nmbr,
                    person.get("name", ""),
                    person.get("pnumber", ""),
                    person.get("birth", "").strftime("%d.%m.%Y"),
                )
            )
        print(line)
    else:
        print("Список людей пуст!")


def correct_date(print_month):
    """
    Скорректировать номер месяца
    """
    month_by_text = {
        "январь": "01",
        "февраль": "02",
        "март": "03",
        "апрель": "04",
        "май": "05",
        "июнь": "06",
        "июль": "07",
        "август": "08",
        "сентябрь": "09",
        "октябрь": "10",
        "ноябрь": "11",
        "декабрь": "12",
    }
    if print_month.isalpha():
        print_month.lower()
        for key, value in month_by_text.items():
            if key == print_month:
                print_month = value
    if len(print_month) == 1:
        return "0" + print_month
    else:
        return print_month


def select_people(cmd, people_list):
    """
    Выбрать людей по заданному месяцу рождения
    """
    parts = cmd.split(" ", maxsplit=1)
    printed_month = parts[1]
    corrected_month = correct_date(printed_month)
    result = []
    for person in people_list:
        birth = person.get("birth")
        if corrected_month == birth.strftime("%m"):
            result.append(person)

    if len(result) > 0:
        display_people(result)
    else:
        print("Людей, чьи дни рождения приходятся на этот месяц нет!")


def main():
    cli()


if __name__ == "__main__":
    main()
