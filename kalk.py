from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

ripp_menuu = None
tk_var = None
category_menu_shown = False # Lisasin puuduoleva muutuja algväärtuse

# --- REKURSIIVNE FUNKTSIOON ---
def tyki_tekst(tekst, indeks=0):
    """Kuvab teksti täht-tähe haaval rekursiooni abil."""
    if indeks < len(tekst):
        # Lisame ühe tähe juurde
        vastuse_silt.config(text=tekst[:indeks+1])
        # Funktsioon kutsub iseennast (rekursioon) läbi Tkinteri 'after' meetodi
        # 30ms on viivitus tähtede vahel
        raam.after(30, lambda: tyki_tekst(tekst, indeks + 1))

def arvuta():
    try:
        nimi = nimi_sisestus.get()
        tulu = float(tulu_sisestus.get())
        kulu = float(kulu_sisestus.get())
        
        kat = tk_var.get() if tk_var else "Määramata"
        jaak = tulu - kulu
        
        if jaak > 0:
            tulemus_tekst = f"Tere {nimi}!\nKategooria: {kat}\nSinu jääk on positiivne: {jaak}€"
        else:
            tulemus_tekst = f"Tere {nimi}!\nKategooria: {kat}\nJääk on negatiivne: {jaak}€"
        
        # Kutsume välja rekursiivse funktsiooni
        tyki_tekst(tulemus_tekst)
        
    except ValueError:
        messagebox.showerror("Viga", "Palun sisesta tulu ja kulu numbrites!")

# --- Ülejäänud funktsioonid jäävad samaks ---

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        teksti_ala.delete("1.0", END)
        teksti_ala.insert(END, content)
        

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        try:
            tulu = float(tulu_sisestus.get())
            kulu = float(kulu_sisestus.get())
            nimi_vaartus = nimi_sisestus.get()
            kat_vaartus = tk_var.get() if tk_var else "Määramata"
            jaak_vaartus = tulu - kulu 

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Kasutaja: {nimi_vaartus}\n")
                f.write(f"Tulu: {tulu} €\n")
                f.write(f"Kulu: {kulu} €\n")
                f.write(f"Jääk: {jaak_vaartus} €\n")
                f.write(f"Kategooria: {kat_vaartus}\n")
                
            messagebox.showinfo("Tehtud", "Fail salvestati edukalt!")
        except ValueError:
            messagebox.showerror("Viga", "Sisesta tulu ja kulu numbritena!")

def open_category():
    global category_menu_shown, tk_var, ripp_menuu
    if not category_menu_shown:
        tk_var = StringVar(raam)
        tk_var.set("Toit") 
            
        valikud = ["Toit", "Transport", "Meelelahutus", "Muu"]
        ripp_menuu = ttk.OptionMenu(top_frame, tk_var, "Toit", *valikud)
        ripp_menuu.pack(side=LEFT, padx=5)
        category_menu_shown = True

def file():
    global shown, category_menu_shown
    if not shown:
        save_btn.pack(side=LEFT, padx=5)
        open_btn.pack(side=LEFT, padx=5)
        category_btn.pack(side=LEFT, padx=5)
        shown = True
    else:
        save_btn.pack_forget()
        open_btn.pack_forget()
        category_btn.pack_forget()
        if ripp_menuu:
            ripp_menuu.pack_forget()
            category_menu_shown = False 
        shown = False

raam = Tk()
raam.title("Eelarve Kalkulaator")
raam.geometry("450x500")

shown = False

top_frame = tk.Frame(raam)
top_frame.pack(anchor="nw", pady=5)

btn1 = tk.Button(top_frame, text="File", command=file)
btn1.pack(side=LEFT, padx=5)

save_btn = tk.Button(top_frame, text="Save", command=save_file)
open_btn = tk.Button(top_frame, text="Open", command=open_file)
category_btn = tk.Button(top_frame, text="Category", command=open_category)

ttk.Label(raam, text="Sinu nimi:").pack(pady=5)
nimi_sisestus = ttk.Entry(raam)
nimi_sisestus.pack()

ttk.Label(raam, text="Lisa tulu (€):").pack(pady=5)
tulu_sisestus = ttk.Entry(raam)
tulu_sisestus.pack()

ttk.Label(raam, text="Lisa kulu (€):").pack(pady=5)
kulu_sisestus = ttk.Entry(raam)
kulu_sisestus.pack()

nupp = ttk.Button(raam, text="Arvuta tulemus", command=arvuta)
nupp.pack(pady=20)

vastuse_silt = ttk.Label(raam, text="", font=("Arial", 10, "bold"), justify=LEFT)
vastuse_silt.pack(pady=10)

teksti_ala = tk.Text(raam, height=10, width=50)
teksti_ala.pack(pady=10)

raam.mainloop()
