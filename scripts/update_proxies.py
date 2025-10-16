#!/usr/bin/env python3
import requests
import json
import re
from datetime import datetime

def fetch_proxies():
    """Obtiene proxies de Geonode API"""
    url = "https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc"
    
    try:
        print("🔍 Fetching proxies from Geonode API...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        proxies = []
        for proxy in data.get('data', []):
            # Filtrar solo proxies HTTP/HTTPS que estén activos
            if (proxy.get('protocols') and 
                any(p in ['http', 'https'] for p in proxy.get('protocols', [])) and 
                proxy.get('ip') and 
                proxy.get('port') and
                proxy.get('uptime', 0) > 80):  # Solo proxies con >80% uptime
                
                proxy_str = f"{proxy['ip']}:{proxy['port']}"
                proxies.append(proxy_str)
        
        print(f"✅ Found {len(proxies)} valid proxies")
        return proxies[:30]  # Limitar a 30 proxies para mejor rendimiento
        
    except Exception as e:
        print(f"❌ Error fetching proxies: {e}")
        return []

def update_pac_file(proxies):
    """Actualiza el archivo PAC con nuevos proxies"""
    try:
        with open('proxy.pac', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not proxies:
            print("⚠️ No proxies to update")
            return False
            
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
    else:
        print("❌ Update failed")
        exit(1)
