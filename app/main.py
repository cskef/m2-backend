# app/main.py
from fastapi import FastAPI

app = FastAPI(title="M2 Backend", version="0.1.0")

# endpoint de test
@app.get("/check") 
def check(): 
    return {"status": "ok", "version": "0.1.0"}