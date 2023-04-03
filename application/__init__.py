from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visualizationDB.db'
# app.config['SECRET_KEY'] = 'asdPIEOdfad89a8da8SD89SGd8fas89a89asd7f9a'

# db = SQLAlchemy(app)

from application import routes