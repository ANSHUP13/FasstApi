from fastapi import FastAPI, Query
import json
from fastapi import HTTPException
import model
from model import Person, Update_Person
from pydantic import Field
from typing import Dict


app = FastAPI()
    
def load_data() -> dict:
    with open('data.json', "r") as file:
        d = dict(json.load(file))
    return d


@app.get("/")
async def root():
    return {"message": "welcome to the FastAPI application!"}


@app.get("/views", response_model=Dict[str, model.Person])
async def views():
    data = load_data()
    return data


@app.get("/views/person/name/{name}")
async def view_by_name(name: str):
    data = load_data()
    for key in data:
        if data[key]['name'] == name:
            return {"data": {key : data[key]}}
    else:
        raise HTTPException(status_code=404, detail="person not found")
    

@app.get("/views/person_id/{id}")
async def view_by_id(id: str):
    data = load_data()
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
     
    data = load_data()
    datalist = list(data.items())
    if sort_by == 'a':
        if order == 'i':
            datalist.sort(key=lambda x: x[1]['age'])
        else:
            datalist.sort(key=lambda x: x[1]['age'], reverse=True)
    if sort_by == 'w':
        if order == 'i':
            datalist.sort(key=lambda x: x[1]['weight'])
        else:
            datalist.sort(key=lambda x: x[1]['weight'], reverse=True)    
    return {"data": datalist}
    

@app.post("/create/person")
async def create_person(person: Person):
    data = load_data()
    if person.id in data:
        raise HTTPException(status_code=400, detail="person with this id already exists")
    
    data[person.id] = person.model_dump()
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

    return {"message": "person created successfully", "data": person}


@app.put("/update/person/{id}")
async def update_person(id: str, person: Update_Person):
    data = load_data()
    if id not in data:
        raise HTTPException(status_code=404, detail="person not found")
    
    cur = data[id]
    update_data = person.model_dump(exclude_unset=True)
    for key, value in update_data.items():
            cur[key] = value
    updated = Person(**cur)
    data[id] = updated.model_dump()
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

    return {"message": "person updated successfully", "data": updated}

@app.delete("/delete/person/{id}")
async def delete_person(id: str):
    data = load_data()
    if id not in data:
        raise HTTPException(status_code=404, detail="person not found")
    
    del data[id]
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

    return {"message": "person deleted successfully"}  

