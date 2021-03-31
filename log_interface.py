from tkinter import *
from datetime import date
import database_ui
import sqlite3
from os import path
from tkinter import messagebox


class Log:
    def __init__(self):
        self.today = date.today().strftime("%d-%m-%y")
        self.window = Tk()
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
        self.log_scrollbar = Scrollbar(orient=VERTICAL)
        self.log_box = Text(width=int(self.width/8.4), yscrollcommand=self.log_scrollbar.set)
        self.log_box.focus()
        self.log_scrollbar.config(command=self.log_box.yview)
        self.log_scrollbar.grid(row=0, column=1, sticky='nsew')
        self.log_box.grid(row=0, column=0)

        #adding file dropdown menu
        self.menu = Menu()
        self.window.config(menu=self.menu)

        self.submenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.submenu)
        self.submenu.add_command(label="New File", command=self.call_database)

        # adding edit dropdown menu
        self.edit_menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Something")

        #adding  the save entries and buttons
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
        database_ui.DatabaseUi()

    #creating or saving information to the database
    def saving_to_database(self):
        if len(self.f_name_entry.get()) ==0 or len(self.l_name_entry.get()) == 0 or \
                len(self.title_entry.get()) == 0:
            messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        else:
            if path.exists("journal.db"):
                print("something")
                self.db_connection = sqlite3.connect("journal.db")
                self.db_cursor = self.db_connection.cursor()

            else:
                print("creating the db")
                self.db_connection = sqlite3.connect("journal.db")
                self.db_cursor = self.db_connection.cursor()
                self.db_cursor.execute("""CREATE TABLE journal(
                                                  first_name text,
                                                  last_name text,
                                                  date integer,
                                                  title text)""")
                self.db_connection.commit()
                self.db_connection.close()
                self.saving_to_database()









#ll = Log()
