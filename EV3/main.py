import funcs, source

def main():
    url = "https://api.frankfurter.dev/v1/"
    while True:
        menu = """----------------------------
MENU
1. Cambiar moneda
2. Ver estadísticas históricas
3. Salir
Selecciona una opción: """
        try: op = int(input(menu))
        except(ValueError): op = None
        if op == 1:
            arch = "cache_currencies.txt"
            currencies = source.carga_cache_currencies(arch, url)
            print("----------------------------")
            for k, v in currencies.items():
                print(f"{k}: {v}")
            flag = True
            while flag:
                base = input("Moneda de entrada: ")
                flag = source.valid_mon(base, currencies)
            currencies.pop(base)
            print("----------------------------")
            for k, v in currencies.items():
                print(f"{k}: {v}")
            flag = True
            while flag:
                change = input("Moneda de salida: ")
                flag = source.valid_mon(change, currencies)
            while True:
                try:
                    qant = float(input("Cantidad a convertir: "))
                    if qant >= 0:
                        break
                except ValueError: print("Entrada inválida")
            apend = f"latest?base={base}"
            arch = "cache_rates.txt"
            rates = source.carga_cache_rates(arch, url, apend, base, change)
            conv = source.convert(base, change, qant, rates)
            print(f"${qant} {base} = ${conv} {change}")
        elif op == 2:
            flag = True
            while flag:
                flag = True
                while flag:
                    fecha1 = input("Ingresa la fecha inicial en formato YYYY-MM-DD: ")
                    flag = source.valid_fecha(fecha1)
                flag = True
                while flag:
                    fecha2 = input("Ingresa la fecha final en formato YYYY-MM-DD: ")
                    flag = source.valid_fecha(fecha1)
                flag = source.valid_rango(fecha1, fecha2)
            apend = f"{fecha1}..{fecha2}"
            source.historia(url, apend, fecha1, fecha2)
        elif op == 3:
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    #try:
    main()
    #except:
     #   print("Ocurrió algo inesperado")
      #  print("Saliendo...")

