import ttkbootstrap
import tkinter as tkinter
from  ttkbootstrap import *
# from tkinter import ttk
from database import Database
from tkinter import messagebox
import login
import sessions
from bench import Benchmarks
import ttkbootstrap.scrolled as st
from tkhtmlview import HTMLScrolledText
import ttkbootstrap as boot


import pyodbc

# creating a database object

db = Database("mainDatabase.db")

class AdminControls:
    def __init__(self, root, cnxn):
        self.root = root

        # local variables
        self.insName = StringVar()
        self.insGender = StringVar()
        self.danceStyles = StringVar()
        self.insTelNo = StringVar()
        self.hrRate = DoubleVar()
        self.avail = StringVar()
        self.uName = StringVar()
        self.pw = StringVar()
        self.database = StringVar()
        self.replaceName= StringVar()
        self.cnxn = cnxn



        # Call the tkinter frames to the window

        self.benchmark = Benchmarks(cnxn)
        self.tableOutputFrame()
        self.adminControlsFrame(cnxn)




    """Instructor Info Entries Frame"""


    def handle_sql_variant_as_string(value):
        print(value)
        return value.decode('utf-16le')
    def adminControlsFrame(self, cnxn):
        # Admin Control Frame Configurations

        self.entriesFrame = Frame(self.root)
        self.entriesFrame.place(x=0, y=420, width=1400, height=520)
        self.admin_frame_title = Label(self.entriesFrame, text="Description", font=("Goudy old style", 20))
        self.admin_frame_title.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        # Instructor Name
        # self.labelName = Label(self.entriesFrame, text="Description", font=("Times New Roman", 16, "bold"), bg="#110a4d",fg="white")
        # self.labelName.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        #self.txtName = st.ScrolledText(self.entriesFrame,  font=("Times New Roman", 16), width=40 , height=7 , relief=GROOVE , wrap= tkinter.WORD)
        self.txtName = HTMLScrolledText(self.entriesFrame  , html= '<html></html>' , height= 21 , width=100)
        #self.txtName.place(x=40, y=100, width=180, height=60)
        self.txtName.grid(row=1, column=0, padx=10, pady=5 ,sticky=W + N + S + E)

        # Instructor Gender
        self.labelAvail = Label(self.entriesFrame, text="Remediation", font=("Times New Roman", 16, "bold"))
        self.labelAvail.place(x= 850 , y = 80)
        self.comboAvail = st.ScrolledText(self.entriesFrame,  font=("Times New Roman", 16), width=40 , height=7 , relief=GROOVE , wrap= tkinter.WORD)
        self.comboAvail.grid(row=1, column=1, padx=10, pady=5, sticky="w")


    def getData(self, event):
        try:
            self.selectedRow = self.out.focus()
            self.selectedData = self.out.item(self.selectedRow)
            self.chosenRow = self.selectedData["values"]
            self.insName.set(self.chosenRow[1])
            self.txtName.delete('1.0', END)
            self.txtName.set_html(self.chosenRow[3])
            self.comboAvail.delete('1.0', END)
            self.comboAvail.insert(INSERT,self.chosenRow[5])

            self.insGender.set(self.chosenRow[2])
            self.danceStyles.set(self.chosenRow[3])
            self.insTelNo.set(self.chosenRow[4])
            self.hrRate.set(self.chosenRow[5])
            self.avail.set(self.chosenRow[6])
            self.selectDays(event)
            self.uName.set(self.chosenRow[8])
            self.pw.set(self.chosenRow[9])
        except IndexError as error:
            pass


    def selectDays(self, event):
        if self.comboAvail.get() == "NOT AVAILABLE":
            self.listDays.delete(0, END)
        else:
            self.listDays.delete(0, END)  # clearing existing entries before inserting
            for day in self.weekdays:
                self.listDays.insert(END, day)

    def getAvailableDays(self):
        self.availDays = []
        for day in self.listDays.curselection():
            # creating a string list from the chosen list indexes
            self.availDays.append(str(self.listDays.get(day)))
        return self.availDays

    """CTA Methods"""

    def addInstructor(self):
        if self.txtName.get() == "" or self.txtTelNo.get() == "" or self.comboAvail.get() == "" or self.comboStyle.get() == "" or self.txthrRate.get() == "" or self.comboGender.get() == "" or self.txtUsername.get() == "" or self.txtPassword.get() == "":
            messagebox.showerror("Error!", "Please fill all the fields!")
            return

        self.tempAvailDays = ', '.join(self.getAvailableDays())  # converting the list of Days into a string

        db.insertInstructor(self.txtName.get(), self.comboGender.get(), self.comboStyle.get(), self.txtTelNo.get(),
                            self.txthrRate.get(), self.comboAvail.get(), self.tempAvailDays,
                            self.txtUsername.get(), self.txtPassword.get())
        messagebox.showinfo("Success!", "Record Successfully Insertered!")
        self.resetForm()
        self.viewIndex()


    def runRemediation(self):
        try:
            print("1111111111" , self.chosenRow[0])
            print("@@@@@@@@@@@@@@",self.chosenRow[4])
            result = self.benchmark.runRemediation(self.chosenRow[4] , self.replaceName)
            if (result == 0):
                messagebox.showerror("warning!","manual rem")

        except AttributeError as error:
            messagebox.showerror("Error!", "Please Choose a Row")



    # Method to display all instructors in the Treeview Frame
    def viewIndex(self):
        self.out.delete(*self.out.get_children())  # emptying the table before reloading
        for row in self.benchmark.view():
            self.out.insert("", END, values=row, tags=row[2] )

    # Method to direct to the next Frame to Assign Instructors
    def manageSessions(self):
        self.entriesFrame.destroy()
        self.buttonsFrame.destroy()
        self.tableFrame.destroy()
        sessions.AssignSession(self.root , self.cnxn)

    # Method to reset all input widgets in the frame
    def resetForm(self):
        self.insName.set("")
        self.insGender.set("")
        self.danceStyles.set("")
        self.insTelNo.set("")
        self.hrRate.set("")
        self.avail.set("")
        self.listDays.delete(0, END)
        self.uName.set("")
        self.pw.set("")

    # Method to redirect to the login frame
    def logOut(self):
        self.entriesFrame.destroy()
        self.buttonsFrame.destroy()
        self.tableFrame.destroy()
        login.Login(self.root)

    """CTA Buttons Frame"""

    def adminFrameButtons(self):
        # Button Frame Configurations
        self.buttonsFrame = Frame(self.entriesFrame)
        self.buttonsFrame.grid(row=10, column=0, padx=10, pady=10, sticky="w", columnspan=8)

        self.btnDlt = Button(self.buttonsFrame, command=self.runRemediation, text="Run Remediation ",cursor="hand2", width=20)
        self.btnDlt.grid(row=0, column=2, padx=10)

        # Display List
        self.btnView = Button(self.buttonsFrame, command=self.viewIndex, text="View List",cursor="hand2", width=20)

        # LogOut
        self.btnLogOut = Button(self.buttonsFrame, command=self.logOut, text="Log Out", cursor="hand2", width=15)
        self.btnLogOut.grid(row=0, column=6, padx=15, sticky="e")

    """Table Frame using TreeView"""

    def print_element(event):
        print("$$$$$$$$$$$$$$$$$$$$$$")
        tree = event.widget
        selection = [tree.item(item)["text"] for item in tree.selection()]
        print("selected items:", selection)
    def tableOutputFrame(self):
        # Treeview Frame Configurations
        self.tableFrame = Frame(self.root)
        self.tableFrame.place(x=0, y=0, width=1400, height=520)
        self.yScroll = Scrollbar(self.tableFrame)
        self.yScroll.pack(side=RIGHT, fill=Y)

        # ttk style object to add configurations
        self.style = boot.Style()
        self.style.configure("mystyle.Treeview", font=('Calibri', 12),
                             rowheight=50)
        self.style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky="w")

        # Formatting the output table view
        self.out = boot.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set,
                                 columns=(1, 2 ,3), style="mystyle.Treeview")
        self.out.tag_configure('1', background='lightgreen')
        self.out.tag_configure('0', background='pink')

        #self.out.bind("<<TreeviewSelect>>", self.print_element)


        self.out.heading("1", text="Index")
        self.out.column("1",anchor=CENTER, stretch=NO, width=100)
        self.out.heading("2", text="Name")
        self.out.column("2",anchor=CENTER, stretch=NO, width=700)
        self.out.heading("3", text="result")
        self.out.column("3", anchor=CENTER, stretch=NO,width=100)

        self.out['show'] = 'headings'

        # Virtual Events to trigger methods
        self.out.bind("<ButtonRelease-1>", self.getData)
        # self.comboAvail.bind("<<ComboboxSelected>>", self.selectDays)

        # TreeView output layout configurations
        self.out.place(relx=0.3, rely=0.01,width=950 , height=400)
        self.yScroll.config(command=self.out.yview)

        self.LabelDatabase = Label(self.tableFrame, text="database", font=("Times New Roman", 16, "bold"))
        self.LabelDatabase.place(relx=0.01 , rely= 0.03)

        res = self.benchmark.get_databases()
        self.databases_combo = boot.Combobox(self.tableFrame, textvariable=self.database, font=("Times New Roman", 15), width=28, state="readonly")
        self.databases_combo['values'] = res
        self.databases_combo.bind("<<ComboboxSelected>>",lambda event, entry=self.databases_combo: self.benchmark.buildCNXN(entry.get()))
        self.databases_combo.place(relx=0.01 , rely= 0.1)

        self.replaceName_lable = Label(self.tableFrame, text="variable name", font=("Times New Roman", 16, "bold"))
        self.replaceName_lable.place(relx=0.01, rely= 0.23)
        self.replaceName_entry = tk.Entry(self.tableFrame, textvariable=self.replaceName, font=("Times New Roman", 15),
                                          width=30)
        self.replaceName_entry.place(relx=0.01, rely= 0.3)

        self.btnView = Button(self.tableFrame, command=self.viewIndex, text="View List", cursor="hand2", width=30)
        self.btnView.place(relx=0.01 , rely= 0.4)

        self.btnDlt = Button(self.tableFrame, command=self.runRemediation, text="Run Remediation ", cursor="hand2",width=30)
        self.btnDlt.place(relx= 0.01, rely= 0.5)

        self.btnLogOut = Button(self.tableFrame, command=self.logOut, text="Log Out", cursor="hand2", width=30)
        self.btnLogOut.place(relx= 0.01, rely= 0.6)


