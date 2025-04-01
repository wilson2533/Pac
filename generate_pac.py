import requests
import json

# URL de la API de Geonode
API_URL = "https://proxylist.geonode.com/api/proxy-list?protocols=https%2Chttp&google=false&limit=500&page=1&sort_by=responseTime&sort_type=asc"

try:
    # Obtener la lista de proxies desde la API
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    # Extraer proxies en formato "IP:PORT"
    proxies = [f"PROXY {proxy['ip']}:{proxy['port']}" for proxy in data.get('data', [])]

    if not proxies:
        raise ValueError("No se encontraron proxies en la respuesta de la API.")

    # Crear el contenido del archivo PAC
    pac_content = f"""function FindProxyForURL(url, host) {{
        var proxyList = {json.dumps(proxies, indent=4)};
        var randomIndex = Math.floor(Math.random() * proxyList.length);
        return proxyList[randomIndex];
    }}"""

    # Guardar el PAC en un archivo
    with open("proxy.pac", "w") as pac_file:
        pac_file.write(pac_content)

    print("✅ Archivo proxy.pac generado con éxito.")

except requests.exceptions.RequestException as e:
    print(f"❌ Error al obtener proxies: {e}")

except Exception as e:
    print(f"❌ Error general: {e}")
