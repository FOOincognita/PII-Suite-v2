import tkinter as tk
from tkinter import filedialog

"""
    * Uses TKInter's filedialog to select local folders & return path
"""

def select_folder():
    (root := tk.Tk()).withdraw()
    root.wm_attributes('-topmost', 1)
    print(filedialog.askdirectory(title="Select Folder"))
    root.destroy()

if __name__ == "__main__":
    select_folder()
