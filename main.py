# main.py
from gui import ModernApp
import tkinter as tk

if __name__ == "__main__":
    print("UKV.v00 running ... ...")
    root = tk.Tk()
    app = ModernApp(root)
    root.mainloop()
    if app.browser_process and app.browser_process.is_alive():
        app.browser_process.terminate()
