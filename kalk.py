from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os

andmed = []  
KATEGOORIAD = ("Toit", "Transport", "Meelelahutus", "Muu")
KATEGOORIAD2 = ("Palk", "Toetus", "Annetus", "Muu")


def lisa_kirje_andmetesse(summa, kat, kat2, kirjeldus, tyyp):
    kirje = {
        "summa": float(summa),
        "kategooria": kat,
        "kategooria2": kat2,
        "kirjeldus": kirjeldus,
        "tyyp": tyyp
    }
    andmed.append(kirje)
    return kirje

def arvuta_summa_rekursiivne(nimekirja):
    if not nimekirja:
        return 0
    kirje = nimekirja[0]
    vaartus = kirje["summa"] if kirje["tyyp"] == "tulu" else -kirje["summa"]
    return vaartus + arvuta_summa_rekursiivne(nimekirja[1:])

def arvuta_statistika():
    stat = {}
    for k in andmed:
        kat = k["kategooria"]
        kat2 = k["kategooria"]
        summa = k["summa"] if k["tyyp"] == "tulu" else -k["summa"]
        stat[kat] = stat.get(kat, 0) + summa
        stat[kat2] = stat.get(kat2, 0) + summa
    return stat


def salvesta_csv(failinimi="eelarve.csv"):
    try:
        with open(failinimi, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            for k in andmed:
                writer.writerow([k["summa"], k["kategooria"], k["kirjeldus"], k["tyyp"]])
        messagebox.showinfo("Tehtud", f"Andmed salvestatud faili {failinimi}")
    except Exception as e:
        messagebox.showerror("Probleem", f"Salvestamine ebaõnnestus: {e}")

def loe_csv(failinimi="eelarve.csv"):
    global andmed
    if not os.path.exists(failinimi):
        messagebox.showwarning("Probleem", "Faili polnud olemas")
        return
    
    andmed = []
    try:
        with open(failinimi, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for rida in reader:
                if rida:
                    andmed.append({
                        "summa": float(rida[0]),
                        "kategooria": rida[1],
                        "kirjeldus": rida[2],
                        "tyyp": rida[3]
                    })
        uuenda_tabelit()
    except Exception as e:
        messagebox.showerror("Probleem", f"Midagi läks rikki: {e}")


def tyki_tekst(tekst, indeks=0):
    if indeks < len(tekst):
        vastuse_silt.config(text=tekst[:indeks+1])
        raam.after(20, lambda: tyki_tekst(tekst, indeks + 1))

def lisa_nupp_vajutatud():
    try:
        tulu_val = tulu_sisestus.get()
        kulu_val = kulu_sisestus.get()
        
        if tulu_val and not kulu_val:
            summa = float(tulu_val)
            tyyp = "tulu"
        elif kulu_val and not tulu_val:
            summa = float(kulu_val)
            tyyp = "kulu"
        else:
            messagebox.showwarning("Oota!", "Vali kas kulu või tulu ainult")
            return

        if summa <= 0:
            raise ValueError
        
        kat = kulu_muutuja.get()
        kat2 = tulu_muutuja.get()
        kirjeldus = kirjeldus_sisestus.get()
        
        lisa_kirje_andmetesse(summa, kat, kat2, kirjeldus, tyyp)
        uuenda_tabelit()
        
        tulu_sisestus.delete(0, tk.END)
        kulu_sisestus.delete(0, tk.END)
        kirjeldus_sisestus.delete(0, tk.END)
        
    except ValueError:
        messagebox.showerror("Viga", "Sisesta korrektne positiivne number!")

def uuenda_tabelit():
    teksti_ala.delete("1.0", tk.END)
    for k in andmed:
        mark = "+" if k['tyyp'] == "tulu" else "-"
        teksti_ala.insert(tk.END, f"{k['tyyp'].upper()} {mark}{k['summa']}€ | {k['kategooria']} | {k['kirjeldus']}\n")

def arvuta_kokkuvote():
    if not andmed:
        tyki_tekst("Andmeid pole!")
        return
    
    jaak = arvuta_summa_rekursiivne(andmed)
    stat = arvuta_statistika()
    
    tulemus = f"Kogusaldo: {jaak:.2f}€\n"
    tulemus += "Kategooriate kaupa:\n"
    for kat, s in stat.items():
        tulemus += f" - {kat}: {s:.2f}€\n"
        
    for kat2, s in stat.items():
        tulemus += f" - {kat2}: {s:.2f}€\n"
    
    tyki_tekst(tulemus)


raam = tk.Tk()
raam.title("Kalkulaator")
raam.geometry("500x750")

ttk.Label(raam, text="Sinu nimi:").pack(pady=2)
nimi_sisestus = ttk.Entry(raam)
nimi_sisestus.pack()

ttk.Label(raam, text="Lisa tulu (€):", foreground="green").pack(pady=2)
tulu_sisestus = ttk.Entry(raam)
tulu_sisestus.pack()

ttk.Label(raam, text="Kategooria:").pack(pady=2)
tulu_muutuja = tk.StringVar(value=KATEGOORIAD2[0])
kat_menu2 = ttk.OptionMenu(raam, tulu_muutuja, KATEGOORIAD2[0], *KATEGOORIAD2)
kat_menu2.pack()

ttk.Label(raam, text="Lisa kulu (€):", foreground="red").pack(pady=2)
kulu_sisestus = ttk.Entry(raam)
kulu_sisestus.pack()

ttk.Label(raam, text="Kategooria:").pack(pady=2)
kulu_muutuja = tk.StringVar(value=KATEGOORIAD[0])
kat_menu = ttk.OptionMenu(raam, kulu_muutuja, KATEGOORIAD[0], *KATEGOORIAD)
kat_menu.pack()

ttk.Label(raam, text="Kirjeldus:").pack(pady=2)
kirjeldus_sisestus = ttk.Entry(raam)
kirjeldus_sisestus.pack()

ttk.Button(raam, text="Lisa kirje", command=lisa_nupp_vajutatud).pack(pady=10)
ttk.Button(raam, text="Arvuta koondvaade", command=arvuta_kokkuvote).pack(pady=5)

f_raam = tk.Frame(raam)
f_raam.pack(pady=10)
ttk.Button(f_raam, text="Salvesta CSV", command=salvesta_csv).pack(side=tk.LEFT, padx=5)
ttk.Button(f_raam, text="Laadi CSV", command=loe_csv).pack(side=tk.LEFT, padx=5)

vastuse_silt = ttk.Label(raam, text="", font=("Arial", 10, "bold"), justify=tk.LEFT)
vastuse_silt.pack(pady=10)

teksti_ala = tk.Text(raam, height=10, width=55)
teksti_ala.pack(pady=10)

raam.mainloop()
