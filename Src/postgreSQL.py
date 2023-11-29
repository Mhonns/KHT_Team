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
    # cursor.execute(query)
    # columns = [desc[0] for desc in cursor.description]
    # results = cursor.fetchall()

    # features = []
    # for row in results:
    #     properties = dict(zip(columns, row))
    #     geometry = properties.pop('geom', None)  # Assuming 'geometry' is the column name for geometry data
    #     feature = geojson.Feature(properties=properties, geometry=geometry)
    #     features.append(feature)

    # feature_collection = geojson.FeatureCollection(features)
    # return geojson.dumps(feature_collection, indent=2)
   
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
        geojson_result = geojson.dumps(feature_collection, indent=2)
        return geojson_result

# Query all vallages datail
def get_table(target_table):
    # Example query
    query = sql.SQL("SELECT * FROM {};").format(sql.Identifier(target_table))
    cursor.execute(query)
    geojson_result = query_to_geojson(cursor, query)
    results = cursor.fetchall()
    # return geojson_result
    return {"villages": geojson_result}

# Establish a connection to the database
try:
    connection = psycopg2.connect(**connection_params)
    print("Connected to the database!")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    print(get_table("village"))

except psycopg2.Error as e:
    print(f"Unable to connect to the database. Error: {e}")

def close_all():
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")
