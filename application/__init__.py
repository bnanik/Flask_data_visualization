from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdPIEOdfad89a8da8SD89SGd8fas89a89asd7f9a'

from application import routes