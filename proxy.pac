function FindProxyForURL(url, host) {
    // Dominios que NO usarán proxy (opcional)
    var directHosts = [
        "localhost",
        "127.0.0.1",
        "*.local",
        "google.com",
        "github.com"
    ];
    
    // Verificar si el host está en la lista directa
    for (var i = 0; i < directHosts.length; i++) {
        if (shExpMatch(host, directHosts[i])) {
            return "DIRECT";
        }
    }
    
    // Lista de proxies (se actualizará automáticamente)
    var proxies = getProxies();
    
    if (proxies.length > 0) {
        // Seleccionar proxy aleatorio para balancear carga
        var randomProxy = proxies[Math.floor(Math.random() * proxies.length)];
        return "PROXY " + randomProxy;
    }
    
    // Si no hay proxies disponibles, conexión directa
    return "DIRECT";
}

function getProxies() {
    try {
        // Aquí iría la lógica para obtener proxies de la API
        // Nota: PAC standard no permite fetch HTTP, necesitarías un servicio intermedio
        return [
            "192.168.1.1:8080",
