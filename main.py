from tkinter import *
from tkinter import colorchooser


class Paint:
    def __init__(self, root):
        # inisialisasi awal
        self.window = root  # masukan variabel root di init ke variabel window
        self.window.title("Grafkom Kelompok 4")  # Judul di kiri atas program

        # inisialiasi canvas (area nya)
        self.canvas = Canvas(self.window, width=1080, height=667, bg="#FFFFFF", relief=RIDGE,
                             bd=10)  # di contoh make_canvas
        self.canvas.place(x=0, y=0)

        # inisialisasi semua tools dan menu dengan null dulu
        self.tab_menu = None
        self.menu_file = None
        self.menu_edit = None
        self.color_menu = None
        self.option_menu = None
        self.koordinat = None  # coord di contoh
        self.status_fungsi = None  # status di contoh
        self.kumpulan_fungsi = None  # controller_set di contoh
        self.choosing_color = None
        self.color = None
        self.notation_box = None  # Daftar Item
        self.segmen_buat = None  # segment_1 di contoh
        self.segmen_tools = None  # segment_2 di contoh
        self.segmen_rotasi = None
        self.segmen_refleksi = None
        self.frame_width = None  # make_width_fram di contoh buat setting ketebalan objek

        # inisialisasi koordinat
        self.x_lama = None
        self.y_lama = None
        self.x_baru = None
        self.y_baru = None

        # inisialisasi tombol pada menu nya
        self.pensil = Button(self.window)
        self.garis = Button(self.window)
        self.lingkaran = Button(self.window)
        self.kotak = Button(self.window)
        self.segitiga = Button(self.window)
        # self.selection_tools = Button(self.window)
        self.reset_button = Button(self.window)
        self.milih_warna_fill = Button(self.window)
        self.milih_warna_outline = Button(self.window)
        self.rotasi = Button(self.window)
        self.refleksi_x = Button(self.window)
        self.refleksi_y = Button(self.window)

        # insialisasi yang perlu disimpan array
        self.tempat_undo = []
        self.temp = []
        self.simpan_koordinat = {}

        # inisialisasi variabel penting
        self.fill_information = IntVar()
        self.outline_information = IntVar()
        self.fill_information.set(0)
        self.outline_information.set(0)

        # inisialisasi warna
        self.fill_color = "#FFFFFF"  # isi kotak, lingkaran, or objek lainnya warnanya putih
        self.fill_color_line = "black"  # warna untuk garis atau pakai pensil
        self.outline_color_line = "black"  # warna pinggiran kotak, lingkaran, or objek

        # inisialisasi beberapa nilai
        self.width_controller_scale = 0  # buat slider ukuran
        self.counter = -1  # untuk itungan copy paste
        self.width_maintainer = 2  # default ketebalan outline (untuk objek) atau ketebalan garis
        self.erase_width_maintainer = 5  # default ukuran penghapus

        # Fungsi default
        # self.fungsi(1)  # secara default ke fungsi 1 yaitu pensil
        self.controller()
        self.make_status_bar()
        # self.buat_menu()
        # self.buat_status_bar()
        self.width_controller()  # pengaturan slider ukuran outline dan penghapus
        self.canvas.bind("<Control-MouseWheel>", self.zoom_controller)  # default ctrl+scroll buat zoom in /out
        self.canvas.bind('<Motion>', self.movement_cursor)  # deteksi pergerakan mouse

    def warna_fill(self):
        color = colorchooser.askcolor(title="Choose color")
        self.fill_color = color[1]
        self.fill_color_line = color[1]

    def warna_outline(self):
        color = colorchooser.askcolor(title="Choose color")
        self.outline_color_line = color[1]

    def fungsi(self, notasi):
        if self.temp:
            self.canvas.delete(self.temp.pop())
        if self.notation_box:
            if self.notation_box['state'] == DISABLED:
                self.notation_box['state'] = NORMAL
        # bentuk kursornya plus
        self.canvas.config(cursor="TCROSS")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<Button-1>")

        if notasi == 1:
            self.canvas.config(cursor="circle")
            self.canvas.bind("<B1-Motion>", self.pakai_pensil)
        elif notasi == 2:
            self.canvas.bind("<B1-Motion>", self.buat_lingkaran)
        elif notasi == 3:
            self.canvas.bind("<B1-Motion>", self.buat_kotak)
        elif notasi == 4:
            self.canvas.bind('<B1-Motion>', self.buat_segitiga)
        elif notasi == 5:
            self.canvas.bind("<B1-Motion>", self.garis_sembarang)
            self.canvas.bind("<Shift-B1-Motion>", self.garis_lurus)
        elif notasi == 7:
            self.canvas.unbind("<B1-Motion>")
            self.canvas.config(cursor="")

    def controller(self):
        # set bar di kanan
        self.kumpulan_fungsi = LabelFrame(self.window, text="Semua Fungsi", bg="RoyalBlue1",
                                          fg="white", width=250, height=688, relief=RAISED, bd=10,
                                          font=("Arial", 12, "bold italic"))
        self.kumpulan_fungsi.place(x=1100, y=0)

        # box notasi untuk milih yang mana objeknya
        self.notation_box = Listbox(self.kumpulan_fungsi, width=5, height=11, font=("Arial", 10, "bold"),
                                    fg="mint cream",
                                    bg="SteelBlue1", relief=SUNKEN, bd=5)
        self.notation_box.place(x=180, y=370)

        # segmen 1 untuk buat garis, kotak, dan objek lainnya
        self.segmen_buat = Label(self.kumpulan_fungsi, text="Buat Objek", bg="SteelBlue1", fg="firebrick2",
                                 font=("Arial", 12, "bold"), relief=GROOVE, bd=1, padx=10, pady=1)
        self.segmen_buat.place(x=60, y=4)

        # taruh tombol pensil
        self.pensil = Button(self.kumpulan_fungsi, text="Pensil", bg="white", fg="firebrick3",
                             font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.fungsi(1))
        self.pensil.place(x=10, y=40)

        # tarug tombol lingkaran
        self.lingkaran = Button(self.kumpulan_fungsi, text="Lingkaran", bg="white", fg="firebrick3",
                                font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.fungsi(2))
        self.lingkaran.place(x=78, y=40)

        # taruh tombol kotak
        self.kotak = Button(self.kumpulan_fungsi, text="Kotak", bg="white", fg="firebrick3",
                            font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.fungsi(3))
        self.kotak.place(x=170, y=40)

        # taruh tombol segitiga
        self.segitiga = Button(self.kumpulan_fungsi, text="Segitiga", bg="white", fg="firebrick3",
                               font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.fungsi(4))
        self.segitiga.place(x=10, y=85)

        # taruh tombol garis
        self.garis = Button(self.kumpulan_fungsi, text="Garis", bg="white", fg="firebrick3",
                            font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.fungsi(5))
        self.garis.place(x=85, y=85)

        # segmen rotasi
        self.segmen_rotasi = Label(self.kumpulan_fungsi, text="Tools Rotasi", bg="SteelBlue1", fg="firebrick2",
                                   font=("Arial", 12, "bold"), relief=GROOVE, bd=1, padx=10, pady=1)
        self.segmen_rotasi.place(x=55, y=130)

        # taruh tombol rotasi 30 derajat
        self.rotasi = Button(self.kumpulan_fungsi, text="30", bg="white", fg="firebrick3",
                             font=("Arial", 10, "bold"), relief=RAISED, bd=3,
                             command=lambda: self.warna_outline())
        self.rotasi.place(x=10, y=160)

        # segmen 2 untuk tools
        self.segmen_tools = Label(self.kumpulan_fungsi, text="Kumpulan Tools", bg="SteelBlue1", fg="firebrick2",
                                  font=("Arial", 12, "bold"), relief=GROOVE, bd=1, padx=10, pady=1)
        self.segmen_tools.place(x=40, y=210)

        # taruh tombol reset
        self.reset_button = Button(self.kumpulan_fungsi, text="Reset", bg="white", fg="firebrick3",
                                   font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.fungsi(7))
        self.reset_button.place(x=15, y=250)

        # taruh tombol milih warna fill
        self.milih_warna_fill = Button(self.kumpulan_fungsi, text="Fill clr", bg="white", fg="firebrick3",
                                       font=("Arial", 10, "bold"), relief=RAISED, bd=3,
                                       command=lambda: self.warna_fill())
        self.milih_warna_fill.place(x=72, y=250)

        # taruh tombol milih warna outline
        self.milih_warna_outline = Button(self.kumpulan_fungsi, text="Outline clr", bg="white", fg="firebrick3",
                                          font=("Arial", 10, "bold"), relief=RAISED, bd=3,
                                          command=lambda: self.warna_outline())
        self.milih_warna_outline.place(x=135, y=250)

        # segmen refleksi
        self.segmen_refleksi = Label(self.kumpulan_fungsi, text="Refleksi", bg="SteelBlue1", fg="firebrick2",
                                     font=("Arial", 12, "bold"), relief=GROOVE, bd=1, padx=10, pady=1)
        self.segmen_refleksi.place(x=72, y=295)

        # taruh tombol refleksi_x
        self.refleksi_x = Button(self.kumpulan_fungsi, text="Refleksi X", bg="white", fg="firebrick3",
                                 font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.refleksikan_x())
        self.refleksi_x.place(x=30, y=328)

        # taruh tombol refleksi_y
        self.refleksi_y = Button(self.kumpulan_fungsi, text="Refleksi Y", bg="white", fg="firebrick3",
                                 font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.refleksikan_y())
        self.refleksi_y.place(x=120, y=328)

        # Pergerakan objek
        self.window.bind('<space>', self.pergerakan)
        self.window.bind('<Left>', self.pergerakan)
        self.window.bind('<Right>', self.pergerakan)
        self.window.bind('<Up>', self.pergerakan)
        self.window.bind('<Down>', self.pergerakan)

    def movement_cursor(self, e):  # For cursor position by movement
        self.koordinat.config(text=str(e.x) + "," + str(e.y) + "px")

    def make_status_bar(self):  # Make status bar
        self.status_fungsi = Label(self.window, text="Grafkom", fg="#292929",
                                   font=("Arial", 12, "bold"))
        self.status_fungsi.place(x=1150, y=690)

        self.koordinat = Label(self.window, text="", fg="#292929", font=("Arial", 9, "bold"))
        self.koordinat.place(x=20, y=690)

    def pakai_pensil(self, e):
        self.status_fungsi['text'] = "Gambar pakai pensil"
        self.status_fungsi.place(x=1130, y=685)

        if self.x_lama and self.y_lama:
            take = self.canvas.create_line(self.x_lama, self.y_lama, e.x, e.y, fill=self.fill_color_line,
                                           width=self.width_maintainer, smooth=True, capstyle=ROUND)
            self.temp.append(take)
        self.x_lama = e.x
        self.y_lama = e.y

        def push_value(e):
            self.tempat_undo.append(self.temp)
            self.notation_box.insert(END,
                                     len(self.tempat_undo) - 1)  # END buat Taruh di index paling terakhir, len -1 buat ngasih nomernya
            self.reset()

        self.canvas.bind("<ButtonRelease-1>", push_value)

    def buat_lingkaran(self, e):
        self.status_fungsi['text'] = "Buat Lingkaran"
        self.status_fungsi.place(x=1130, y=685)

        if self.x_lama and self.y_lama:
            take = self.canvas.create_oval(self.x_lama, self.y_lama, e.x, e.y, width=self.width_maintainer,
                                           outline=self.outline_color_line, fill=self.fill_color)
            self.temp.append(take)
        else:
            self.x_lama = e.x
            self.y_lama = e.y

        def circle_make(e):
            for x in self.temp:
                self.canvas.delete(x)
            try:
                koordinatnya = [self.x_lama, self.y_lama, e.x, e.y]
                ambil = self.canvas.create_oval(self.x_lama, self.y_lama, e.x, e.y,
                                                width=self.width_maintainer,
                                                fill=self.fill_color, outline=self.outline_color_line)
                self.simpan_koordinat[ambil] = koordinatnya, 'lingkaran'
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()

            except:
                print("Error: click only not motion")

        self.canvas.bind('<ButtonRelease-1>', circle_make)

    def buat_kotak(self, e):
        self.status_fungsi['text'] = "Buat Persegi"
        self.status_fungsi.place(x=1130, y=685)

        if self.x_lama and self.y_lama:
            take = self.canvas.create_rectangle(self.x_lama, self.y_lama, e.x, e.y, width=self.width_maintainer,
                                                fill=self.fill_color, outline=self.outline_color_line)
            self.temp.append(take)
        else:
            self.x_lama = e.x
            self.y_lama = e.y

        def rectangle_make(e):
            for x in self.temp:
                self.canvas.delete(x)
            try:
                koordinatnya = [self.x_lama, self.y_lama, e.x, e.y]
                ambil = self.canvas.create_rectangle(self.x_lama, self.y_lama, e.x, e.y, width=self.width_maintainer,
                                                     fill=self.fill_color, outline=self.outline_color_line)
                self.simpan_koordinat[ambil] = koordinatnya, 'persegi'
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()
            except:
                print("Error: click only not motion")

        self.canvas.bind('<ButtonRelease-1>', rectangle_make)

    def buat_segitiga(self, e):
        self.status_fungsi['text'] = "Buat Segitiga"
        self.status_fungsi.place(x=1130, y=685)

        if self.x_lama and self.y_lama:
            take = self.canvas.create_polygon(self.x_lama, self.y_lama, self.x_lama - (e.x - self.x_lama), e.y, e.x,
                                              e.y,
                                              width=self.width_maintainer, fill=self.fill_color,
                                              outline=self.outline_color_line)
            self.temp.append(take)
        else:
            self.x_lama = e.x
            self.y_lama = e.y

        def triangle_make(e):
            for x in self.temp:
                self.canvas.delete(x)
            try:
                koordinatnya = [self.x_lama, self.y_lama, e.x, e.y]
                ambil = self.canvas.create_polygon(self.x_lama, self.y_lama, self.x_lama - (e.x - self.x_lama), e.y,
                                                   e.x, e.y,
                                                   width=self.width_maintainer, fill=self.fill_color,
                                                   outline=self.outline_color_line)
                self.simpan_koordinat[ambil] = koordinatnya, "segitiga"
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()
            except:
                print("Error: click only not motion")

        self.canvas.bind('<ButtonRelease-1>', triangle_make)

    def garis_sembarang(self, e):
        self.status_fungsi['text'] = "Buat Garis"
        self.status_fungsi.place(x=1130, y=685)

        if self.x_lama and self.y_lama:
            take = self.canvas.create_line(self.x_lama, self.y_lama, e.x, e.y, width=self.width_maintainer,
                                           fill=self.fill_color_line)
            self.temp.append(take)
        else:
            self.x_lama = e.x
            self.y_lama = e.y

        def buat_garis(e):
            for x in self.temp:
                self.canvas.delete(x)
            try:
                koordinatnya = [self.x_lama, self.y_lama, e.x, e.y]
                ambil = self.canvas.create_line(self.x_lama, self.y_lama, e.x, e.y, width=self.width_maintainer,
                                                fill=self.fill_color_line)
                self.simpan_koordinat[ambil] = koordinatnya, 'garis_r'
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()
            except:
                print("Error: click only not motion")

        self.canvas.bind('<ButtonRelease-1>', buat_garis)

    def garis_lurus(self, e):
        self.status_fungsi['text'] = "Buat Garis Lurus"
        self.status_fungsi.place(x=1130, y=685)
        status = ""
        if self.x_lama and self.y_lama:
            if abs(e.x - self.x_lama) > abs(e.y - self.y_lama):  # ngecek apakah horizontal
                take = self.canvas.create_line(self.x_lama, self.y_lama, e.x, self.y_lama,
                                               width=self.width_maintainer, fill=self.fill_color_line)
                self.temp.append(take)
                status = "horizontal"
            else:  # ini vertikal;
                take = self.canvas.create_line(self.x_lama, self.y_lama, self.x_lama, e.y,
                                               width=self.width_maintainer, fill=self.fill_color_line)
                self.temp.append(take)
                status = "vertikal"
        else:
            self.x_lama = e.x
            self.y_lama = e.y

        def buat_garis(e):
            for x in self.temp:
                self.canvas.delete(x)
            try:
                if status == 'horizontal':
                    koordinatnya = [self.x_lama, self.y_lama, self.x_lama, e.y]
                    ambil = self.canvas.create_line(self.x_lama, self.y_lama, e.x, self.y_lama,
                                                    width=self.width_maintainer, fill=self.fill_color_line)
                else:
                    koordinatnya = [self.x_lama, self.y_lama, e.x, self.y_lama]
                    ambil = self.canvas.create_line(self.x_lama, self.y_lama, self.x_lama, e.y,
                                                    width=self.width_maintainer, fill=self.fill_color_line)
                self.simpan_koordinat[ambil] = koordinatnya, 'garis_l'
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()

            except:
                print("Error: click only not motion")

        self.canvas.bind('<Shift-ButtonRelease-1>', buat_garis)

    def refleksikan_x(self):
        try:
            self.status_fungsi['text'] = "Refleksi terhadap sumbu X"
            self.status_fungsi.place(x=1180, y=685)

            take = self.notation_box.get(ACTIVE)
            self.notation_box.config(state=DISABLED)
            take = self.tempat_undo[take]

            koordinatnya = self.simpan_koordinat[take]

            if koordinatnya[1] == 'persegi':
                if koordinatnya[0][1] < koordinatnya[0][3]:
                    x1 = koordinatnya[0][0]
                    y1 = koordinatnya[0][3] + 20
                    x2 = koordinatnya[0][2]
                    y2 = y1 + (koordinatnya[0][3] - koordinatnya[0][1])
                    ambil = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                         width=self.width_maintainer,
                                                         fill=self.fill_color, outline=self.outline_color_line)
                    self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'persegi'
                    self.notation_box.config(state=NORMAL)
                    self.tempat_undo.append(ambil)
                    self.notation_box.insert(END, len(self.tempat_undo) - 1)
                    self.reset()
                elif koordinatnya[0][1] > koordinatnya[0][3]:
                    x1 = koordinatnya[0][2]
                    y1 = koordinatnya[0][1] + 20
                    x2 = koordinatnya[0][0]
                    y2 = y1 + (koordinatnya[0][1] - koordinatnya[0][3])
                    ambil = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                         width=self.width_maintainer,
                                                         fill=self.fill_color, outline=self.outline_color_line)
                    self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'persegi'
                    self.notation_box.config(state=NORMAL)
                    self.tempat_undo.append(ambil)
                    self.notation_box.insert(END, len(self.tempat_undo) - 1)
                    self.reset()

            elif koordinatnya[1] == 'segitiga':
                if koordinatnya[0][1] > koordinatnya[0][3]:  # ujung dibawah alas diatas
                    x1 = koordinatnya[0][0]
                    y1 = koordinatnya[0][1] + 20
                    x2 = koordinatnya[0][2]
                    y2 = y1 + (koordinatnya[0][1] - koordinatnya[0][3])
                    x3 = x1 - (x2 - x1)
                    y3 = y2
                    ambil = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, width=self.width_maintainer,
                                                       fill=self.fill_color,
                                                       outline=self.outline_color_line)
                    self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'segitiga'
                    self.notation_box.config(state=NORMAL)
                    self.tempat_undo.append(ambil)
                    self.notation_box.insert(END, len(self.tempat_undo) - 1)
                    self.reset()
                elif koordinatnya[0][1] < koordinatnya[0][3]:  # ujung diatas alas dibawah
                    x1 = koordinatnya[0][0]
                    y1 = koordinatnya[0][3] + 20 + (koordinatnya[0][3] - koordinatnya[0][1])
                    x2 = koordinatnya[0][2]
                    y2 = koordinatnya[0][3] + 20
                    x3 = x1 - (x2 - x1)
                    y3 = y2
                    ambil = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, width=self.width_maintainer,
                                                       fill=self.fill_color,
                                                       outline=self.outline_color_line)
                    self.simpan_koordinat[ambil] = [x1, y1, x3, y3], 'segitiga'
                    self.notation_box.config(state=NORMAL)
                    self.tempat_undo.append(ambil)
                    self.notation_box.insert(END, len(self.tempat_undo) - 1)
                    self.reset()
            elif koordinatnya[1] == 'lingkaran':
                if koordinatnya[0][1] < koordinatnya[0][3]:
                    x1 = koordinatnya[0][0]
                    y1 = koordinatnya[0][3] + 20
                    x2 = koordinatnya[0][2]
                    y2 = y1 + (koordinatnya[0][3] - koordinatnya[0][1])
                    ambil = self.canvas.create_oval(x1, y1, x2, y2,
                                                    width=self.width_maintainer,
                                                    fill=self.fill_color, outline=self.outline_color_line)
                    self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'lingkaran'
                    self.notation_box.config(state=NORMAL)
                    self.tempat_undo.append(ambil)
                    self.notation_box.insert(END, len(self.tempat_undo) - 1)
                    self.reset()
                elif koordinatnya[0][1] > koordinatnya[0][3]:
                    x1 = koordinatnya[0][2]
                    y1 = koordinatnya[0][1] + 20
                    x2 = koordinatnya[0][0]
                    y2 = y1 + (koordinatnya[0][1] - koordinatnya[0][3])
                    ambil = self.canvas.create_oval(x1, y1, x2, y2,
                                                         width=self.width_maintainer,
                                                         fill=self.fill_color, outline=self.outline_color_line)
                    self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'lingkaran'
                    self.notation_box.config(state=NORMAL)
                    self.tempat_undo.append(ambil)
                    self.notation_box.insert(END, len(self.tempat_undo) - 1)
                    self.reset()

        except:
            print("Error: Nothing selected from indexing box")

    def refleksikan_y(self):
        self.status_fungsi['text'] = "Refleksi terhadap sumbu Y"
        self.status_fungsi.place(x=1180, y=685)

        take = self.notation_box.get(ACTIVE)
        self.notation_box.config(state=DISABLED)
        take = self.tempat_undo[take]

        koordinatnya = self.simpan_koordinat[take]

        if koordinatnya[1] == 'persegi':
            if koordinatnya[0][0] < koordinatnya[0][2]:
                x1 = koordinatnya[0][2] + 20
                y1 = koordinatnya[0][1]
                x2 = x1 + (koordinatnya[0][2] - koordinatnya[0][0])
                y2 = koordinatnya[0][3]
                ambil = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                     width=self.width_maintainer,
                                                     fill=self.fill_color, outline=self.outline_color_line)
                self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'persegi'
                self.notation_box.config(state=NORMAL)
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()
            elif koordinatnya[0][0] > koordinatnya[0][2]:
                x1 = koordinatnya[0][0] + 20
                y1 = koordinatnya[0][3]
                x2 = x1 + (koordinatnya[0][0] - koordinatnya[0][2])
                y2 = koordinatnya[0][1]

                ambil = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                     width=self.width_maintainer,
                                                     fill=self.fill_color, outline=self.outline_color_line)
                self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'persegi'
                self.notation_box.config(state=NORMAL)
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()

        elif koordinatnya[1] == 'segitiga':
            if koordinatnya[0][0] > koordinatnya[0][2]:  # ujung dibawah alas diatas
                x1 = koordinatnya[0][0] + (koordinatnya[0][0] - koordinatnya[0][2]) + 20 + (koordinatnya[0][0] - koordinatnya[0][2])
                y1 = koordinatnya[0][1]
                x2 = x1 + (koordinatnya[0][0] - koordinatnya[0][2])
                y2 = koordinatnya[0][3]
                x3 = x1 - (x2 - x1)
                y3 = y2
                ambil = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, width=self.width_maintainer,
                                                   fill=self.fill_color,
                                                   outline=self.outline_color_line)
                self.simpan_koordinat[ambil] = [x1, y1, x3, y3], 'segitiga'
                self.notation_box.config(state=NORMAL)
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()
            elif koordinatnya[0][0] < koordinatnya[0][2]:  # ujung diatas alas dibawah
                x1 = koordinatnya[0][2] + 20 + (koordinatnya[0][2]-koordinatnya[0][0])
                y1 = koordinatnya[0][1]
                x2 = koordinatnya[0][2] + 20
                y2 = koordinatnya[0][3]
                x3 = x1 - (x2 - x1)
                y3 = y2
                ambil = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, width=self.width_maintainer,
                                                   fill=self.fill_color,
                                                   outline=self.outline_color_line)
                self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'segitiga'
                self.notation_box.config(state=NORMAL)
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()
        elif koordinatnya[1] == 'lingkaran':
            if koordinatnya[0][0] < koordinatnya[0][2]:
                x1 = koordinatnya[0][2] + 20
                y1 = koordinatnya[0][1]
                x2 = x1 + (koordinatnya[0][2] - koordinatnya[0][0])
                y2 = koordinatnya[0][3]
                ambil = self.canvas.create_oval(x1, y1, x2, y2,
                                                     width=self.width_maintainer,
                                                     fill=self.fill_color, outline=self.outline_color_line)
                self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'lingkaran'
                self.notation_box.config(state=NORMAL)
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()
            elif koordinatnya[0][0] > koordinatnya[0][2]:
                x1 = koordinatnya[0][0] + 20
                y1 = koordinatnya[0][3]
                x2 = x1 + (koordinatnya[0][0] - koordinatnya[0][2])
                y2 = koordinatnya[0][1]

                ambil = self.canvas.create_oval(x1, y1, x2, y2,
                                                     width=self.width_maintainer,
                                                     fill=self.fill_color, outline=self.outline_color_line)
                self.simpan_koordinat[ambil] = [x1, y1, x2, y2], 'lingkaran'
                self.notation_box.config(state=NORMAL)
                self.tempat_undo.append(ambil)
                self.notation_box.insert(END, len(self.tempat_undo) - 1)
                self.reset()

    def pergerakan(self, e):
        try:
            self.status_fungsi['text'] = "Movement"
            self.status_fungsi.place(x=1180, y=685)
            take = self.notation_box.get(ACTIVE)
            self.notation_box.config(state=DISABLED)
            take = self.tempat_undo[take]
            if e.keycode == 32:  # spasi
                self.notation_box.config(state=NORMAL)
            if e.keycode == 37:  # arrow left
                if type(take) == list:
                    for x in take:
                        self.canvas.move(x, -5, 0)
                else:
                    self.canvas.move(take, -5, 0)
            if e.keycode == 38:  # arrow down
                if type(take) == list:
                    for x in take:
                        self.canvas.move(x, 0, -5)
                else:
                    self.canvas.move(take, 0, -5)
            if e.keycode == 39:  # arrow right
                if type(take) == list:
                    for x in take:
                        self.canvas.move(x, 5, 0)
                else:
                    self.canvas.move(take, 5, 0)
            if e.keycode == 40:  # arrow up
                if type(take) == list:
                    for x in take:
                        self.canvas.move(x, 0, 5)
                else:
                    self.canvas.move(take, 0, 5)
        except:
            print("Error: Nothing selected from indexing box")

    def width_controller(self):
        self.frame_width = Frame(self.kumpulan_fungsi, relief=GROOVE, bd=5, width=10, height=10, bg="chocolate")
        self.frame_width.place(x=10, y=370)

        def shape_outline_width_controller(e):  # Shape Border Width Controller
            self.width_maintainer = e

        self.shape_outline_width_label = Label(self.frame_width, text="Outline Width", font=("Arial", 12, "bold"),
                                               bg="chocolate", fg="yellow", padx=20)
        self.shape_outline_width_label.pack(pady=4)

        self.width_controller_scale = Scale(self.frame_width, orient=HORIZONTAL, from_=0, to=30, bg="green",
                                            fg="yellow", font=("Arial", 8, "bold"), relief=RAISED, bd=3,
                                            command=shape_outline_width_controller, activebackground="red")
        self.width_controller_scale.set(self.width_maintainer)
        self.width_controller_scale.pack(pady=7)

    def zoom_controller(self, e):
        self.status_fungsi['text'] = "Zoom Controller"
        self.status_fungsi.place(x=1180, y=685)
        try:
            if e.delta > 0:
                self.canvas.scale("all", e.x, e.y, 1.1, 1.1)
            elif e.delta < 0:
                self.canvas.scale("all", e.x, e.y, 0.9, 0.9)
        except:
            if e == 1:
                self.canvas.scale("all", 550, 350, 1.1, 1.1)
            else:
                self.canvas.scale("all", 550, 350, 0.9, 0.9)

    def reset(self):  # Reset
        print(self.simpan_koordinat)
        self.status_fungsi['text'] = "Grafkom"
        self.status_fungsi.place(x=1140, y=690)
        if self.notation_box['state'] == DISABLED:
            self.notation_box['state'] = NORMAL
        self.x_baru = None
        self.y_baru = None
        self.x_lama = None
        self.y_lama = None
        self.temp = []


if __name__ == "__main__":
    window = Tk()
    window.geometry("1350x730")
    window.maxsize(1350, 712)
    window.minsize(1350, 712)
    p = Paint(window)
    window.mainloop()
