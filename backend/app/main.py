from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import User, Attraction, TravelPlan, PlanDay, PlanItem
from .api.auth import router as auth_router
from .api.attractions import router as attractions_router
from .api.plans import router as plans_router
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


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_attractions()


@app.get("/")
def root():
    return {"message": "Travel Plan API", "version": "1.0.0"}
