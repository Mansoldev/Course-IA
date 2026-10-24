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

    async def get_tools_for_gemini(self):
        """Convierte herramientas MCP a formato Google GenAI (Gemini)"""
        async with await self._get_mcp_client() as cliente:
            tools = await cliente.list_tools()

            gemini_declarations = []
            for tool in tools:
                # Estructura compatible con function declarations de Gemini
                gemini_declarations.append({
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema
                })
            
            # Retorna la estructura de herramientas envuelta para GenAI y el cliente vivo
            return [{"function_declarations": gemini_declarations}], cliente

    # El LLM no tiene un forma nativa de llamar a un recurso, asique tenemos que encapsularlos como herramientas
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
                            "required": params
                        }
                    }
                })

                resource_map[func_name] = {"template": uri_template, "params": params}
            
            return resource_tools, resource_map

    async def get_resources_as_tools_for_gemini(self):
        """Encapsula recursos y templates como herramientas en formato compatible con Gemini."""
        async with await self._get_mcp_client() as cliente:
            # Obtener recursos y templates
            resources = await cliente.list_resources()
            templates = await cliente.list_resource_templates()

            resource_declarations = []
            resource_map = {}

            # 1. Recursos estáticos
            for resource in resources:
                uri = str(resource.uri)
                func_name = f"get_resource_{uri.replace('://', '_').replace('/', '_')}"

                # Formato plano para Gemini (sin anidar dentro de "function")
                resource_declarations.append({
                    "name": func_name,
                    "description": resource.description or resource.name,
                    "parameters": {"type": "object", "properties": {}, "required": []}
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

                # Formato plano para Gemini
                resource_declarations.append({
                    "name": func_name,
                    "description": template.description or template.name,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": params
                    }
                })

                resource_map[func_name] = {"template": uri_template, "params": params}
            
            # Retorna la lista envuelta en la estructura de function_declarations de Gemini y el mapa
            return [{"function_declarations": resource_declarations}], resource_map
        
    