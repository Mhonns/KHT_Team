from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import postgreSQL
import json
import hashlib

app = FastAPI()

user_dict = {}

# Encryption ensuring the private connection
def generate_password(seed, characters = 16):
    # Use SHA-256 hash function (you can choose a different one if needed)
    hashed_seed = hashlib.sha256(seed.encode()).hexdigest()
    password = hashed_seed[:characters]
    return password

# CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace '*' with specific origins
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Origin", "Content-Type"],
)

class DistanceRequest(BaseModel):
    marker1: str
    marker2: str

@app.get("/")
def read_root():
    return {"message": "The data hosting is working!"}

@app.get("/api/get/")
def pull_static_data(table: str, village_id=""):
    if table == "project":
        json_data = postgreSQL.get_table(table, False, village_id)
        return json_data
    else:
        geojson_data = postgreSQL.get_table(table)
        return geojson_data

@app.post("/api/auth")
def get_authenticate(username: str, password: str):
    access_token = generate_password("1234", 20)
    user_dict[username] = access_token
    return {"access-token": access_token}

@app.post("/auth")
def get_auth(response : Response, username: str, key: str):
    response.set_cookie(key="Username", value=generate_password("1234", 20))
    return {"message": "Come to the dark side, we have cookies"}

@app.get("/.well-known/pki-validation/78AE459F1B584324BF32399DA646034B.txt")
async def get_txt_file():
    file_name = "78AE459F1B584324BF32399DA646034B.txt"
    file_path = f"./{file_name}"
    file = open(file_path, "r")
    return PlainTextResponse(file.read())

if __name__ == "__main__":
    import uvicorn
    host = '0.0.0.0'  # '0.0.0.0' to bind to all available network interfaces
    port = 80  # Change this to your desired port
    uvicorn.run(app, host=host, port=port)
