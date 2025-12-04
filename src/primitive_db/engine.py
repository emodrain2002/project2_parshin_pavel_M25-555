import shlex

import prompt

from .core import (
    create_table,
    delete_records,
    drop_table,
    filter_records,
    insert_record,
    list_tables,
    print_table,
    update_records,
)
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def parse_where(args):
    if len(args) != 3:
        raise ValueError("Некорректное выражение WHERE.")

    col, op, raw_value = args

    if op != "=":
        raise ValueError("Поддерживается только оператор '='.")

    return col, raw_value


def parse_set(args):
    if len(args) != 3:
        raise ValueError("Некорректное выражение SET.")

    col, op, raw_value = args

    if op != "=":
        raise ValueError("Поддерживается только '='.")

    return col, raw_value


def print_help():
    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) \
        - 'создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> - \
        прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where \
        <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить \
        запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print(
        "<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. \
        - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    print("***База данных***\n")
    print_help()

    while True:
        user_input = prompt.string(">>>Введите команду: ")

        if not user_input:
            continue

        try:
            args = shlex.split(user_input)
        except:  # noqa: E722
            print("Некорректный ввод.")
            continue

        if not args:
            continue

        cmd = args[0]
        metadata = load_metadata()

        if cmd == "exit":
            print("Выход...")
            break

        if cmd == "help":
            print_help()
            continue

        # Таблицы

        if cmd == "create_table":
            if len(args) < 2:
                print("Укажите имя таблицы.")
                continue

            table_name = args[1]
            columns = args[2:]

            meta = create_table(metadata, table_name, columns)
            save_metadata(meta)
            continue

        if cmd == "list_tables":
            list_tables(metadata)
            continue

        if cmd == "drop_table":
            if len(args) != 2:
                print("Укажите имя таблицы.")
                continue

            meta = drop_table(metadata, args[1])
            save_metadata(meta)
            continue

        # INSERT

        if cmd == "insert":
            if len(args) < 4 or args[1] != "into" or args[3] != "values":
                print("Ожидалось: insert into <table> values (...)")
                continue

            table_name = args[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            try:
                start = user_input.index("(") + 1
                end = user_input.rindex(")")
                values_raw = user_input[start:end]
                values = [v.strip() for v in values_raw.split(",")]
            except ValueError:
                print("Некорректный формат values.")
                continue

            data = load_table_data(table_name)
            new_data = insert_record(metadata, table_name, values, data)
            save_table_data(table_name, new_data)
            continue

        # SELECT

        if cmd == "select":
            if len(args) < 3 or args[1] != "from":
                print("Ожидалось: select from <table> [where ...]")
                continue

            table_name = args[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            data = load_table_data(table_name)
            schema = metadata[table_name]

            if len(args) == 3:
                print_table(table_name, schema, data)
                continue

            if args[3] != "where":
                print("Некорректная команда.")
                continue

            col, raw_value = parse_where(args[4:])

            try:
                rows = filter_records(data, schema, col, raw_value)
                print_table(table_name, schema, rows)
            except ValueError as e:
                print(f"Ошибка: {e}")
            continue

        # UPDATE

        if cmd == "update":
            table_name = args[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            data = load_table_data(table_name)
            schema = metadata[table_name]

            if len(args) < 4 or args[2] != "set":
                print("Ожидалось: update <table> set ... where ...")
                continue

            try:
                idx_where = args.index("where")
            except ValueError:
                print("Ожидалось: where")
                continue

            try:
                set_col, set_raw = parse_set(args[3:idx_where])
                where_col, where_raw = parse_where(args[idx_where + 1 :])
                new_data = update_records(
                    table_name, data, schema, set_col, set_raw, where_col, where_raw
                )
                save_table_data(table_name, new_data)
            except ValueError as e:
                print(f"Ошибка: {e}")
            continue

        # DELETE

        if cmd == "delete":
            if len(args) < 4 or args[1] != "from":
                print("Ожидалось: delete from <table> where ...")
                continue

            table_name = args[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            data = load_table_data(table_name)
            schema = metadata[table_name]

            if args[3] != "where":
                print("Ожидалось: where")
                continue

            try:
                col, raw_value = parse_where(args[4:])
                new_data = delete_records(table_name, data, schema, col, raw_value)
                save_table_data(table_name, new_data)
            except ValueError as e:
                print(f"Ошибка: {e}")
            continue

        # INFO

        if cmd == "info":
            if len(args) != 2:
                print("Укажите имя таблицы.")
                continue

            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            schema = metadata[table_name]
            data = load_table_data(table_name)

            print(f"Таблица: {table_name}")
            print("Столбцы: " + ", ".join([f"{k}:{v}" for k, v in schema.items()]))
            print(f"Количество записей: {len(data)}")
            continue

        print(f"Функции {cmd} нет. Попробуйте снова.")
