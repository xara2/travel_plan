from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL, PGVECTOR_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PostgreSQL engine for vector store + conversations (lazy init)
_pg_engine = None
_pg_available = None


def _init_pg_engine():
    global _pg_engine, _pg_available
    if _pg_available is not None:
        return _pg_engine
    try:
        _pg_engine = create_engine(PGVECTOR_URL, pool_size=3, max_overflow=5)
        with _pg_engine.connect() as conn:
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
        _pg_available = True
    except Exception:
        _pg_available = False
        _pg_engine = None
    return _pg_engine


PG_SessionLocal = None


def _get_pg_session_local():
    global PG_SessionLocal
    if PG_SessionLocal is None:
        eng = _init_pg_engine()
        if eng is not None:
            PG_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=eng)
        else:
            PG_SessionLocal = False  # Sentinel: PG not available
    return PG_SessionLocal if PG_SessionLocal is not False else None


PG_Base = declarative_base()


def get_pg_db():
    sm = _get_pg_session_local()
    if sm is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=503,
            detail="PostgreSQL 数据库未连接，请检查 PGVECTOR_URL 配置",
        )
    db = sm()
    try:
        yield db
    finally:
        db.close()
