from pydantic import BaseModel
from typing import List
from ingredient import IngredientOut
from models.shemas import IngredientCreate


class RecipeCreate(BaseModel):
    title: str
    ingredients: List[IngredientCreate]

class RecipeOut(BaseModel):
    id: int
    title: str