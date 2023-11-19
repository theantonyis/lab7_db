import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def select_table_from_query(sql_split, query_type):
    if query_type == 'insert':
        query_table = sql_split.index('into') + 1
    elif query_type == 'update':
        query_table = sql_split.index('update') + 1
    else:
        query_table = sql_split.index('from') + 1

    table_name = sql_split[query_table]
    sql = 'SELECT * FROM ' + table_name

    return sql


def execute(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)

        print('Запит: ' + sql)

        sql_split = sql.lower().split()

        if sql_split[0] == 'select':
            rows = cur.fetchall()
            for row in rows:
                print(row)
            print()

        elif sql_split[0] == 'insert':
            print('Запис додано')
            execute(conn, select_table_from_query(sql_split, sql_split[0]))

        elif sql_split[0] == 'update' or sql_split[0] == 'delete':
            conn.commit()
            print('Запис змінено / видалено')
            execute(conn, select_table_from_query(sql_split, sql_split[0]))

    except Error as e:
        print(e)


def main():
    database = r"db.db"

    conn = create_connection(database)

    with conn:
        print("1. Вивести всі записи з таблиці expenses")
        execute(conn, "SELECT * FROM expenses")

        print("2. Зміна категорії в записі з id = 3 на 5")
        execute(conn, "UPDATE expenses SET category_id = 5 WHERE id = 3")

        print("3. Видалення запису з витратами з id = 8")
        execute(conn, "DELETE FROM expenses WHERE id = 8")

        print("4. Додати новий запис про витрати")
        execute(conn, """
                INSERT INTO
                expenses (expense_date, amount, category_id, method_id)
                VALUES ('2023-11-18 15:46:54', 876.00, 12, 2);
            """)

        print(
            "5. Вивести всі витрати які оплачувались карткою, дату, назву категорії та суму витрачених грошей")
        execute(conn, """
                SELECT expenses.id, expenses.expense_date, categories.name, expenses.amount, payment_methods.method
                FROM expenses
                JOIN categories ON categories.id = expenses.category_id
                JOIN payment_methods ON payment_methods.id = expenses.method_id
                WHERE payment_methods.id = 2
            """)


if __name__ == '__main__':
    main()
