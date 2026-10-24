from fastmcp import Client
import asyncio
from pathlib import Path
from pprint import pprint  # <-- Importar pprint

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

mcp_client = GmailMCPClient()

info = asyncio.run(mcp_client.get_system_info()) # Para arrancar código asincrono

#print(info)
print("\n--- INFORMACIÓN DEL SISTEMA MCP ---")
pprint(info, sort_dicts=False, indent=4)

