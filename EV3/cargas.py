import requests, os

def carga_cache_currencies(arch, url):
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
    return currencies

def carga_cache_rates(arch, url, apend, base, change):
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
    return rates
