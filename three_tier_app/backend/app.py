from fastapi import FastAPI
import psycopg2
import redis
import os
import json

app = FastAPI()

# DB connection
def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )

# Redis connection
cache = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True)


# 🔹 Create table (auto init)
@app.on_event("startup")
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT
        )
    """)
    conn.commit()
    conn.close()


# 🔹 CREATE user
@app.post("/users")
def create_user(name: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id", (name,))
    user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    # ❗ Invalidate cache
    cache.delete("users")

    return {"id": user_id, "name": name}


# 🔹 READ users (with caching)
@app.get("/users")
def get_users():
    cached = cache.get("users")

    if cached:
        return {"source": "cache", "data": json.loads(cached)}

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users")
    rows = cur.fetchall()
    conn.close()

    users = [{"id": r[0], "name": r[1]} for r in rows]

    cache.set("users", json.dumps(users), ex=30)

    return {"source": "db", "data": users}


# 🔹 UPDATE user
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET name=%s WHERE id=%s", (name, user_id))
    conn.commit()
    conn.close()

    cache.delete("users")

    return {"message": "updated"}


# 🔹 DELETE user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    conn.close()

    cache.delete("users")

    return {"message": "deleted"}