import prompt


def welcome():
    print("Первая попытка запустить проект!\n")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        cmd = prompt.string("Введите команду: ")

        if cmd == "exit":
            print("Выход из программы...")
            break

        elif cmd == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")

        elif cmd == "":
            continue

        else:
            print(f"Неизвестная команда: {cmd}")
