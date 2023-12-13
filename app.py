import tkinter as tk
from threading import Thread
import time
from pynput.keyboard import Listener, Key
import pygetwindow as gw

class AppCloser:
    def __init__(self, update_status_func):
        self.last_space_press = 0
        self.active = False
        self.update_status = update_status_func

    def on_press(self, key):
        if not self.active:
            return

        if key == Key.space:
            if time.time() - self.last_space_press < 0.3:  # Tempo entre pressionamentos
                self.close_active_window()
            self.last_space_press = time.time()

    def close_active_window(self):
        try:
            fw = gw.getActiveWindow()
            if fw:
                fw.close()
                self.update_status("Janela fechada com sucesso.")
        except Exception as e:
            self.update_status(f"Erro ao fechar janela: {e}")

    def run(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def toggle(self):
        self.active = not self.active

# Funções da GUI
def toggle_app_closer():
    app_closer.toggle()
    animate_switch()

def animate_switch():
    if app_closer.active:
        switch_button.pack(side="right", fill="both", expand=True)
        switch_frame.config(bg="green")
        switch_label.config(text="ON", bg="green")
        update_status("Aplicativo ativado.")
    else:
        switch_button.pack(side="left", fill="both", expand=True)
        switch_frame.config(bg="grey")
        switch_label.config(text="OFF", bg="grey")
        update_status("Aplicativo desativado.")

def update_status(message):
    status_label.config(text=message)

app_closer = AppCloser(update_status)

root = tk.Tk()
root.title("Fechador de Aplicativos")
root.geometry("400x200")

# Centralizando a janela
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Estilo do Switch Button
switch_frame = tk.Frame(root, bg="grey", bd=2, relief="raised", width=50, height=25)
switch_frame.pack_propagate(False)  # Impede o frame de redimensionar
switch_button = tk.Button(switch_frame, bg="white", width=2, height=1, command=toggle_app_closer, relief="flat")
switch_label = tk.Label(switch_frame, text="OFF", bg="grey", fg="white")

# Vinculando o mesmo comando do botão ao rótulo
switch_label.bind("<Button-1>", lambda e: toggle_app_closer())

switch_frame.pack(pady=60)
switch_button.pack(side="left", fill="both", expand=True)
switch_label.pack(side="left")

# Label de Status
status_label = tk.Label(root, text="Status: Desativado")
status_label.pack()

# Execução em thread separada
thread = Thread(target=app_closer.run)
thread.daemon = True
thread.start()

root.mainloop()
