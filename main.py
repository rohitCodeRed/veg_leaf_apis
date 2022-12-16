from crypt import methods
from datetime import timedelta
import logging
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS, cross_origin
import os
#from flask import Flask, request, redirect, url_for
#from werkzeug.utils import secure_filename

from resources.user.security import authenticate, identity
from resources.user.user import UserRegister
from resources.ai_model.model_upload import UploadModel,ModelList
from resources.image_classifier.leaf_image import LeafImage
from resources.price_predict.wheat_price_predict import PricePredict

UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)


app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL_PATH'] = UPLOAD_FOLDER + 'models/'
app.config['IMAGE_PATH'] = UPLOAD_FOLDER + 'images/'
app.config['PREDICTION_DATA_PATH'] = './data/prediction'
app.config['PREDICTION_DATA_FILE_NAME']='wheat_price.csv'
app.config['CLASSIFICATION_DATA_PATH'] = './data/classification'
app.config['DEFAULT_LEAF_CLASS_NAMES']=['pepper','potato','tomato']

app.secret_key = 'veg_leaf_classifier'
api = Api(app)


jwt = JWT(app, authenticate, identity)

# @app.route("/")
# def index():
#     return "Welcome to AI-veges server."
# @app.route("/get_csv_data",methods=["GET"])
# def getData():
#     data={"data":{"year":[],"average_temperature":[],"crude_oil_price":[],"rainfall":[],"wheat_production":[],"inflation":[],"wheat_price":[]}}
#     response = jsonify(data)

#     # Enable Access-Control-Allow-Origin
#     #response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response, 200

  
api.add_resource(UploadModel, '/model/upload/<string:role>')
api.add_resource(ModelList, '/models')
api.add_resource(UserRegister, '/register')
api.add_resource(LeafImage, '/leaf/upload_and_classify')
api.add_resource(PricePredict,'/predict_wheat_price')

CORS(app)


#logging.getLogger('flask_cors').level = logging.DEBUG

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000, debug=True)  # important to mention debug=True
