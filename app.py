from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Optional,Annotated
import pickle
import pandas as pd

with open("model.pkl", 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

class UserInput(BaseModel):
