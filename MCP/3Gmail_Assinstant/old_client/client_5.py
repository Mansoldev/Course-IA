from fastmcp import Client
#from openai import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

class GmailMCPClient:
    def __init__(self):
        #self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.openai_client = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
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
                            "requiered": params
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

    # Proporcionarle al llm métodos al mcp para que ejecute las herramientas
    async def call_tool(self, tool_name: str, arguments: dict, client):
        """Ejecuta una herramienta MCP"""
        result = await client.call_tool(tool_name, arguments)
        # Verificar la estructura de la respuesta
        if result and result.content and len(result.content) > 0:
            if hasattr(result.content[0], 'text'):
                return result.content[0].text
        return "Herramienta ejecutada sin resultados"

    # Proporcionarle al llm método para solicitar un recurso cuando lo necesite
    async def get_resource(self, uri: str, client):
        """Obtiene un recurso MCP"""
        result = await client.read_resource(uri)
        # Verificar estructura de la respuesta
        if result and len(result) > 0:
            if hasattr(result[0], 'text'):
                return result[0].text
            elif hasattr(result[0], 'content'):
                return result[0].content
        return "Recurso no disponible"