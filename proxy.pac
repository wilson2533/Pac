// Proxy Auto-Config file - Actualizado automáticamente
// Última actualización: 2024-01-01 00:00:00 UTC

function FindProxyForURL(url, host) {
    // Dominios que NO usarán proxy
    var directHosts = [
        "localhost",
        "127.0.0.1",
        "*.local",
        "*.internal",
        "192.168.*",
        "10.*",
        "172.16.*", "172.17.*", "172.18.*", "172.19.*",
        "172.20.*", "172.21.*", "172.22.*", "172.23.*",
        "172.24.*", "172.25.*", "172.26.*", "172.27.*",
        "172.28.*", "172.29.*", "172.30.*", "172.31.*"
    ];
    
    // Verificar si el host está en la lista directa
    for (var i = 0; i < directHosts.length; i++) {
        if (shExpMatch(host, directHosts[i])) {
            return "DIRECT";
        }
    }
    
    // Usar la lista actualizada de proxies
    return "PROXY " + getRandomProxy();
}

function getRandomProxy() {
    // Lista de proxies actualizada automáticamente
    var proxies = [
        "45.95.147.218:8080",
        "45.95.147.221:8080",
        "45.95.147.222:8080"
    ];
    
    if (proxies.length === 0) {
        return "DIRECT";
    }
    
    // Selección aleatoria para balancear carga
    var randomIndex = Math.floor(Math.random() * proxies.length);
    return proxies[randomIndex];
}
