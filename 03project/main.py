from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str,Field(...,description="Patient ID",examples=['P001'])]
    name: Annotated[str,Field(...,min_length=4,max_length=50,description="Patient Name",examples=['Gaurav'])]
    city: Annotated[str,Field(...,description="Patient City",examples=['Mumbai'])]
    age: Annotated[int,Field(...,gt=0,lt=120,description="Patient Age",examples=[4])]
    gender: Annotated[Literal['Male','Female','other'],Field(...,description="Patient Gender",examples=['Male','Female'])]
    height: Annotated[float,Field(...,gt=0,description="Patient Height in meters")]
    weight: Annotated[float,Field(...,gt=0,description="Patient Weight in kgs")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=703*(self.weight/(self.height**2))
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return  'Underweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Overweight'
        else:
            return 'Obese'

class Patient_update(BaseModel):
    name: Annotated[Optional[str], Field(min_length=4, max_length=50, description="Patient Name", examples=['Gaurav'],default=None)]
    city: Annotated[Optional[str], Field(description="Patient City", examples=['Mumbai'],default=None)]
    age: Annotated[Optional[int], Field(gt=0, lt=120, description="Patient Age", examples=[4],default=None)]
    gender: Annotated[Optional[Literal['Male', 'Female', 'other']], Field(description="Patient Gender", examples=['Male', 'Female'],default=None)]
    height: Annotated[Optional[float], Field( gt=0, description="Patient Height in meters",default=None)]
    weight: Annotated[Optional[float], Field(gt=0, description="Patient Weight in kgs",default=None)]

def load_data():
    with open("patients.json", "r") as f:
        data=json.load(f)
    return data
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data,f)

@app.get("/")
def home():
    return {"message":"Patient Management System API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API for Patient records"}

@app.get("/view")
def view():
    data = load_data()
    return {"data": data}

@app.get("/view/patients/") #sort_by=[weight,height,bmi] order=[ascending,descending]
def view_patients(sort_by:str=Query(...,description="Sort on the basis of height, weight, and age"),order:str=Query('asc',description="Sort in asc and desc order")):
    valid_fields = ["height","weight","age"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail="Sort must be one of the following: height, weight, age")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail="Order must be one of the following: asc or desc")
    data =load_data()
    order=True if order == "desc" else False
    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=order)
    return {"data": sorted_data}

@app.get("/patients/{patient_id}")
def patient(patient_id: str=Path(...,title="Patient ID",description="Patient ID",example="P001")):
    data = load_data()
    if patient_id in data:
        return {f"patient {patient_id}": data[patient_id]}
    raise HTTPException(status_code=404, detail="Patient not found")

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    #check if the patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # new patient add to the database
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={"patient created": data[patient.id]})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str,patient: Patient_update):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient = data[patient_id]
    updated_patient_info=patient.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        existing_patient[key] = value
    existing_patient['id']=patient_id
    updated_patient=Patient(**existing_patient)
    existing_patient=updated_patient.model_dump(exclude=['id'])
    #add this dict to data
    data[patient_id]=existing_patient
    save_data(data)
    return JSONResponse(status_code=200, content={"patient updated": data[patient_id]})
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message":"patient deleted"})