#%%
from fastapi import FastAPI
app= FastAPI()

@app.get("/")
def read_root():
    return {"message": "This is my first FastAPI"}

@app.get("/about")
def about():
    return {"message": "CampusX is an education platform where you can learn AI"}
#%%
