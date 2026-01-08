from tkinter import *
from tkinter import filedialog
import tkinter as tk

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(content)

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("See on test\nEelarve andmed siia")

def file():
    global shown
    if not shown:
        save_btn.pack(side=LEFT, padx=5)
        open_btn.pack(side=LEFT, padx=5)
        shown = True

raam = tk.Tk()
raam.title("Eelarve kalkulaator")

shown = False

top_frame = tk.Frame(raam)
top_frame.pack(anchor="nw")

btn1 = tk.Button(top_frame, text="File", command=file)
btn1.pack(side=LEFT, padx=5)

save_btn = tk.Button(top_frame, text="Save", command=save_file)
open_btn = tk.Button(top_frame, text="Open", command=open_file)

main_frame = tk.Frame(raam)
main_frame.pack()

tahvel = tk.Canvas(main_frame, width=900, height=600, bg="white")
tahvel.pack()

raam.mainloop()
