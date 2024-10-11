import datetime as dt

nume_client = "Popescu Marius"
valoare_factura = 1230.5

print("Valoarea facturii pentru clientul {nume} este {valoare:5.2f}".format(nume=nume_client, valoare=valoare_factura))
print(f"Valoarea facturii pentru clientul {nume_client} este {valoare_factura:7.3f}")

format_data1 = "%d.%m.%Y"
format_data2 = "%d/%m/%Y"

azi = dt.datetime.today()
print("Azi:", format(azi, format_data1))
liviu = dt.datetime(2009, 6, 10)
diana = dt.datetime(2005, 11, 11)
print(f"Data nastere Liviu:{liviu:%d.%m.%Y}. Data nastere Diana:{diana:%d/%m/%Y}")
diferenta = liviu - diana
print(type(diferenta))
print("Diferenta in zile dintre Liviu si Diana:", format(diferenta.days, "#d"))
if liviu < diana:
    print("Diana este mai mica cu ", diferenta.days, " zile")
else:
    print("Diana este mai mare cu ", diferenta.days, " zile")
