#!/usr/bin/env python3
import requests
import json
import re
from datetime import datetime

def fetch_proxies():
    """Obtiene proxies de Geonode API"""
    url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        proxies = []
        for proxy in data.get('data', []):
            if (proxy.get('protocols') and 
                'http' in proxy.get('protocols', []) and 
                proxy.get('ip') and 
                proxy.get('port')):
                
                proxy_str = f"{proxy['ip']}:{proxy['port']}"
                proxies.append(proxy_str)
        
        return proxies[:100]  # Limitar a 100 proxies
        
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

def update_pac_file(proxies):
    """Actualiza el archivo PAC con nuevos proxies"""
    with open('proxy.pac', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Crear array JavaScript con los proxies
    proxies_js = ',\n        '.join([f'"{proxy}"' for proxy in proxies])
    
    # Reemplazar la sección de proxies
    new_content = re.sub(
        r'var proxies = \[\s*.*?\s*\];',
        f'var proxies = [\n        {proxies_js}\n    ];',
        content,
        flags=re.DOTALL
    )
    
    # Agregar timestamp de actualización
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_content = re.sub(
        r'// Esta función será actualizada automáticamente.*',
        f'// Actualizado automáticamente el {timestamp}',
        new_content
    )
    
    with open('proxy.pac', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated PAC file with {len(proxies)} proxies")

if __name__ == "__main__":
    proxies = fetch_proxies()
    if proxies:
        update_pac_file(proxies)
    else:
        print("No proxies found, keeping existing list")
