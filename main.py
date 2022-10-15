from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import os
#from flask import Flask, request, redirect, url_for
#from werkzeug.utils import secure_filename

from security import authenticate, identity
from user import UserRegister
from ai_model import AiModel, AiModelList
from leaf_image import LeafImage

UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'veg_leaf_classifier'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(AiModel, '/model/upload/<string:role>')
api.add_resource(AiModelList, '/models')
api.add_resource(UserRegister, '/register')
api.add_resource(LeafImage, '/leaf/upload_and_classify')

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # important to mention debug=True
