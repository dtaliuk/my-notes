import tkinter as tk
import customtkinter
import sqlite3


def db_start():
    global conn, cur

    # подключимся к базе данных notes
    conn = sqlite3.connect('notes.db')

    # создадим объект курсора
    cur = conn.cursor()

    # пропишем SQL-запрос создания таблицы notes только в том случае,
    # если в базе данных ее нет
    cur.execute("""CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)""")


def save_note():
    """Сохранение заметок"""

    note = note_entry.get()
    cur.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    update_notes_list()
    note_entry.delete(0, customtkinter.END)


def delete_note():
    """Удаление заметок"""

    index = notes_list.curselection()
    if index:
        # выбираем заметку
        selected_note = notes_list.get(index)
        # удаляем заметку из базы данных
        cur.execute("DELETE FROM notes WHERE note=?", (selected_note,))
        conn.commit()
        # Обновим список заметок
        update_notes_list()


def update_notes_list():
    """ Обновление списка заметок """

    # очистка виджета ЛистБокс
    notes_list.delete(0, customtkinter.END)

    # получим заметки, хранящиеся в базе данных
    cur.execute('SELECT * FROM notes')
    notes = cur.fetchall()

    # при помощи цикла отобразим на виджете ЛистБокс
    for note in notes:
        note_text = note[1]
        notes_list.insert(customtkinter.END, note_text)


root = customtkinter.CTk()
root.title('Заметки')

# Создадим размер окна и запретим его изменять
root.geometry('400x500')
root.resizable(False, False)

# Создадим виджет с текстом Заметка
note_label = customtkinter.CTkLabel(root, text='Новая заметка:', font=('Comic Sans MS', 22))
# Отобразим его при помощи метода .pack()
note_label.pack(pady=5)  # добавим отступ по Y равный 5

# Создадим текстовое поле, куда пользователь будет вводить текст добавляемой заметки
note_entry = customtkinter.CTkEntry(root, width=300)
note_entry.pack(pady=5)

# Создадим две кнопки: одна - для добавления заметки, другая - для ее удаления
save_button = customtkinter.CTkButton(root, text='Добавить', font=('Comic Sans MS', 14), command=save_note)
save_button.pack(pady=5)

delete_button = customtkinter.CTkButton(root, text='Удалить', font=('Comic Sans MS', 14), command=delete_note)
delete_button.pack(pady=5)

# Создадим ЛистБокс для отображения всех заметок, хранящихся в базе данных
notes_list = tk.Listbox(root, width=42, height=17, font=(None, 18))
notes_list.pack(pady=5)

db_start()
update_notes_list()

root.mainloop()

# закроем соединение с базой
conn.close()
