import os
import json
import csv
import random
import time

os.system("cls")


def leerJson(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def guardarJson(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def guardar_csv(file_path, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Tienda ID", "Sueldo más alto", "Sueldo más bajo", "Promedio de sueldos", "Número de ventas", "Promedio de ventas"])
        writer.writerows(data)


def precargar_ventas(ventas, cantidad=500):
    for _ in range(cantidad):
        venta = {
            "id_venta": str(1000000 + len(ventas["ventas"]) + 1),
            "id_vendedor": random.choice(vendedores)["id_vendedor"],
            "id_tienda": random.choice(tiendas)["id_tienda"],
            "fecha": "04-07-2024",
            "total_venta": round(random.uniform(100000, 300000), -2)
        }
        ventas["ventas"].append(venta)
    guardarJson('ventas.json', ventas)
    print(f"{cantidad} ventas precargadas.")


def crear_venta():
    id_vendedor = input("Ingrese el ID del vendedor: ")
    vendedor = next((v for v in vendedores if v["id_vendedor"] == id_vendedor), None)
    if vendedor:
        venta = {
            "id_venta": str(1000000 + len(ventas["ventas"]) + 1),
            "id_vendedor": id_vendedor,
            "id_tienda": vendedor["id_tienda"],
            "fecha": "04-07-2024",
            "total_venta": round(random.uniform(100000, 300000), -2)
        }
        ventas["ventas"].append(venta)
        guardarJson('ventas.json', ventas)
        print("Venta creada: ", venta)
    else:
        print("Vendedor no encontrado.")


def calcular_sueldos_por_tienda():
    sueldos_por_tienda = {}
    for vendedor in vendedores:
        tienda_id = vendedor["id_tienda"]
        if tienda_id not in sueldos_por_tienda:
            sueldos_por_tienda[tienda_id] = []
       
        total_ventas = sum(venta["total_venta"] for venta in ventas["ventas"] if venta["id_vendedor"] == vendedor["id_vendedor"])
        bono = 0
        if total_ventas > 5000000:
            bono = total_ventas * 0.15
        elif total_ventas > 3000000:
            bono = total_ventas * 0.12
        elif total_ventas > 1000000:
            bono = total_ventas * 0.10
       
        sueldo_bruto = vendedor["sueldo_base"]
        salud = sueldo_bruto * 0.07
        afp = sueldo_bruto * 0.12
        sueldo_liquido = (sueldo_bruto - salud - afp) + bono


        sueldos_por_tienda[tienda_id].append({
            "id_vendedor": vendedor["id_vendedor"],
            "nombre": vendedor["nombre"],
            "apellido": vendedor["apellido"],
            "sueldo_bruto": sueldo_bruto,
            "salud": salud,
            "afp": afp,
            "bono": bono,
            "sueldo_liquido": sueldo_liquido
        })
    return sueldos_por_tienda


def reporte_sueldos():
    sueldos_por_tienda = calcular_sueldos_por_tienda()
    for tienda_id, sueldos in sueldos_por_tienda.items():
        print(f"\nTienda ID: {tienda_id}")
        for sueldo in sueldos:
            print(sueldo)


def mostrar_estadisticas():
    sueldos_por_tienda = calcular_sueldos_por_tienda()
    estadisticas = []
    for tienda in tiendas:
        tienda_id = tienda["id_tienda"]
        sueldos = [sueldo["sueldo_liquido"] for sueldo in sueldos_por_tienda[tienda_id]]
        ventas_tienda = [venta["total_venta"] for venta in ventas["ventas"] if venta["id_tienda"] == tienda_id]


        if sueldos:
            max_sueldo = max(sueldos)
            min_sueldo = min(sueldos)
            avg_sueldo = sum(sueldos) / len(sueldos)
        else:
            max_sueldo = min_sueldo = avg_sueldo = 0
       
        if ventas_tienda:
            num_ventas = len(ventas_tienda)
            avg_ventas = sum(ventas_tienda) / num_ventas
        else:
            num_ventas = avg_ventas = 0
       
        estadisticas.append([
            tienda_id,
            max_sueldo,
            min_sueldo,
            avg_sueldo,
            num_ventas,
            avg_ventas
        ])
        print(f"\nTienda: {tienda['nombre']}")
        print(f"Sueldo más alto: {max_sueldo}")
        print(f"Sueldo más bajo: {min_sueldo}")
        print(f"Promedio de sueldos: {avg_sueldo}")
        print(f"Número de ventas: {num_ventas}")
        print(f"Promedio de ventas: {avg_ventas}")


    guardar_csv('estadisticas.csv', estadisticas)


tiendas = leerJson('tiendas.json')
vendedores = leerJson('vendedores.json')
ventas = leerJson('ventas.json')




def menu():
        print("=========Menú=========")
        print("1. Precargar ventas")
        print("2. Crear nueva venta")
        print("3. Reporte de sueldos")
        print("4. Ver estadísticas")
        print("5. Salir")

def error():
    os.system("cls")
    print("La opción ingresada no es válida, intente nuevamente.")
    time.sleep(1.5)
    os.system("cls")

def main():
    while True:
        menu()
        try:
            opc1= int(input("Ingrese una opción >> "))
            if opc1 < 1 or opc1 > 5:
                error()
            else:
                if opc1 == 1:
                    precargar_ventas(ventas)
                elif opc1 == 2:
                    crear_venta()
                elif opc1 == 3:
                    reporte_sueldos()
                elif opc1 == 4:
                    mostrar_estadisticas()
                elif opc1 == 5:
                    os.system("cls")
                    print("Saliendo de la aplicación...")
                    time.sleep(2)
                    os.system("cls")
                    break
        except:
            error()


if __name__ == "__main__":
    main()





