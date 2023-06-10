import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd
from bing_image_downloader import downloader
from PIL import ImageTk, Image
import tempfile
from csv import writer


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_labels()
        self.__create_widgets()

    def __create_labels(self):
        header = ttk.Label(text="Porównywarka aut", background='green', foreground='white',
                           font=("Times New Roman", 30))
        label1 = ttk.Label(text="Wybierz typ napędu:")
        label2 = ttk.Label(text="Wybierz silnik:")
        label3 = ttk.Label(text="Wybierz nadwozie:")
        header.grid(row=0, column=1)
        label1.grid(column=0, row=1)
        label2.grid(column=1, row=1)
        label3.grid(column=2, row=1)

    def __create_widgets(self):

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
        body.config(state="readonly", values=('Sedan', 'Coupe', 'SUV', 'Pickup', 'Hatchback'), textvariable=bodyvalue)
        img = ImageTk.PhotoImage(Image.open('images/kar.png'))
        panel = tk.Label(image=img)
        panel.image = img
        drive.grid(column=0, row=2)
        engine.grid(column=1, row=2)
        body.grid(column=2, row=2)
        panel.grid(row=3, column=1)
        bt.grid(row=2, column=3, sticky="e")
        carlabel.grid(row=4, column=1)
        exitbt.grid(row=8, column=3, sticky="e")
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
                try:
                    downloader.download(randcar_text, limit=1, output_dir=f'{tmpdir}', adult_filter_off=True,
                                        force_replace=False, timeout=60, verbose=True)
                    time.sleep(7)
                    path = f'{tmpdir}/{randcar_text}/Image_1.jpg'
                    img2 = ImageTk.PhotoImage(Image.open(path).resize((854, 480)))
                    self.panel.configure(image=img2)
                    self.panel.image = img2
                except FileNotFoundError:
                    self.carlabel.config(text="Nie udało się pobrać zdjęcia, sprawdź łącze internetowe.")

    def adios(self):
        self.quit()


class AddCar(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_labels()
        self.__create_widgets()

    def __create_labels(self):
        addl = ttk.Label(self, text="Dodawanie aut do bazy:", background='green', foreground='white', font=("Times "
                                                                                                            "New "
                                                                                                            "Roman",
                                                                                                            16))
        brandl = ttk.Label(self, text="Marka:")
        modell = ttk.Label(self, text="Model:")
        yrl = ttk.Label(self, text="Rocznik:")
        drvl = ttk.Label(self, text="Napęd:")
        enginel = ttk.Label(self, text="Silnik:")
        bodyl = ttk.Label(self, text="Nadwozie:")
        addl.grid(column=0, row=5)
        brandl.grid(column=0, row=6)
        modell.grid(column=1, row=6)
        yrl.grid(column=2, row=6)
        drvl.grid(column=3, row=6)
        enginel.grid(column=4, row=6)
        bodyl.grid(column=5, row=6)

    def __create_widgets(self):
        brandvalue = tk.StringVar()
        modelvalue = tk.StringVar()
        yrvalue = tk.StringVar()
        addbrand = ttk.Entry(self, textvariable=brandvalue)
        addmodel = ttk.Entry(self, textvariable=modelvalue)
        addyr = ttk.Entry(self, textvariable=yrvalue)
        adddrv = ttk.Combobox(self)
        addengine = ttk.Combobox(self)
        addbody = ttk.Combobox(self)
        addcar = ttk.Button(self, text="Dodaj", command=self.addbuttonclick)
        addcarl = ttk.Label(self)
        addbrand.grid(column=0, row=7)
        addmodel.grid(column=1, row=7)
        addyr.grid(column=2, row=7)
        adddrv.grid(column=3, row=7)
        addengine.grid(column=4, row=7)
        addbody.grid(column=5, row=7)
        addcar.grid(column=6, row=7)
        addcarl.grid(column=0, row=8)
        drivevalue = tk.StringVar()  # potrzebne do ustalenia wartości comboboxa
        enginevalue = tk.StringVar()
        bodyvalue = tk.StringVar()
        adddrv.config(state="readonly", values=('FWD', 'RWD', 'AWD'), textvariable=drivevalue)
        addengine.config(state="readonly", values=('Spalinowy', 'Elektryczny'), textvariable=enginevalue)
        addbody.config(state="readonly", values=('Sedan', 'Coupe', 'SUV', 'Pickup', 'Hatchback'), textvariable=bodyvalue
                       )
        self.addcarl = addcarl
        self.brand = brandvalue
        self.model = modelvalue
        self.year = yrvalue
        self.drive = drivevalue
        self.engine = enginevalue
        self.body = bodyvalue

    def addbuttonclick(self):
        try:
            rekord = [self.brand.get(), self.model.get(), int(self.year.get()), self.drive.get(), self.engine.get(),
                      self.body.get()]
            with open('baza.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(rekord)
                f_object.close()
            self.addcarl.config(text="Pomyślnie dodano auto.")
        except ValueError:
            self.addcarl.config(text="Nie udało się dodać auta, sprawdź składnię.")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.geometry("1610x900")
        self.title('Porównywarka aut')
        # self.resizable(0, 0)
        # self.attributes('-toolwindow', True)
        self.__create_labels()
        self.__create_widgets()

    def __create_labels(self):
        main_frame = MainFrame(self)
        main_frame.grid(column=0, row=0)

        addcar_frame = AddCar(self)
        addcar_frame.grid(column=1, row=6)

    def __create_widgets(self):
        main_frame = MainFrame(self)
        main_frame.grid(column=0, row=0)

        addcar_frame = AddCar(self)
        addcar_frame.grid(column=1, row=6)


if __name__ == "__main__":
    app = App()
    app.mainloop()
