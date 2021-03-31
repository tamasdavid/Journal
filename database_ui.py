from tkinter import *
from tkinter import ttk
import log_interface


class DatabaseUi:
    def __init__(self):
        self.window = Tk()

        #positioning the window in the middle of the screen
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_heigth = self.window.winfo_screenheight()
        self.width = 580
        self.heigth = 390
        self.x_coor = int((self.screen_width / 2) - (self.width / 2))
        self.y_coor = int((self.screen_heigth / 2) - (self.heigth / 2))
        self.window.config(padx=20, pady=5)
        self.window.geometry(f"{self.width}x{self.heigth}+{self.x_coor}+{self.y_coor}")
        self.window.resizable(0, 0)

        #creating  treeview and adding the scrollbar
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",
                             backgroud="#D3D3D3",
                             foreground="black",
                             rowheigth=25,
                             fieldbackground="#D3D3D3")
        self.style.map("Treeview",
                       background=[("selected", "#347083")])
        self.treeview_frame = Frame()
        self.treeview_frame.grid(row=1, column=0, padx=10, sticky="ne")
        self.treeview_scroll = Scrollbar(self.treeview_frame)
        self.treeview_scroll.pack(side=RIGHT, fill=Y)
        self.tree_view = ttk.Treeview(self.treeview_frame, yscrollcommand=self.treeview_scroll.set,
                                      selectmode="extended")
        self.tree_view.pack()
        self.treeview_scroll.config(command=self.tree_view.yview)
        self.tree_view["columns"] = ("First Name", "Last Name", "Date", "Title")

        self.tree_view.column("#0", width=0, stretch=NO)
        self.tree_view.column("First Name", anchor=W, width=140)
        self.tree_view.column("Last Name", anchor=W, width=140)
        self.tree_view.column("Date", anchor=CENTER, width=140)
        self.tree_view.column("Title", anchor=CENTER, width=100)

        self.tree_view.heading("#0", text="", anchor=W)
        self.tree_view.heading("First Name", text="First Name", anchor=W)
        self.tree_view.heading("Last Name", text="Last Name", anchor=W)
        self.tree_view.heading("Date", text="Date", anchor=CENTER)
        self.tree_view.heading("Title", text="Title", anchor=CENTER)
        #creating search option

        self.search_frame = LabelFrame(text="Search", font=("Calibri", 11))
        self.search_frame.grid(row=2, column=0, pady=20)

        self.date_label = Label(self.search_frame, text="Date", font=("Calibri", 11))
        self.date_label.grid(row=0, column=0, pady=5)
        self.title_label = Label(self.search_frame, text="Title", font=("Calibri", 11))
        self.title_label.grid(row=1, column=0, pady=5)

        self.date_entry = Entry(self.search_frame, font=("Calibri", 11))
        self.date_entry.grid(row=0, column=1, padx=10)
        self.title_entry = Entry(self.search_frame, font=("Calibri", 11))
        self.title_entry.grid(row=1, column=1, padx=10, pady=5)

        self.date_search_btn = Button(self.search_frame, text="Search by Date", font=("Calibri", 11))
        self.date_search_btn.grid(row=0, column=2, padx=10)
        self.title_search_btn = Button(self.search_frame, text="Search by Title", font=("Calibri", 11))
        self.title_search_btn.grid(row=1, column=2, padx=10)

        #creating a back to the journal button
        self.journal_btn = Button(text="Go to Journal", width=10, command=self.go_to_journal)
        self.journal_btn.grid(row=0, column=0, padx=7, pady=5, sticky=W)

        self.window.mainloop()

    def go_to_journal(self):
        self.window.destroy()
        log_interface.Log()


#s = DatabaseUi()
