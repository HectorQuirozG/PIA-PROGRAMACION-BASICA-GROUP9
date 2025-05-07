import requests

url = "https://api.frankfurter.dev/v1/"
while True:
    menu = """----------------------------
MENU
1. Cambiar moneda
2. Ver estadísticas históricas
3. Salir
"""
    try: op = int(input(menu))
    except(ValueError): op = None
    if op == 1:
        response = requests.get(url + "currencies")
        if response.status_code == 200:
            currencies = response.json()
            while True:
                print("----------------------------")
                for k, v in currencies.items():
                    print(f"{k}: {v}")
                base = input("Moneda de entrada: ")
                if base in currencies:
                    break
                else: print("No encontrado, revisa la entrada")
            currencies.pop(base)
            while True:
                print("----------------------------")
                for k, v in currencies.items():
                    print(f"{k}: {v}")
                change = input("Moneda de salida: ")
                if change in currencies:
                    break
                else: print("No encontrado, revisa la entrada")
            while True:
                try:
                    qant = float(input("Cantidad a convertir: "))
                    if qant >= 0:
                        break
                except ValueError: print("Entrada inválida")
            apend = f"latest?base={base}"
            response = requests.get(url + apend)
            if response.status_code == 200:
                rates = response.json()
                x = 2
                while round(rates['rates'][change]*qant, x) == 0:
                    x += 1
                print(f"\n${qant} {base} = ${round(rates['rates'][change]*qant, x)} {change}")
            else: print(f"Ocurrió un error inesperado #{response.status_code}")                
        else: print(f"Ocurrió un error inesperado #{response.status_code}")
    elif op == 2:
        fecha = input("Ingresa la fecha en formato YYYY-MM-DD: ")
        response = requests.get(url + fecha)
        if response.status_code == 200:
            date = response.json()
            print("Monedas disponibles:")
            monedas = list(date['rates'].keys()) + ["EUR"]
            monedas.sort()
            for i in monedas:
                print(f"- {i}")
            while True:
                base = input("Selecciona una moneda: ")
                if base in monedas:
                    break
                else: print("No encontrado, revisa la entrada")
            apend = f"{fecha}?base={base}"
            response = requests.get(url + apend)
            if response.status_code == 200:
                datos = response.json()
                print("----------------------------")
                for k, v in datos.items():
                    if k == 'amount':
                           continue
                    if k == 'date':
                        v = fecha
                    if type(v) == dict:
                        print("--- Equivalencias ---")
                        for x, y in v.items():
                            print(f"    {x}: ${y}")
                    else:
                        print(f"{k.capitalize()}: {v}")
            else: print(f"Ocurrió un error inesperado #{response.status_code}")
        else: print(f"Ocurrió un error inesperado #{response.status_code}. Es posible que la fecha no sea válida")
    elif op == 3:
        print("Saliendo...")
        break
    else:
        print("Opción inválida")
