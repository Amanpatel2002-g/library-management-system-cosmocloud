from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel

# MongoDB connection
url = "mongodb+srv://apofficial2002:aOVVzQ2RZIZVoRyj@cluster0.qt02vp5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(url)
db = client["students_database"]
collection = db["students_collection"]

# FastAPI app
app = FastAPI()

# MongoDB Model
class MongoDBModel(BaseModel):
    id: str = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

# Pydantic Model for Student
class Student(BaseModel):
    name: str
    age: int
    address: dict

# Create Student
@app.post("/students", response_model=MongoDBModel)
async def create_student(student: Student):
    student_dict = student.dict()
    result = collection.insert_one(student_dict)
    inserted_id = str(result.inserted_id)
    return {"id": inserted_id}

# List Students
@app.get("/students", response_model=list[Student])
async def list_students(country: str = Query(None), age: int = Query(None)):
    filter_query = {}
    if country:
        filter_query['address.country'] = country
    if age:
        filter_query['age'] = {"$gte": age}

    students = collection.find(filter_query)
    return list(students)

# Fetch Student
@app.get("/students/{student_id}", response_model=Student)
async def fetch_student(student_id: str):
    student = collection.find_one({"_id": ObjectId(student_id)})
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")

# Update Student
@app.patch("/students/{student_id}", response_model=None)
async def update_student(student_id: str, student_data: Student):
    student_data = jsonable_encoder(student_data)
    update_result = collection.update_one({"_id": ObjectId(student_id)}, {"$set": student_data})
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

# Delete Student
@app.delete("/students/{student_id}", response_model=None)
async def delete_student(student_id: str):
    delete_result = collection.delete_one({"_id": ObjectId(student_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
