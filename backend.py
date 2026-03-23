from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API działa"}


@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Wojtek"},
        {"id": 2, "name": "Anna"}
    ]


@app.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return {"status": "ok", "token": "abc123"}
    else:
        return {"status": "error"}