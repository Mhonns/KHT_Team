from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import postgreSQL
import json
import hashlib
import uvicorn
import ssl
from village_url_model import village_url_data
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

@app.get("/api/village/")
def pull_village_data(village_id="", year="", start_year="", end_year=""):
    if year != "" or (start_year != "" and end_year != ""):
        geojson_data = postgreSQL.get_village_project_by_year(year, start_year, end_year)
    else:
        geojson_data = postgreSQL.get_village(village_id)
    return geojson_data

@app.get("/api/project/")
def pull_project_data(village_id="", start_year="", end_year=""):
    json_data = postgreSQL.get_project(village_id, start_year, end_year)
    return json_data

# @app.get("/api/get_village_project_by_year/")
# def pull_village_project_by_year(year="", start_year="", end_year=""):
#     geojson_data = postgreSQL.get_village_project_by_year(year, start_year, end_year)
#     return geojson_data

# 4 types of project data: WASH, Irrigation, Further Education Scholarships, Dormitory Meals, School Buses
@app.get("/api/project_type/")
def pull_project_type_data(project_type=""):
    geojson_data = postgreSQL.get_project_type(project_type)
    return geojson_data

@app.get("/api/project_donor/")
def pull_project_donor_data(project_id=""):
    json_data = postgreSQL.get_project_donor(project_id)
    return json_data

@app.get("/api/school/")
def pull_school_data():
    geojson_data = postgreSQL.get_school()
    return geojson_data

@app.get("/api/hospital/")
def pull_hospital_data():
    geojson_data = postgreSQL.get_hospital()
    return geojson_data

@app.get("/api/mhs_districts/")
def pull_mhs_districts_data():
    geojson_data = postgreSQL.get_mhs_districts()
    return geojson_data

@app.get("/api/mhs_roads/")
def pull_mhs_roads():
    geojson_data = postgreSQL.get_mhs_roads()
    return geojson_data

@app.get("/api/mhs_water_areas/")
def pull_mhs_water_ares():
    geojson_data = postgreSQL.get_mhs_water_ares()
    return geojson_data

@app.get("/api/mhs_water_lines")
def pull_mhs_water_ares():
    geojson_data = postgreSQL.get_mhs_water_lines()
    return geojson_data

@app.get("/api/village/distance/")
def get_village_from_distance(distance="", facility_type="", facility_name=""):
    geojson_data = postgreSQL.get_village_from_distance(distance, facility_type, facility_name)
    return geojson_data

@app.post("/auth")
def get_auth(response : Response, username: str, key: str):
    response.set_cookie(key="Username", value=generate_password("1234", 20))
    return {"message": "Come to the dark side, we have cookies"}

# Post for requesting village_name and url # article_title and posted_date is not necessary
@app.post("/api/post/village_url/")
async def create_village_url(village_url_data: village_url_data):
    # Insert the data into the database
    message = postgreSQL.insert_village_url(village_url_data)
    return {"message": message}

if __name__ == "__main__":

    host = '0.0.0.0'  # '0.0.0.0' to bind to all available network interfaces
    port = 443  # Change this to your desired port for HTTPS (443 is the default HTTPS port)

    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ssl_context.load_cert_chain('cert.pem', keyfile='key.pem')

    # uvicorn.run(app, host=host, port=port, ssl_keyfile='key.pem', ssl_certfile='cert.pem', ssl_keyfile_password=passphrase)

    cert_file = 'cert.pem'
    key_file = 'key.pem'
    passphrase = b'khtteam1234'

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file, password=passphrase)

    uvicorn.run(app, host=host, port=port, ssl_keyfile=key_file, ssl_certfile=cert_file, ssl_keyfile_password=passphrase)
    # uvicorn.run(app, host=host, port=2546)
