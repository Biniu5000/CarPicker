import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd
from bing_image_downloader import downloader
from PIL import ImageTk, Image
import shutil
import tempfile


baza = pd.read_csv("baza.csv")
root = tk.Tk()
# root.geometry("1400x900")
root.title('Porównywarka aut')

# labels
header = ttk.Label(text="Porównywarka aut", background='green', foreground='white', font=("Times New Roman", 30))
label1 = ttk.Label(text="Wybierz typ napędu:")
label2 = ttk.Label(text="Wybierz silnik:")
label3 = ttk.Label(text="Wybierz nadwozie:")
carlabel = ttk.Label()
selected_car = tk.StringVar()


# kod do bt
def buttonclick():
    paramdata = baza.loc[(baza["naped"] == drivevalue.get()) & (baza["silnik"] == enginevalue.get())
                         & (baza["nadwozie"] == bodyvalue.get())]
    if len(drivevalue.get()) == 0 or len(enginevalue.get()) == 0 or len(bodyvalue.get()) == 0:
        carlabel.config(text="Nie podano parametrów!")
    elif paramdata.empty:
        carlabel.config(text="Nie znaleziono szukanego auta!")
        img3 = ImageTk.PhotoImage(Image.open('images/shrug-emoji.gif'))
        panel.configure(image=img3)
        panel.image = img3
    else:
        randcar = paramdata.sample(n=1)  # zwraca 1 losowo wybrany wiersz
        randcar_tuple = randcar["marka"].item(), randcar["model"].item(), randcar["rocznik"].item()
        randcar_text = " ".join(map(str, randcar_tuple))
        carlabel.config(text=randcar_text)
        with tempfile.TemporaryDirectory(dir='images/') as tmpdir:
            downloader.download(randcar_text, limit=1, output_dir=f'images/{tmpdir}', adult_filter_off=True, force_replace=False,
                                timeout=60, verbose=True)
            time.sleep(10)
            path = f'images/{tmpdir}/{randcar_text}/Image_1.jpg'
            img2 = ImageTk.PhotoImage(Image.open(path).resize((640, 360)))
            panel.configure(image=img2)
            panel.image = img2


def adios():
    root.destroy()
    # shutil.rmtree(f'/images/{randcar_text}')


# create a combobox
drive = ttk.Combobox(root, textvariable=selected_car)
engine = ttk.Combobox(root)
body = ttk.Combobox(root)
bt = Button(text="Generuj", command=buttonclick)
exitbt = Button(text="Wyjście", command=adios)

drivevalue = tk.StringVar()  # potrzebne do ustalenia wartości comboboxa
enginevalue = tk.StringVar()
bodyvalue = tk.StringVar()
# comboboxes, prevent typing a value
drive.config(state="readonly", values=('FWD', 'RWD', 'AWD'), textvariable=drivevalue)
engine.config(state="readonly", values=('Spalinowy', 'Elektryczny'), textvariable=enginevalue)
body.config(state="readonly", values=('Sedan', 'Coupe', 'SUV', 'Pickup'), textvariable=bodyvalue)

# place the widget
header.grid(row=0, column=1)
label1.grid(column=0, row=1)
label2.grid(column=1, row=1)
label3.grid(column=2, row=1)
drive.grid(column=0, row=2)
engine.grid(column=1, row=2)
body.grid(column=2, row=2)
bt.grid(row=2, column=3, sticky="e")

# zdjęcie
img = ImageTk.PhotoImage(Image.open('images/kar.png'))
panel = tk.Label(root, image=img)
panel.grid(row=3, column=1)

carlabel.grid(row=4, column=1)
exitbt.grid(row=5, column=3, sticky="e")

# dodawanie auta do bazy
textbox = Text(root, height=1, width=5, bg="light yellow")
addbrand = textbox.grid(column=0, row=4)
#addmodel = textbox.grid(column=1, row=4)
# addyr = textbox.grid(column=2, row=4)
# adddrv = textbox.grid(column=3, row=4)
# addengine = textbox.grid(column=4, row=4)
# addbody = textbox.grid(column=5, row=4)
# drive.set("Typ napędu")
# engine.set("Rodzaj silnika")
# body.set("Typ nadwozia")
root.mainloop()
