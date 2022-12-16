# Veg Leaf Apis
Rest Apis which used to upload leaf photo and detect it with AI CNN model of Tensor Flow. And Also predict MSP wheat price with help of TensorFlow RNN model

# Prerequisites
* python 3.4 or above

# Steps for running project
* git clone https://github.com/rohitCodeRed/veg_leaf_apis
* cd veg_leaf_apis
* pip install virtualenv
* virtualenv --no-site-packages .
* source bin/activate              #->Activate local environment
* pip install -r requirements.txt  #-> Install all required package

## Initialize Sqlite DB Table
* rm data.db
* python create_table.py  #-> will create table users and ai_saved_models

## Run the server
* python main.py  #-> server will start at port 4000

## Upload defaults two models
* rm ./uploads/models/*  #-> Delete old models..

* curl --location --request POST 'http://localhost:4000/model/upload/prediction' \
--header 'Content-Type: multipart/form-data' \
--form 'file=@"./DEFAULT_MODELS/wheat_price_model.h5"'

* curl --location --request POST 'http://localhost:4000/model/upload/classifier' \
--header 'Content-Type: multipart/form-data' \
--form 'file=@"./DEFAULT_MODELS/veg_leaf_classification_model.h5"'


### Fore more Detail please refer meduim page: https://medium.com/@alwaysHopeGood/veg-leaf-ai-53d657c257bb
