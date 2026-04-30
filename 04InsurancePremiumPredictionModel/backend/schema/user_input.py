# Pydantic model to validate incoming data
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, computed_field
from config.cities_tier import tier_1_cities, tier_2_cities

class UserInput(BaseModel):

    age:Annotated[int,Field(...,gt=0,lt=120,description="User age in years.")]
    weight:Annotated[float,Field(...,gt=0,description="User weight in kilograms.")]
    height:Annotated[float,Field(...,gt=0,description="User height in meters.")]
    income_lpa:Annotated[float,Field(...,gt=0,description="User income in lpa.")]
    smoker:Annotated[bool,Field(...,description="User smoking.")]
    city:Annotated[str,Field(...,description="User city.")]
    occupation:Annotated[str,Field(...,description="User occupation.")]

    @field_validator('city')
    @classmethod
    def validate_city(cls, value: str) -> str:
        value=value.strip().title()
        return value

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