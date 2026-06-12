"""RAG pipeline for semantic attraction search."""
from .llm_client import get_llm_client
from ..config import SIMILARITY_THRESHOLD, RAG_TOP_K


class RAGPipeline:
    def __init__(self):
        self.llm = get_llm_client()

    async def embed_attractions(self, pg_db, sqlite_db) -> int:
        """Generate embeddings for all attractions and store in PGVector."""
        from ..models.attraction import Attraction
        from ..models.embedding import AttractionEmbedding

        existing_ids = {e.attraction_id for e in pg_db.query(AttractionEmbedding.attraction_id).all()}
        attractions = sqlite_db.query(Attraction).filter(~Attraction.id.in_(existing_ids)).all()
        if not attractions:
            return 0

        chunks = []
        for a in attractions:
            text = f"【{a.name}】{a.category}景点，评分{a.rating}。{a.description}。位于{a.city}{a.province}。门票{'免费' if a.ticket_price == 0 else f'{a.ticket_price}元'}，游玩约{a.visit_duration}分钟。"
            chunks.append(text)

        embeddings = await self.llm.embed(chunks)

        for attr, emb in zip(attractions, embeddings):
            text = f"【{attr.name}】{attr.category}景点，评分{attr.rating}。{attr.description}。位于{attr.city}{attr.province}。"
            pg_db.add(AttractionEmbedding(
                attraction_id=attr.id,
                content=text,
                embedding=emb,
            ))

        pg_db.commit()
        return len(attractions)

    async def search_similar(
        self, pg_db, query: str, city: str | None = None,
        category: str | None = None, top_k: int = RAG_TOP_K,
        threshold: float = SIMILARITY_THRESHOLD,
    ) -> list[dict]:
        """Vector similarity search with optional filters."""
        from ..models.embedding import AttractionEmbedding
        from ..models.attraction import Attraction
        from sqlalchemy import text

        query_emb = (await self.llm.embed([query]))[0]

        # Cosine similarity: 1 - cosine_distance
        sql = text("""
            SELECT ae.attraction_id, ae.content,
                   1 - (ae.embedding <=> :vec) AS similarity
            FROM attraction_embeddings ae
            WHERE 1 - (ae.embedding <=> :vec) >= :threshold
            ORDER BY similarity DESC
            LIMIT :k
        """)
        result = pg_db.execute(sql, {"vec": query_emb, "threshold": threshold, "k": top_k * 2})
        rows = result.fetchall()

        if not rows:
            return []

        # Fetch attraction details from SQLite and apply filters
        from ..models.attraction import Attraction as AttrModel
        results = []
        for row in rows:
            aid = row[0]
            similarity = row[2]
            attr = pg_db.query(AttrModel).get(aid) if hasattr(self, '_sqlite_db') else None
            if attr is None:
                # We need to use sqlite_db to fetch attractions
                continue
            if city and attr.city != city:
                continue
            if category and attr.category != category:
                continue
            results.append({
                "id": attr.id,
                "name": attr.name,
                "city": attr.city,
                "category": attr.category,
                "rating": attr.rating,
                "visit_duration": attr.visit_duration,
                "ticket_price": attr.ticket_price,
                "description": attr.description,
                "image_url": attr.image_url,
                "similarity": round(float(similarity), 4),
            })

        return results[:top_k]

    async def semantic_search_attractions(
        self, pg_db, sqlite_db, query: str,
        city: str | None = None, category: str | None = None,
        top_k: int = RAG_TOP_K,
    ) -> list[dict]:
        """Full semantic search: embed -> filter via SQLite -> return with scores."""
        from ..models.embedding import AttractionEmbedding
        from sqlalchemy import text

        query_emb = (await self.llm.embed([query]))[0]

        sql = text("""
            SELECT ae.attraction_id, ae.content,
                   1 - (ae.embedding <=> :vec) AS similarity
            FROM attraction_embeddings ae
            WHERE 1 - (ae.embedding <=> :vec) >= :threshold
            ORDER BY similarity DESC
            LIMIT :k
        """)
        result = pg_db.execute(sql, {
            "vec": query_emb,
            "threshold": SIMILARITY_THRESHOLD,
            "k": top_k * 3,
        })
        rows = result.fetchall()
        if not rows:
            return []

        aid_to_score = {row[0]: float(row[2]) for row in rows}
        aid_list = list(aid_to_score.keys())

        from ..models.attraction import Attraction as AttrModel
        q = sqlite_db.query(AttrModel).filter(AttrModel.id.in_(aid_list))
        if city:
            q = q.filter(AttrModel.city.contains(city))
        if category:
            q = q.filter(AttrModel.category == category)
        attractions = q.all()

        results = []
        for a in attractions:
            results.append({
                "id": a.id, "name": a.name, "city": a.city,
                "category": a.category, "rating": a.rating,
                "visit_duration": a.visit_duration,
                "ticket_price": a.ticket_price,
                "description": a.description,
                "image_url": a.image_url,
                "similarity": round(aid_to_score.get(a.id, 0), 4),
            })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
