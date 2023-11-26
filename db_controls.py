import datetime
import sqlite3


def columns_names_values_to_string(columns_names, values):
    columns_names_string = ""
    values_string = ""
    for columns_name in columns_names:
        columns_names_string += columns_name + ","
    columns_names_string = columns_names_string[:-1]
    for value in values:
        if isinstance(value, str):
            values_string += "'" + value + "'" + ","
        else:
            values_string += str(value) + ','
    values_string = values_string[:-1]
    return columns_names_string, values_string


def connect_table(db_path, table_name, columns_types_dict=None, unique=False):
    """
    :param db_path: string database name
    :param table_name: string table name
    :param columns_types_dict: dictionary {string column name : string column type }
    :return:
    """
    db = sqlite3.connect(f"{db_path}.db")
    cur = db.cursor()
    columns_types_string = ""
    for column_name in columns_types_dict:
        columns_types_string += column_name + " " + columns_types_dict[column_name] + ",\n"

    columns_types_string = columns_types_string[:-2]

    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY,
    {columns_types_string})""")

    db.commit()
    db.close()


def insert(db_path, table_name, columns_values_dict):
    db = sqlite3.connect(f"{db_path}.db")
    cur = db.cursor()
    columns_names = columns_values_dict.keys()
    columns_values = columns_values_dict.values()
    columns_names, columns_values = columns_names_values_to_string(columns_names, columns_values)
    try:
        cur.execute(f"""INSERT INTO {table_name} ({columns_names}) VALUES({columns_values})""")
    except sqlite3.IntegrityError:
        pass
    db.commit()
    db.close()


def select(db_path, table_name, column_name, condition_column_name, condition_value):
    db = sqlite3.connect(f"{db_path}.db")
    cur = db.cursor()
    try:
        cur.execute(f"""SELECT {column_name} FROM {table_name} WHERE {condition_column_name} = {condition_value}""")
        ret_value = cur.fetchone()
        db.close()
        if ret_value is not None:
            return ret_value[0]
        else:
            return None
    except sqlite3.OperationalError:
        return None


def update(db_path, table_name, column_name, value, condition_column_name, condition_value):
    db = sqlite3.connect(f"{db_path}.db")
    cur = db.cursor()
    if isinstance(value, str):
        if isinstance(condition_value, str):
            cur.execute(
                f"""UPDATE {table_name} SET {column_name} = '{value}' WHERE {condition_column_name} = '{condition_value}'""")
        else:
            cur.execute(
                f"""UPDATE {table_name} SET {column_name} = '{value}' WHERE {condition_column_name} = {condition_value}""")
    else:
        if isinstance(condition_value, str):
            cur.execute(
                f"""UPDATE {table_name} SET {column_name} = {value} WHERE {condition_column_name} = '{condition_value}'""")
        else:
            cur.execute(
                f"""UPDATE {table_name} SET {column_name} = {value} WHERE {condition_column_name} = {condition_value}""")

    db.commit()
    db.close()


def main():
    chat_attributes = {
        "chat_id": "INTEGER UNIQUE",
        "message_count": "INTEGER",

    }
    insert_values = {
        "chat_id": 5,
        "message_count": 1,

    }
    connect_table("BotDB", "chats", chat_attributes)
    insert("BotDB", "chats", insert_values)


def main():
    print(datetime.datetime.now().strftime("%D"))


if __name__ == '__main__':
    main()
