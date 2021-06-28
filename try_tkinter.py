from tkinter import *
from tkinter import colorchooser


class Paint():
    def __init__(self, root):
        # inisialisasi semua hal disini
        self.window = root   # masukan variabel root di init ke variabel window
        self.window.title("Grafkom Kelompok 4")  # Judul di kiri atas program
        self.window.geometry("800x520")
        self.window.configure(background='white')
        self.window.resizable(0, 0)

        self.button_colorcode = Button(root, text="Warna", width=10, command=lambda: self.pilih_warna())
        # colorchooser.askcolor(title="Choose color")
        self.button_colorcode.place(x=0, y=0)

    def pilih_warna(self):
        colorchooser.askcolor(title="Choose color")


if __name__ == "__main__":
    root = Tk()
    p = Paint(root)
    root.mainloop()
