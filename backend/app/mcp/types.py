"""MCP JSON-RPC 2.0 protocol types."""
from __future__ import annotations
from pydantic import BaseModel


class ToolDefinition(BaseModel):
    name: str
    description: str
    inputSchema: dict = {}


class ToolCallParams(BaseModel):
    name: str
    arguments: dict = {}


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int | None = None
    method: str
    params: dict | list | None = None


class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int | None = None
    result: dict | list | None = None
    error: dict | None = None


class MCPError(BaseModel):
    code: int
    message: str
    data: dict | None = None
