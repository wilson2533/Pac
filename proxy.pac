// Proxy Auto-Config file - 10 PUBLIC proxies
// Última actualización: 2025-12-20 12:22:26 UTC

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
    ];
    
    if (proxies.length === 0) {
        return "DIRECT";
    }
    
    // Selección aleatoria para balancear carga
    var randomIndex = Math.floor(Math.random() * proxies.length);
    return proxies[randomIndex];
}
