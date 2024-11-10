from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import base64
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


# Allow CORS for specific origins (replace with your frontend URL if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins; you can replace '*' with specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


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

# Response model for sending user data
class UserResponse(BaseModel):
    id: str
    name: str
    designation: str
    image_base64: Optional[str] = None

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

# Endpoint to search user by ID
@app.get("/search-user/{user_id}", response_model=UserResponse)
async def search_user(user_id: str):
    try:
        # Fetch user data by ID
        cursor.execute('''
        SELECT id, name, designation, image FROM users WHERE id = ?
        ''', (user_id,))
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Extract user details
        user_id, name, designation, image_data = result

        # Convert binary image data to base64 string
        image_base64 = base64.b64encode(image_data).decode('utf-8') if image_data else None

        # Return user details
        return UserResponse(
            id=user_id,
            name=name,
            designation=designation,
            image_base64=image_base64
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the server with: uvicorn api:app --reload
