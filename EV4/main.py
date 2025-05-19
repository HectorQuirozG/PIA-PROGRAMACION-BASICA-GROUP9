import source, cargas, datetime, sys, os

def main():
    ruta_script = os.path.abspath(sys.argv[0])
    carpeta_script = os.path.dirname(ruta_script)
    os.chdir(carpeta_script)

    if sys.stdout.isatty():
        print("""ADVERTENCIA:
Este script se está ejecutando desde un entorno de desarrollo genérico.
Algunas funciones gráficas o de archivo pueden fallar.
Se recomienda ejecutar el script desde la terminal o desde el explorador de archivos.""")
    url = "https://api.frankfurter.dev/v1/"
    while True:
        menu = """----------------------------
MENU
1. Cambiar moneda
2. Ver estadísticas históricas
3. Cargar archivo estadístico
4. Salir
Selecciona una opción: """
        mgraph = """----------------------
1. Grafíco lineal
2. Gráfico de barras
3. Gráfico horizontal
4. Diagrama de dispersión
Selecciona una opción: """
        try: op = int(input(menu))
        except(ValueError): op = None
        if op == 1:
            arch = "cache_currencies.txt"
            currencies = cargas.carga_cache_currencies(arch, url)
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
            rates = cargas.carga_cache_rates(arch, url, apend, base, change)
            conv = source.convert(base, change, qant, rates)
            print(f"\n${qant} {base} = ${conv} {change}\n")
        elif op == 2:
            while True:
                try:
                    print("1-)Corto plazo\n2-)Largo plazo")
                    a=int(input("Ingrese opcion deseada: "))
                    if (a==1 or a==2):
                        break
                    else:
                        print("Valor invalido")
                except ValueError:
                    print("Ingresar un número entero")
            if a == 1:
                flag = True
                while flag:
                    flag = True
                    while flag:
                        fecha1 = input("Ingresa la fecha inicial en formato YYYY-MM-DD: ")
                        if fecha1 == "Hoy":
                            fecha1 = str(datetime.date.today())
                        flag = source.valid_fecha(fecha1)
                    flag = True
                    while flag:
                        fecha2 = input("Ingresa la fecha final en formato YYYY-MM-DD: ")
                        if fecha2 == '':
                            fecha2 = fecha1
                        elif fecha2 == "Hoy":
                            fecha2 = str(datetime.date.today())
                        else:
                            flag = source.valid_fecha(fecha2)
                        flag = source.valid_rango(fecha1, fecha2)
                apend = f"{fecha1}..{fecha2}"
                print("Monedas disponibles: ")
                monedas = source.divis_fecha(url, apend, fecha1)
                for i in monedas:
                    print(i)
                flag = True
                while flag:
                    base = input("Selecciona una moneda: ")
                    flag = source.valid_mon(base, monedas)
                apend += f"?base={base}"
                datos, history, fechas = source.registro(url, apend, base)
                stats = source.stats((datos, history), base, fecha1, fecha2)
                print("Un gráfico está a punto de generarse...")
                while True:
                    try:
                        formato = int(input(mgraph))
                        if formato >= 1 and formato <= 4:
                            break
                    except ValueError: print("Opción inválida")
                source.graficar_fechas(fechas, history, base, formato)
                for k, v in stats.items():
                    print(f"{k}: {v}")
                equivalencias = source.zipeo(fechas, history)
                print("Advertencia: Algunas fechas no están registradas debido a que fueron días feriados")
                print("\n")
                while True:
                    op = input("¿Desea guardar la información? (Y/N): ")
                    if op == "Y":
                        arch = f"{base}_stats_{fecha1}..{fecha2}"
                        cargas.guardar_stats(arch, equivalencias, stats, base)
                        cargas.generar_excel(arch, equivalencias)
                        break
                    elif op == "N":
                        break
                    else: print("Opción inválida")        
            elif a == 2:
                monedasd=["EUR", "USD", "GBP", "JPY"]
                print("monedas disponibles: ")
                for i in range(len(monedasd)):
                    print(monedasd[i])
                while True:
                    base = input("Selecciona una moneda base: ")
                    if base in monedasd:
                        break
                    else:
                        print("Moneda invalida")
                flag = True
                while flag:
                    flag = True
                    while flag:
                        fecha1 = input("Ingresa la fecha inicial en formato YYYY-MM-DD: ")
                        if fecha1 == "Hoy":
                            fecha1 = str(datetime.date.today())
                        flag = source.valid_fecha(fecha1)
                    flag = True
                    while flag:
                        fecha2 = input("Ingresa la fecha final en formato YYYY-MM-DD: ")
                        if fecha2 == '':
                            fecha2 = fecha1
                        elif fecha2 == "Hoy":
                            fecha2 = str(datetime.date.today())
                        flag = source.valid_fecha(fecha2)
                apend = f"{fecha1}..{fecha2}?base={base}"
                data,fechas, history = source.registro_largoplazo(url, apend, base)
                print("Un gráfico está a punto de generarse...")
                while True:
                    try:
                        formato = int(input(mgraph))
                        if formato >= 1 and formato <= 4:
                            break
                    except ValueError: print("Opción inválida")
                source.graficar_fechaslargoplazo(fechas,history,base,formato)
                stats = source.stats((data, history), base, fecha1, fecha2)
                equivalencias = source.zipeo(fechas, history)
                for k, v in stats.items():
                    print(f"{k}: {v}")
                print("Advertencia: Algunas fechas no están registradas debido a que fueron días feriados")
                print("\n")
                while True:
                    op = input("¿Desea guardar la información? (Y/N): ")
                    if op == "Y" or op == "y":
                        arch = f"{base}_stats_{fecha1}..{fecha2}.txt"
                        cargas.guardar_stats(arch, equivalencias, stats, base)
                        cargas.generar_excel(arch, equivalencias)
                        break
                    elif op == "N" or op == "n":
                        break
                    else: print("Opción inválida")
        elif op == 3:
            arch = cargas.buscar_arch()
            flag = source.validar_arch(arch)
            if flag:
                try:
                    base = source.buscar_base(arch)
                    equivalencias = cargas.procesar_equivalencias(arch)
                    fechas = list()
                    for i in equivalencias.keys():
                        fechas.append(i)
                    history = list()
                    for i in equivalencias.values():
                        history.append(i)
                    print("Un gráfico está a punto de generarse...")
                    while True:
                        try:
                            formato = int(input(mgraph))
                            if formato >= 1 and formato <= 4:
                                break
                        except ValueError: print("Opción inválida")
                    source.graficar_fechaslargoplazo(fechas, history, base, formato)
                    stats = cargas.procesar_stats(arch)
                    print(f"----- Estadísticas {base} -----")
                    for k, v in stats.items():
                        print(f"{k}: {v}")
                except: print("Ocurrió un error inesperado. Es posible que el archivo esté dañado.")
        elif op == 4:
            print("Saliendo...")
            break
        else:
            print("Opción inválida")
    return op    

if __name__ == "__main__":
    while True:
        try:
            cmd = main()
            if cmd == 4: break
        except: print("Ocurrió algo inesperado")
