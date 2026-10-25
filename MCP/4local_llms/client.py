from fastmcp import Client
#from openai import OpenAI
# from google import genai
import ollama
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()


class GmailMCPClient:
    def __init__(self):
        # Clientes de IA
        #self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        #self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen3:8")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
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

    async def get_tools_for_llm(self):
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
                        "parameters": tool.input_schema
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
                uri_template = str(template.uri_template)
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

    # Para openai
    # async def chat(self, messages: list) -> str:
    #     """Procesa una conversación con GPT utilizando MCP"""
    #     async with await self._get_mcp_client() as mcp:
    #         # Obtener herramientas y recursos
    #         tools, _ = await self.get_tools_for_openai()
    #         resource_tools, resource_map = await self.get_resources_as_tools()
    #         all_tools = tools + resource_tools

    #         # LLamada inicial a OpenAI
    #         response = self.openai_client.chat.completions.create(
    #             model="gpt-4o-mini",
    #             messages=messages,
    #             tools=all_tools,
    #             tool_choice="auto"
    #         )

    #         response_message = response.choices[0].message
    #         tool_calls = response_message.tool_calls

    #         # Si no hay tool calls, retornar respuesta directa
    #         if not tool_calls:
    #             return response_message.content

    #         # Processar tool calls
    #         messages.append({
    #             "role": "assistant",
    #             "content": response_message.content,
    #             "tool_calls": [
    #                 {
    #                     "id": tc.id,
    #                     "type": "function",
    #                     "function": {
    #                         "name": tc.function.name,
    #                         "arguments": tc.function.arguments
    #                     }
    #                 }
    #                 for tc in tool_calls
    #             ]
    #         })

    #         for tool_call in tool_calls:
    #             function_name = tool_call.function.name
    #             function_args = eval(tool_call.function.arguments)

    #             # Verficar si es un recurso
    #             if function_name in resource_map:
    #                 resource_info = resource_map[function_name]

    #                 if "template" in resource_info:
    #                     # Resource template: construir URI
    #                     uri = resource_info["template"]
    #                     for param in resource_info["params"]:
    #                         uri = uri.replace(f"{{{param}}}", str(function_args.get(param, "")))
    #                 else:
    #                     # REcurso estatico
    #                     uri = resource_info['uri']

    #                 function_response = await self.get_resource(uri, mcp)
    #             else:
    #                 # Herramienta normal
    #                 function_response = await self.call_tool(function_name, function_args, mcp)

    #             messages.append({
    #                 "tool_call_id": tool_call.id,
    #                 "role": "tool",
    #                 "name": function_name,
    #                 "content": function_response
    #             })

    #             # Segunda llamada con resultados de la herramienta
    #             second_response = self.openai_client.chat.completions.create(
    #                 model="gpt-4o-mini",
    #                 messages=messages
    #             )

    #            return second_response.choices[0].messages.content

    # Para Gemini
    # async def chat(self, contents: list | str) -> str:
    #     """Procesa una conversación con Gemini utilizando MCP"""
    #     async with await self._get_mcp_client() as mcp:
    #         # 1. Obtener herramientas de MCP en formato Gemini
    #         tools_data, _ = await self.get_tools_for_gemini()
    #         resource_tools, resource_map = await self.get_resources_as_tools_for_gemini()
            
    #         # Combinar todas las declaraciones de funciones para Gemini
    #         # Nota: 'tools_data' ya es una lista con el diccionario {"function_declarations": [...]}
    #         all_function_declarations = tools_data[0]["function_declarations"] + resource_tools[0]["function_declarations"]
            
    #         gemini_tools = [{"function_declarations": all_function_declarations}]

    #         # 2. Llamada inicial a Gemini
    #         response = self.gemini_client.models.generate_content(
    #             model="gemini-3.5-flash-lite",  # O el modelo que prefieras (ej: gemini-2.5-pro)
    #             contents=contents,
    #             config={
    #                 "tools": gemini_tools
    #             }
    #         )

    #         # 3. Comprobar si Gemini quiere llamar a una herramienta (Function Calling)
    #         # El SDK de google-genai maneja las llamadas a funciones en response.function_calls
    #         if response.function_calls:
    #             for function_call in response.function_calls:
    #                 tool_name = function_call.name
    #                 tool_args = function_call.args
                    
    #                 tool_result = None
                    
    #                 # Verificar si es una herramienta normal del servidor MCP o un recurso encapsulado
    #                 if tool_name in resource_map:
    #                     # Es un recurso o template mapeado
    #                     res_info = resource_map[tool_name]
    #                     if "uri" in res_info:
    #                         read_res = await mcp.read_resource(res_info["uri"])
    #                         tool_result = read_res
    #                     elif "template" in res_info:
    #                         # Remplazar parámetros en el template del recurso
    #                         uri_filled = res_info["template"]
    #                         for k, v in tool_args.items():
    #                             uri_filled = uri_filled.replace(f"{{{k}}}", str(v))
    #                         read_res = await mcp.read_resource(uri_filled)
    #                         tool_result = read_res
    #                 else:
    #                     # Es una herramienta normal de MCP (ej: list_emails, send_email)
    #                     tool_result = await mcp.call_tool(tool_name, arguments=tool_args)
                    
    #                 # 4. Enviar el resultado de vuelta a Gemini para que genere la respuesta final
    #                 # (Esto se puede estructurar como un chat continuo o una segunda llamada pasándole el historial)
    #                 final_response = self.gemini_client.models.generate_content(
    #                     model="gemini-3.5-flash-lite",
    #                     contents=[
    #                         contents,
    #                         response.text or "", # Mensaje del modelo con la intención de llamada
    #                         f"Resultado de la herramienta {tool_name}: {tool_result}"
    #                     ]
    #                 )
    #                 return final_response.text

    #         # Si no llamó a ninguna herramienta, devuelve el texto directamente
    #         return response.text

    #Para Ollama
    # async def chat(self, messages: list) -> str:
    #     """Procesa una conversación con GPT utilizando MCP"""
    #     async with await self._get_mcp_client() as mcp:
    #         # Obtener herramientas y recursos
    #         tools, _ = await self.get_tools_for_llm()
    #         resource_tools, resource_map = await self.get_resources_as_tools()
    #         all_tools = tools + resource_tools

    #         # LLamada inicial a Ollama
    #         response = ollama.chat(
    #             model=self.ollama_model,
    #             messages=messages,
    #             tools=all_tools
    #         )

    #         response_message = response['message']
    #         tool_calls = response_message.get('tool_calls', [])

    #         # Si no hay tool calls, retornar respuesta directa
    #         if not tool_calls:
    #             return response_message.get('content', '')

    #         # Processar tool calls
    #         messages.append({
    #             "role": "assistant",
    #             "content": response_message.get('content', ''),
    #             "tool_calls": tool_calls
    #         })

    #         for tool_call in tool_calls:
    #             function_name = tool_call['function']['name']
    #             function_args = tool_call['function']['arguments']

    #             # Verficar si es un recurso
    #             if function_name in resource_map:
    #                 resource_info = resource_map[function_name]

    #                 if "template" in resource_info:
    #                     # Resource template: construir URI
    #                     uri = resource_info["template"]
    #                     for param in resource_info["params"]:
    #                         uri = uri.replace(f"{{{param}}}", str(function_args.get(param, "")))
    #                 else:
    #                     # REcurso estatico
    #                     uri = resource_info['uri']

    #                 function_response = await self.get_resource(uri, mcp)
    #             else:
    #                 # Herramienta normal
    #                 function_response = await self.call_tool(function_name, function_args, mcp)

    #             messages.append({
    #                 "role": "tool",
    #                 "content": "Tool response to add to context: " + function_response,
    #                 "name": function_name
    #             })

    #             # Segunda llamada con resultados de la herramienta
    #             second_response = ollama.chat(
    #                 model=self.ollama_model,
    #                 messages=messages
    #             )

    #         return second_response['message'].get('content', '')

    #Para Ollama pero mas seguro:
    async def chat(self, messages: list) -> str:
        """Procesa una conversación con Ollama utilizando MCP de forma segura"""
        async with await self._get_mcp_client() as mcp:
            tools, _ = await self.get_tools_for_llm()
            resource_tools, resource_map = await self.get_resources_as_tools()
            all_tools = tools + resource_tools

            try:
                # Llamada inicial a Ollama
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=messages,
                    tools=all_tools
                )
            except Exception as e:
                return f"Error al conectar con Ollama: {str(e)}"

            response_message = response.get('message', {})
            tool_calls = response_message.get('tool_calls', [])

            # Si no hay tool calls, retornar respuesta directa
            if not tool_calls:
                return response_message.get('content', '')

            # Procesar tool calls
            messages.append({
                "role": "assistant",
                "content": response_message.get('content', ''),
                "tool_calls": tool_calls
            })

            for tool_call in tool_calls:
                function_name = tool_call['function']['name']
                function_args = tool_call['function']['arguments']

                if function_name in resource_map:
                    resource_info = resource_map[function_name]
                    if "template" in resource_info:
                        uri = resource_info["template"]
                        for param in resource_info["params"]:
                            uri = uri.replace(f"{{{param}}}", str(function_args.get(param, "")))
                    else:
                        uri = resource_info['uri']

                    function_response = await self.get_resource(uri, mcp)
                else:
                    function_response = await self.call_tool(function_name, function_args, mcp)

                messages.append({
                    "role": "tool",
                    "content": str(function_response),
                    "name": function_name
                })

            try:
                # Segunda llamada con los resultados de la herramienta
                second_response = ollama.chat(
                    model=self.ollama_model,
                    messages=messages
                )
                return second_response.get('message', {}).get('content', 'Respuesta vacía del modelo.')
            except Exception as e:
                return f"Error en la segunda llamada a Ollama: {str(e)}"
