import time
from functools import wraps


def handle_db_errors(func):
    """Handles database errors."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. Возможно, база данных не \
                инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    return wrapper


def confirm_action(action_name):
    """Asks user to confirm the action."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            confirm = (
                input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
                .strip()
                .lower()
            )
            if confirm != "y":
                print(f"Операция '{action_name}' отменена.")
                return args[0]
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    """Logs execution time of the function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        print(f"Функция {func.__name__} выполнилась за {end - start:.3f} секунд.")
        return result

    return wrapper


def create_cacher():
    """Creates memory caching."""
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    def invalidate_cache():
        cache.clear()

    cache_result.invalidate = invalidate_cache
    return cache_result