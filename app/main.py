from fastapi import FastAPI

from app.api import tenders
from app.api.v1 import auth, users

app = FastAPI(title="TenderTruck API")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(tenders.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "TenderTruck API успешно запущен"}
