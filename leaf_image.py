from flask import current_app
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os,glob
from flask_jwt import jwt_required


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class LeafImage(Resource):
    #TABLE_NAME = 'ai_saved_models'

    parser = reqparse.RequestParser()
    
    parser.add_argument('file', type=FileStorage, location='files')

    @classmethod
    def allowed_file(cls,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    @jwt_required()
    def post(self):
        data = LeafImage.parser.parse_args()
        image_file = data['file']
        
        if image_file.filename == '':
            return {"message": "An error occurred uploading the model."}, 400

        try:
            if image_file and self.allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'] +"images/", filename))
            
            #LeafImage.insert(modelData)
            return {"message": "Image uploaded"}, 200
        except:
            return {"message": "An error occurred saving the Image."}, 500
    
    @jwt_required()
    def delete(self):
        try:

            for f in glob.glob(os.path.join(current_app.config['UPLOAD_FOLDER'] +"images/*")):
                os.remove(f)
            
            return {"message": "All Images Deletd"}, 200
        except:
            return {"message": "An error occurred deleting the Image."}, 500

    @classmethod
    def delete_image(cls, image_name):
        del_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'] +"images/", image_name)
        if os.path.exists(del_file_path):
            os.remove(del_file_path)
        else:
            print("The file does not exist")


        return {'message': 'Image: '+image_name +' is deleted'}

    

