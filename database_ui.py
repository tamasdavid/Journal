from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import date
from os import path
from tkinter import messagebox


class DatabaseUi:

    def __init__(self):
        self.window = Tk()
        self.window.title("Database")
        # positioning the window in the middle of the screen
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.width = 580
        self.height = 390
        self.x_coor = int((self.screen_width / 2) - (self.width / 2))
        self.y_coor = int((self.screen_height / 2) - (self.height / 2))
        self.window.config(padx=20, pady=5)
        self.window.geometry(f"{self.width}x{self.height}+{self.x_coor}+{self.y_coor}")
        self.window.resizable(0, 0)

        # creating  treeview and adding the scrollbar
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",
                             backgroud="#D3D3D3",
                             foreground="black",
                             rowheigth=25,
                             fieldbackground="#D3D3D3")
        self.style.map("Treeview",
                       background=[("selected", "#347083")])
        self.tree_view_frame = Frame()
        self.tree_view_frame.grid(row=1, column=0, padx=10, sticky="ne")
        self.treeview_scroll = Scrollbar(self.tree_view_frame)
        self.treeview_scroll.pack(side=RIGHT, fill=Y)
        self.tree_view = ttk.Treeview(self.tree_view_frame, yscrollcommand=self.treeview_scroll.set,
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

        # creating the stiped row tags
        self.tree_view.tag_configure("orddrow", background="white")
        self.tree_view.tag_configure("evenrow", background="lightblue")
        # binding double click for tree view to open the content of it
        self.tree_view.bind("<Double-1>", self.just_open)

        # creating search option
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

        self.date_search_btn = Button(self.search_frame, text="Search by Date", font=("Calibri", 11),
                                      command=self.search_by_date)
        self.date_search_btn.grid(row=0, column=2, padx=10)
        self.title_search_btn = Button(self.search_frame, text="Search by Title", font=("Calibri", 11),
                                       command=self.search_by_title)
        self.title_search_btn.grid(row=1, column=2, padx=10)

        # creating a back to the journal button
        self.journal_btn = Button(text="Go to Journal", width=10, command=self.go_to_journal)
        self.journal_btn.grid(row=0, column=0, padx=7, pady=5, sticky=W)

        self.content = []
        self.chosen_text = ""
        self.add_data_to_treeview()
        self.window.mainloop()

    def go_to_journal(self):
        self.window.destroy()
        Journal()

    def add_data_to_treeview(self):
        try:
            self.db_connection = sqlite3.connect("journal.db")
            self.db_cursor = self.db_connection.cursor()
            self.db_cursor.execute("SELECT *, oid FROM journal")
            self.records = self.db_cursor.fetchall()

        except sqlite3.OperationalError:
            pass

        else:
            self.count = 0
            for self.record in self.records:
                self.content.append(self.record)

            for self.rec in self.content:
                if self.count % 2 == 0:
                    self.tree_view.insert(parent="", index="end", iid=self.count, text="",
                                          values=(self.content[self.count][0], self.content[self.count][1],
                                                  self.content[self.count][2], self.content[self.count][3]),
                                          tags=("evenrow",))

                else:
                    self.tree_view.insert(parent="", index="end", iid=self.count, text="",
                                          values=(self.content[self.count][0], self.content[self.count][1],
                                                  self.content[self.count][2], self.content[self.count][3]),
                                          tags=("oddrow",))
                self.count += 1

    def search_by_date(self):
        # looping trough the list and matching the date with the tuple item and displaying in the tree view
        for self.search_tuple in self.content:
            if self.date_entry.get() == self.search_tuple[2]:
                for self.item in self.tree_view.get_children():
                    self.tree_view.delete(self.item)
                self.tree_view.insert(parent="", index="end", iid=0, text="", values=(self.search_tuple[0],
                                                                                      self.search_tuple[1],
                                                                                      self.search_tuple[2],
                                                                                      self.search_tuple[3]))

    def search_by_title(self):
        # looping trough the list and matching the title with the tuple item and displaying in the tree view
        for self.search_tuple in self.content:
            if self.title_entry.get().capitalize() == self.search_tuple[3]:
                self.title_entry.delete(0, END)
                for self.item in self.tree_view.get_children():
                    self.tree_view.delete(self.item)
                self.tree_view.insert(parent="", index="end", iid=0, text="", values=(self.search_tuple[0],
                                                                                     self.search_tuple[1],
                                                                                     self.search_tuple[2],
                                                                                     self.search_tuple[3]))

    def just_open(self, event):
        self.current_item = self.tree_view.focus()
        self.chosen = self.tree_view.item(self.current_item, "values")
        for self.search_tup in self.content:
            # if there is a match creating a new window to display the journal content
            if self.chosen[3] == self.search_tup[3]:
                self.chosen_text = self.search_tup[4]

                self.data_gui = Toplevel()
                self.data_gui.title("Read the journal")
                self.data_gui.config(padx=10)
                self.height = 445
                self.data_gui.geometry(f"{self.width}x{self.height}+{self.x_coor}+{self.y_coor}")

                self.back_btn = Button(self.data_gui, text="Back", width=10, command=lambda:self.data_gui.destroy())
                self.back_btn.grid(row=0, column=0, pady=10, sticky="w")

                self.data_gui_frame = Frame(self.data_gui)
                self.data_gui_frame.grid(row=1, column=0)

                self.data_gui_txt_box_scroll = Scrollbar(self.data_gui_frame)
                self.data_gui_txt_box = Text(self.data_gui_frame, width=65, yscrollcommand=self.data_gui_txt_box_scroll.set)
                self.data_gui_txt_box.insert("1.0", self.chosen_text)
                self.data_gui_txt_box_scroll.config(command=self.data_gui_txt_box.yview)
                self.data_gui_txt_box_scroll.grid(row=0, column=1, sticky="nsew")
                self.data_gui_txt_box.grid(row=0, column=0)




class Journal():
    def __init__(self):
        self.today = date.today().strftime("%d-%m-%y")
        self.window = Tk()
        self.window.title("Journal")
        self.window.config(padx=10, pady=20)
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_heigth = self.window.winfo_screenheight()
        self.width = 900
        self.heigth = 580
        self.x_coor = int((self.screen_width / 2) - (self.width / 2))
        self.y_coor = int((self.screen_heigth / 2) - (self.heigth / 2))
        self.window.geometry(f"{self.width}x{self.heigth}+{self.x_coor}+{self.y_coor}")
        self.window.resizable(0, 0)

        # adding a scrollbar
        self.journal_scrollbar = Scrollbar(orient=VERTICAL)
        self.journal_box = Text(width=int(self.width / 8.4), yscrollcommand=self.journal_scrollbar.set)
        self.journal_box.focus()
        self.journal_scrollbar.config(command=self.journal_box.yview)
        self.journal_scrollbar.grid(row=0, column=1, sticky='nsew')
        self.journal_box.grid(row=0, column=0)

        # adding file dropdown menu
        self.menu = Menu()
        self.window.config(menu=self.menu)

        self.submenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.submenu)
        self.submenu.add_command(label="Back to Database", command=self.call_database)

        # adding  the save entries and buttons
        self.save_frame = LabelFrame(text="Save", font=("Calibri", 11))
        self.save_frame.grid(row=1, column=0, pady=20)

        self.f_name_label = Label(self.save_frame, text="First Name", font=("Calibri", 11))
        self.f_name_label.grid(row=0, column=0)
        self.l_name_label = Label(self.save_frame, text="Last Name", font=("Calibri", 11))
        self.l_name_label.grid(row=0, column=2)
        self.date_label = Label(self.save_frame, text="Date", font=("Calibri", 11))
        self.date_label.grid(row=1, column=0)
        self.title_label = Label(self.save_frame, text="Title", font=("Calibri", 11))
        self.title_label.grid(row=1, column=2)

        self.f_name_entry = Entry(self.save_frame, font=("Calibri", 11))
        self.f_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.l_name_entry = Entry(self.save_frame, font=("Calibri", 11))
        self.l_name_entry.grid(row=0, column=3, padx=10, pady=5)
        self.date_entry = Entry(self.save_frame, font=("Calibri", 11))
        self.date_entry.insert(0, self.today)
        self.date_entry.grid(row=1, column=1, padx=10, pady=5)
        self.title_entry = Entry(self.save_frame, font=("Calibri", 11))
        self.title_entry.grid(row=1, column=3, padx=10, pady=5)

        self.save_btn = Button(self.save_frame, text="Save", width=15, command=self.saving_to_database)
        self.save_btn.grid(row=3, column=1, columnspan=2, pady=5, sticky=E)

        self.window.mainloop()

    def call_database(self):
        self.window.destroy()
        DatabaseUi()

    # creating or saving information to the database
    def saving_to_database(self):
        if len(self.f_name_entry.get()) ==0 or len(self.l_name_entry.get()) == 0 or \
                len(self.title_entry.get()) == 0:
            messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        else:
            if path.exists("journal.db"):
                # connecting to the database
                self.db_connection = sqlite3.connect("journal.db")
                self.db_cursor = self.db_connection.cursor()
                self.db_cursor.execute("INSERT INTO journal VALUES (:f_name, :l_name, :date, :title, :journal_text)",
                                       {
                                           "f_name": self.f_name_entry.get(),
                                           "l_name": self.l_name_entry.get(),
                                           "date": self.date_entry.get(),
                                           "title": self.title_entry.get(),
                                           "journal_text": self.journal_box.get("1.0", "end-1c")
                                       })

                self.db_connection.commit()
                self.db_connection.close()

                self.f_name_entry.delete(0, END)
                self.l_name_entry.delete(0, END)
                self.title_entry.delete(0, END)
                self.journal_box.delete("1.0", "end-1c")

            else:
                #creating the database if it does not exist
                self.db_connection = sqlite3.connect("journal.db")
                self.db_cursor = self.db_connection.cursor()
                self.db_cursor.execute("""CREATE TABLE journal(
                                                  f_name text,
                                                  l_name text,
                                                  date text,
                                                  title text, 
                                                  journal_text text)""")
                self.db_connection.commit()
                self.db_connection.close()
                self.saving_to_database()


