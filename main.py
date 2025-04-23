import os

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


CONNECTION = {
    "database": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
}


@app.route("/")
def index():
    return "it's working"


@app.route("/elevation", methods=["GET"])
def elevation():
    output = fetch_data("postgres.elevation")
    return jsonify(output)


@app.route("/temp", methods=["GET"])
def temp():
    output = fetch_data("postgres.temp")
    return jsonify(output)


def fetch_data(table_name):
    with psycopg2.connect(**CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                    SELECT JSON_BUILD_OBJECT('type', 'FeatureCollection',
                    'features', JSON_AGG(ST_AsGeoJSON({table_name}.*)::json)) FROM {table_name};
            """)

            return cur.fetchone()[0]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
