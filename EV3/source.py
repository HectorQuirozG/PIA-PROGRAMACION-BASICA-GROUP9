import requests, re, datetime, statistics
import numpy as np

def valid_mon(a, currencies):
    if a in currencies:
        flag = False
    else:
        print("No encontrado, revisa la entrada")
        flag = True
    return flag

def acortar(equi, qant = 1):
    x = 2
    while round(equi*qant, x) == 0:
        x += 1
    acortado = round(equi*qant, x)
    return acortado

def convert(base, change, qant, rates):
    equi = float(rates[f'{base}, {change}'])
    conv = acortar(equi, qant)
    return conv

def valid_fecha_format(fecha):
    fech = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    mo = fech.search(fecha)
    try:
        if mo != None:
            verf = datetime.date(int(mo.group(1)), int(str(mo.group(2))), int(str(mo.group(3))))
            return verf
    except ValueError: print("Los meses o días están fuera de rango")
    
def valid_fecha(fecha):
    flag = True
    verf = valid_fecha_format(fecha)
    if verf != None:
        if verf < datetime.date(1999, 1, 4):
            print("La fecha más antigua es 1999-01-04")
        elif verf > datetime.date.today():
            print("La fecha debe ser igual o anterior a la actual")
        else: flag = False
    else: print("Fecha inválida")
    return flag

def valid_rango(fecha1, fecha2):
    flag = True
    verf1 = valid_fecha_format(fecha1)
    verf2 = valid_fecha_format(fecha2)
    if verf2 < verf1:
        print("La fecha final debe ser posterior a la inicial")
    elif verf2 - verf1 > datetime.timedelta(days = 30):
        print("El rango máximo es de 30 días")
    else: flag = False
    return flag

def divis_fecha(url, apend, fecha1):
    response = requests.get(url + apend)
    if response.status_code == 200:
        data = response.json()
        verf = fecha1
        while True:
            try:
                monedas = list((data['rates'][verf]).keys()) + ["EUR"]
                monedas.sort()
            except KeyError:
                mo = valid_fecha_format(verf)
                mo -= datetime.timedelta(days = 1)                   
                verf = str(mo)
            else:
                break
    else: print(f"Ocurrió un error inesperado #{response.status_code}")
    return monedas

def registro(url, apend, base):
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
    return data, history

def buscar_fecha(valor, data):
    for k, v in data.items():
        if type(v) == dict:
            for x, y in v.items():
                if type(y) == dict:
                    for a, b in y.items():
                        if b == valor:
                            valor = x
    return valor

def stats(datos, base, fecha1, fecha2):
    stats = {'Base': base,
             'Fecha inicial': fecha1,
             'Fecha final': fecha2,
             }
    print("--- Estadísticas ---")
    maxi = max(datos[1])
    mini = min(datos[1])
    fech_max = buscar_fecha(maxi, datos[0])
    fech_min = buscar_fecha(mini, datos[0])
    stats['Máximo valor'] = fech_max
    stats['Mínimo valor'] = fech_min
    if base != "USD":
        media = statistics.mean(datos[1])
        mediana = statistics.median(datos[1])
        stats['Valor promedio'] = f"${acortar(media)} USD"
        stats['Valor medio'] = f"${acortar(mediana)} USD"
        if len(datos[1]) > 1:
            rang = maxi - mini
            varianza = np.var(datos[1])
            desv_media = np.sqrt(varianza)
            stats['Diferencia'] = f"${acortar(rang)} USD"
            stats['Varianza'] = f"${acortar(varianza)} USD"
            stats['Desviación media'] = f"${acortar(desv_media)} USD"
    return stats
