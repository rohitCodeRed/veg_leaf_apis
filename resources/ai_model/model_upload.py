from flask import current_app
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_jwt import jwt_required
import sqlite3
import os


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','h5'])


class UploadModel(Resource):
    TABLE_NAME = 'ai_saved_models'

    parser = reqparse.RequestParser()
    
    parser.add_argument('file', type=FileStorage, location='files')

    @classmethod
    def allowed_file(cls,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @jwt_required()
    def get(self, role):
        model = self.find_by_role(role)
        if model:
            return model
        return {'message': 'model not found'}, 404

    @classmethod
    def find_by_role(cls, role):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE role=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (role,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'model': {'role': row[0], 'model_name': row[1]}}

    def post(self, role):
        if self.find_by_role(role):
            return {'message': "An model with role '{}' already exists.".format(role)}
        
        data = UploadModel.parser.parse_args()
        
        image_file = data['file']
        
        if image_file.filename == '':
            return {"message": "An error occurred uploading the model."}, 400

        try:
            if image_file and self.allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'] +"models/", filename))
            else:
                return {"message": "Model is not alowed to upload"}, 200
            modelData = {'role': role, 'model_name': image_file.filename}
            
            UploadModel.insert(modelData)
            return modelData
        except:
            return {"message": "An error occurred saving the model."}, 500

        

    @classmethod
    def insert(cls, model):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (model['role'], model['model_name']))

        connection.commit()
        connection.close()

    #@jwt_required()
    def delete(self, role):

        mData = self.find_by_role(role)
        if not mData:
            return {'message': 'Model with role:'+role +' not found'}, 404

        file_name = mData["model"]["model_name"]
        del_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'] +"models/", file_name)
        if os.path.exists(del_file_path):
            os.remove(del_file_path)
        else:
            print("The file does not exist")


        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE role=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (role,))

        connection.commit()
        connection.close()

        return {'message': 'Model: '+file_name +' deleted'}


class ModelList(Resource):
    TABLE_NAME = 'ai_saved_models'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        models = []
        for row in result:
            models.append({'role': row[0], 'model_name': row[1]})
        connection.close()

        return {'models': models}
