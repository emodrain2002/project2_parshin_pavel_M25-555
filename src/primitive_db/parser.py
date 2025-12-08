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


def parse_value(raw_value, expected_type):
    value = raw_value.strip()

    if expected_type == "str":
        return value.strip('"')

    if expected_type == "int":
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Некорректное целое число: {value}")

    if expected_type == "bool":
        lowered = value.lower()
        if lowered in ("true", "false"):
            return lowered == "true"
        raise ValueError(f"Некорректное булево значение: {value}")

    raise ValueError(f"Тип {expected_type} не поддерживается")
