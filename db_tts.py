import sqlite3
from config_tts import DB_NAME, TABLE_NAME

def create_db(database_name=DB_NAME):
    db_path = f'{database_name}'
    conn = sqlite3.connect(db_path)
    conn.close()



def execute_query(sql_query, data=None, db_path=DB_NAME):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)
        connection.commit()


def execute_selection_query(sql_query, data=None, db_path=DB_NAME):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.close()
    return rows


def create_table(TABLE_NAME):
    sql_query = (f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}'
                 f'(id INTEGER PRIMARY KEY,'
                 f'user_id INTEGER,'
                 f'message TEXT,'
                 f'tts_symbols INTEGER)')
    execute_query(sql_query)
def is_value_in_table(table_name, column_name, value):
    sql_query = f'SELECT {column_name} FROM {table_name} WHERE {column_name} = {value} LIMIT 1'
    rows = execute_selection_query(sql_query)
    return any(rows) > 0

def update_row_value(user_id, column_name, new_value):
    if is_value_in_table(TABLE_NAME, "user_id", user_id):
        sql_query = f'UPDATE {TABLE_NAME} SET {column_name} = ? WHERE user_id = {user_id}'
        execute_query(sql_query, [new_value])
    else:
        print("DATABASE: Пользователь с таким id не найден")

def insert_row(user_id, message, tts_symbols):
    sql_query = f"""
    INSERT INTO {TABLE_NAME} 
    (user_id, message, tts_symbols)
    VALUES(?,?,?)"""
    execute_query(sql_query, [user_id, message, tts_symbols])

def newdata(user_id, message, tts_symbols):
    if is_value_in_table(TABLE_NAME, 'user_id', user_id):
        update_row_value(user_id, 'message', message)
        update_row_value(user_id, 'tts_symbols', tts_symbols)
    else:
        insert_row(user_id, message, tts_symbols)
    prepare_db(True)


def count_all_symbol(user_id):
    sql_query = f"""
    SELECT SUM(tts_symbols)
    FROM {TABLE_NAME}
    WHERE user_id = "{user_id}"
    GROUP BY user_id
    """
    data = execute_selection_query(sql_query)

    if data:
        return data[0][0]


def prepare_db(clean_if_exists=False):
    create_db()
    create_table(TABLE_NAME)
