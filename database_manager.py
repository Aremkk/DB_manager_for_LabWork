import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def create_database(db_name):
    """Создает новую базу данных."""
    try:
        conn = sqlite3.connect(db_name)
        conn.close()
        print(f"База данных '{db_name}' создана.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")

def create_table(db_name, table_name, columns):
    """Создает новую таблицу в базе данных."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        columns_str = ', '.join([f"{col} TEXT" for col in columns])
        cursor.execute(f"CREATE TABLE {table_name} ({columns_str})")
        conn.commit()
        conn.close()
        print(f"Таблица '{table_name}' создана.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")

def insert_data(db_name, table_name, data):
    """Добавляет данные в таблицу."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * len(data[0]))
        cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        conn.commit()
        conn.close()
        print(f"Данные добавлены в таблицу '{table_name}'.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных: {e}")

def select_data(db_name, table_name, condition=None):
    """Получает данные из таблицы."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        sql_query = f"SELECT * FROM {table_name}"
        if condition:
            sql_query += f" WHERE {condition}"
        cursor.execute(sql_query)
        data = cursor.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        print(f"Ошибка при выборке данных: {e}")
        return None


def update_data(db_name, table_name, set_values, condition):
    """Обновляет данные в таблице."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        set_str = ', '.join([f"{col} = ?" for col in set_values.keys()])
        values = list(set_values.values())
        sql_query = f"UPDATE {table_name} SET {set_str} WHERE {condition}"
        cursor.execute(sql_query, values)
        conn.commit()
        conn.close()
        print(f"Данные обновлены в таблице '{table_name}'.")
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении данных: {e}")

def delete_data(db_name, table_name, condition):
    """Удаляет данные из таблицы."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        sql_query = f"DELETE FROM {table_name} WHERE {condition}"
        cursor.execute(sql_query)
        conn.commit()
        conn.close()
        print(f"Данные удалены из таблицы '{table_name}'.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении данных: {e}")

def visualize_data(data):
    """Визуализация данных."""
    if not data:
        print("Нет данных для визуализации.")
        return

    df = pd.DataFrame(data)
    if df.shape[1] >= 2: # Check if there are at least two columns
        try:
           plt.plot(df.iloc[:,0], df.iloc[:,1])
           plt.xlabel("X")
           plt.ylabel("Y")
           plt.title("Data Visualization")
           plt.show()
        except Exception as e:
            print(f"Ошибка при визуализации данных: {e}")
    else:
        print("Недостаточно данных для визуализации.")
        print(df) # Print the data instead


def create_report(data, report_name):
  """Создаёт отчёт в текстовом файле."""
  if not data:
      print("Нет данных для отчёта.")
      return

  try:
    with open(report_name, 'w') as f:
        for row in data:
            f.write(str(row) + '\n')
    print(f"Отчёт '{report_name}' создан.")
  except Exception as e:
    print(f"Ошибка при создании отчёта: {e}")

def main():
    while True:
        print("\n=== Меню ===")
        print("1. Создать базу данных")
        print("2. Создать таблицу")
        print("3. Добавить данные")
        print("4. Выбрать данные")
        print("5. Обновить данные")
        print("6. Удалить данные")
        print("7. Визуализировать данные")
        print("8. Создать отчёт")
        print("9. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            db_name = input("Введите имя базы данных: ")
            create_database(db_name)
        elif choice == '2':
            db_name = input("Введите имя базы данных: ")
            table_name = input("Введите имя таблицы: ")
            columns_str = input("Введите имена столбцов через запятую: ")
            columns = [col.strip() for col in columns_str.split(',')]
            create_table(db_name, table_name, columns)
        elif choice == '3':
            db_name = input("Введите имя базы данных: ")
            table_name = input("Введите имя таблицы: ")
            data_str = input("Введите данные через запятую (каждая строка через `;`): ")
            try:
              data = [row.strip().split(',') for row in data_str.split(';')]
              insert_data(db_name, table_name, data)
            except Exception as e:
              print(f"Ошибка при вводе данных: {e}")
        elif choice == '4':
            db_name = input("Введите имя базы данных: ")
            table_name = input("Введите имя таблицы: ")
            condition = input("Введите условие (WHERE clause, или оставьте пустым): ")
            data = select_data(db_name, table_name, condition)
            if data:
                print("Данные:")
                for row in data:
                    print(row)
        elif choice == '5':
            db_name = input("Введите имя базы данных: ")
            table_name = input("Введите имя таблицы: ")
            set_values_str = input("Введите значения для обновления (например, column1=value1, column2=value2): ")
            set_values = dict(item.split('=') for item in set_values_str.split(','))
            condition = input("Введите условие (WHERE clause): ")
            update_data(db_name, table_name, set_values, condition)
        elif choice == '6':
            db_name = input("Введите имя базы данных: ")
            table_name = input("Введите имя таблицы: ")
            condition = input("Введите условие (WHERE clause): ")
            delete_data(db_name, table_name, condition)
        elif choice == '7':
            db_name = input("Введите имя базы данных: ")
            table_name = input("Введите имя таблицы: ")
            condition = input("Введите условие (WHERE clause, или оставьте пустым): ")
            data = select_data(db_name, table_name, condition)
            visualize_data(data)
        elif choice == '8':
            db_name = input("Введите имя базы данных: ")
            table_name = input("Введите имя таблицы: ")
            condition = input("Введите условие (WHERE clause, или оставьте пустым): ")
            data = select_data(db_name, table_name, condition)
            report_name = input("Введите имя файла отчета: ")
            create_report(data, report_name)
        elif choice == '9':
            print("Выход.")
            break
        else:
            print("Некорректный ввод. Попробуйте еще раз.")

if __name__ == "__main__":
    main()