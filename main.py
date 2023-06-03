import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd

baza = pd.read_csv("baza.csv")
root = tk.Tk()
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
    else:
        carlabel.config(text=paramdata)


# create a combobox
drive = ttk.Combobox(root, textvariable=selected_car)
engine = ttk.Combobox(root)
body = ttk.Combobox(root)
bt = Button(text="Generuj", command=buttonclick)
adios = Button(text="Wyjście", command=root.destroy)

drivevalue = tk.StringVar()  # potrzebne do ustalenia wartości comboboxa
enginevalue = tk.StringVar()
bodyvalue = tk.StringVar()
# comboboxes, prevent typing a value
drive.config(state="readonly", values=('FWD', 'RWD', 'AWD'), textvariable=drivevalue)
engine.config(state="readonly", values=('Spalinowy', 'Elektryczny'), textvariable=enginevalue)
body.config(state="readonly", values=('Sedan', 'Coupe', 'SUV', 'Pickup'), textvariable=bodyvalue)

# place the widget
header.grid(row=0, column=0)
label1.grid(column=0, row=1)
label2.grid(column=1, row=1)
label3.grid(column=2, row=1)
drive.grid(column=0, row=2)
engine.grid(column=1, row=2)
body.grid(column=2, row=2)
bt.grid(row=2, column=3)

# zdjęcie
img = PhotoImage(file='images/kar2.gif')
Label(
    root,
    image=img
).grid(row=3, column=0)

carlabel.grid(row=4, column=0)
adios.grid(row=4, column=1)

#drive.set("Typ napędu")
#engine.set("Rodzaj silnika")
#body.set("Typ nadwozia")
root.mainloop()
