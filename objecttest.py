import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd
from bing_image_downloader import downloader
from PIL import ImageTk, Image
import tempfile


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        header = ttk.Label(text="Porównywarka aut", background='green', foreground='white',
                           font=("Times New Roman", 30))
        label1 = ttk.Label(text="Wybierz typ napędu:")
        label2 = ttk.Label(text="Wybierz silnik:")
        label3 = ttk.Label(text="Wybierz nadwozie:")
        carlabel = ttk.Label()
        selected_car = tk.StringVar()
        drive = ttk.Combobox(textvariable=selected_car)
        engine = ttk.Combobox()
        body = ttk.Combobox()
        bt = Button(text="Generuj", command=self.buttonclick)
        exitbt = Button(text="Wyjście", command=self.adios)
        drivevalue = tk.StringVar()  # potrzebne do ustalenia wartości comboboxa
        enginevalue = tk.StringVar()
        bodyvalue = tk.StringVar()
        # comboboxes, prevent typing a value
        drive.config(state="readonly", values=('FWD', 'RWD', 'AWD'), textvariable=drivevalue)
        engine.config(state="readonly", values=('Spalinowy', 'Elektryczny'), textvariable=enginevalue)
        body.config(state="readonly", values=('Sedan', 'Coupe', 'SUV', 'Pickup'), textvariable=bodyvalue)
        img = ImageTk.PhotoImage(Image.open('images/kar.png'))
        panel = tk.Label(image=img)
        panel.image = img
        header.grid(row=0, column=1)
        label1.grid(column=0, row=1)
        label2.grid(column=1, row=1)
        label3.grid(column=2, row=1)
        drive.grid(column=0, row=2)
        engine.grid(column=1, row=2)
        body.grid(column=2, row=2)
        panel.grid(row=3, column=1)
        bt.grid(row=2, column=3, sticky="e")
        carlabel.grid(row=4, column=1)
        exitbt.grid(row=6, column=3, sticky="e")
        # dla buttonclick??
        self.drivevalue = drivevalue
        self.enginevalue = enginevalue
        self.bodyvalue = bodyvalue
        self.carlabel = carlabel
        self.panel = panel

    def buttonclick(self):
        baza = pd.read_csv("baza.csv")
        paramdata = baza.loc[(baza["naped"] == self.drivevalue.get()) & (baza["silnik"] == self.enginevalue.get())
                             & (baza["nadwozie"] == self.bodyvalue.get())]
        if len(self.drivevalue.get()) == 0 or len(self.enginevalue.get()) == 0 or len(self.bodyvalue.get()) == 0:
            self.carlabel.config(text="Nie podano parametrów!")
        elif paramdata.empty:
            self.carlabel.config(text="Nie znaleziono szukanego auta!")
            img3 = ImageTk.PhotoImage(Image.open('images/shrug-emoji.gif'))
            self.panel.configure(image=img3)
            self.panel.image = img3
        else:
            randcar = paramdata.sample(n=1)  # zwraca 1 losowo wybrany wiersz
            randcar_tuple = randcar["marka"].item(), randcar["model"].item(), randcar["rocznik"].item()
            randcar_text = " ".join(map(str, randcar_tuple))
            self.carlabel.config(text=randcar_text)
            with tempfile.TemporaryDirectory(dir='images/') as tmpdir:
                downloader.download(randcar_text, limit=1, output_dir=f'images/{tmpdir}', adult_filter_off=True,
                                    force_replace=False, timeout=60, verbose=True)
                time.sleep(10)
                path = f'images/{tmpdir}/{randcar_text}/Image_1.jpg'
                img2 = ImageTk.PhotoImage(Image.open(path).resize((640, 360)))
                self.panel.configure(image=img2)
                self.panel.image = img2

    def adios(self):
        self.quit()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # root.geometry("1400x900")
        self.title('Porównywarka aut')


if __name__ == "__main__":
    app = App()
    frame = MainFrame(app)
    app.mainloop()
