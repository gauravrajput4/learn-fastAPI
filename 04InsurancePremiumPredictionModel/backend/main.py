from fastapi import FastAPI
from  pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
import pickle
from typing import Annotated
import pandas as pd

# import the ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()
tier_1_cities=["Mumbai","Delhi","Banglore","Chennai","Kolkata","Hyderbad","Pune"]
tier_2_cities=[
    "Jaipur","Chandigarh","Indore","Lucknow","Patna","Ranchi","Visakhapatnam","Coimbatore",
    "Bhopal","Nagppur","Vadodara","Surat","Rajkot","Jodhpur","Raipur","Amritsar","Varanasi",
    "Agra","Dehradun","Mysore","Jabalpur","Guwahati","Thiruvananthpuram","Ludhiana","Nashik",
    "Bhavnagar","Gwalior","Dhanbad","Bareilly","Aligarh","Gaya","Kozhikode","Warangal",
    "Kolhapur","Bilaspur","Jalandhar","Noida","Guntur","Asansol","Siliguri"
]

# Pydantic model to validate incoming data
class UserInput(BaseModel):

    age:Annotated[int,Field(...,gt=0,lt=120,description="User age in years.")]
    weight:Annotated[float,Field(...,gt=0,description="User weight in kilograms.")]
    height:Annotated[float,Field(...,gt=0,description="User height in meters.")]
    income_lpa:Annotated[float,Field(...,gt=0,description="User income in lpa.")]
    smoker:Annotated[bool,Field(...,description="User smoking.")]
    city:Annotated[str,Field(...,description="User city.")]
    occupation:Annotated[str,Field(...,description="User occupation.")]

    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker and self.bmi > 27:
            return 'medium'
        else:
            return 'low'

    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_age"
        return "senior"

    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        return 3

@app.get('/')
def home():
    return {'message': 'Welcome to Insurance Premium Prediction Model'}

@app.post("/predict")
async def predict(user_input:UserInput):
    inputDF=pd.DataFrame([{
        'bmi':user_input.bmi,
        'age_group':user_input.age_group,
        'city_tier':user_input.city_tier,
        'lifestyle_risk':user_input.lifestyle_risk,
        'income_lpa':user_input.income_lpa,
        'occupation':user_input.occupation
    }])
    prediction=model.predict(inputDF)[0]

    return JSONResponse(status_code=200,content={"predicted_category":prediction})
