
import tensorflow as tf
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


class predictionModel:
    def __init__(self,data_path,model_path):
        self.data_path = data_path
        self.model_path = model_path
    
    def predict(self,pred_param):
        csv_path=self.data_path
        data = pd.read_csv(csv_path)

        #print(data.head())
        ct = make_column_transformer((MinMaxScaler(), ['average_temperature','rainfall','crude_oil_price','wheat_production','inflation']))
        #print(type(ct))

        X_df = data.drop(columns=['year','wheat_price'],axis=1)
        y_df = data['wheat_price']
        # print(X_df.head())
        # print(y_df.head())

        X_train,X_test, y_train,y_test = train_test_split(X_df,y_df,test_size=0.2,random_state=42)
        #print(X_train.head())
        #print(y_df.head())
        ct.fit(X_train)
        #print(pred_param)
        predict_df = pd.DataFrame(pred_param)
        #print(predict_df)

        predictData_normal = ct.transform(predict_df)

        # print(X_df.head())
        # print(y_df.head())
        # print(predictData_normal)
        # print(self.model_path)
        model = tf.keras.models.load_model(self.model_path)
        price = model.predict(predictData_normal)
        return price[0][0]





