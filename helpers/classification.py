import tensorflow as tf

DEFAULT_IMAGE_SHAPE = 128


class classificationModel:
    def __init__(self,image_path,model_path):
        self.image_path =image_path
        self.model_path = model_path
    
    def prepare_image(self,file_path, img_shape):
        # Read in target file (an image)
        img = tf.io.read_file(file_path)

        # Decode the read file into a tensor & ensure 3 colour channels 
        # (our model is trained on images with 3 colour channels and sometimes images have 4 colour channels)
        img = tf.image.decode_image(img, channels=3)

        # Resize the image (to the same size our model was trained on)
        img = tf.image.resize(img, size = [img_shape, img_shape])

        # Rescale the image (get all values between 0 and 1)
        img = img/255.
        return img

    def predict_class(self, class_names):
  
        # Import the target image and preprocess it
        img = self.prepare_image(self.image_path,DEFAULT_IMAGE_SHAPE)
        #print(img)
        model = tf.keras.models.load_model(self.model_path)
        #print(model)

        # Make a prediction
        pred = model.predict(tf.expand_dims(img, axis=0))

        
        # Get the predicted class
        if len(pred[0]) > 1: # check for multi-class
            pred_class = class_names[pred[0].argmax()] # if more than one output, take the max
        else:
            pred_class = class_names[int(tf.round(pred)[0][0])] # if only one output, round

        #print(pred_class)
        return {"image_name":pred_class}

