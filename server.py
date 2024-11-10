from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import base64

app = FastAPI()

# SQLite Database setup
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT,
    designation TEXT,
    image BLOB
)
''')
conn.commit()

# Request model for receiving data
class User(BaseModel):
    id: str
    name: str
    designation: str
    image_base64: str

# Endpoint to save data to the SQLite database
@app.post("/submit-data")
async def submit_data(user: User):
    try:
        # Decode base64 image data to binary
        image_data = base64.b64decode(user.image_base64)

        # Insert data into SQLite
        cursor.execute('''
        INSERT INTO users (id, name, designation, image) 
        VALUES (?, ?, ?, ?)
        ''', (user.id, user.name, user.designation, image_data))
        conn.commit()
        return {"message": "Data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the server with: uvicorn api:app --reload
