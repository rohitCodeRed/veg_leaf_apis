import sqlite3
from flask import current_app
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os,glob
from flask_jwt import jwt_required
from helpers.classification import classificationModel


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class LeafImage(Resource):
    TABLE_NAME = 'ai_saved_models'

    parser = reqparse.RequestParser()
    
    parser.add_argument('file', type=FileStorage, location='files')

    @classmethod
    def allowed_file(cls,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    @jwt_required()
    def post(self):
        data = LeafImage.parser.parse_args()
        image_file = data['file']
        response={}
        
        if image_file.filename == '':
            return {"message": "An error occurred uploading the model."}, 400

        try:
            if image_file and self.allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(current_app.config['IMAGE_PATH'], filename)
                image_file.save(image_path)

                model_name = self.find_by_role('classification')
                if model_name:
                    model_path = os.path.join(current_app.config['MODEL_PATH'],model_name['model']['model_name'])
                    class_names = current_app.config['DEFAULT_LEAF_CLASS_NAMES']
                    
                    clModel = classificationModel(image_path,model_path)
                    response = clModel.predict_class(class_names)

                    self.delete_image(filename)
                else:
                    return {"message": "Model not found"}, 404

                return {"message": response}, 200
            #LeafImage.insert(modelData)
            return {"message": "Invalid Image file..upload again"}, 200
        except:
            return {"message": "An error occurred while predicting the image."}, 500
    
    @jwt_required()
    def delete(self):
        try:

            for f in glob.glob(os.path.join(current_app.config['IMAGE_PATH'] +"*")):
                os.remove(f)
            
            return {"message": "All Images Deletd"}, 200
        except:
            return {"message": "An error occurred deleting the Image."}, 500

    @classmethod
    def delete_image(cls, image_name):
        del_file_path = os.path.join(current_app.config['IMAGE_PATH'], image_name)
        if os.path.exists(del_file_path):
            os.remove(del_file_path)
        else:
            print("The file does not exist")


        return {'message': 'Image: '+image_name +' is deleted'}
    
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

    

