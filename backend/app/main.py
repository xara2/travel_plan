from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .database import engine, Base
from .models import User, Attraction, TravelPlan, PlanDay, PlanItem
from .api.auth import router as auth_router
from .api.attractions import router as attractions_router
from .api.plans import router as plans_router
from .api.chat import router as chat_router
from .api.image_search import router as image_router
from .api.agent import router as agent_router
from .seed import seed_attractions

app = FastAPI(title="Travel Plan API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(attractions_router)
app.include_router(plans_router)
app.include_router(chat_router)
app.include_router(image_router)
app.include_router(agent_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_attractions()
    _init_pgvector()


def _init_pgvector():
    """Initialize pgvector extension and PG tables."""
    from .database import _init_pg_engine, PG_Base
    from .models.conversation import Conversation, Message
    from .models.embedding import AttractionEmbedding

    pg_engine = _init_pg_engine()
    if pg_engine is None:
        import warnings
        warnings.warn("PostgreSQL not available — AI chat features disabled")
        return

    try:
        with pg_engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
    except Exception:
        pass  # Extension may already exist

    PG_Base.metadata.create_all(bind=pg_engine)


@app.get("/")
def root():
    return {"message": "Travel Plan API", "version": "1.0.0"}
