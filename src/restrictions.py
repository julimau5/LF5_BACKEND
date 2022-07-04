from flask_restful import Resource
from flask import request
from main import db

def convertToRestriction(row):
    return {
        "id": row[0],
        "name": row[1],
    }

def setGetStatement(args):
    queryType = args['type']
    match queryType:
        case 'all':
            return f"SELECT * FROM Beschränkungen"

class Restriction(Resource):
    def get(self):
        try:
            rawStatement = setGetStatement(request.args)
            result = db.engine.execute(rawStatement)
            data = []
            for r in result:
                data.append(convertToRestriction(r))
            return data
        except Exception as e:
            return {"error: ": e}
    def post(self):
        try:
            body = request.get_json() 
            name = body['name']
            result = db.engine.execute("SELECT MAX(BeschID) FROM Beschränkungen")
            for r in result:
                newId = r[0] + 1
            rawStatement = f"INSERT INTO Beschränkungen (BeschID, Name) VALUES ({newId}, '{name}')"
            db.engine.execute(rawStatement)
            return {"tolis": "perris"} 
        except Exception as e:
            return {"error: ": e}