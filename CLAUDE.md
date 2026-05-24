# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Travel Plan (旅行计划助手) — a full-stack travel planning web app. Users search attractions by destination city, pick their favorites, set travel dates, and auto-generate a day-by-day itinerary with an interactive map route.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + Ant Design 5 + Tailwind CSS + Leaflet |
| Backend | Python FastAPI + SQLAlchemy ORM |
| Database | SQLite (dev) at `backend/data/travel.db` |
| Auth | JWT (python-jose) with phone/email verification codes |
| Maps | OpenStreetMap via Leaflet (free, no key required) |

## Commands

```bash
# Backend
cd backend
pip install -r requirements.txt
python run.py                          # http://localhost:8000

# Frontend
cd frontend
npm install
npm run dev                            # http://localhost:5173

# Build frontend for production
cd frontend && npm run build
```

Dev mode: verification code `123456` works as universal login code. Real codes print to the backend console.

## Project Structure

```
backend/
├── app/
│   ├── main.py            # FastAPI app, CORS, router registration
│   ├── config.py           # DB URL, JWT secret, token expiry
│   ├── database.py         # SQLAlchemy engine + session factory
│   ├── seed.py             # 30+ Chinese tourist attractions seed data
│   ├── models/             # User, Attraction, TravelPlan, PlanDay, PlanItem
│   ├── schemas/            # Pydantic request/response models
│   ├── api/                # auth (login/send-code), attractions (search), plans (CRUD + generate)
│   └── utils/auth.py       # JWT create/verify, get_current_user dependency
├── data/                   # travel.db (auto-created on first run)
└── run.py                  # uvicorn entrypoint with reload

frontend/
├── src/
│   ├── App.jsx             # Routes: /, /login, /plans/:id, /my-plans
│   ├── pages/
│   │   ├── Home.jsx        # City search → attraction grid → date picker → generate plan
│   │   ├── Login.jsx       # Phone/email + verification code
│   │   ├── PlanDetail.jsx  # Day-by-day timeline + Leaflet map with route polyline
│   │   └── MyPlans.jsx     # Card grid of saved plans with delete
│   ├── components/
│   │   ├── Layout.jsx      # Top nav bar, auth guard
│   │   └── MapView.jsx     # Leaflet wrapper: markers, popups, polyline, fitBounds
│   └── services/api.js     # Axios instance with JWT interceptor
└── index.html
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /api/auth/send-code | No | Send verification code (phone/email) |
| POST | /api/auth/login | No | Login with code, returns JWT |
| GET | /api/auth/me | Yes | Current user info |
| GET | /api/attractions?city=&keyword= | No | Search attractions |
| GET | /api/attractions/cities | No | List all cities with attractions |
| GET | /api/attractions/:id | No | Get single attraction |
| POST | /api/plans/generate | Yes | Generate plan from selected attraction IDs + dates |
| GET | /api/plans | Yes | List user's plans |
| GET | /api/plans/:id | Yes | Get plan with days, items, and attraction details |
| DELETE | /api/plans/:id | Yes | Delete a plan |

## Plan Generation Algorithm

`backend/app/api/plans.py:_build_plan_out()` handles distribution:
1. Sorts attractions with coordinates by latitude for geographic grouping
2. Splits evenly across the given number of days
3. Assigns time slots (上午/下午/傍晚) per item
4. Eager-loads all related data (days → items → attraction) for the response
