"""Image search and MCP API endpoints."""
from fastapi import APIRouter, Depends
from ..utils.auth import get_current_user
from ..models.user import User
from ..schemas.image_search import ImageSearchRequest, ImageResult
from ..mcp.image_tool import search_images
from ..mcp.types import MCPRequest, MCPResponse
from ..mcp.server import get_mcp_server
from ..mcp.image_tool import search_images as mcp_image_search

router = APIRouter(prefix="/api/images", tags=["images"])

# Register MCP tools on startup
_mcp = get_mcp_server()
_mcp.register_tool(
    "image_search",
    "搜索目的地或景点的真实照片。参数: query(关键词), destination(目的地), count(数量)",
    mcp_image_search,
    {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"},
            "destination": {"type": "string", "description": "目的地或景点名称"},
            "count": {"type": "integer", "description": "返回图片数量", "default": 5},
        },
        "required": ["query"],
    },
)


@router.post("/search", response_model=list[ImageResult])
async def image_search(
    req: ImageSearchRequest,
    user: User = Depends(get_current_user),
):
    results = await search_images(
        query=req.query,
        destination=req.destination,
        count=req.count,
    )
    return [
        ImageResult(
            url=r["url"],
            alt_text=r.get("alt_text", ""),
            thumbnail_url=r.get("thumbnail_url", ""),
            source=r.get("source", ""),
        )
        for r in results
    ]


@router.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    """MCP JSON-RPC 2.0 endpoint for tool discovery and invocation."""
    response = await _mcp.handle_request(request)
    return response.model_dump(exclude_none=True)
