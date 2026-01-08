name = input("Lisa enda nimi siia palun: ")
print("Tere, " + (name))
print("\n")

print("=================================")
add_income = float(input("Lisa enda tulu siia numbrites: "))
add_income_cat = str(input("Lisa enda tulu kategooria siia: "))
print("=================================")
print("\n")
print("=================================")
add_expenses = float(input("Lisa enda kulu siia numbrites: "))
add_expenses_cat = str(input("Lisa enda kulu kategooria siia: "))
print("=================================")

money_together = add_income - add_expenses
if money_together >0:
    print("Siin on sinu raha sissetulek: " + str(money_together) + "€")
else:
    print("\n")
    print(name + ", teie raha sissetulek ei ole positiivne " + str(money_together) + "€")
    print("\n")
    abi = input("Kas soovite abi? (Jah/Ei): ")
    if abi == "Jah" and "jah":
        print("\n")
        print("Soovitan rohkem raha teenida")
    elif abi == "Ei" or "ei":
        print("\n")
        print("Sobib, soovin head päeva!")
        print("Võta ennast kokku ja saa raha ikka...")

    


