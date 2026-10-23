# Agente:

El rasgo que define a los agentes es su capacidad para elegir el mejor orden de acciones para resolver un problema dado un conjunto de herramientas

## COMPONENTES DE UN AGENTE:

1. Modelo de lenguaje (LLM)
2. Tools (Herramientas que puede usar)
3. Prompt de agente (Plantilla de razonamiento, guía al llm patron de pensamiento)
4. Memoria

# Agentes preconfigurados recomendados en LangChain y LangGraph

El ecosistema de agentes en LangChain ha evolucionado significativamente. Mientras que las versiones anteriores dependían de tipos de agente enumerados (`AgentType.ZERO_SHOT_REACT_DESCRIPTION`, etc.), el enfoque moderno se basa en **builders** (constructores) más flexibles y la migración hacia **LangGraph** para casos de producción.

#### LangChain Builders (Compatibilidad y Casos Específicos)

LangChain mantiene varios builders para compatibilidad con proyectos existentes y casos de uso específicos:

**Agentes modernos recomendados:**

* `create_tool_calling_agent`: Builder "moderno" que usa **tool-calling nativo** del modelo (OpenAI, Anthropic, Gemini, etc.). Recomendado por defecto si tu LLM soporta herramientas estructuradas. Este agente aprovecha las capacidades nativas de function calling de los modelos más recientes, resultando en llamadas más precisas y eficientes.
* `create_react_agent`: Implementa el patrón **ReAct** (razonar-actuar) dentro de LangChain tradicional. Útil si quieres el bucle ReAct clásico, aunque la documentación oficial recomienda preferir la versión de LangGraph para producción.

**Agentes especializados:**

* `create_openai_functions_agent`: Builder para el antiguo esquema de **function calling** de OpenAI. Úsalo si necesitas compatibilidad con flujos legacy que dependían de la implementación anterior.
* `create_openai_tools_agent`: Variante centrada en el formato  **OpenAI Tools** . Conveniente si ya estandarizas tus prompts/parsers a ese esquema.
* `create_structured_chat_agent`: Diseñado para herramientas con **múltiples entradas** y flujos de diálogo estructurados. Útil cuando tus herramientas requieren parámetros complejos.
* `create_json_chat_agent`: Requiere que el LLM emita **JSON** para su lógica/acciones. Útil para auditoría y parsing determinista.
* `create_self_ask_with_search_agent`: Implementa el patrón **self-ask** (preguntas descompuestas + búsqueda). Útil para QA con descomposición explícita de problemas complejos.
* `create_xml_agent`: Usa **XML** para formatear razonamiento/acciones. Interesante si tus sistemas de parseo o guardrails ya esperan XML.

#### LangGraph Prebuilt (Recomendado para Producción)

LangGraph representa el futuro de los agentes en el ecosistema LangChain, proporcionando mayor control, robustez y características avanzadas:

**Agente principal:**

* `create_react_agent` (langgraph-prebuilt): El **prebuilt** recomendado para producción. Incluye bucle de tool-calling con memoria opcional, prompt estático/dinámico, **structured output** (`response_format`), y manejo robusto de errores. Es la vía rápida y confiable para un agente de propósito general.

**Arquitecturas multi-agente:**

* **Supervisor** : Paquete `langgraph-supervisor` con `create_supervisor` para coordinar varios agentes especializados. Incluye herramientas de **handoff** y  *forwarding* . Útil cuando quieres orquestar un "equipo de agentes" bajo supervisión central.
* **Swarm** : Paquete `langgraph-swarm` con `create_swarm` y utilidades de *handoff routing* entre agentes. Útil para sistemas donde los agentes se pasan el control dinámicamente según especialidad.

**APIs de bajo nivel:** Para casos que requieren control total, LangGraph ofrece **Graph API / Functional API** (StateGraph, nodos, herramientas, memoria, pausing, etc.) para construir agentes completamente personalizados.
