from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
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

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)


api.add_resource(UploadModel, '/model/upload/<string:role>')
api.add_resource(ModelList, '/models')
api.add_resource(UserRegister, '/register')
api.add_resource(LeafImage, '/leaf/upload_and_classify')
api.add_resource(PricePredict,'/predict_wheat_price')

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # important to mention debug=True
