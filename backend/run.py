import uvicorn
import os

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
