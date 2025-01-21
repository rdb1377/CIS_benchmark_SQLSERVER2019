import ttkbootstrap as tk
from tkinter import ttk
import login
from tkinter import Tk

#main method
class Application:
    def main():
        root = tk.Window()
        root.title("CIS Hardening")
        photo = tk.PhotoImage(file="ico.png")
        root.iconphoto(False , photo)
        root.geometry("1270x850+100+50")
        root.resizable(height=True,width=True)

        #Parsing the root window to the Login class
        #Initiating the System
        login.Login(root)

        root.mainloop()

if __name__ == '__main__':
    Application.main()
