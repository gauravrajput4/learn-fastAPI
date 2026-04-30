from typing import Dict

from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    prediction_category: str=Field(...,description="The category of the prediction")

    confidence: float=Field(...,description="The confidence score of the prediction")
    class_probs: Dict[str,float]=Field(...,description="The class probabilities of the prediction",example={"low":0.1,"medium":0.15,"high":0.84})