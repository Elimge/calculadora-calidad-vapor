# Este programa te ayudará a analizar tablas de agua saturada y calcular la calidad del vapor a partir de la base de datos

import csv
import os

# Detectar la ruta absoluta de este archivo csv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(BASE_DIR, 'datos_vapor.csv')

# Función para interpolar valores
def interpolar(x, x1, x2, y1, y2):
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

print("---------------------------------------------------------------------")
print("|                   Calculadora de Calidad del Vapor                |")
print("|-------------------------------------------------------------------|")
print("|   Este programa te ayudará a analizar tablas de agua saturada     |")
print("|   y calcular la calidad del vapor a partir de la base de datos    |")
print("---------------------------------------------------------------------")


print("\nInstrucciones de uso:")
print("1. Ingresa '1' para obtener los datos establecidos en la base de datos.")
print("2. Ingresa '2' para calcular la calidad del vapor según la presión del sistema.")
print("3. Escribe 'salir' en cualquier momento para finalizar el programa. \n" )

while True:

    # Menú principal
    print("\n¿Qué deseas realizar?")
    print("1. Obtener el dato de las variables según la presión del sistema")
    print("2. Calcular la calidad del vapor según la presión, la  temperatura y la entalpía del sistema.\n") 

    decision_menu = input("Escribe 1 ó 2 y presiona Enter (Escribe 'salir' para finalizar el programa): ").lower()

    if decision_menu == "1": 

        # Opción 1: Obtener datos de la base de datos

        with open(ARCHIVO, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)    #DictReader aplica la primera linea como cabecera y asigna esos strings como nombre de las columnas
            dato_presion = input("Ingrese la presión del vapor (Kpa): ")

            # Lectura de los datos del CSV
            dato_encontrado = False
            for fila in lector:

                if fila['Presion_kPa'] == dato_presion:
                    print(
                    f"\nPresión: {fila['Presion_kPa']} KPa \n"
                    f"Temperatura de saturación: {fila['Temperatura_C']} °C \n"
                    f"Volumen en líquido saturado: {fila['vf_m3kg']} m\u00B3/kg \n"
                    f"Volumen en vapor saturado: {fila['vg_m3kg']} m\u00B3/kg \n"
                    f"Entalpía en líquido saturado: {fila['hf_kJkg']} kJ/kg \n"
                    f"Entalpía en vapor saturado: {fila['hg_kJkg']} kJ/kg \n"
                    f"Entropía en líquido saturado: {fila['sf_kJkgK']} kJ/kg * K \n"
                    f"Entropía en vapor saturado: {fila['sg_kJkgK']} kJ/kg * K \n"
                    )
                    dato_encontrado = True
                    break
            if not dato_encontrado:    
                print("\nHas ingresado un dato no incluido en la base de datos o un dato no válido.\n")
                    

    elif decision_menu == "2":

        # Opción 2: Calcular la calidad del vapor

        print("\nPara calcular la calidad del vapor, ingresa los siguientes datos:")
        while True:
            try: 
            # Datos del sistema
                presion_input = input("Ingresa la presión del sistema (kPa): ")         
                temperatura_input = input("Ingresa la temperatura del vapor (°C): ")      
                entalpia_input = input("Ingresa la entalpía del sistema (Kj/Kg): ")        

                presion_input = float(presion_input)     
                temperatura_input = float(temperatura_input)    
                entalpia_input = float(entalpia_input)  
                break
            except ValueError:
                print("Error: Debes ingresar un dato válido.")
                continue
            
        # Leer datos del CSV
        datos = []
        with open(ARCHIVO, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            next(lector)  # Saltar la cabecera de la base de datos
            for fila in lector:
                datos.append([float(x) for x in fila])

        # Buscar las dos filas entre las que está la presión
        fila1 = fila2 = None
        for i in range(len(datos) - 1):
            if datos[i][0] <= presion_input <= datos[i+1][0]:
                fila1 = datos[i]
                fila2 = datos[i+1]
                break

        if fila1 and fila2:
            # Interpolar T_sat, hf, hg
            p1 = fila1[0]
            p2 = fila2[0]
            T_sat = interpolar(presion_input, p1, p2, fila1[1], fila2[1])
            hf = interpolar(presion_input, p1, p2, fila1[4], fila2[4])
            hg = interpolar(presion_input, p1, p2, fila1[5], fila2[5])
            
            print(f"Presión ingresada: {presion_input} kPa")
            print(f"Temperatura de saturación interpolada: {T_sat:.2f} °C")
            
           ## Calcular calidad del vapor
            if abs(temperatura_input - T_sat) < 1.5:
                hfg = hg - hf
                x = (entalpia_input - hf) / hfg
                if 0 <= x <= 1:
                    print(f"Calidad del vapor: {x:.4f} ó {x*100:.2f}% vapor, {100 - x*100:.2f}% líquido")
                else:
                    print("Entalpia ingresada fuera de rango.")
            elif temperatura_input < T_sat:
                print("Estado: líquido comprimido (no se puede calcular calidad del vapor).")
            else:
                print("Estado: vapor sobrecalentado (no se puede calcular calidad del vapor).")
        else:
            print("No se encontró un rango de presión adecuado en la tabla.")

    elif decision_menu == "salir":
        print("Gracias por usar la calculadora de calidad del vapor. ¡Hasta luego!")
        break
    
    else:
        print("\nOpción no válida. Por favor, elige '1', '2' o 'salir'.")
    print("---------------------------------------------------------------------")  