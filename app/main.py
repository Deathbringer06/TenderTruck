from fastapi import FastAPI

app = FastAPI(title="TenderTruck API")

@app.get("/")
def read_root():
    return {"message": "Сервер TenderTruck успешно запущен!"}