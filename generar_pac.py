import requests
import random
import json

# URL de la lista de proxies
url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"

# Descargar la lista de proxies
response = requests.get(url)
proxies_raw = response.text.strip().splitlines()

# Convertir cada línea a una cadena con el formato "PROXY IP:PUERTO"
proxies = []
for line in proxies_raw:
    # Si la línea ya contiene el protocolo en mayúsculas ("HTTP", "SOCKS4", etc.), se usa tal cual
    if not line.startswith("PROXY "):
        proxies.append("PROXY " + line)
    else:
        proxies.append(line)

# Opcional: limitar el número de proxies (por ejemplo, a 50) para evitar que el archivo sea muy pesado
max_proxies = 50
if len(proxies) > max_proxies:
    proxies = proxies[:max_proxies]

# Crear el contenido del archivo PAC. Se genera un arreglo en JavaScript con la lista de proxies.
# La función elige uno al azar cada vez que se consulta el PAC.
pac_content = f"""
function FindProxyForURL(url, host) {{
    var proxies = {json.dumps(proxies)};
    // Seleccionar un proxy al azar
    var index = Math.floor(Math.random() * proxies.length);
    return proxies[index] + "; DIRECT";
}}
"""

# Guardar el archivo PAC
with open("proxy.pac", "w") as f:
    f.write(pac_content)

print("Archivo 'proxy.pac' generado correctamente.")
