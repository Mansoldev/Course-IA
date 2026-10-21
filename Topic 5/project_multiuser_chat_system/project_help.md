
# Caso práctico (abstracto): combinar memoria volátil por chat + memoria vectorial global

## Arquitectura lógica

LangGraph + MemorySaver → historial activo del chat (barato y rápido).
Vector store (Chroma) → memoria global del usuario (perfil, gustos, datos duraderos).
Nodo de chat:

1. Lee último HumanMessage (la consulta).
2. Recupera memorias globales relevantes ( k fijo, filtra por user_id ).
3. Inyecta memorias a SystemMessage (o como contexto adicional).
4. Invoca LLM con [System] + (ventana deslizante del chat) + [Último Human] .
5. Actualiza: añade AIMessage al estado + (opcional) extrae del último mensaje humano datos para guardar en vectorial

## Funciones típicas

save_memory(text, user_id, type=…) → añade document , id=uuid4() , metadata .
search_memory(query, user_id, k=5) → vector_store.query + filtros.
Heurística de guardado (rápida) o Clasificador con LLM (mejor calidad) para decidir qué persistir:

* Nombre: “me llamo…”
* Ubicación: “vivo en… / soy de…”
* Profesión: “trabajo como… / soy …”
* Preferencias: “me gusta… / me encanta…”

## Consejos de implementación

* Mantén comandos de depuración (p. ej., memorias ) para listar lo guardado.
* Sanitiza/normaliza texto (minúsculas, trimming, deduplicación por hash).
* Añade TTL o políticas (importancia, frescura) si temes crecimiento descontrolado.
* Registra fuente (chat_id, timestamp) en metadatos.
