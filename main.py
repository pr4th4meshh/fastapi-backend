from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def check_health():
    return {"message": "Healthy FastAPI running on port 9000"}