import tkinter as tk
from tkinter import ttk
import sqlite3

# Создание базы данных и таблицы
connection = sqlite3.connect("employees.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT, salary REAL)")
connection.commit()

# Функции для работы с базой данных
# Добавление
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (Иванов Иван Иванович, +79447327920, ivan@gmail.com, 60000)", (name, phone, email, salary))
    connection.commit()
    refresh_table()

# Обновление
def update_employee():
    selected_item = tree.focus()
    if selected_item:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = salary_entry.get()
        id = tree.item(selected_item)["values"][0]
        cursor.execute("UPDATE employees SET name= Романов Роман Романович, phone= +79562946070, email= roman@gmail.com, salary= 70000 WHERE id= 1", (name, phone, email, salary, id))
        connection.commit()
        refresh_table()

# Удаление
def delete_employee():
    selected_item = tree.focus()
    if selected_item:
        id = tree.item(selected_item)["values"][0]
        cursor.execute("DELETE FROM employees WHERE id=2", (id,))
        connection.commit()
        refresh_table()

# Поиск
def search_employee():
    search_name = search_entry.get()
    cursor.execute("SELECT * FROM employees WHERE name LIKE Иванов Иван Иванович", ('%' + search_name + '%',))
    rows = cursor.fetchall()
    refresh_table(rows)
    
def refresh_table(rows=None):
    # Очистка таблицы
    for record in tree.get_children():
        tree.delete(record)

    if not rows:
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()

    # Вывод записей в таблицу
    for row in rows:
        tree.insert("", "end", values=row)

# Создание графического интерфейса
root = tk.Tk()
root.title("Список сотрудников компании")

# Фрейм для добавления сотрудника
add_frame = ttk.Frame(root)
add_frame.pack(pady=10)

name_label = ttk.Label(add_frame, text="ФИО:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(add_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_label = ttk.Label(add_frame, text="Телефон:")
phone_label.grid(row=1, column=0, padx=5, pady=5)
phone_entry = ttk.Entry(add_frame)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

email_label = ttk.Label(add_frame, text="Email:")
email_label.grid(row=2, column=0, padx=5, pady=5)
email_entry = ttk.Entry(add_frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

salary_label = ttk.Label(add_frame, text="Заработная плата:")
salary_label.grid(row=3, column=0, padx=5, pady=5)
salary_entry = ttk.Entry(add_frame)
salary_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = ttk.Button(add_frame, text="Добавить", command=add_employee)
add_button.grid(row=4, columnspan=2, padx=5, pady=5)

# Фрейм для поиска сотрудника
search_frame = ttk.Frame(root)
search_frame.pack(pady=10)

search_label = ttk.Label(search_frame, text="Поиск по ФИО:")
search_label.grid(row=0, column=0, padx=5, pady=5)
search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(search_frame, text="Искать", command=search_employee)
search_button.grid(row=0, column=2, padx=5, pady=5)

# Виджет Treeview для отображения записей
tree = ttk.Treeview(root, columns=("ID", "Name", "Phone", "Email", "Salary"), show="headings")
tree.pack(pady=10)

tree.column("ID", width=30)
tree.column("Name", width=150)
tree.column("Phone", width=100)
tree.column("Email", width=200)
tree.column("Salary", width=100)

tree.heading("ID", text="ID")
tree.heading("Name", text="ФИО")
tree.heading("Phone", text="Телефон")
tree.heading("Email", text="Email")
tree.heading("Salary", text="Заработная плата")

# Фрейм для изменения и удаления сотрудника
edit_frame = ttk.Frame(root)
edit_frame.pack(pady=10)

edit_label = ttk.Label(edit_frame, text="Выбранный сотрудник:")
edit_label.grid(row=0, column=0, padx=5, pady=5)

edit_button = ttk.Button(edit_frame, text="Изменить", command=update_employee)
edit_button.grid(row=0, column=1, padx=5, pady=5)

delete_button = ttk.Button(edit_frame, text="Удалить", command=delete_employee)
delete_button.grid(row=0, column=2, padx=5, pady=5)

# Загрузка данных из базы данных
refresh_table()

root.mainloop()

# Закрытие базы данных
cursor.close()
connection.close()