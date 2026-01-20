from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

andmed = []

KATEGOORIAD = ("Toit", "Transport", "Meelelahutus", "Muu")
KATEGOORIAD2 = ("Palk", "Toetus", "Annetus", "Muu")


def lisa_kirje_andmetesse(summa, valitud_kat, kirjeldus, tyyp):
    kirje = {
        "summa": float(summa),
        "kategooria": valitud_kat,
        "kirjeldus": kirjeldus,
        "tyyp": tyyp
    }
    andmed.append(kirje)


def arvuta_summa_rekursiivne(nimekirja):
    if not nimekirja:
        return 0
    kirje = nimekirja[0]
    vaartus = kirje["summa"] if kirje["tyyp"] == "tulu" else -kirje["summa"]
    return vaartus + arvuta_summa_rekursiivne(nimekirja[1:])


def arvuta_kategooria():
    stat = {}
    for k in andmed:
        kat = k["kategooria"]
        summa = k["summa"] if k["tyyp"] == "tulu" else -k["summa"]
        stat[kat] = stat.get(kat, 0) + summa
    return stat


def salvesta_csv(failinimi="eelarve.csv"):
    try:
        with open(failinimi, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            for k in andmed:
                writer.writerow([k["summa"], k["kategooria"], k["kirjeldus"], k["tyyp"]])
        messagebox.showinfo("Tehtud", "Andmed salvestatud!")
    except Exception as e:
        messagebox.showerror("Viga", str(e))


def loe_csv(failinimi="eelarve.csv"):
    global andmed
    if not os.path.exists(failinimi):
        messagebox.showwarning("Viga", "Faili ei leitud")
        return

    andmed = []
    try:
        with open(failinimi, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for rida in reader:
                andmed.append({
                    "summa": float(rida[0]),
                    "kategooria": rida[1],
                    "kirjeldus": rida[2],
                    "tyyp": rida[3]
                })
        uuenda_tabelit()
    except Exception as e:
        messagebox.showerror("Viga", str(e))


def tyki_tekst(tekst, indeks=0):
    if indeks < len(tekst):
        vastuse_silt.config(text=tekst[:indeks + 1])
        raam.after(15, lambda: tyki_tekst(tekst, indeks + 1))


def lisa_kulu_tulu():
    try:
        tulu_val = tulu_sisestus.get()
        kulu_val = kulu_sisestus.get()

        if tulu_val and not kulu_val:
            summa = float(tulu_val)
            tyyp = "tulu"
            valitud_kat = tulu_muutuja.get()
        elif kulu_val and not tulu_val:
            summa = float(kulu_val)
            tyyp = "kulu"
            valitud_kat = kulu_muutuja.get()
        else:
            messagebox.showwarning("Hoiatus", "Sisesta kas tulu või kulu")
            return

        if summa <= 0:
            raise ValueError

        kirjeldus = kirjeldus_sisestus.get()

        lisa_kirje_andmetesse(summa, valitud_kat, kirjeldus, tyyp)
        uuenda_tabelit()

        tulu_sisestus.delete(0, END)
        kulu_sisestus.delete(0, END)
        kirjeldus_sisestus.delete(0, END)

    except ValueError:
        messagebox.showerror("Viga", "Sisesta korrektne positiivne number")


def uuenda_tabelit():
    teksti_ala.delete("1.0", END)
    for k in andmed:
        mark = "+" if k["tyyp"] == "tulu" else "-"
        teksti_ala.insert(
            END,
            f"{k['tyyp'].upper()} {mark}{k['summa']}€ | {k['kategooria']} | {k['kirjeldus']}\n"
        )


def kuva_andmed():
    if not andmed:
        tyki_tekst("Andmeid pole!")
        return

    jaak = arvuta_summa_rekursiivne(andmed)
    stat = arvuta_kategooria()

    tulemus = f"Kogusaldo: {jaak:.2f}€\n\nKategooriate kaupa:\n"
    for kat, s in stat.items():
        tulemus += f"- {kat}: {s:.2f}€\n"

    tyki_tekst(tulemus)


raam = tk.Tk()
raam.title("Eelarve kalkulaator")
raam.geometry("500x750")

tk.Label(raam, text="Sinu nimi:").pack(pady=2)
nimi_sisestus = ttk.Entry(raam)
nimi_sisestus.pack()

tk.Label(raam, text="Lisa tulu (€):", fg="green").pack(pady=2)
tulu_sisestus = ttk.Entry(raam)
tulu_sisestus.pack()

tk.Label(raam, text="Tulu kategooria:").pack()
tulu_muutuja = tk.StringVar(value=KATEGOORIAD2[0])
ttk.OptionMenu(raam, tulu_muutuja, KATEGOORIAD2[0], *KATEGOORIAD2).pack()

tk.Label(raam, text="Lisa kulu (€):", fg="red").pack(pady=2)
kulu_sisestus = ttk.Entry(raam)
kulu_sisestus.pack()

tk.Label(raam, text="Kulu kategooria:").pack()
kulu_muutuja = tk.StringVar(value=KATEGOORIAD[0])
ttk.OptionMenu(raam, kulu_muutuja, KATEGOORIAD[0], *KATEGOORIAD).pack()

tk.Label(raam, text="Kirjeldus:").pack()
kirjeldus_sisestus = ttk.Entry(raam)
kirjeldus_sisestus.pack()

ttk.Button(raam, text="Lisa kirje", command=lisa_kulu_tulu).pack(pady=10)
ttk.Button(raam, text="Arvuta koondvaade", command=kuva_andmed).pack()

f = tk.Frame(raam)
f.pack(pady=10)
ttk.Button(f, text="Salvesta CSV", command=salvesta_csv).pack(side=LEFT, padx=5)
ttk.Button(f, text="Laadi CSV", command=loe_csv).pack(side=LEFT, padx=5)

vastuse_silt = ttk.Label(raam, text="", justify=LEFT, font=("Arial", 10, "bold"))
vastuse_silt.pack(pady=10)

teksti_ala = tk.Text(raam, height=10, width=55)
teksti_ala.pack()

raam.mainloop()

