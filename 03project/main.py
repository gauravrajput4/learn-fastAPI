

from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def load_date():
    with open("patients.json", "r") as f:
        data=json.load(f)
    return data

@app.get("/")
def home():
    return {"message":"Patient Management System API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API for Patient records"}

@app.get("/view")
def view():
    data = load_date()
    return {"data": data}

@app.get("/view/patients/") #sort_by=[weight,height,bmi] order=[ascending,descending]
def view_patients(sort_by:str=Query(...,description="Sort on the basis of height, weight, and age"),order:str=Query('asc',description="Sort in asc and desc order")):
    valid_fields = ["height","weight","age"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail="Sort must be one of the following: height, weight, age")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail="Order must be one of the following: asc or desc")
    data =load_date()
    order=True if order == "desc" else False
    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=order)
    return {"data": sorted_data}



@app.get("/patients/{patient_id}")
def patient(patient_id: str=Path(...,title="Patient ID",description="Patient ID",example="P001")):
    data = load_date()
    if patient_id in data:
        return {f"patient {patient_id}": data[patient_id]}
    raise HTTPException(status_code=404, detail="Patient not found")