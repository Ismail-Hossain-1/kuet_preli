### Add a new ingrediant
`/ingredients`

-POST (body):
```
{ 
    "id": "ingredient_001", 
    "name": "Sugar", 
    "quantity": 500, 
    "unit": "grams" 
}
```

`/recipes`

-POST
```
{
    "id": "recipe_001",
    "name": "Chocolate Cake",
    "description": "A rich chocolate cake.",
    "instructions": "Preheat oven, mix ingredients, bake for 25 minutes.",
    "taste": "sweet",
    "reviews": 5,
    "cuisine_type": "Italian",
    "prep_time": 30,
    "is_sweet": true
}
```
`/recipes  `
-GET

### POST /recipes/{id}/ingredients - Add Ingredients to a Recipe
`POST /recipes/{id}/ingredients`

```
{
    "id": "recipe_001",
    "name": "Chocolate Cake",
    "description": "A rich chocolate cake.",
    "instructions": "Preheat oven, mix ingredients, bake for 25 minutes.",
    "taste": "sweet",
    "reviews": 5,
    "cuisine_type": "Italian",
    "prep_time": 30,
    "is_sweet": true
}
```

