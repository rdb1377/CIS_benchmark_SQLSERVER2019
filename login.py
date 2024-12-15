import ttkbootstrap as tk
from tkinter import messagebox
import admin
import instructor
from database import Database

import pyodbc
import tkinter.font as TkFont
import ttkbootstrap as ttk

# creating a database object
db = Database("mainDatabase.db")

class ConnectionString:
    def __init__(self, servername , username , password , authmethod , driver):
        self.servername = servername
        self.username = username
        self.password = password
        self.authmethod = authmethod
        self.driver = driver
        self.driver = driver

class Login:
    def __init__(self, root):
        self.root = root
        self.root.resizable(0, 0)


        self.servername = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.authMethod = tk.StringVar()
        self.driver = tk.StringVar()

        # Background Color
        self.root.config(bg="#110a4d")

        # Call the tkinter frame to the window
        self.loginControlFrame()

    """CTA Methods"""

    # login method to redirect to the next frames
    # def loginFunc(self):
    #     if self.username_entry.get() == 'admin' and self.password_entry.get() == 'admin':
    #         self.loginFrame.destroy()
    #         self.rightFrame.destroy()
    #         admin.AdminControls(self.root ,self.servername)
    #
    #     elif db.instructorLogin(self.username_entry.get(), self.password_entry.get()):
    #         self.loginFrame.destroy()
    #         self.rightFrame.destroy()
    #         instructor.InstructorControls(self.root)
    #     else:
    #         messagebox.showerror("Error!", "Check your credentials or Please Contact System Admin!")
    #         self.username.set("")
    #         self.password.set("")

    """Login Frame"""

    def loginControlFrame(self):
        # Login Frame Configurations
        self.loginFrame = tk.Frame(self.root)
        self.loginFrame.pack(side=tk.LEFT, fill=tk.X, padx=60)
        self.login_frame_title = tk.Label(self.loginFrame, text="Login Here", font=("Impact", 35))
        self.login_frame_title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")


        # Username
        self.username_label = tk.Label(self.loginFrame, text="Username", font=("Times New Roman", 16, "bold"))
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = tk.Entry(self.loginFrame, textvariable=self.username, font=("Times New Roman", 15), width=30)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Password
        self.password_label = tk.Label(self.loginFrame, text="Password", font=("Times New Roman", 16, "bold"))
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(self.loginFrame, textvariable=self.password, font=("Times New Roman", 15), width=30,  show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        #server
        self.server_label = tk.Label(self.loginFrame, text="Server Name:" ,font=("Times New Roman", 16, "bold"))
        self.server_label.grid(row=3, column=0, padx=10, pady=5,sticky="w")
        self.server_entry = tk.Entry(self.loginFrame, textvariable=self.servername , font=("Times New Roman", 15), width=30)
        self.server_entry.configure()
        self.server_entry.grid(row=3, column=1, padx=10, pady=5,sticky="w" )
        self.server_entry.bind('<KeyRelease>', lambda server_entry: disable_connect_btn())

        #auth
        self.auth_label = tk.Label(self.loginFrame, text="Authentication:" ,font=("Times New Roman", 16, "bold"))
        self.auth_label.grid(row=4, column=0, padx=10, pady=5,sticky="w")
        self.auth_combo = ttk.Combobox(self.loginFrame, textvariable=self.authMethod, state='readonly' , font=("Times New Roman", 15), width=30 )
        self.auth_combo['values'] = ['Windows Authetication', 'SQL Server Authetication']
        self.auth_combo.current(0)
        self.auth_combo.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.auth_combo.bind("<<ComboboxSelected>>",lambda event, entry=self.auth_combo: self.UserPassEnable(entry.get()))

        #driver
        driver_list = self.detect_driver()
        self.driver_label = tk.Label(self.loginFrame, text="Driver:", font=("Times New Roman", 16, "bold"))
        self.driver_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.driver_combo = ttk.Combobox(self.loginFrame, textvariable=self.driver, state='readonly' , font=("Times New Roman", 15), width=30)
        self.driver_combo['values'] = driver_list
        self.driver_combo.current(0)
        self.driver_combo.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Login Button
        self.connect_btn = tk.Button(self.loginFrame, command=lambda: self.connect(), text="Login", cursor="hand2",  width=10 , )
        self.connect_btn['state'] = 'disable'
        self.connect_btn.grid(row=6, column=1, padx=10, sticky="e")

        # empty label for spacing in grid
        self.emptyLabel = tk.Label(self.loginFrame, font=("Times New Roman", 16, "bold"))
        self.emptyLabel.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Right Side Frame as Welcome Message
        self.rightFrame = tk.Frame(self.root)
        self.rightFrame.pack(side=tk.RIGHT)

        # self.labelCompanyName = tk.Label(self.rightFrame, text="eee", font=("Goudy Old Style", 55),bg="#110a4d", fg="white")
        # self.labelCompanyName.grid(row=0, column=2, columnspan=2, padx=10)
        # self.labelDesc = tk.Label(self.rightFrame, text="", font=("Times New Roman", 25, "italic"), bg="#110a4d", fg="white")
        # self.labelDesc.grid(row=1, column=2, columnspan=2, padx=10, pady=6)

        def disable_connect_btn():
            if self.server_entry.get() != '':
                self.connect_btn['state'] = 'normal'
                #self.controller.label_change(PageOne)
            else:
                self.connect_btn['state'] = 'disabled'


    def detect_driver(self):
        driver_name = ''
        driver_names = [x for x in pyodbc.drivers() if x.endswith('for SQL Server')]

        if driver_names:
            driver_name = driver_names[0]

        if driver_name:
            conn_str = 'DRIVER={}; ...'.format(driver_name)

        else:
            print('(No suitable driver found. Cannot connect. please install driver 17 or 18.)')

        return driver_names

    def connect(self):
        server = self.servername.get()
        driver = self.driver.get()
        error = 0
        #
        # if self.authMethod.get() == 'Windows Authetication':
        #     cnxn = pyodbc.connect('DRIVER={'+driver+'};SERVER=' + server + ';Trusted_Connection={yes} ;TrustServerCertificate={yes};  NeedODBCTypesOnly=1 ')
        #
        #
        # elif self.authMethod.get() == 'SQL Server Authetication':
        #     username = self.username.get()
        #     password = self.password.get()

            # try:
            #     cnxn = pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+';UID='+username+';PWD='+ password)
            # except:
            #     self.password.set("")
            #     error = 1

        if not error:
            self.loginFrame.destroy()
            self.rightFrame.destroy()
            cnxn = ConnectionString(self.servername.get() , self.username.get() , self.password.get() ,self.authMethod.get(), self.driver.get() )
            admin.AdminControls(self.root, cnxn)


    def handle_sql_variant_as_string(value):
        print(value)
        return value.decode('utf-16le')
    def UserPassEnable(self, text):
        if  text == 'Windows Authetication':
            self.username_entry.config(state="disable")
            self.password_entry.config(state="disable")
        else :
            self.username_entry.config(state="normal")
            self.password_entry.config(state="normal")
