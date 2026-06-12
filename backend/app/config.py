import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'travel.db')}"
SECRET_KEY = os.environ.get("SECRET_KEY", "travel-plan-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
AMAP_API_KEY = os.environ.get("AMAP_API_KEY", "bda1fef72f188e7766fe00d50de7c496")

# LLM Configuration
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "qwen")
QWEN_API_KEY = os.environ.get("QWEN_API_KEY", "")
ERNIE_API_KEY = os.environ.get("ERNIE_API_KEY", "")
GLM_API_KEY = os.environ.get("GLM_API_KEY", "")

# PGVector Configuration
PGVECTOR_URL = os.environ.get(
    "PGVECTOR_URL",
    "postgresql://postgres:password@localhost:5432/travel_plan",
)

# RAG Configuration
EMBEDDING_DIM = int(os.environ.get("EMBEDDING_DIM", "1536"))
SIMILARITY_THRESHOLD = float(os.environ.get("SIMILARITY_THRESHOLD", "0.7"))
RAG_TOP_K = int(os.environ.get("RAG_TOP_K", "5"))
