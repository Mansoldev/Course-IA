from fastmcp import Client
from pathlib import Path

class GmailMCPClient:
    def __init__(self):
        current_dir = Path(__file__).parent
        self.mcp_server_path = current_dir / "gmail_mcp_server.py"

    async def _get_mcp_client(self):
        """Crea conexión con el servidor MCP"""
        return Client(self.mcp_server_path)
    
    async def get_system_info(self) -> dict:
        """Información del sistema MCP"""
        async with await self._get_mcp_client() as cliente:
            tools = await cliente.list_tools()
            resources = await cliente.list_resources()
            templates = await cliente.list_resource_templates()
            prompts = await cliente.list_prompts()

            return {
                "tools": [t.name for t in tools],
                "resources": [r.name for r in resources],
                "templates": [t.name for t in templates],
                "prompts": [p.name for p in prompts],
                "server": self.mcp_server_path
            }

    async def get_tools_for_openai(self):
        """Convierte herramientas MCP a formato OpenAI"""
        async with await self._get_mcp_client() as cliente:
            tools = await cliente.list_tools()

            openai_tools = []
            for tool in tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema
                    }
                })
            
            return openai_tools, cliente
        
    async def get_resources_as_tools(self):
        """Encapsula recursos y templates como herramientas."""
        async with await self._get_mcp_client() as cliente:
            # Obtener recursos y templates
            resources = await cliente.list_resources()
            templates = await cliente.list_resource_templates()

            resource_tools = []
            resource_map = {}

            # 1. Recursos estáticos
            for resource in resources:
                uri = str(resource.uri)
                func_name = f"get_resource_{uri.replace('://', '_').replace('/', '_')}"

                resource_tools.append({
                    "type": "function",
                    "function": {
                        "name": func_name,
                        "description": resource.description or resource.name,
                        "parameters": {"type": "object", "properties": {}, "required": []}
                    }
                })

                resource_map[func_name] = {"uri": uri}

            # 2. Resource templates
            for template in templates:
                uri_template = str(template.uriTemplate)
                func_name = template.name

                # Extraer parametros del template
                import re
                params = re.findall(r'\{(\w+)\}', uri_template)

                properties = {p: {"type": "string", "description": f"Parametro {p}"} for p in params}

                resource_tools.append({
                    "type": "function",
                    "function": {
                        "name": func_name,
                        "description": template.description or template.name,
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                        }
                    }
                })

                resource_map[func_name] = {"template": uri_template, "params": params}
            
            return resource_tools, resource_map
        
    # async def get_prompt_messages(self, prompt_name: str, **kwargs) -> str:
    #     """Obtiene el mensaje de un prompt especifico."""
    #     async with await self._get_mcp_client() as cliente:
    #         prompt = await cliente.get_prompt(prompt_name, arguments=kwargs)
    #         return eval(prompt.messages[0].content.text)

    # Los problemas del método anterior:
    # eval() es muy peligroso: Usar eval() sobre un texto que viene devuelto por el servidor (prompt.messages[0].content.text) ejecuta código de Python de forma arbitraria. Si por alguna razón el texto contiene algo malicioso o inesperado, puede romper la ejecución o comprometer la seguridad.
    # Estructura de mensajes: Dependiendo de cómo devuelva FastMCP el mensaje, el contenido ya suele ser un texto plano o una estructura accesible mediante atributos o diccionarios directos, sin necesidad de parsearlo con eval.
    async def get_prompt_messages(self, prompt_name: str, **kwargs) -> str:
        """Obtiene y formatea el mensaje de un prompt específico de forma segura."""
        async with await self._get_mcp_client() as cliente:
            prompt_result = await cliente.get_prompt(prompt_name, arguments=kwargs)
            
            # Verificamos si hay mensajes disponibles
            if not prompt_result.messages:
                return ""
            
            # Obtenemos el primer mensaje
            msg = prompt_result.messages[0]
            
            # Accedemos de forma segura al contenido dependiendo de cómo venga estructurado
            # (FastMCP suele estructurarlo en content.text si es un mensaje de texto)
            if hasattr(msg, "content") and hasattr(msg.content, "text"):
                return msg.content.text
            elif isinstance(msg.content, str):
                return msg.content
            else:
                # Fallback por si viene en formato diccionario o texto plano directo
                return str(msg.content)