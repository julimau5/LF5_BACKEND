from flask import Flask 
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbeaver:dbeaver@172.16.5.15:3306/krautundrueben'
db = SQLAlchemy(app)

if __name__ == "__main__":
    from ingredients import Ingredients
    from recipes import Recipes
    api.add_resource(Ingredients, "/ingredients")
    api.add_resource(Recipes, "/recipes")
    app.run(debug=True)
