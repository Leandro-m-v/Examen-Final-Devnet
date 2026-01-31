import requests

API_KEY = "0def34d8-b7d3-4207-a894-d5a87bb07b4e"

GEOCODE_URL = "https://graphhopper.com/api/1/geocode"
ROUTE_URL = "https://graphhopper.com/api/1/route"

def geocodificar_ciudad(ciudad):
    params = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }

    response = requests.get(GEOCODE_URL, params=params)
    data = response.json()

    if "hits" not in data or len(data["hits"]) == 0:
        return None

    lat = data["hits"][0]["point"]["lat"]
    lon = data["hits"][0]["point"]["lng"]
    return f"{lat},{lon}"

def obtener_ruta(origen, destino, medio):
    params = {
        "point": [origen, destino],
        "vehicle": medio,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    response = requests.get(ROUTE_URL, params=params)
    return response.json()

def mostrar_resultados(data):
    path = data["paths"][0]

    distancia_m = path["distance"]
    distancia_km = distancia_m / 1000
    distancia_millas = distancia_km * 0.621371

    duracion_s = path["time"] / 1000
    horas = int(duracion_s // 3600)
    minutos = int((duracion_s % 3600) // 60)

    print("\n📏 Distancia del viaje:")
    print(f" - Kilómetros : {distancia_km:.2f} km")
    print(f" - Millas     : {distancia_millas:.2f} mi")

    print("\n⏱️ Duración estimada:")
    print(f" - {horas} horas y {minutos} minutos")

    print("\n🧭 Narrativa del viaje:")
    for inst in path["instructions"]:
        print(f" - {inst['text']} ({inst['distance']/1000:.2f} km)")

def menu_transporte():
    print("\nSeleccione medio de transporte:")
    print("1 - Auto")
    print("2 - Bicicleta")
    print("3 - Peatón")
    print("v - Volver / Salir")

    op = input("Opción: ").lower()

    if op == "1":
        return "car"
    elif op == "2":
        return "bike"
    elif op == "3":
        return "foot"
    elif op == "v":
        return "v"
    else:
        print("❌ Opción inválida")
        return None

def main():
    print("🌎 Calculador de Rutas Chile - Argentina (GraphHopper)")
    print("Presione 'v' en cualquier momento para salir\n")

    while True:
        origen_txt = input("Ciudad de Origen: ")
        if origen_txt.lower() == "v":
            break

        destino_txt = input("Ciudad de Destino: ")
        if destino_txt.lower() == "v":
            break

        origen = geocodificar_ciudad(origen_txt)
        destino = geocodificar_ciudad(destino_txt)

        if not origen or not destino:
            print("❌ No se pudo encontrar una de las ciudades.")
            continue

        medio = menu_transporte()
        if medio == "v":
            break
        if not medio:
            continue

        try:
            resultado = obtener_ruta(origen, destino, medio)
            if "paths" in resultado:
                mostrar_resultados(resultado)
            else:
                print("❌ Error al obtener la ruta.")
        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    main()
