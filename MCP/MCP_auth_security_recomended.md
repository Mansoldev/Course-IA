
# Mecanismos recomendados de autenticación para MCP

La autenticación en servidores MCP es uno de los aspectos más relevantes a la hora de configurar un entorno seguro. A continuación os dejo los mecanismo más recomendados con referencias para poder ampliar información.

## 1 Tres Patrones Principales de Autenticación

FastMCP ofrece tres niveles complementarios de autenticación basados en la responsabilidad que asume tu servidor FastMCPMedium:

### A. Bearer Token / JWT Verification (Recomendado para la mayoría)

Este patrón valida tokens JWT emitidos por un proveedor externo, actuando tu servidor como servidor de recursos que confía en tokens firmados por un emisor conocido Secure Your FastMCP Server: 3 Auth Patterns That Scale | by Guangya Liu | Aug, 2025 | Medium.

Ventajas:

- Mínima complejidad de implementación Authentication - FastMCP
- Ideal si ya tienes un IdP o API Gateway emitiendo JWTs
- Proporciona seguridad basada en tokens con cifrado asimétrico RSA FastMCP Bearer Token Authentication Quick Start | by Guangya Liu | Medium

Casos de uso:

- Microservicios que necesitan validación consistente Secure Your FastMCP Server: 3 Auth Patterns That Scale | by Guangya Liu | Aug, 2025 | Medium
- Ya existe infraestructura de autenticación establecida
- Necesitas el menor overhead de implementación

### B. OAuth Proxy (Para proveedores tradicionales)

Permite que servidores FastMCP se autentiquen con proveedores OAuth que no soportan Dynamic Client Registration (DCR), incluyendo prácticamente todos los proveedores tradicionales: GitHub, Google, Azure, AWS, Discord, Facebook y la mayoría de sistemas empresariales OAuth Proxy - FastMCP.

Funcionalidad clave:

- Presenta una interfaz compatible con DCR a clientes MCP mientras usa credenciales pre-registradas con el proveedor upstream OAuth Proxy - FastMCP
- Maneja la complejidad del reenvío de callbacks
- Almacena URLs de callback dinámicos del cliente

### C. Remote Auth Provider (Para proveedores con DCR)

Para proveedores que soportan Dynamic Client Registration como Descope y WorkOS AuthKit.

## 2 Proveedores OAuth Empresariales Soportados

FastMCP proporciona soporte de autenticación integral con proveedores de nivel empresarial GitHub - jlowin/fastmcp: 🚀 The fast, Pythonic way to build MCP servers and clients:

Proveedores integrados:

- Google OAuth
- GitHub OAuth
- Microsoft Azure Entra ID
- Auth0
- WorkOS
- AWS Cognito

También existe soporte para Pangea AuthN con flujo estándar de OAuth Authorization Code FastMCP: Streamline with Pangea AuthN Integration.

## 3 Mejores Prácticas de Seguridad

### Autenticación Obligatoria

La autenticación debe ser obligatoria para implementaciones no-stdio, a pesar de ser opcional en la especificación MCP

### Validación de Tokens

Siempre incluye validación de audiencia especificando el parámetro audience, que valida el claim aud en el JWT para asegurar que el token fue emitido específicamente para tu servidor MCP Configure Bearer auth in MCP server | MCP Auth.

### Gestión de Sesiones

Los servidores MCP NO DEBEN usar sesiones para autenticación y DEBEN usar IDs de sesión seguros y no determinísticos Security Best Practices - Model Context Protocol.

### Principio de Mínimo Privilegio

Comienza con un conjunto mínimo de scopes iniciales (como mcp:tools-basic) conteniendo solo operaciones de lectura/descubrimiento de bajo riesgo, con elevación incremental mediante desafíos WWW-Authenticate cuando se intenten operaciones privilegiadas Security Best Practices - Model Context Protocol.

### Protección de Recursos

Las actualizaciones de junio 2025 de la especificación MCP clasifican formalmente a los servidores MCP como OAuth Resource Servers e implementan Resource Indicators (RFC 8707) para prevenir el mal uso de tokens Model Context Protocol (MCP) Spec Updates from June 2025.

## 4 Consideraciones Arquitectónicas

### Desafíos Únicos de MCP

La autenticación web tradicional asume un usuario humano con navegador que puede interactuar con formularios de login, pero los clientes MCP son a menudo sistemas automatizados que necesitan autenticarse sin intervención humana Authentication - FastMCP.

Esto requiere:

- Descubrimiento automático: Los clientes deben descubrir requisitos examinando metadatos del servidor
- OAuth programático: Flujos OAuth sin interacción humana
- Gestión de tokens: Obtención, renovación y gestión automática de tokens
- Integración de protocolo: Integración limpia con mecanismos de transporte MCP

### Riesgos de Implementación Completa OAuth

La implementación completa de OAuth solo tiene sentido cuando necesitas control completo del proceso de autenticación, operas en ambientes aislados (air-gapped), o tienes requisitos especializados que los proveedores externos no pueden satisfacer, pero requiere experiencia significativa en seguridad y compromiso de mantenimiento continuo Authentication - FastMCP.

## 5 Patrón Recomendado según el Caso de Uso

Para nuevos proyectos:

- Usa JWT/Bearer Token con un proveedor externo (Auth0, Google, Azure)
- FastMCP 2.6+ proporciona validación de Bearer token tan simple como proporcionar una clave pública Blast Auth with FastMCP 2.6

Para integración con sistemas existentes:

- Si ya tienes JWT/API Gateway: Bearer Auth Provider
- Si necesitas OAuth tradicional: OAuth Proxy
- Si el proveedor soporta DCR: Remote Auth Provider

Para desarrollo local:

- Considera que la autenticación web tradicional no funciona bien con clientes MCP automatizados Authentication - FastMCP
- Usa Bearer tokens para pruebas

## 6 Controles de Seguridad Adicionales

Las mejores prácticas incluyen: Top MCP Security Best Practices for 2025

- Segregar servidores MCP por subnets VPC o VLANs
- Implementar mTLS y WAFs para inspección profunda
- Reverificar cada solicitud MCP con autorización por-request
- Monitorear sesiones continuamente
- Rotar claves regularmente
- Implementar autenticación multifactor para acciones de alto riesgo

## Conclusión

Para la mayoría de implementaciones de producción con fastMCP, el enfoque recomendado es:

1. Usar Bearer Token/JWT Verification con un proveedor OAuth externo establecido
2. Implementar OAuth Proxy si necesitas integrarte con proveedores tradicionales sin DCR
3. Seguir las mejores prácticas de seguridad: validación de audiencia, rotación de tokens, y principio de mínimo privilegio
4. Nunca exponer servidores MCP sin autenticación en entornos de producción
5. Considerar la evolución hacia OAuth 2.1 completo conforme el ecosistema madure
