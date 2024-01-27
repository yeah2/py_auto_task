import threading
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext

from PIL import Image
from pystray import Icon, Menu
from pystray import MenuItem as item

APP_NAME = "任务助手"
LINE_LIMIT = 1000


class App:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.root, self.log_text = self.create_window()
        self.icon = self.create_tray_icon()

    @classmethod
    def get_instance(cls):
        return App._instance

    def start(self):
        threading.Thread(target=self.icon.run, daemon=True).start()
        # self.hide_to_tray()
        self.root.mainloop()

    def create_window(self):
        root = tk.Tk()
        root.title(APP_NAME)
        root.geometry("600x400")

        root.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        root.protocol("WM_ICONIFY", self.hide_to_tray)
        root.bind("<Unmap>", self.on_unmap)
        # root.bind("<Map>", catch_maximize)

        # 创建内容区
        log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
        log_text.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        return root, log_text

    def create_tray_icon(self):
        # 创建托盘图标
        image = Image.open("res/task.png")
        menu = (
            item('显示', self.show_window),
            item('退出', self.exit_app)
        )
        icon = Icon(APP_NAME, image, menu=Menu(*menu))
        return icon

    def hide_to_tray(self):
        self.root.withdraw()

    def on_unmap(self, event):
        self.hide_to_tray()

    def show_window(self):
        self.root.deiconify()

    def exit_app(self):
        self.icon.stop()
        self.root.destroy()

    def log(self, message):
        formatted_message = self.format_message(message)
        current_log = self.log_text.get("1.0", tk.END)
        current_log = current_log.strip()
        lines = []
        if current_log:
            lines = current_log.split('\n')
        if len(lines) > LINE_LIMIT - 1:
            lines = lines[-(LINE_LIMIT - 1):]
        new_log = '\n'.join(lines + [formatted_message])
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, new_log)
        self.log_text.config(state=tk.DISABLED)

    def format_message(self, message):
        return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}"


gui = App()
