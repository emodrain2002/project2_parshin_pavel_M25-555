import os

from prettytable import PrettyTable

from .constants import SUPPORTED_TYPES
from .decorators import confirm_action, handle_db_errors, log_time
from .parser import parse_value
from .utils import BASE_DIR


@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    schema = {"ID": "int"}

    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

        name, t = col.split(":", 1)

        if t not in SUPPORTED_TYPES:
            print(f"Ошибка: неподдерживаемый тип '{t}'")
            return metadata

        schema[name] = t

    metadata[table_name] = schema
    print(
        f'Таблица "{table_name}" успешно создана со столбцами: '
        + ", ".join([f"{k}:{v}" for k, v in schema.items()])
    )

    return metadata


def list_tables(metadata):
    if not metadata:
        print("Таблиц нет.")
        return

    for table in metadata:
        print(f"- {table}")


@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]

    path = os.path.join(BASE_DIR, f"{table_name}.json")
    if os.path.exists(path):
        os.remove(path)

    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


@log_time
@handle_db_errors
def insert_record(metadata, table_name, values, table_data):
    schema = metadata[table_name]
    cols = list(schema.keys())[1:]

    if len(values) != len(cols):
        print("Ошибка: неправильное количество значений.")
        return table_data

    parsed = {}
    for col, val in zip(cols, values):
        col_type = schema[col]
        parsed[col] = parse_value(val, col_type)

    new_id = (max((row["ID"] for row in table_data), default=0)) + 1

    table_data.append({"ID": new_id, **parsed})

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data


@log_time
@handle_db_errors
def filter_records(table_data, schema, col, raw_value):
    if col not in schema:
        raise ValueError(f"Столбец '{col}' не существует.")

    typed_value = parse_value(raw_value, schema[col])

    return [row for row in table_data if row.get(col) == typed_value]


@handle_db_errors
def update_records(
    table_name, table_data, schema, set_col, set_raw, where_col, where_raw
):
    if set_col not in schema:
        raise ValueError(f"Столбец '{set_col}' не существует.")
    if where_col not in schema:
        raise ValueError(f"Столбец '{where_col}' не существует.")

    set_typed = parse_value(set_raw, schema[set_col])
    where_typed = parse_value(where_raw, schema[where_col])

    updated_ids = []

    for row in table_data:
        if row.get(where_col) == where_typed:
            row[set_col] = set_typed
            updated_ids.append(row["ID"])

    if not updated_ids:
        print("Нет записей для обновления.")
    elif len(updated_ids) == 1:
        print(
            f'Запись с ID={updated_ids[0]} в таблице "{table_name}" успешно обновлена.'
        )
    else:
        print(f'Обновлено {len(updated_ids)} записей в таблице "{table_name}".')

    return table_data


@confirm_action("удаление записи")
@handle_db_errors
def delete_records(table_name, table_data, schema, col, raw_value):
    if col not in schema:
        raise ValueError(f"Столбец '{col}' не существует.")

    typed_value = parse_value(raw_value, schema[col])

    deleted_ids = [row["ID"] for row in table_data if row.get(col) == typed_value]
    new_data = [row for row in table_data if row.get(col) != typed_value]

    if not deleted_ids:
        print("Нет записей для удаления.")
    elif len(deleted_ids) == 1:
        print(
            f'Запись с ID={deleted_ids[0]} успешно удалена из таблицы "{table_name}".'
        )
    else:
        print(f'Удалено {len(deleted_ids)} записей из таблицы "{table_name}".')

    return new_data


def print_table(table_name, schema, rows):
    table = PrettyTable()
    table.field_names = list(schema.keys())

    for row in rows:
        table.add_row([row.get(col) for col in schema])

    print(table)
