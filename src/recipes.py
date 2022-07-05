from tkinter import W
from flask_restful import Resource
from flask import request
from main import db


def convertToRecipeShort(row):
    return {
        "id": row[0],
        "name": row[1],
        "imageUrl": row[3]
    }

def convertToRecipeLong(row):
    return {
        "id": row[0],
        "name": row[1],
        "directions": row[2],
        "imageUrl": row[3]
    }

def convertIngredients(row):
    amount = None if len(row) < 9 else row[9] 
    return {
        "id": row[0],
        "name": row[1],
        "units": row[2],
        "price": float(row[3]),
        "stock": row[4],
        "supplierId": row[5],
        "calories": float(row[6]),
        "carbs": float(row[7]),
        "protein": float(row[8]),
        "amount": amount
    }
def convertRestrictions(row):
    return {

    }


def setGetStatement(args):
    queryType = args['type']
    match queryType:
        case 'all':
            return f"SELECT * FROM Rezepte"
        case 'byCategory':
            category = args['category']
            return f"""SELECT Rezepte.* 
                    FROM Rezepte 
                    JOIN RezeptKategorien ON Rezepte.RezeptID = RezeptKategorien.RezeptID 
                    JOIN Ernährungskategorien ON Ernährungskategorien.EkID = RezeptKategorien.EkID 
                    WHERE Ernährungskategorien.Name = '{category}';"""
        case 'byIngredient':
            ingredient = args['ingredient']
            return f"""SELECT Rezepte.* 
                    FROM Rezepte 
                    JOIN ZutatenDerRezepte ON Rezepte.RezeptID = ZutatenDerRezepte.RezeptID 
                    JOIN ZUTAT ON ZUTAT.ZUTATENNR = ZutatenDerRezepte.ZUTATENNR 
                    WHERE ZUTAT.Bezeichnung = '{ingredient}';"""




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
            rawRecipeStatement = f"""INSERT INTO Rezepte (RezeptID, Rezeptname, Zubereitung, bildUrl) 
                                    VALUES ({newId}, '{body['name']}', '{body['directions']}', '{body['imageUrl']}');"""

            rawIngredientsStatement = "INSERT INTO ZutatenDerRezepte VALUES "
            for ingID in body['ingredientsIds']:
                rawIngredientsStatement += f"({ingID['id']}, {newId}, {ingID['amount']} ),"
            rawIngredientsStatement = rawIngredientsStatement[:-1]

            rawCategoriesStatement = "INSERT INTO RezeptKategorien VALUES "
            for catId in body['categoriesIds']:
                rawCategoriesStatement += f"({newId}, {catId}),"
            rawCategoriesStatement = rawCategoriesStatement[:-1]

            rawRestrictionsStatement = "INSERT INTO RezeptBeschränkungen VALUES "
            for resId in body['restrictionsIds']:
                rawRestrictionsStatement += f"({newId}, {resId}),"
            rawRestrictionsStatement = rawRestrictionsStatement[:-1]

            db.engine.execute(rawRecipeStatement)
            if len(body['categoriesIds']):
                db.engine.execute(rawCategoriesStatement)
            if len(body['restrictionsIds']):
                db.engine.execute(rawRestrictionsStatement)
            if len(body['ingredientsIds']):
                db.engine.execute(rawIngredientsStatement)

            return {"message": "successfull creation"}
        except Exception as e:
            return {"error: ": str(e)}

class FullRecipe(Resource):
    def get(self):
        try:
            recipeId = request.args['id']
            res1 = db.engine.execute(f"SELECT * FROM Rezepte WHERE RezeptID = {recipeId}" )
            data = convertToRecipeLong(res1.fetchone())

            res2 = db.engine.execute(f"""SELECT z.*, zdr.Menge 
                                        FROM ZUTAT z
                                        JOIN ZutatenDerRezepte zdr ON zdr.ZUTATENNR = z.ZUTATENNR
                                        WHERE zdr.RezeptID = {recipeId}""" )
            data['ingredients'] = [convertIngredients(row) for row in res2]

            res3 = db.engine.execute(f"""SELECT b.*
                                        FROM Beschränkungen b
                                        JOIN RezeptBeschränkungen rb ON rb.BeschID = b.BeschId
                                        WHERE rb.RezeptID = {recipeId}""" )
            restrictions = []
            for r in res3:
                restrictions.append(r[1])
            data['restrictions'] = restrictions
           
            res4 = db.engine.execute(f"""SELECT k.*
                                        FROM Ernährungskategorien k
                                        JOIN RezeptKategorien rk ON rk.EkID = k.EkID
                                        WHERE rk.RezeptID = {recipeId}""" )
            categories= []
            for r in res4:
                categories.append(r[1])
            data['categories'] = categories

            return data

        except Exception as e:
            return {"error: ": str(e)}



