"""RAG-powered semantic attraction search tool."""
import json
from ..rag import RAGPipeline


async def search_attractions_tool(
    query: str = "",
    city: str = "",
    category: str = "",
    top_k: int = 5,
) -> str:
    """Semantic search for attractions using RAG."""
    from ...database import SessionLocal, _get_pg_session_local

    pg_sm = _get_pg_session_local()
    if pg_sm is None:
        return "向量数据库未连接。请直接告诉我你想去的城市和喜好，我可以帮你搜索景点。"

    sqlite_db = SessionLocal()
    pg_db = pg_sm()
    try:
        pipeline = RAGPipeline()
        results = await pipeline.semantic_search_attractions(
            pg_db=pg_db,
            sqlite_db=sqlite_db,
            query=query or city or "热门景点",
            city=city or None,
            category=category or None,
            top_k=top_k,
        )

        if not results:
            return f"未找到与'{query or city}'相关的景点。请尝试更具体的关键词。"

        items = []
        for r in results:
            items.append({
                "id": r["id"],
                "name": r["name"],
                "city": r["city"],
                "category": r["category"],
                "rating": r["rating"],
                "duration": r["visit_duration"],
                "ticket": r["ticket_price"],
                "description": r["description"][:150] if r["description"] else "",
                "similarity": r["similarity"],
            })

        return json.dumps(items, ensure_ascii=False, indent=2)
    finally:
        pg_db.close()
        sqlite_db.close()
