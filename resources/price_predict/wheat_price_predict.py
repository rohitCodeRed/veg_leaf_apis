from flask import current_app
from flask_restful import Resource, reqparse
import os
import pandas as pd
import sqlite3
from flask_jwt import jwt_required
from helpers.prediction import predictionModel



#DATA_FILE_NAME = 'wheat_price.csv'

class PricePredict(Resource):
    TABLE_NAME = 'ai_saved_models'

    parser = reqparse.RequestParser()
    parser.add_argument('average_temperature',
                        type=str,
                        required=True,
                        help="average_temperature field cannot be left blank!"
                        )
    parser.add_argument('rainfall',
                        type=str,
                        required=True,
                        help="rainfall field cannot be left blank!"
                        )
    parser.add_argument('crude_oil_price',
                        type=str,
                        required=True,
                        help="crude_oil_price field cannot be left blank!"
                        )
    parser.add_argument('wheat_production',
                        type=str,
                        required=True,
                        help="wheat_production field cannot be left blank!"
                        )
    parser.add_argument('inflation',
                        type=str,
                        required=True,
                        help="inflation field cannot be left blank!"
                        )


    @jwt_required()
    def get(self):
        csv_path = os.path.join(current_app.config['PREDICTION_DATA_PATH'],current_app.config['PREDICTION_DATA_FILE_NAME'])
        data = pd.read_csv(csv_path)
        response={}
        for col in data.columns:
            response[col] =[]
        
        for index, row in data.iterrows():
            for key in response:
                response[key].append(row[key]) 

        #print(response)

        return {"data":response}, 200


    #@jwt_required()
    def post(self):
        bodyParams = PricePredict.parser.parse_args()
        
        try:
            model_name = self.find_by_role('prediction')
            if model_name:
                converted_params ={}
                for key, val in bodyParams.items():
                    converted_params[key] = [float(val)]
                
                model_path = os.path.join(current_app.config['MODEL_PATH'],model_name['model']['model_name'])
                data_path = os.path.join(current_app.config['PREDICTION_DATA_PATH'],current_app.config['PREDICTION_DATA_FILE_NAME'])

                model = predictionModel(data_path,model_path)
                price = model.predict(converted_params)
                #LeafImage.insert(modelData)
                return {"price": str(price),'unit':'rs per Quintal'}, 200
            return {"message":"No model found"}, 200
        except:
            return {"message": "An error occurred in predicting price."}, 500
    

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

 

    

