
# [Opcional] Tarea Avanzada: Implementación de Herramientas de Threat Intelligence

En esta tarea opcional se propone al alumno la implementación de un conjunto de herramientas de threat intelligence que serán aprovechadas por los agentes de IA que implementaremos a continuación.

## Objetivo de la Tarea

El objetivo principal es desarrollar capacidades de análisis de amenazas mediante la creación de herramientas que permitan:

1. Análisis Automático de Indicadores de Compromiso (IOCs)

Implementar detección automática del tipo de indicador (IP, URL, hash, dominio)

Crear funciones de validación y clasificación de diferentes tipos de IOCs

Establecer patrones de reconocimiento para identificar amenazas potenciales

2. Integración con APIs de Threat Intelligence

Conectar con servicios públicos como AbuseIPDB para enriquecer el análisis de IPs

Implementar manejo de respuestas API y gestión de errores

Establecer sistemas de puntuación y clasificación de amenazas

3. Análisis de Reputación Web

Desarrollar algoritmos básicos para evaluar la reputación de URLs y dominios

Implementar detección de patrones sospechosos en nombres de dominio

Crear sistemas de alerta basados en características estructurales

4. Capacidades OSINT Básicas

Implementar búsquedas de patrones conocidos de amenazas

Desarrollar sistemas de correlación de indicadores

Crear mecanismos de enriquecimiento de contexto

## Aplicación Práctica

Las herramientas implementadas servirán como base para los agentes especializados que se desarrollarán posteriormente, proporcionando capacidades de:

- Enriquecimiento automático de alertas de seguridad
- Análisis contextual de indicadores sospechosos
- Soporte para toma de decisiones en respuesta a incidentes
- Integración con flujos de trabajo de SOC (Security Operations Center)

## Código fuente de las herramientas

```Python
# 4. Threat Intelligence@tool
def threat_intel_lookup(indicator: str, intel_type: str = "auto") -> str:
    """Busca threat intelligence usando APIs públicas.  
  
    Args:
        indicator: IOC a investigar
        intel_type: Tipo ('ip', 'url', 'hash' o 'auto')  
      
    Returns:
        Información de threat intelligence
    """
  
    try:
        if intel_type == "auto":
            intel_type = _detect_indicator_type(indicator)      
        
      	results = []      

		# AbuseIPDB para IPs
        if intel_type == "ip" and config.ABUSEIPDB_API_KEY:
            abuse_result = _check_abuseipdb(indicator)
            results.append(f"🛡️ AbuseIPDB: {abuse_result}")     
        
        # Análisis básico de URLs/dominios
        if intel_type in ["url", "domain"]:
            url_result = _analyze_url_reputation(indicator)
            results.append(f"🌐 URL Analysis: {url_result}")      
        
        # OSINT básico
        osint_result = _basic_osint(indicator)
        results.append(f"🔍 OSINT: {osint_result}")      
    
  		return f"""🔍 THREAT INTELLIGENCE:
🎯 Indicador: {indicator} ({intel_type.upper()})
📅 Análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{chr(10).join(results)}"""  
    
    except Exception as e:
        return f"❌ Error threat intel: {str(e)}"
    
def _detect_indicator_type(indicator: str) -> str:
    """Detecta automáticamente el tipo de indicador"""
    try:
        ipaddress.ip_address(indicator)
        return "ip"
    except ValueError:
        pass  
    
  	if indicator.startswith(('http://', 'https://')):
        return "url"
    elif '.' in indicator:
        return "domain"
    elif len(indicator) in [32, 40, 64]:
        return "hash"
    return "unknown"

def _check_abuseipdb(ip: str) -> str:
    """Consulta AbuseIPDB API"""
    try:
        headers = {'Key': config.ABUSEIPDB_API_KEY, 'Accept': 'application/json'}
        params = {'ipAddress': ip, 'maxAgeInDays': 90}    
    
      	response = requests.get(
            'https://api.abuseipdb.com/api/v2/check',
            headers=headers, params=params, timeout=10
        )      
    
      	if response.status_code == 200:
            data = response.json()['data']
            confidence = data.get('abuseConfidencePercentage', 0)
            country = data.get('countryCode', 'Unknown')          
        
          	level = "🔴 MALICIOSO" if confidence > 50 else "🟡 SOSPECHOSO" if confidence > 25 else "🟢 LIMPIO"
            return f"{level} - Confianza: {confidence}% - País: {country
          
        else:
            return f"Error {response.status_code}"  
  	except Exception as e:
        return f"Error: {str(e)}"

def _analyze_url_reputation(url: str) -> str:
    """Análisis básico de reputación URL"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path      

		suspicious_patterns = ['temp', 'test', 'suspicious', 'evil', 'malicious']      
		if any(pattern in domain.lower() for pattern in suspicious_patterns):
            return "🟡 PATRONES SOSPECHOSOS detectados"
        elif len(domain) < 5 or domain.count('-') > 3:
            return "🟡 DOMINIO SOSPECHOSO por estructura"
        else:
            return "🟢 DOMINIO SIN ALERTAS evidentes"   

	except Exception as e:
        return f"Error: {str(e)}"

def _basic_osint(indicator: str) -> str:
    """OSINT básico"""
    suspicious_patterns = ['temp', 'test', 'malicious', 'suspicious', 'evil', 'bad']  

	if any(pattern in indicator.lower() for pattern in suspicious_patterns):
        return "🟡 PATRONES SOSPECHOSOS en el indicador"
    else:
        return "🟢 Sin patrones sospechosos evidentes"
```
