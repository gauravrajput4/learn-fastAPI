from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import predict_output,MODEL_VERSION
from schema.prediction_response import PredictionResponse
app = FastAPI()
@app.get('/')
def home():
    return {'message': 'Welcome to Insurance Premium Prediction Model'}

@app.get('/health')
def health():
    return {
        'status':'OK',
        'version':MODEL_VERSION
    }
@app.post("/predict",response_model=PredictionResponse)
async def predict(user_input:UserInput):
    user_input={
        'bmi':user_input.bmi,
        'age_group':user_input.age_group,
        'city_tier':user_input.city_tier,
        'lifestyle_risk':user_input.lifestyle_risk,
        'income_lpa':user_input.income_lpa,
        'occupation':user_input.occupation
    }

    try:
        prediction=predict_output(user_input)
        return JSONResponse(status_code=200,content={"predicted_category":prediction})
    except Exception as e:
        return JSONResponse(status_code=500,content={"message":"An error occurred during prediction","error":str(e)})
