
# Lectura: Definición de servidores MCP locales en Claude Desktop

Cuando Claude Desktop **arranca**, **busca** un archivo de configuración en formato **JSON (claude_desktop_config.json)**. Dentro de este archivo puede existir una sección llamada:

```JSON
"mcpServers": {
  ...
}
```

Este objeto es un **diccionario de servidores MCP**, donde cada clave es un nombre identificador del servidor (por ejemplo "filesystem", "memory", "fetch", etc.) y cada valor es la **definición de cómo lanzar el proceso servidor MCP local**.

La idea es muy sencilla: cada servidor MCP es un **programa ejecutable** (puede ser un binario, un script Node, Python, etc.) que Claude Desktop tiene que arrancar para conectarse a él. El JSON indica **qué comando ejecutar, con qué argumentos, y en qué entorno**.

## Campos admitidos en la definición de un servidor

Cada entrada bajo "mcpServers" puede incluir los siguientes campos principales:

```JSON
"mcpServers": {
  "nombreServidor": {
    "command": "ejecutable",
    "args": ["arg1", "arg2", "..."],
    "env": {
      "CLAVE": "valor"
    },
    "workingDirectory": "ruta/opcional"
  }
}
```

### 1 command (obligatorio)

Es la orden o binario que Claude ejecutará para lanzar el servidor.

Ejemplos típicos:

- "npx" → para servidores distribuidos como paquetes npm.
- "python" → si el servidor está implementado en Python.
- "./mi_servidor" → si tienes un binario compilado en la carpeta local.

### 2 args (opcional pero usualmente necesario)

Lista de argumentos que acompañan al comando.

Aquí indicas:

- El paquete o script a ejecutar (ej: "@modelcontextprotocol/server-filesystem").
- Rutas de carpetas (para Filesystem).
- Flags como -y (para que npx no pida confirmación).

Es un array porque cada argumento debe ser un elemento separado (ej: ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\...\\Desktop"]).

### 3 env (opcional)

Permite definir variables de entorno que se pasarán al proceso del servidor.

Útil cuando un servidor necesita claves API, configuración regional, tokens, etc.

Ejemplo:

```JSON
"env": {
  "API_KEY": "tu_clave_aqui",
  "APPDATA": "C:\\Users\\TuUsuario\\AppData\\Roaming"
}
```

### 4 workingDirectory (opcional)

Define desde qué carpeta se lanzará el servidor (el “current working directory”).

Por defecto, Claude usará el directorio raíz de la aplicación, pero si tu servidor necesita ejecutarse en una ruta específica, puedes forzarla aquí.

### 5 (Otros posibles campos)

- **Nombre de servidor (clave externa)**: La clave dentro de "mcpServers" no es decorativa: es el alias interno con el que Claude identifica ese servidor. Aparecerá en logs y a veces en el interfaz. Conviene que sea corto y descriptivo ("filesystem", "git", "myCustomServer").
- **Comentarios**: JSON no permite comentarios nativos, por lo que cada entrada debe estar limpia. Si quieres documentar tu configuración, puedes mantener un README aparte o dejar comentarios en el propio repositorio del curso.

Ejemplo completo con varios servidores

```JSON
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\Alumno\\Desktop",
        "C:\\Users\\Alumno\\Documents"
      ]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {
        "MEMORY_DB_PATH": "C:\\Users\\Alumno\\AppData\\Roaming\\Claude\\memory.sqlite"
      }
    }
  }
}
```

En este ejemplo:

* "filesystem" limita su alcance a dos carpetas concretas.
* "fetch" no necesita argumentos adicionales, solo el paquete.
* "memory" define una ruta específica donde almacenar la base de datos de memoria persistente, a través de una variable de entorno.

## ¿Por qué se define así?

El motivo de esta estructura es que Claude Desktop no “sabe” de antemano qué servidores usarás ni cómo lanzarlos.

Cada servidor MCP es un proceso externo que habla con Claude Desktop mediante el protocolo MCP.

El archivo JSON funciona como una lista de instrucciones de lanzamiento. Por cada servidor, Claude:

1. Ejecuta el command indicado.
2. Le pasa los args necesarios.
3. Le añade el entorno (env) si se especificó.
4. Mantiene la conexión abierta vía MCP mientras Claude se está ejecutando.

De este modo, la configuración es genérica y extensible: puedes añadir cualquier servidor nuevo, aunque no esté creado por Anthropic, siempre que siga el protocolo MCP.

## Buenas prácticas

Un servidor, un alias claro. Usa nombres sencillos ("git", "db", "fsTrabajo") para identificar mejor los servidores en logs.

Restringe accesos. No expongas carpetas enteras del disco en filesystem (ej. C:\\ completo) salvo que tengas una necesidad justificada.

Usa env para secretos. No escribas claves API directamente en args, siempre en env.

Prueba manualmente. Lanza el mismo comando en la terminal antes de ponerlo en el JSON, así detectas fallos de instalación.

## Tarea práctica

1. Edita tu archivo claude_desktop_config.json.
2. Añade un nuevo servidor llamado "memory" con la siguiente definición (ajusta la ruta si es necesario):

```JSON
"memory": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-memory"],
  "env": {
    "MEMORY_DB_PATH": "C:\\Users\\TuUsuario\\AppData\\Roaming\\Claude\\memory.sqlite"
  }
}
```

1. Guarda y reinicia Claude Desktop.
2. Pídele a Claude: “Recuerda que mi proyecto se llama Proyecto Fénix”. Luego inicia un nuevo hilo y pregúntale “¿Cómo se llama mi proyecto?”.
3. Observa si Claude recupera la información: habrás comprobado que el servidor Memory funciona.
