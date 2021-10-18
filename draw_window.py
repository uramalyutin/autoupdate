
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.scrolledtext import ScrolledText


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

# Создадим область текстового редактора
json_content = ScrolledText(width=97, height=20)
json_content.grid(columnspan=3, rowspan=2, row=2)

# Создадим рабочую облаять
header = Frame(root, width=800, height=240, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

if __name__ == "__main__":
    draw_window()
