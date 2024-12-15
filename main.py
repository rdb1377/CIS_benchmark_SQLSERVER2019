import ttkbootstrap as tk
from tkinter import ttk
import login

#main method
def main():
    root = tk.Window()
    root.title("CIS Hardening")
    root.geometry("1400x930+100+50")
    root.resizable(0,0)

    #Parsing the root window to the Login class
    #Initiating the System
    login.Login(root)

    root.mainloop()

if __name__ == '__main__':
    main()
