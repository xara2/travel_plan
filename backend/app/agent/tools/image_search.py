"""Image search tool via MCP."""
import json
from ...mcp.image_tool import search_images


async def search_images_tool(query: str = "", destination: str = "", count: int = 5) -> str:
    """Search for destination/scenic spot images.

    Args:
        query: Search keywords (e.g. "海滩日落")
        destination: Destination city or attraction name
        count: Number of images to return (max 10)
    """
    count = min(count, 10)
    results = await search_images(
        query=query,
        destination=destination,
        count=count,
    )

    if not results:
        return "未找到相关图片。"

    # Return structured image data
    images = []
    for r in results:
        images.append({
            "url": r["url"],
            "thumbnail": r.get("thumbnail_url", r["url"]),
            "alt": r.get("alt_text", ""),
            "source": r.get("source", ""),
        })

    return json.dumps(images, ensure_ascii=False)
