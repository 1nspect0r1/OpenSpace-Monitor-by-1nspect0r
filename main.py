import tkinter as tk
from tkinter import colorchooser
import psutil
import GPUtil
import webbrowser
import platform

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

def get_cpu_temp():
    system = platform.system()
    if system == "Linux":
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name in temps:
                        for entry in temps[name]:
                            if hasattr(entry, 'label') and 'Package' in entry.label:
                                return entry.current
                            elif hasattr(entry, 'current'):
                                return entry.current
        except Exception:
            return None

    elif system == "Windows":
        try:
            import wmi
            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            temperature_infos = w.Sensor()
            for sensor in temperature_infos:
                if sensor.SensorType == u'Temperature' and 'CPU' in sensor.Name:
                    return float(sensor.Value)
        except Exception:
            return None

    return None

def get_gpu_load_and_temp():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return None
    return [(gpu.load * 100, getattr(gpu, 'temperature', None)) for gpu in gpus]

def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.used // (1024 ** 2), mem.total // (1024 ** 2)  # в МБ

class SystemMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Open-Space Monitor by 1nspect0r1")
        self.geometry("600x500")
        self.configure(bg="black")

        try:
            self.iconbitmap("icon.ico")
        except Exception:
            pass

        self.ascii_label = tk.Label(self, text=ASCII_ART, font=("Courier", 10), fg="cyan", bg="black", justify=tk.LEFT, anchor="nw")
        self.ascii_label.pack(pady=10, fill='both', expand=False)

        settings_btn = tk.Button(self, text="Настройки цвета ASCII-арта", command=self.open_color_settings,
                                 bg='black', fg='white', activebackground='gray20', activeforeground='white', bd=0, highlightthickness=0)
        settings_btn.pack(pady=5)

        self.welcome_label = tk.Label(self, text="Добро пожаловать в открытый космос!", font=("Arial", 14), fg="white", bg="black")
        self.welcome_label.pack(pady=5)

        self.cpu_label = tk.Label(self, text="", font=("Arial", 12), fg="white", bg="black")
        self.cpu_label.pack(pady=5, anchor='w')

        self.gpu_label = tk.Label(self, text="", font=("Arial", 12), fg="white", bg="black")
        self.gpu_label.pack(pady=5, anchor='w')

        self.ram_label = tk.Label(self, text="", font=("Arial", 12), fg="white", bg="black")
        self.ram_label.pack(pady=5, anchor='w')

        self.github_link = tk.Label(self, text="GitHub: github.com/1nspect0r1", fg="cyan", bg="black", cursor="hand2",
                                    font=("Arial", 10, "underline"))
        self.github_link.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)
        self.github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/1nspect0r1"))

        self.update_load()

    def open_color_settings(self):
        color = colorchooser.askcolor(title="Выберите цвет текста ASCII-арта", initialcolor=self.ascii_label.cget("fg"))
        if color and color[1]:
            self.ascii_label.config(fg=color[1])

    def update_load(self):
        cpu_load = get_cpu_load()
        cpu_temp = get_cpu_temp()
        cpu_text = f"Нагрузка CPU: {cpu_load:.1f}%"
        if cpu_temp is not None:
            cpu_text += f" | Температура CPU: {cpu_temp:.1f}°C"
        else:
            cpu_text += " | Температура CPU: недоступна"
        self.cpu_label.config(text=cpu_text)

        gpu_data = get_gpu_load_and_temp()
        if gpu_data is None:
            self.gpu_label.config(text="GPU не обнаружен или данные недоступны.")
        else:
            gpu_text = ""
            for i, (load, temp) in enumerate(gpu_data):
                gpu_text += f"Нагрузка GPU #{i+1}: {load:.1f}%"
                if temp is not None:
                    gpu_text += f" | Температура: {temp:.1f}°C"
                else:
                    gpu_text += " | Температура: недоступна"
                gpu_text += "\n"
            self.gpu_label.config(text=gpu_text.strip())

        ram_percent, ram_used, ram_total = get_ram_usage()
        self.ram_label.config(text=f"Оперативная память: {ram_used} МБ / {ram_total} МБ ({ram_percent:.1f}%)")

        self.after(1000, self.update_load)

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.mainloop()
