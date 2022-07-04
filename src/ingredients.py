from flask_restful import Resource
from flask import request
from main import db

def converToIngredientShort(ingredient):
    return {
        "id": ingredient[0],
        "name": ingredient[1],
        "price": float(ingredient[3]),
    }

class Ingredients(Resource):
    def get(self):
        try:
            rawStatement = f"SELECT * FROM ZUTAT "
            result = db.engine.execute(rawStatement)
            data = []
            for r in result:
                data.append(converToIngredientShort(r))
            return data
        except Exception as e:
            return {"error: ": e}
    def post(self):
        print(request.get_json())

