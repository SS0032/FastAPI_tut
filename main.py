from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data= json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str=Path(..., description="The ID of the patient to retrieve", example="P001")):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
    
@app.get("/sort")
def sort_patients(sort_by: str=Query(..., description="The field to sort patients by", example="age"), order: str=Query("asc", description="The sort order (asc or desc)", example="asc")):
    data=load_data()
    valid_fields=['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field selected. Valid fields are: {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid sort order. Valid options are: asc, desc')
    
    sort_order= True if order=='asc' else False
    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=  not sort_order)
    return sorted_data