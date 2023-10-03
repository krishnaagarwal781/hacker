from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
import datetime
app = FastAPI()

# MongoDB configuration
mongo_client = MongoClient("mongodb+srv://parth01:parth123@cluster0.77are8z.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB URI
db = mongo_client["Hacking"]  # Replace with your database name
collection = db["Users"]  # Replace with your collection name

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for the information to be stored
class DisplayedInfo(BaseModel):
    data: dict

@app.post("/store_information")
async def store_information(info: DisplayedInfo):
    print(DisplayedInfo)
    try:
        # Add a timestamp to the data
        info.data["timestamp"] = datetime.datetime.now()
        
        # Insert the data into the MongoDB collection
        result = collection.insert_one(info.data)

        if result.acknowledged:
            return {"message": "Data stored successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to store data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


