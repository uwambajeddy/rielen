from distutils.log import debug
from math import degrees
from flask import Flask
from datetime import timedelta
from flask_cors import CORS
app = Flask(__name__)



from routes import admin, jwt, userSide, apiBlueprint # importing modules from routes folder
from models import db, mail, cache # importing modules from models folder
import os

#Flask-cors

CORS(app)

# configs

''' FLASK SECRETY KEY '''
app.config['SECRET_KEY'] = 'hardsecretkeyyy'

''' FLASK_JWT_TOKEN '''
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days= 3)
app.config["JWT_SECRET_KEY"] = 'akeza'

''' FLASK_MYSQLDB '''
app.config['MYSQL_HOST'] = 'sql9.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql9584391'
app.config['MYSQL_PASSWORD'] = 'aupKsndbId'
app.config['MYSQL_DB'] = 'sql9584391'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

''' FLASK_MAIL '''
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abdoulkarim5027@gmail.com'
app.config['MAIL_PASSWORD'] = 'hussenbt'
app.config['MAIL_DEFAULT_SENDER'] = 'abdoulkarim5027@gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# end


# initing packages

jwt.init_app(app)
db.init_app(app)
mail.init_app(app)
cache.init_app(app)

# end




# importing routes from routes folder
app.register_blueprint(admin)
app.register_blueprint(userSide)
app.register_blueprint(apiBlueprint)

if __name__ == "__main__":
    app.run(threaded=True, debug=False)