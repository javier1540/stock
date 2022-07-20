import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from stock import *

class App1(ttk.Frame):
    def __init__(self,main_window):
        super().__init__(main_window)
        main_window.title("Lobo Uniformes")

        self.libro = ttk.Notebook(self)
        self.pestana_stock = Stock(self.libro)
        self.libro.add(self.pestana_stock,text="Stock")
        self.libro.pack()

        self.pack()

main_window = tk.Tk()
app = App1(main_window)
app.mainloop()
