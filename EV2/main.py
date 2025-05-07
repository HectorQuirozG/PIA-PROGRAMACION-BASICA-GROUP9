import funcs

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
            funcs.convert(url)
        elif op == 2:
            funcs.stats(url)
        elif op == 3:
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    try:
        main()
    except:
        print("Ocurrió algo inesperado")
        print("Saliendo...")

