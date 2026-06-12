"""MCP JSON-RPC 2.0 server — tool registration and dispatch."""
from __future__ import annotations
from .types import MCPRequest, MCPResponse, ToolDefinition


class MCPServer:
    def __init__(self):
        self._tools: dict[str, dict] = {}

    def register_tool(self, name: str, description: str, handler, input_schema: dict | None = None):
        self._tools[name] = {
            "definition": ToolDefinition(
                name=name,
                description=description,
                inputSchema=input_schema or {},
            ),
            "handler": handler,
        }

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        method = request.method
        req_id = request.id

        try:
            if method == "tools/list":
                result = [t["definition"].model_dump() for t in self._tools.values()]
                return MCPResponse(id=req_id, result=result)

            elif method == "tools/call":
                params = request.params or {}
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})

                tool = self._tools.get(tool_name)
                if not tool:
                    return MCPResponse(id=req_id, error={
                        "code": -32601,
                        "message": f"Tool not found: {tool_name}",
                    })

                output = await tool["handler"](**arguments)
                return MCPResponse(id=req_id, result={"content": output})

            else:
                return MCPResponse(id=req_id, error={
                    "code": -32601,
                    "message": f"Method not found: {method}",
                })

        except Exception as e:
            return MCPResponse(id=req_id, error={
                "code": -32603,
                "message": str(e),
            })


_mcp_server: MCPServer | None = None


def get_mcp_server() -> MCPServer:
    global _mcp_server
    if _mcp_server is None:
        _mcp_server = MCPServer()
    return _mcp_server
