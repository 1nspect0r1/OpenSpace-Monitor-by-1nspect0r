import tkinter as tk
from tkinter import colorchooser
import psutil
import GPUtil

ASCII_ART = r"""
                _..._
              .'     '.      _
             /    .-""-\   _/ \   ||Open-Space Monitor||
           .-|   /:.   |  |   |   ||by 1nspect0r1     ||
           |  \  |:.   /.-'-./
           | .-'-;:__.'    =/
           .'=  *=|     _.='
          /   _.  |    ;
         ;-.-'|    \   |
        /   | \    _\  _\
        \__/'._;.  ==' ==\
                 \    \   |
                 /    /   /
                 /-._/-._/
                 \   `\  \
                  `-._/._/
"""

def get_cpu_load():
    return psutil.cpu_percent(interval=None)

def get_gpu_load():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return None
    return [gpu.load * 100 for gpu in gpus]

class SystemMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Open-Space Monitor by 1nspect0r1")
        self.geometry("600x500")
        self.configure(bg="black")

        # Иконка .ico (если есть)
        try:
            self.iconbitmap("icon.ico")
        except Exception:
            pass  # если иконка не найдена, просто игнорируем

        # ASCII-арт в Label с моноширинным шрифтом
        self.ascii_label = tk.Label(self, text=ASCII_ART, font=("Courier", 10), fg="cyan", bg="black", justify=tk.LEFT, anchor="nw")
        self.ascii_label.pack(pady=10, fill='both', expand=False)

        # Кнопка для открытия окна настроек цвета ASCII-арта
        settings_btn = tk.Button(self, text="Настройки цвета ASCII-арта", command=self.open_color_settings,
                                 bg='black', fg='white', activebackground='gray20', activeforeground='white', bd=0, highlightthickness=0)
        settings_btn.pack(pady=5)

        # Приветствие
        self.welcome_label = tk.Label(self, text="Добро пожаловать в открытый космос!", font=("Arial", 14), fg="white", bg="black")
        self.welcome_label.pack(pady=5)

        # Метки для нагрузки CPU и GPU
        self.cpu_label = tk.Label(self, text="", font=("Arial", 12), fg="white", bg="black")
        self.cpu_label.pack(pady=5, anchor='w')

        self.gpu_label = tk.Label(self, text="", font=("Arial", 12), fg="white", bg="black")
        self.gpu_label.pack(pady=5, anchor='w')

        # Добавляем ссылку на GitHub внизу справа
        self.github_link = tk.Label(self, text="GitHub: github.com/1nspect0r1", fg="cyan", bg="black", cursor="hand2",
                                    font=("Arial", 10, "underline"))
        self.github_link.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # отступы от правого нижнего угла
        self.github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/1nspect0r1"))

        # Запускаем обновление данных
        self.update_load()

    def open_color_settings(self):
        # Окно выбора цвета
        color = colorchooser.askcolor(title="Выберите цвет текста ASCII-арта", initialcolor=self.ascii_label.cget("fg"))
        if color and color[1]:
            self.ascii_label.config(fg=color[1])

    def update_load(self):
        cpu_load = get_cpu_load()
        self.cpu_label.config(text=f"Нагрузка CPU: {cpu_load:.1f}%")

        gpu_loads = get_gpu_load()
        if gpu_loads is None:
            self.gpu_label.config(text="GPU не обнаружен или данные недоступны.")
        else:
            gpu_text = "\n".join([f"Нагрузка GPU #{i+1}: {load:.1f}%" for i, load in enumerate(gpu_loads)])
            self.gpu_label.config(text=gpu_text)

        self.after(1000, self.update_load)


if __name__ == "__main__":
    app = SystemMonitorApp()
    app.mainloop()
