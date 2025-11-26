from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
from passlib.context import CryptContext

# --- FastAPI app ---
app = FastAPI(title="User Management API")

# --- Password hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- Database connection ---
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="fastapi_db",
        user="postgres",
        password="newpassword"  # replace with your actual password
    )

# --- Pydantic model ---
class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    phone_number: str

# --- Routes ---

# Root
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Create user
@app.post("/users/")
def create_user(user: User):
    conn = get_connection()
    cur = conn.cursor()
    try:
        hashed_password = hash_password(user.password)
        cur.execute("""
            INSERT INTO users (first_name, last_name, username, password, email, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user.first_name, user.last_name, user.username, hashed_password, user.email, user.phone_number))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
    return {"message": "User created successfully"}

# Get user by username
@app.get("/get_user")
def get_user(username: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT first_name, last_name, username, email, phone_number
        FROM users
        WHERE username = %s
    """, (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

# Update user by username
@app.put("/users/{username}")
def update_user(username: str, user: User):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = hash_password(user.password)
    cur.execute("""
        UPDATE users
        SET first_name=%s, last_name=%s, username=%s, password=%s, email=%s, phone_number=%s
        WHERE username=%s
    """, (user.first_name, user.last_name, user.username, hashed_password, user.email, user.phone_number, username))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "User updated successfully"}

# Delete user by username
@app.delete("/users/{username}")
def delete_user(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    cur.execute("DELETE FROM users WHERE username = %s", (username,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "User deleted successfully"}