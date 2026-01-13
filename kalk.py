from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- FUNKTSIOONID ---

def arvuta():
    try:
        nimi = nimi_sisestus.get()
        tulu = float(tulu_sisestus.get())
        kulu = float(kulu_sisestus.get())
        
        # Proovime kätte saada kategooria, kui see on loodud
        try:
            kat = tk_var.get()
        except NameError:
            kat = "Määramata"
            
        jaak = tulu - kulu
        
        if jaak > 0:
            tulemus_tekst = f"Tere {nimi}!\nKategooria: {kat}\nSinu jääk on positiivne: {jaak}€"
        else:
            tulemus_tekst = f"Tere {nimi}!\nKategooria: {kat}\nJääk on negatiivne: {jaak}€"
        
        vastuse_silt.config(text=tulemus_tekst)
        
    except ValueError:
        messagebox.showerror("Viga", "Palun sisesta tulu ja kulu numbrites!")

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
        try:
            tulu_vaartus = tulu_sisestus.get()
            kulu_vaartus = kulu_sisestus.get()
            nimi_vaartus = nimi_sisestus.get()
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Kasutaja: {nimi_vaartus}\n")
                f.write(f"Siin on teie tulu: {tulu_vaartus} €\n")
                f.write(f"Siin on teie kulu: {kulu_vaartus} €")
                f.write(f"Siin on teie kategooria: {kulu_vaartus} €")
            
            messagebox.showinfo("Tehtud", "Fail salvestati edukalt!")
        except Exception as e:
            messagebox.showerror("Viga", f"Salvestamisel tekkis viga: {e}")

# Eraldi muutuja kategooria menüü jaoks, et see ei läheks "File" menüüga konflikti
category_menu_shown = False
def open_category():
    global category_menu_shown, tk_var
    if not category_menu_shown:
        # Loome muutuja, mis hoiab valitud väärtust
        tk_var = StringVar(raam)
        tk_var.set("Toit") # Vaikimisi valik
            
        valikud = ["Toit", "Transport", "Meelelahutus", "Muu"]
        # Teeme rippmenüü
        ripp_menuu = ttk.OptionMenu(top_frame, tk_var, "Vali kategooria", *valikud)
        ripp_menuu.pack(side=LEFT, padx=5)
            
        category_menu_shown = True


def file():
    global shown
    if not shown:
        save_btn.pack(side=LEFT, padx=5)
        open_btn.pack(side=LEFT, padx=5)
        category_btn.pack(side=LEFT, padx=5)
        shown = True
    else:
        save_btn.pack_forget()
        open_btn.pack_forget()
        category_btn.pack_forget()
        ripp_menuu.pack_forget()
        shown = False
        
        

# --- AKNA SEADISTUS ---
raam = Tk()
raam.title("Eelarve Kalkulaator")
raam.geometry("450x500")

shown = False

top_frame = tk.Frame(raam)
top_frame.pack(anchor="nw", pady=5)

btn1 = tk.Button(top_frame, text="File", command=file)
btn1.pack(side=LEFT, padx=5)

# Nupud on loodud, aga neid ei pakita enne kui "File" vajutatakse
save_btn = tk.Button(top_frame, text="Save", command=save_file)
open_btn = tk.Button(top_frame, text="Open", command=open_file)
category_btn = tk.Button(top_frame, text="Category", command=open_category)

# --- Sisestusväljad ---
ttk.Label(raam, text="Sinu nimi:").pack(pady=5)
nimi_sisestus = ttk.Entry(raam)
nimi_sisestus.pack()

ttk.Label(raam, text="Lisa tulu (€):").pack(pady=5)
tulu_sisestus = ttk.Entry(raam)
tulu_sisestus.pack()

ttk.Label(raam, text="Lisa kulu (€):").pack(pady=5)
kulu_sisestus = ttk.Entry(raam)
kulu_sisestus.pack()

# --- Nupp ---
nupp = ttk.Button(raam, text="Arvuta tulemus", command=arvuta)
nupp.pack(pady=20)

# --- Koht tulemuse jaoks ---
vastuse_silt = ttk.Label(raam, text="", font=("Arial", 10, "bold"))
vastuse_silt.pack(pady=10)

raam.mainloop()
