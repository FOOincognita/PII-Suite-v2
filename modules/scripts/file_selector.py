import tkinter as tk
from tkinter import filedialog

"""
    * Uses TKInter's filedialog to select 1 local file & return path
"""

def select_file():
    (root := tk.Tk()).withdraw()  
    root.wm_attributes('-topmost', 1)
    print(filedialog.askopenfilename(filetypes = (("CSV files","*.csv"),("all files","*.*")), title="Select CSV File")) 
    root.destroy()

if __name__ == "__main__":
    select_file()
