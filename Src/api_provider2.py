from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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
def pull_static_data(request: Request, table: str, private_key="", village_id=""):
    if private_key == user_dict[request.client.host]:
        if table == "project":
            json_data = postgreSQL.get_table(table, False, village_id)
            return json_data
        else:
            geojson_data = postgreSQL.get_table(table)
            return geojson_data
    else:
        print(current_seed)

@app.post("/api/auth")
def get_authenticate(request: Request, username: str, password: str):
    if generate_password(password) == username:
        access_token = generate_password("1234", 20)
        user_dict[request.client.host] = access_token
	return {"access-token": access_token}

if __name__ == "__main__":
    import uvicorn
    host = '127.0.0.1'  # '0.0.0.0' to bind to all available network interfaces
    port = 443  # Change this to your desired port
    uvicorn.run(app, host=host, port=port)
