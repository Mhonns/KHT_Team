from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import postgreSQL
import json
app = FastAPI()

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
async def pull_static_data(table: str):
    print(table)
    geojson_data = postgreSQL.get_table(table)
    return geojson_data

@app.post("/api/get-distance")
def get_distance(request: DistanceRequest):
    marker1 = request.marker1
    marker2 = request.marker2
    distance = f"TODO Return distance between {marker1} to {marker2}"
    return {"message": distance}

@app.get("/api/find-nearest-hospital")
def find_nearest_hospital():
    # Implement logic to find the nearest hospital
    return {"message": "TODO"}

if __name__ == "__main__":
    import uvicorn

    host = '127.0.0.1'  # '0.0.0.0' to bind to all available network interfaces
    port = 443  # Change this to your desired port
    uvicorn.run(app, host=host, port=port)
