from fastapi import APIRouter, Depends, HTTPException
from models.shemas import RecipeCreate, RecipeOut, IngredientOut
from auth import require_api_key
from database.database import get_connection
from typing import List

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post("/", response_model=RecipeOut, dependencies=[Depends(require_api_key)])
def create_recipe(recipe: RecipeCreate, _:str=Depends(require_api_key)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO recipes (owner_id, title, description)
        VALUES (?, ?, ?)
    """, (1, recipe.title, recipe.description))

    recipe_id = cur.lastrowid

    ingredients_out = []

    for ing in recipe.ingredients:
        cur.execute("""
            INSERT INTO ingredients (recipe_id, name, amount, unit)
            VALUES (?, ?, ?, ?)
        """, (recipe_id, ing.name, ing.amount, ing.unit))

        ingredients_out.append(
            IngredientOut(
                name=ing.name,
                amount=ing.amount,
                unit=ing.unit,
                calories=0,
                recipe_id=recipe_id,
                id=2,
            )
        )

    conn.commit()
    conn.close()

    return RecipeOut(
        id=recipe_id,
        title=recipe.title,
        description=recipe.description,
        ingredients=ingredients_out,
        owner_id=1
    )

