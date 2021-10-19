
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.scrolledtext import ScrolledText
import paphra_tktable.table as tktable


def open_file():
    file = askopenfile(parent=root, mode='r', filetypes=[("JSON file", "*.json")])
    if file:
        with open(file.name, 'r') as f:
            json_content.insert(1.0, f.read())


def draw_window():
    # Отрисуем окно с учетом виджетов
    root.update_idletasks()
    s = root.geometry()
    s = s.split('+')
    s = s[0].split('x')
    width_root = int(s[0])
    height_root = int(s[1])

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w // 2
    h = h // 2
    w = w - width_root // 2
    h = h - height_root // 2
    root.geometry(f'+{w}+{h}')

    root.mainloop()


root = Tk()
root.title("AutoUpdate")

# Создадим главное меню
mainmenu = Menu(root)
root.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Новый")
filemenu.add_command(label="Открыть...", command=open_file)
filemenu.add_command(label="Сохранить...")
filemenu.add_separator()
filemenu.add_command(label="Выход")
mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_command(label="Обновить")

# Создадим рабочую облаять
header = Frame(root, width=800, height=240, bg="white")
header.grid(columnspan=2, rowspan=2, row=0)
# Создаем таблицу
keys = ["ver",
        "platform_path",
        "server_name_port",
        "db_name",
        "user_name",
        "user_pwd",
        "repository",
        "rep_user_name",
        "rep_user_pwd",
        "lock_time",
        "update"]
titles = [
          {"text": "Версия платформы", "width": 20, "type": 'l'},
          {"text": "Путь к платформе", "width": 60, "type": 'l'},
          {"text": "Имя сервера : порт", "width": 30, "type": 'l'},
          {"text": "Имя базы", "width": 20, "type": 'l'},
          {"text": "Имя пользователя (база)", "width": 20, "type": 'l'},
          {"text": "Пароль (база)", "width": 20, "type": 'l'},
          {"text": "Хранилище}", "width": 30, "type": 'l'},
          {"text": "Имя пользователя (хранилище)", "width": 20, "type": 'l'},
          {"text": "Пароль (хранилище)", "width": 20, "type": 'l'},
          {"text": "Время блокировки", "width": 10, "type": 'l'},
          {"text": "Обновлять", "width": 10, "type": 'l'}
          ]

# Создадим область текстового редактора
json_content = ScrolledText(width=97, height=20)
json_content.grid(columnspan=2, rowspan=2, row=2)

tb = tktable.Table(header,
                   _keys_=keys,
                   titles=titles)
tb.add_rows([{"ver": "8.3.12.1790",
              "platform_path": "C:\\Program Files\\1cv8\\8.3.12.1790\\bin",
              "server_name_port": "77dln-s-a01.1plt.ru:1540",
              "db_name": "tester",
              "user_name": "UpdateUser",
              "user_pwd": "Update1Update",
              "repository": "",
              "rep_user_name": "",
              "rep_user_pwd": "",
              "lock_time": "2",
              "update": "True"}
             ])

if __name__ == "__main__":
    draw_window()
