#!/usr/bin/env python3
import requests
import json
import re
from datetime import datetime

def fetch_proxies():
    """Obtiene proxies de Geonode API con filtros más flexibles"""
    url = "https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc"
    
    try:
        print("🔍 Fetching proxies from Geonode API...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        proxies = []
        valid_count = 0
        
        for proxy in data.get('data', []):
            try:
                # Debug: mostrar información del proxy
                ip = proxy.get('ip')
                port = proxy.get('port')
                protocols = proxy.get('protocols', [])
                uptime = proxy.get('uptime', 0)
                
                print(f"  Checking: {ip}:{port} - Protocols: {protocols} - Uptime: {uptime}%")
                
                # Condiciones más flexibles
                if (ip and port and protocols and 
                    any(p in ['http', 'https', 'socks4', 'socks5'] for p in protocols)):
                    
                    proxy_str = f"{ip}:{port}"
                    proxies.append(proxy_str)
                    valid_count += 1
                    print(f"  ✅ Added: {proxy_str}")
                    
            except Exception as e:
                print(f"  ❌ Error with proxy: {e}")
                continue
        
        print(f"✅ Found {valid_count} valid proxies from {len(data.get('data', []))} total")
        return proxies[:50]  # Limitar a 50 proxies
        
    except Exception as e:
        print(f"❌ Error fetching from API: {e}")
        # Fallback: retornar algunos proxies de respaldo
        return get_fallback_proxies()

def get_fallback_proxies():
    """Proxies de respaldo en caso de que la API falle"""
    fallback_proxies = [
        "45.95.147.218:8080",
        "45.95.147.221:8080",
        "45.95.147.222:8080",
        "45.95.147.226:8080",
        "45.95.147.228:8080",
        "45.95.147.230:8080",
        "45.95.147.231:8080",
        "45.95.147.232:8080"
    ]
    print(f"🔄 Using fallback proxies: {len(fallback_proxies)} proxies")
    return fallback_proxies

def update_pac_file(proxies):
    """Actualiza el archivo PAC con nuevos proxies"""
    try:
        with open('proxy.pac', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Si no hay proxies de la API, usar fallback
        if not proxies:
            print("⚠️ No proxies from API, using fallback")
            proxies = get_fallback_proxies()
            
        # Crear array JavaScript con los proxies
        proxies_js = ',\n        '.join([f'"{proxy}"' for proxy in proxies])
        
        # Reemplazar la sección de proxies
        new_content = re.sub(
            r'var proxies = \[[\s\S]*?\];',
            f'var proxies = [\n        {proxies_js}\n    ];',
            content
        )
        
        # Agregar timestamp de actualización
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        new_content = re.sub(
            r'// Última actualización:.*',
            f'// Última actualización: {timestamp}',
            new_content
        )
        
        # Agregar contador de proxies
        new_content = re.sub(
            r'// Proxy Auto-Config file.*',
            f'// Proxy Auto-Config file - {len(proxies)} proxies activos',
            new_content
        )
        
        with open('proxy.pac', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"📝 Updated PAC file with {len(proxies)} proxies")
        return True
        
    except Exception as e:
        print(f"❌ Error updating PAC file: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting proxy update...")
    proxies = fetch_proxies()
    if update_pac_file(proxies):
        print("✅ Update completed successfully")
        exit(0)
    else:
        print("❌ Update failed")
        exit(1)
