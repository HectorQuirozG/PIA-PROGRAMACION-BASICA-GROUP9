import requests, re, os, datetime, statistics

def convert(url):
    try:
        arch = "cache_currencies.txt"
        if os.path.exists(f".\\cache\\{arch}"):
            currencies = {}
            with open(f".\\cache\\{arch}", "r", encoding = 'utf-8') as f:
                for linea in f:
                    if ":" in linea:
                        k, v = linea.strip().split(":")
                    currencies[k] = v
        else:
            os.mkdir(f".\\cache")
            response = requests.get(url + "currencies")
            if response.status_code == 200:
                currencies = response.json()
                with open(f".\\cache\\{arch}", "w", encoding = 'utf-8') as f:
                    for k, v in currencies.items():
                        f.write(f"{k}: {v}\n")
            else: print(f"Ocurrió un error inesperado #{response.status_code}")
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
        arch = "cache_rates.txt"
        if os.path.exists(f".\\cache\\{arch}"):
            with open(f".\\cache\\{arch}", "r", encoding = 'utf-8') as f:
                rates = {}
                for linea in f:
                    if ":" in linea:
                        k, v = linea.strip().split(":")
                    rates[k] = v
            if f"{base}, {change}" not in rates:
                response = requests.get(url + apend)
                if response.status_code == 200:
                    rates = response.json()
                    data = response.json()
                    rates = {}
                    rates[f'{base}, {change}'] = data['rates'][change]
                    with open(f".\\cache\\{arch}", "a", encoding = 'utf-8') as f:
                        for k, v in rates.items():
                            f.write(f"{k}: {v}\n")
                else: print(f"Ocurrió un error inesperado #{response.status_code}")
        else:
            response = requests.get(url + apend)
            if response.status_code == 200:
                data = response.json()
                rates = {}
                rates[f'{base}, {change}'] = data['rates'][change]
                with open(f".\\cache\\{arch}", "w", encoding = 'utf-8') as f:
                    for k, v in rates.items():
                        f.write(f"{k}: {v}\n")
            else: print(f"Ocurrió un error inesperado #{response.status_code}")
        x = 2
        equi = float(rates[f'{base}, {change}'])
        while round(equi*qant, x) == 0:
            x += 1
        print(f"\n${qant} {base} = ${round(equi*qant, x)} {change}")
    except requests.exceptions.ConnectionError: print("Revisa tu conexión a internet")


def stats(url):
    try:
        while True:
            fech = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
            while True:
                fecha1 = input("Ingresa la fecha inicial en formato YYYY-MM-DD: ")
                mo = fech.search(fecha1)
                try:
                    if mo != None:
                        verf1 = datetime.date(int(mo.group(1)), int(str(mo.group(2))), int(str(mo.group(3))))
                        if verf1 < datetime.date(1999, 1, 4):
                            print("La fecha más antigua es 1999-01-04")
                        elif verf1 > datetime.date.today():
                            print("La fecha debe ser igual o anterior a la actual")
                        else: break
                    else: print("Fecha inválida")
                except ValueError: print("Los meses o días están fuera de rango")
            while True:
                fecha2 = input("Ingresa la fecha final en formato YYYY-MM-DD: ")
                mo = fech.search(fecha2)
                try:
                    if mo != None:
                        verf2 = datetime.date(int(mo.group(1)), int(str(mo.group(2))), int(str(mo.group(3))))
                        if verf2 < datetime.date(1999, 1, 4):
                            print("La fecha más antigua es 1999-01-04")
                        elif verf2 > datetime.date.today():
                            print("La fecha debe ser igual o anterior a la actual")
                        elif verf2 < verf1:
                            print("La fecha debe ser igual o posterior a la de inicio")
                        else: break
                    else: print("Fecha inválida")
                except ValueError: print("Los meses o días están fuera de rango")
            if verf2 - verf1 <= datetime.timedelta(days = 30):
                break
            else: print("El rango máximo es de 30 días")
        apend = f"{fecha1}..{fecha2}"
        response = requests.get(url + apend)
        if response.status_code == 200:
            data = response.json()
            print("Monedas disponibles:")
            verf = fecha1
            while True:
                try:
                    monedas = list(data['rates'][verf].keys()) + ["EUR"]
                    monedas.sort
                except KeyError:
                    mo = fech.search(verf)
                    resta = datetime.date(int(mo.group(1)), int(str(mo.group(2))), int(str(mo.group(3)))) - datetime.timedelta(days = 1)                   
                    verf = str(resta)
                else:
                    break
            for i in monedas:
                print(i)
            while True:
                base = input("Selecciona una moneda: ")
                if base in monedas:
                    break
                else: print("No encontrado, revisa la entrada")
            apend = f"{fecha1}..{fecha2}?base={base}"
            response = requests.get(url + apend)
            if response.status_code == 200:
                data = response.json()
                history = list()
                print("----------------------------")
                for k, v in data.items():
                    if k == 'amount':
                        continue
                    if type(v) == dict:
                        print("--- Equivalencias ---")
                        for x, y in v.items():
                            print(f" -- {x} --")
                            for a, b in y.items():
                                print(f"    {a}: ${b}")
                                if base != "USD" and a == "USD":
                                    history.append(b)
                                elif base == "USD" and a == "EUR":
                                    history.append(b)
                print("--- Estadísticas ---")
                maxi = max(history)
                mini = min(history)
                for k, v in data.items():
                    if type(v) == dict:
                        for x, y in v.items():
                            if type(y) == dict:
                                for a, b in y.items():
                                    if b == maxi:
                                        fech_max = x
                for k, v in data.items():
                    if type(v) == dict:
                        for x, y in v.items():
                            if type(y) == dict:
                                for a, b in y.items():
                                    if b == mini:
                                        fech_min = x
                print(f"Máximo valor: {fech_max}")
                print(f"Mínimo valor: {fech_min}")
                if base != "USD":
                    prom = statistics.mean(history)
                    rang = maxi - mini
                    print(f"Valor promedio: ${prom:.5f} USD")
                    print(f"Diferencia: ${rang:.5f} USD")
            print("Advertencia: Algunas fechas no están registradas debido a que presentaron cambios mínimos")
        else: print(f"Ocurrió un error inesperado #{response.status_code}")
    except requests.exceptions.ConnectionError: print("Revisa tu conexión a internet")
