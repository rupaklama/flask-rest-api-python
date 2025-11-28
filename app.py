from flask import Flask 
from flask_smorest import Api

from resources.store import bp as StoreBlueprint
from resources.item import bp as ItemBlueprint

app = Flask(__name__)

# Configuration for Flask-Smorest (API documentation and error handling)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = 'Store REST API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

# Connecting the blueprints to the main API
api = Api(app)
api.register_blueprint(StoreBlueprint)
api.register_blueprint(ItemBlueprint)

@app.route('/')
def home():
    return "Welcome to the Store API!"

