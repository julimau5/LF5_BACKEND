from unittest import result
from flask_restful import Resource
from flask import request
from main import db

class Recipes(Resource):
    def get(self):
        try:
            rawStatement = f"SELECT * FROM Rezepte"
            result = db.engine.execute(rawStatement)
            for r in result:
                print(r)
            return{ "jay": "digga"}
        except Exception as e:
            return {"error: ": e}