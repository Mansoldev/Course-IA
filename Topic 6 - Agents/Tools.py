# Respuesta tradicional (texto libre)
"Necesito usar la herramienta de búsqueda con el término 'clima Madrid'"

# Tool calling moderno (estructurado)
{
    "tool_calls": [
        {
            "name": "buscar_clima",
            "args": {"ciudad": "Madrid", "pais":"España"},
            "id": "call_123"
        }
    ]
}

