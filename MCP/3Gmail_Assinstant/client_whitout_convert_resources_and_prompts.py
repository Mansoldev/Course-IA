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