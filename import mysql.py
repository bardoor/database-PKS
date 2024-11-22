import mysql.connector
from abc import ABC


class DateBase:
    __cursor = None
    __connection = None

    @classmethod
    def connect(cls):
        cls.__connection = mysql.connector.connect(
            host="109.206.169.221",
            user="seschool_01",
            password="seschool_01",
            database="seschool_01"
        )

        cls.__cursor = cls.__connection.cursor()

    @classmethod
    def cursor(cls):
        return cls.__cursor

    @classmethod
    def commit(cls):
        cls.__connection.commit()


class Table(ABC):
    @staticmethod
    def add(values: dict):
        pass
    @staticmethod
    def get_fields_name():
        pass
    @staticmethod
    def find(values: dict):
        pass
    @staticmethod
    def delete(values: dict):
        pass


class ListenersTable(Table):

    @staticmethod
    def add(values: dict):
        name = values["NAME"]
        age = values["age"]
        query = "INSERT INTO `Listeners` (NAME) VALUES (%s);"
        DateBase.cursor().execute(query, (name,))
        DateBase.commit()

    @staticmethod
    def get_fields_name():
        return ["NAME","age"]
    @staticmethod
    def find(values: dict):
        name = values["NAME"] if "NAME" in values else None
        age = values["age"] if "age" in values else None
        (sort_name, asc) = values["sort"] if "sort" in values else (None,None)

        limit = values["limit"] if "limit" in values else None
        params = []

        if name is not None and age is not None:
            query = "SELECT `NAME`,`age` FROM `Listeners` WHERE `NAME`=%s AND `age`=%s"
            params += [name,age]
        elif name is not None and age is None:
            query = "SELECT `NAME`,`age` FROM `Listeners` WHERE `NAME`=%s"
            params += [name]
        elif name is None and age is not None:
            query = "SELECT `NAME`,`age` FROM `Listeners` WHERE `age`=%s"
            params += [age]

        else:
            query = "SELECT `NAME`,`age` FROM `Listeners`"

        query += f" ORDER BY {sort_name} {asc};"
        print(params)
        print(query)
        DateBase.cursor().execute(query,params)
        return DateBase.cursor().fetchall()


    @staticmethod
    def delete(values: dict):
        name = values["NAME"]
        query = "DELETE FROM `Listeners` WHERE `NAME`=%s;"
        DateBase.cursor().execute(query, (name,))
        DateBase.commit()



class TracksTable(Table):

    @staticmethod
    def add(values: dict):
        name = values["NAME"]
        query = "INSERT INTO `Tracks` (NAME) VALUES (%s)"
        DateBase.cursor().execute(query, (name,))
        DateBase.commit()
    @staticmethod
    def get_fields_name():
        return ["NAME","date"]

    @staticmethod
    def find(values: dict):
        name = values["NAME"] if "NAME" in values else None
        date = values["date"] if "date" in values else None
        (sort_name, asc) = values["sort"] if "sort" in values else (None, None)

        limit = values["limit"] if "limit" in values else None
        params = []

        if name is not None and date is not None:
            query = "SELECT `NAME`,`date` FROM `Tracks` WHERE `NAME`=%s AND `date`=%s"
            params += [name, date]
        elif name is not None and date is None:
            query = "SELECT `NAME`,`date` FROM `Tracks` WHERE `NAME`=%s"
            params += [name]
        elif name is None and date is not None:
            query = "SELECT `NAME`,`date` FROM `Tracks` WHERE `date`=%s"
            params += [date]

        else:
            query = "SELECT `NAME`,`date` FROM `Tracks`"

        query += f" ORDER BY {sort_name} {asc};"
        # params += [sort_name]
        # {'ASC' if asc == 'ASC' else 'DESC'}
        print(params)
        print(query)
        DateBase.cursor().execute(query, params)
        return DateBase.cursor().fetchall()

    @staticmethod
    def delete(values: dict):
        name = values["NAME"]
        query = "DELETE FROM `Tracks` WHERE `NAME`=%s;"
        DateBase.cursor().execute(query, (name,))
        DateBase.commit()


class Program:
    __is_finished: bool = False
    __current_table: Table

    @classmethod
    def __handle_table_choice(cls):
        print("1: Работать с таблицей Listeners")
        print("2: Работать с таблицей Tracks")

        choice = int(input(">> "))
        if choice == 1:
            cls.__current_table = ListenersTable
        elif choice == 2:
            cls.__current_table = TracksTable

    @classmethod
    def __handle_choice(cls):
        print(f"1: Добавить запись")
        print(f"2: Найти запись")
        print(f"3: Удалить запись")

        choice = int(input(">> "))
        if choice == 1:
            field_names = cls.__current_table.get_fields_name()
            values = dict()

            for field_name in field_names:
                values[field_name] = str(input(f"{field_name}: "))


            cls.__current_table.add(values)
            print("Запись успешно добавлена!")

        elif choice == 2:
            field_names = cls.__current_table.get_fields_name()
            values = dict()

            for field_name in field_names:
                data = str(input(f"Значение для {field_name}: "))
                if data != "":
                    values[field_name] = data
            asc = input("Чтобы выбрать сортировку по возрастанию,напишите ASC ,для сорировки по убыванию напишите DESC:")
            sort_name = input("Напишите столбец который хотите сортировать:")
            values["sort"] = (sort_name,asc)


            print("Поиск выдал данные результаты")
            for strings in cls.__current_table.find(values):
                for string in strings:
                    print(string)
            #print(cls.__current_table.find(values))

        elif choice == 3:
            field_names = cls.__current_table.get_fields_name()
            values = dict()

            for field_name in field_names:
                values[field_name] = input(f"Значение для {field_name}: ")
            cls.__current_table.delete(values)
            print("Запись успешно удалена!")

        elif choice == 6:
            cls.__is_finished = True

    @classmethod
    def main(cls):
        DateBase.connect()
        while (not cls.__is_finished):
            cls.__handle_table_choice()
            cls.__handle_choice()




Program.main()