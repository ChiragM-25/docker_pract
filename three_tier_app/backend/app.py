from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}

@app.get("/db")
def test_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        conn.close()
        return {"db_version": version}
    except Exception as e:
        return {"error": str(e)}