import requests

API_KEY = "0def34d8-b7d3-4207-a894-d5a87bb07b4e"
BASE_URL = "https://graphhopper.com/api/1/route"

def obtener_ruta(origen, destino, medio):
    params = {
        "point": [origen, destino],
        "vehicle": medio,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    return response.json()

def mostrar_resultados(data):
    path = data["paths"][0]

    distancia_metros = path["distance"]
    distancia_km = distancia_metros / 1000
    distancia_millas = distancia_km * 0.621371

    duracion_segundos = path["time"] / 1000
    horas = int(duracion_segundos // 3600)
    minutos = int((duracion_segundos % 3600) // 60)

    print("\n📏 Distancia del viaje:")
    print(f" - Kilómetros : {distancia_km:.2f} km")
    print(f" - Millas     : {distancia_millas:.2f} mi")

    print("\n⏱️ Duración estimada:")
    print(f" - {horas} horas y {minutos} minutos")

    print("\n🧭 Narrativa del viaje:")
    for instruccion in path["instructions"]:
        print(f" - {instruccion['text']} ({instruccion['distance'] / 1000:.2f} km)")

def menu():
    print("\nSeleccione medio de transporte:")
    print("1 - Auto")
    print("2 - Bicicleta")
    print("3 - Peatón")
    print("v - Volver / Salir")

    opcion = input("Opción: ").lower()

    if opcion == "1":
        return "car"
    elif opcion == "2":
        return "bike"
    elif opcion == "3":
        return "foot"
    elif opcion == "v":
        return "v"
    else:
        print("❌ Opción inválida")
        return None

def main():
    print("🌎 Calculador de Rutas Chile - Argentina (GraphHopper)")
    print("Presione 'v' en cualquier momento para salir\n")

    while True:
        origen = input("Ciudad de Origen: ")
        if origen.lower() == "v":
            break

        destino = input("Ciudad de Destino: ")
        if destino.lower() == "v":
            break

        medio = menu()
        if medio == "v":
            break
        if not medio:
            continue

        try:
            resultado = obtener_ruta(origen, destino, medio)
            if "paths" in resultado:
                mostrar_resultados(resultado)
            else:
                print("❌ Error al obtener la ruta. Verifique las ciudades.")
        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    main()
