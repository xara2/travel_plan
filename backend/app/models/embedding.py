from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from pgvector.sqlalchemy import Vector
from ..database import PG_Base
import datetime


class AttractionEmbedding(PG_Base):
    __tablename__ = "attraction_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    attraction_id = Column(Integer, nullable=False, index=True)
    chunk_index = Column(Integer, default=0)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
