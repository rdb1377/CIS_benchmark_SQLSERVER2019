import ttkbootstrap
import tkinter as tkinter
from  ttkbootstrap import *
# from tkinter import ttk
from tkinter import messagebox
import login
from bench import Benchmarks
import ttkbootstrap.scrolled as st
from tkhtmlview import HTMLScrolledText
import ttkbootstrap as boot


# creating a database object

class AdminControls:
    def __init__(self, root, connectionString):

        self.root = root
        self.database = StringVar()
        self.replaceName = StringVar()
        self.remediation_label = None
        self.description = None
        self.dsc_label = None
        self.entriesFrame = None
        self.remediation = None
        self.selectedRow = None
        self.btnLogOut = None
        self.btnDlt = None
        self.btnView = None
        self.connectionString = connectionString
        self.benchmark = Benchmarks(connectionString)

        self.tableOutputFrame()
        self.adminControlsFrame()

    def adminControlsFrame(self):
        self.entriesFrame = Frame(self.root)
        self.entriesFrame.place(x=0, y=450, width=1400, height=500)

        self.dsc_label = Label(self.entriesFrame, text="Description", font=("Goudy old style", 20))
        self.dsc_label.place(x=550, y=0)

        self.description = HTMLScrolledText(self.entriesFrame, html='<html></html>', height= 23, width=120)
        self.description.place(x=550, y=30)

        self.remediation_label = Label(self.entriesFrame, text="Remediation Result", font=("Goudy old style", 20))
        self.remediation_label.place(x=10, y=0)

        self.remediation = st.ScrolledText(self.entriesFrame, font=("Courier", 9), width=70, height=9, relief=GROOVE, wrap= tkinter.WORD)
        self.remediation.place(x=10, y=30)

    def getData(self, event):
        try:
            self.selectedRow = self.out.focus()
            self.selectedData = self.out.item(self.selectedRow)
            self.chosenRow = self.selectedData["values"]
            self.description.delete('1.0', END)
            self.description.set_html(self.chosenRow[3])
            self.remediation.delete('1.0', END)
            self.remediation.insert(INSERT, self.chosenRow[5])
        except IndexError as error:
            pass

    def runRemediation(self):
        try:
            result = self.benchmark.runRemediation(self.chosenRow[4], self.replaceName)
            if result == 0:
                messagebox.showerror("warning!","This recommendation has a manual remediation")
            else:
                print("$1231412413!@#$%^", result , type(result))
                self.remediation.delete('1.0', END)
                self.remediation.insert(INSERT, result)

        except AttributeError as error:
            messagebox.showerror("Error!", "Please Choose a Row")

    def viewResults(self):
        self.out.delete(*self.out.get_children())  # fill the table with benchmark results
        for row in self.benchmark.runAudit():
            self.out.insert("", END, values=row, tags=row[2])

    # Method to direct to the next Frame to Assign Instructors


    # Method to redirect to the login frame
    def logOut(self):
        self.entriesFrame.destroy()
        # self.buttonsFrame.destroy()
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
        self.btnView = Button(self.buttonsFrame, command=self.viewResults, text="View List", cursor="hand2", width=20)

        # LogOut
        self.btnLogOut = Button(self.buttonsFrame, command=self.logOut, text="Log Out", cursor="hand2", width=15)
        self.btnLogOut.grid(row=0, column=6, padx=15, sticky="e")

    """Table Frame using TreeView"""


    def tableOutputFrame(self):
        # Treeview Frame Configurations
        self.tableFrame = Frame(self.root)
        self.tableFrame.place(x=0, y=0, width=1400, height=550)
        self.yScroll = Scrollbar(self.tableFrame)
        self.yScroll.pack(side=RIGHT, fill=Y)

        # ttk style object to add configurations
        self.style = boot.Style()
        self.style.configure("mystyle.Treeview", font=('Calibri', 12),
                             rowheight=50)
        self.style.configure("mystyle.Treeview.Heading", font=("Goudy old style", 14), sticky="w")

        # Formatting the output table view
        self.out = boot.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set,
                                 columns=(1, 2 ,3), style="mystyle.Treeview")
        self.out.tag_configure('PASS', background='lightgreen')
        self.out.tag_configure('FAIL', background='pink')
        self.out.tag_configure('MANUAL', background='lightyellow')

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
        self.out.place(relx = 0.25,rely=0.1,width=950 , height=400)
        self.yScroll.config(command=self.out.yview)

        self.LabelDatabase = Label(self.tableFrame, text="List of Recommendations", font=("Goudy old style", 20))
        self.LabelDatabase.place(relx=0.25, rely=0.01)

        self.LabelDatabase = Label(self.tableFrame, text="database", font=("Goudy old style", 20))
        self.LabelDatabase.place(relx=0.01 , rely= 0.03)

        res = self.benchmark.get_databases()
        self.databases_combo = boot.Combobox(self.tableFrame, textvariable=self.database, font=("Times New Roman", 15), width=28, state="readonly")
        self.databases_combo['values'] = res
        self.databases_combo.bind("<<ComboboxSelected>>",lambda event, entry=self.databases_combo: self.benchmark.buildCNXN(entry.get()))
        self.databases_combo.place(relx=0.01 , rely= 0.1)

        self.replaceName_lable = Label(self.tableFrame, text="variable name", font=("Goudy old style", 20))
        self.replaceName_lable.place(relx=0.01, rely= 0.23)
        self.replaceName_entry = tk.Entry(self.tableFrame, textvariable=self.replaceName, font=("Times New Roman", 15),
                                          width=30)
        self.replaceName_entry.place(relx=0.01, rely= 0.3)

        self.btnView = Button(self.tableFrame, command=self.viewResults, text="View List", cursor="hand2", width=30)
        self.btnView.place(relx=0.01 , rely= 0.4)

        self.btnDlt = Button(self.tableFrame, command=self.runRemediation, text="Run Remediation ", cursor="hand2",width=30)
        self.btnDlt.place(relx= 0.01, rely= 0.5)

        self.btnLogOut = Button(self.tableFrame, command=self.logOut, text="Log Out", cursor="hand2", width=30)
        self.btnLogOut.place(relx= 0.01, rely= 0.6)


