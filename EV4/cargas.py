import requests, os, source
import tkinter as tk
from tkinter import filedialog
import pandas as pd

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

def guardar_stats(arch, equivalencias, stats, base):
    if not os.path.exists(f".\\stats"):
        os.mkdir(f".\\stats")
    elif os.path.exists(f".\\stats\\{arch}.txt"):
        print("El archivo ya existe")
        return None
    with open(f".\\stats\\{arch}.txt", "w", encoding= 'utf-8') as f:
        f.write(f"&&&&& Guardado de stats {base} &&&&&\n\n")
        for k, v in equivalencias.items():
            f.write(f"{k}: {v}\n")
        f.write("\n")
        for k, v in stats.items():
            f.write(f"{k}: {v}\n")
        print("Archivos guardados con éxito")

def buscar_arch():
    root = tk.Tk()
    arch = filedialog.askopenfilename()
    root.update()
    root.withdraw()
    root.destroy()
    return arch

def procesar_equivalencias(arch):    
    with open(arch, "r", encoding = 'utf-8') as f:
        equivalencias = {}
        for linea in f:
            if ":" in linea:
                k, v = linea.strip().split(":")
                flag = source.valid_fecha_format(k)
                if flag != None:
                    equivalencias[k] = float(v)
    return equivalencias

def procesar_stats(arch):
    with open(arch, "r", encoding = 'utf-8') as f:
        stats = {}
        for linea in f:
            if ":" in linea:
                k, v = linea.strip().split(":")
                flag = source.valid_fecha_format(k)
                if flag == None:
                    stats[k] = v
    return stats

def generar_excel(arch, equivalencias):
    df = pd.DataFrame([equivalencias], index=[0])
    df = df.transpose()
    df.columns = ['Equivalencias']
    df.to_excel(f".\\stats\\{arch}.xlsx", index = True, header = True)
