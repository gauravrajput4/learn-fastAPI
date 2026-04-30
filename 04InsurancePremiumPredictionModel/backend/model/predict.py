import pickle

import pandas as pd

with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# MLFLOW
MODEL_VERSION='1.0.0'

#Get class label from the model (important for matching probabilities to class names)
class_labels=model.classes_.tolist()

def predict_output(user_input:dict):
    input_data=pd.DataFrame([user_input] )

    #Predict the Class
    predicted_class=model.predict(input_data)[0]

    # Get Probabilities for all classes
    probability=model.predict_proba(input_data)[0]
    confidence=max(probability)

    # create mapping {class_name:probability}
    class_probs=dict(zip(class_labels,map(lambda p:round(p,4),probability)))

    return {
        'predicted_category':predicted_class,
        'confidence':round(confidence,4),
        'class_probs':class_probs
    }

