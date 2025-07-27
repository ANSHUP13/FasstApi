from fastapi import FastAPI, Query
import json
from fastapi import HTTPException
import model
from model import Person, Group
from typing import Literal
from pydantic import Field

app = FastAPI()
    
def load_data(filename) -> dict:
    with open(filename, "r") as file:
        d = dict(json.load(file))
    return d


@app.get("/")
async def root():
    return {"message": "welcome to the FastAPI application!"}


@app.get("/views", response_model=Dict[str, model.Person])
async def views():
    data = load_data('dataPerson.json')
    return data


@app.get("/views/person/name/{name}")
async def view_by_name(name: str):
    data = load_data('dataPerson.json')
    for key in data:
        if data[key].name == name:
            return {"data": {key : data[key]}}
    else:
        raise HTTPException(status_code=404, detail="person not found")
    

@app.get("/views/person_id/{id}")
async def view_by_id(id: str):
    data = load_data('dataPerson.json')
    print(f"Searching for ID: {id}")
    print(f"Available IDs: {list(data.keys())}")
    if id in data:
        return {"data": {id: data[id]}}
    raise HTTPException(status_code=404, detail="person not found")

@app.get("/view/{data_type}")
async def view_sorted(sort_by: str = Query('a', description="Sort by a specific field ('a' for age, 'w' for weight)"),
                      order: str = Query('i', description="Order of sorting: 'i' for ascending, 'd' for descending"),
                      data_type: str = 'person'):
    
    if order not in ['i', 'd']:
        raise HTTPException(status_code=400, detail="order must be 'i' or 'd'")
    
    if sort_by not in ['a', 'w']:
        raise HTTPException(status_code=400, detail="sort_by must be 'a' or 'w'")
    
    if data_type not in ['person', 'group']:
        raise HTTPException(status_code=400, detail="data_type must be 'person' or 'group'")
    
    if data_type == 'person':
        filename = 'dataPerson.json'    
        data = load_data(filename)
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
    else:
        filename = 'dataGroup.json'  
        data = load_data(filename)
        datalist = list(data.items())
        if order == 'i':
            datalist.sort(key=lambda x: len(x[1].members))
        else:
            datalist.sort(key=lambda x: len(x[1].members), reverse=True)   
        return {"data": datalist}
    

@app.post("/create/person")
async def create_person(person: Person):
    data = load_data('dataPerson.json')
    if person.id in data:
        raise HTTPException(status_code=400, detail="person with this id already exists")
    
    data[person.id] = person.model_dump()
    print(data)
    with open('dataPerson.json', 'w') as file:
        json.dump(data, file, indent=4)

    return {"message": "person created successfully", "data": person}

@app.post("/create/group")
async def create_group(group: Group):   
    data = load_data('dataGroup.json')
    if group.group_id in data:
        raise HTTPException(status_code=400, detail="group with this id already exists")
    
    data[group.group_id] = group.model_dump()
    print(data)
    with open('dataGroup.json', 'w') as file:
        json.dump(data, file)

    return {"message": "group created successfully", "data": group}