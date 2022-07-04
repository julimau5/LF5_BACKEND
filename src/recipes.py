from flask_restful import Resource
from flask import request
from main import db


def convertToRecipeShort(row):
    return {
        "id": row[0],
        "name": row[1],
        "imageUrl": row[3]
    }

def setGetStatement(args):
    queryType = args['type']
    match queryType:
        case 'all':
            return f"SELECT * FROM Rezepte"
        case 'byCategory':
            category = args['category']
            return f"SELECT Rezepte.* FROM Rezepte JOIN RezeptKategorien ON Rezepte.RezeptID = RezeptKategorien.RezeptID JOIN Ernährungskategorien ON Ernährungskategorien.EkID = RezeptKategorien.EkID WHERE Ernährungskategorien.Name = '{category}';"
        case 'byIngredient':
            ingredient = args['ingredient']
            return f"SELECT Rezepte.* FROM Rezepte JOIN ZutatenDerRezepte ON Rezepte.RezeptID = ZutatenDerRezepte.RezeptID JOIN ZUTAT ON ZUTAT.ZUTATENNR = ZutatenDerRezepte.ZUTATENNR WHERE ZUTAT.Bezeichnung = '{ingredient}';"

class Recipes(Resource):
    def get(self):
        try:
            rawStatement = setGetStatement(request.args)
            result = db.engine.execute(rawStatement)
            data = []
            for r in result:
                data.append(convertToRecipeShort(r))
            return data
        except Exception as e:
            return {"error: ": e}
    def post(self):
        try:
            body = request.get_json() 
            result = db.engine.execute("SELECT MAX(RezeptID) FROM Rezepte")
            for r in result:
                newId = r[0] + 1
            rawRecipeStatement = f"INSERT INTO Rezepte (RezeptID, Rezeptname, Zubereitung, bildUrl) VALUES ({newId}, '{body['name']}', '{body['directions']}', '{body['imageUrl']}');"
            rawIngredientsStatement = f""
            rawCategoriesStatement = f""
            rawRestrictionsStatement = f""
            print(rawRecipeStatement)
            db.engine.execute(rawRecipeStatement)
            return {"message": "successfull creation"}
        except Exception as e:
            return {"error: ": e}

