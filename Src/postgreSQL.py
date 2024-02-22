from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import geojson
from psycopg2 import sql
from shapely import wkb
from shapely.geometry import mapping
import json
import psycopg2
import geojson
from psycopg2 import sql
from shapely import wkb
from shapely.geometry import mapping
import json

# Database configurations
db_host = "127.0.0.1" # "103.153.118.77"
db_port = "5432" # "2547"
db_name = "mhs_geographic"
db_user = "postgres"
db_password = "postgres"

# Connection parameters
connection_params = {
    "host": db_host,
    "port": db_port,
    "dbname": db_name,
    "user": db_user,
    "password": db_password,
}

def query_to_geojson(cursor, query):
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    features = []
    for row in results:
        properties = dict(zip(columns, row))
        geometry_key = 'geom'
        geometry_str = properties.get(geometry_key)
        if geometry_str is not None:
            try:
                # Convert the hex WKB to a Shapely geometry
                geometry = wkb.loads(geometry_str, hex=True)
                # Convert the Shapely geometry to GeoJSON
                geometry_geojson = mapping(geometry)
                feature = geojson.Feature(properties=properties, geometry=geometry_geojson)
                features.append(feature)
            except (json.JSONDecodeError, ValueError):
                print(f"Invalid GeoJSON string: {geometry_str}")

    feature_collection = geojson.FeatureCollection(features)
    # geojson_result = geojson.dumps(feature_collection, indent=2)
    return feature_collection

# Query all data into json format
def query_to_json(cursor, query):
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    features = []
    for row in results:
        properties = dict(zip(columns, row))
        feature = {"properties": properties}
        features.append(feature)
    feature_collection = {"type": "FeatureCollection", "features": features}
    # json_result = json.dumps(feature_collection, indent=2)
    return feature_collection

# Query all column datail
def get_table(target_table, geojson_format=True, argument=""):
    # Example query
    query = None
    if argument == "":
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(target_table))
    elif target_table == "project":
        query = sql.SQL("""SELECT DISTINCT project.id,project_name_en,start_date,end_date,projectvillage.village_id 
                           FROM {} 
                           JOIN projectvillage ON projectvillage.project_id = project.id
                           WHERE village_id = {}::uuid""").format(sql.Identifier(target_table), sql.Literal(argument))

    try:
        cursor.execute(query)
        results = None
        if geojson_format:
            geojson_result = query_to_geojson(cursor, query)
            return geojson_result
        else:
            json_result = query_to_json(cursor, query)
            return json_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

# Query village
def get_village(village_id=""):
    query = None
    if village_id == "":
        query = sql.SQL("SELECT * FROM village")
    else:
        query = sql.SQL("SELECT * FROM village WHERE id = {}").format(sql.Literal(village_id))
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

# Query project
def get_project(village_id="", start_year="", end_year=""):
    query = None
    if village_id == "":
        if start_year == "":
            start_year = -1
        if end_year == "":
            end_year = 9999
        query = sql.SQL("""SELECT projecttest.*, projectStatus.status_name
                            FROM projecttest 
                            JOIN projectStatus ON projecttest.status_id = projectStatus.status_id
                            WHERE start_date >= {} 
                            AND end_date <= {}""").format(sql.Literal(str(start_year)), sql.Literal(str(end_year)))
        print(query.as_string(cursor))
    else:
        query = sql.SQL("""SELECT DISTINCT projecttest.id,project_name_en,start_date,end_date,projectvillagetest.village_id, projectStatus.status_name
                            FROM projecttest
                            JOIN projectvillagetest ON projectvillagetest.project_id = projecttest.id
                            JOIN projectStatus ON projecttest.status_id = projectStatus.Status_id
                            WHERE village_id = {}::uuid""").format(sql.Literal(village_id))
    try:
        cursor.execute(query)
        json_result = query_to_json(cursor, query)
        return json_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction


def get_project_donor(project_id=""):
    query = None
    query = sql.SQL("""SELECT donor.id,donor.donator_name
                        FROM donor
                        JOIN projectdonor ON projectdonor.donor_id = donor.id
                        WHERE projectdonor.project_id= {}::uuid""").format(sql.Literal(project_id))
    try:
        cursor.execute(query)
        json_result = query_to_json(cursor, query)
        return json_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_hospital():
    query = None
    query = sql.SQL("SELECT * FROM hospital")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_school():
    query = None
    query = sql.SQL("SELECT * FROM school")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_mhs_districts():
    query = None
    query = sql.SQL("SELECT * FROM mhs_districts")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_mhs_roads():
    query = None
    query = sql.SQL("SELECT * FROM mhs_roads")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_mhs_water_ares():
    query = None
    query = sql.SQL("SELECT * FROM mhs_water_areas")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_mhs_water_lines():
    query = None
    query = sql.SQL("SELECT * FROM mhs_water_lines")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction 

# Establish a connection to the database
try:
    connection = psycopg2.connect(**connection_params)
    print("Connected to the database!")
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

except psycopg2.Error as e:
    print(f"Unable to connect to the database. Error: {e}")

def close_all():
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")