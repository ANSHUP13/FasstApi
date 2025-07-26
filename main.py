from fastapi import FastAPI, Query
import json
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List, Optional, Annotated

app = FastAPI()

class Person(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50)]
    age: Annotated[int, Field(ge=0, le=120)]  # age must be between 0 and 120
    weight: Annotated[float, Field(gt=0, strict=True)]  # weight must be greater than 0
    height: Annotated[float, Field(gt=0)]  # height must be greater than 0
    email: EmailStr
    contact: str
    address: Optional[str] = None
    hobbies: Optional[List[str]] = Field(default_factory=list, max_length=5)  # max 5 hobbies allowed
    # instantiate a new list for each instance similar to hobbies: Optional[List[str]] = [] 


def loaddata():
    with open("data.json", "r") as file:
        data = json.load(file)
        for key in data:
            data[key] = Person(**data[key])
    return data


@app.get("/")
async def root():
    return {"message": "welcome to the FastAPI application!"}


@app.get("/views")
async def views():
    data = loaddata()
    return data


@app.get("/views/name/{name}")
async def view_by_name(name: str):
    data = loaddata()
    for key in data:
        if data[key].name == name:
            return {"data": {key : data[key]}}
    else:
        raise HTTPException(status_code=404, detail="person not found")
    

@app.get("/views/id/{id}")
async def view_by_id(id: str):
    data = loaddata()
    print(f"Searching for ID: {id}")
    print(f"Available IDs: {list(data.keys())}")
    if id in data:
        return {"data": {id: data[id]}}
    raise HTTPException(status_code=404, detail="person not found")

@app.get("/view/")
async def view_sorted(sort_by: str = Query('a', description="Sort by a specific field ('a' for age, 'w' for weight)"),
                      order: str = Query('i', description="Order of sorting: 'i' for ascending, 'd' for descending")):
    
    if order not in ['i', 'd']:
        raise HTTPException(status_code=400, detail="order must be 'i' or 'd'")
    
    if sort_by not in ['a', 'w']:
        raise HTTPException(status_code=400, detail="sort_by must be 'a' or 'w'")
    
    data = loaddata()
    datalist = list(data.items())
    if sort_by == 'a':
        if order == 'i':
            datalist.sort(key=lambda x: x[1].age)
        else:
            datalist.sort(key=lambda x: x[1].age, reverse=True)
    if sort_by == 'w':
        if order == 'i':
            datalist.sort(key=lambda x: x[1].weight)
        else:
            datalist.sort(key=lambda x: x[1].weight, reverse=True)    
    return {"data": datalist}

