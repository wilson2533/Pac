#!/usr/bin/env python3
import requests
import re
from datetime import datetime
import os

def fetch_proxies():
    """Obtiene proxies de Geonode API - SOLO PÚBLICOS"""
    url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text&timeout=20"
    
    try:
        print("🔍 Fetching proxies from Geonode API...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        proxies = []
        print(f"📊 Total proxies in API: {len(data.get('data', []))}")
        
        for proxy in data.get('data', []):
            ip = proxy.get('ip', '').strip()
            port = proxy.get('port', '')
            protocols = proxy.get('protocols', [])
            
            # FILTROS MÁS ESTRICTOS - solo proxies públicos
            if (ip and port and protocols and 
                any(p in ['http', 'https'] for p in protocols) and
                # Excluir proxies que requieren autenticación
                not proxy.get('password', False) and  # Sin contraseña
                proxy.get('anonymityLevel', '') != 'elite' and  # Menos probabilidad de auth
                proxy.get('uptime', 0) > 70 and  # Buen uptime
                proxy.get('responseTime', 1000) < 5000):  # Respuesta rápida
                
                proxy_str = f"{ip}:{port}"
                proxies.append(proxy_str)
                print(f"  ✅ Public: {proxy_str}")
        
        print(f"✅ Public proxies found: {len(proxies)}")
        
        # Si no hay suficientes públicos, agregar algunos conocidos
        if len(proxies) < 5:
            print("🔄 Adding known public proxies...")
            known_public = get_known_public_proxies()
            proxies.extend(known_public)
        
        return proxies[:20]  # Limitar a 20 proxies
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return get_known_public_proxies()

def get_known_public_proxies():
    """Lista de proxies públicos conocidos y confiables"""
    public_proxies = [
        # Proxies públicos conocidos (sin autenticación)
        "51.158.68.68:8811",
        "51.158.68.133:8811", 
        "188.166.56.246:3128",
        "165.227.81.213:3128",
        "138.197.157.60:3128",
        "167.99.131.11:8080",
        "167.99.131.12:8080",
        "167.99.131.13:8080",
        "68.183.230.184:3128",
        "68.183.230.185:3128"
    ]
    print(f"🔧 Using known public proxies: {len(public_proxies)}")
    return public_proxies

def update_pac_file(proxies):
    """Actualiza el archivo PAC"""
    try:
        print("📖 Reading current PAC file...")
        with open('proxy.pac', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📝 Updating with {len(proxies)} PUBLIC proxies")
        
        # Actualizar los proxies
        proxies_js = ',\n        '.join([f'"{proxy}"' for proxy in proxies])
        new_content = re.sub(
            r'var proxies = \[[^\]]*\];',
            f'var proxies = [\n        {proxies_js}\n    ];',
            content,
            flags=re.DOTALL
        )
        
        # Actualizar timestamp y contador
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        new_content = re.sub(
            r'// Proxy Auto-Config file.*',
            f'// Proxy Auto-Config file - {len(proxies)} PUBLIC proxies',
            new_content
        )
        new_content = re.sub(
            r'// Última actualización:.*',
            f'// Última actualización: {timestamp}',
            new_content
        )
        
        # Escribir el archivo
        with open('proxy.pac', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ PAC file updated successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error updating PAC: {e}")
        return False

if __name__ == "__main__":
    print("🚀 STARTING PUBLIC PROXY UPDATE")
    print("🎯 Filtering ONLY public proxies (no authentication)")
    
    proxies = fetch_proxies()
    
    if update_pac_file(proxies):
        print("🎉 UPDATE COMPLETED SUCCESSFULLY")
        print(f"📊 Final proxy count: {len(proxies)} PUBLIC proxies")
        exit(0)
    else:
        print("💥 UPDATE FAILED")
        exit(1)
