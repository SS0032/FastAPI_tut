from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(..., description="The full name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="The city where the patient resides", example="New York")]
    age: Annotated[int, Field(..., description="The age of the patient", example=30)]
    gender: Annotated[Literal['male','female','others'], Field(..., description="The gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in meters", example=1.755)]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kilograms", example=70.2)]

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self)->str:
        bmi_value=self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 25:
            return "Normal weight"
        elif 25 <= bmi_value < 30:
            return "Overweight"
        else:
            return "Obese"


def load_data():
    with open("patients.json", "r") as f:
        data= json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


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

@app.post('/create')
def create_patient(patient: Patient):
    #Load existing data
    data=load_data()
    #Check if patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    #Add new patient to data
    data[patient.id]=patient.model_dump(exclude=['id'])

    #Save updated data back to file
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201) 