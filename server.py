from fastapi import FastAPI

app = FastAPI()

data = {
    "fastfood":["Pizza","Burger"],
    "desifood":["Chicken Karahi","Nihari"],
}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/{item}")
async def root(item):
    if item in data:
       return {"Item Found": data[item]}
