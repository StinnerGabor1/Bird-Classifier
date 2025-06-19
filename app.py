from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
import cv2
import pandas as pd
from image_preprocessing import preprocess_image
import json
from load_custom_model import load_custom_model

tf.get_logger().setLevel('ERROR')

app=Flask(__name__)

model= load_custom_model()

with open('bird_classes.json', 'r') as f:
    class_data = json.load(f)

class_data= pd.DataFrame(class_data)
labels=list(class_data["common_name"])
encoded_labels= list(class_data["id"])
@app.route("/")

def home():
    return render_template("index.html")

@app.route("/", methods=["GET","POST"])
def classify():
    imagefile = request.files["imagefile"]
    image_path = "static/images/" + imagefile.filename
    st_image_path= "images/" + imagefile.filename
    imagefile.save(image_path)

    img = cv2.imread(image_path)
    img= preprocess_image(img)

    prediction= model(img)
    y_pred= tf.math.argmax(model(img)["dense"], axis=1).numpy()
    prediction= labels[y_pred[0]+1]
    prob=[x for x in np.asarray(tf.reduce_max(model(img)["dense"], axis = 1))][0]
    prob= np.round(prob,2)

    return render_template("index.html",prediction=prediction ,prob=prob, file=st_image_path)

if __name__=="__main__":
    app.run(debug=True)
