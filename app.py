import tkinter as tk
from threading import Thread
import time
from pynput.keyboard import Listener, Key
import pygetwindow as gw

class AppCloser:
    def __init__(self):
        self.last_space_press = 0
        self.active = False

    def on_press(self, key):
        if not self.active:
            return

        if key == Key.space:
            if time.time() - self.last_space_press < 0.3:  # 0.3 segundos entre pressionamentos
                self.close_active_window()
            self.last_space_press = time.time()

    def close_active_window(self):
        try:
            fw = gw.getActiveWindow()
            if fw:
                fw.close()
        except Exception as e:
            print(f"Erro ao fechar janela: {e}")

    def run(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def toggle(self):
        self.active = not self.active


def toggle_app_closer():
    app_closer.toggle()
    if app_closer.active:
        toggle_button.config(text="Off", bg="red")
    else:
        toggle_button.config(text="On", bg="blue")


app_closer = AppCloser()

root = tk.Tk()
root.title("Fechador de Aplicativos")
root.geometry("300x150")  # Tamanho da janela

toggle_button = tk.Button(root, text="On", command=toggle_app_closer,
                          bg="blue", fg="white", font=("Helvetica", 12), height=2, width=10)
toggle_button.pack(pady=20)

# Roda o listener em uma thread separada para não bloquear a GUI
thread = Thread(target=app_closer.run)
thread.daemon = True
thread.start()

root.mainloop()
