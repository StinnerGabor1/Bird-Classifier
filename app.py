from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from cv2 import imread
import pandas as pd
import json
import os

from image_preprocessing import preprocess_image
from load_custom_model import load_custom_model
from ImageSearch import get_bird_images, get_verified_wikipedia_url

tf.get_logger().setLevel('ERROR')

app=Flask(__name__)

model= load_custom_model()

with open('bird_classes.json', 'r') as f:
    class_data = json.load(f)

class_data= pd.DataFrame(class_data)
labels=list(class_data["common_name"])
@app.route("/")

def home():
    return render_template("index.html")

@app.route("/", methods=["GET","POST"])
def classify():
    imagefile = request.files["imagefile"]
    image_path = "static/images/" + imagefile.filename
    st_image_path= "images/" + imagefile.filename
    imagefile.save(image_path)

    img = imread(image_path)
    img= preprocess_image(img)

    y_pred= tf.math.argmax(model(img)["dense"], axis=1).numpy()
    prediction= labels[y_pred[0]+1]
    prob=[x for x in np.asarray(tf.reduce_max(model(img)["dense"], axis = 1))][0]*10
    prob= np.round(prob,2)

    image_urls = get_bird_images(prediction)
    wiki_url= get_verified_wikipedia_url(prediction)

    if wiki_url==None: wiki_url=False

    if image_urls==[]:
        image_urls = ["https://via.placeholder.com/600x400?text=No+Image+Found"]

    return render_template("index.html",prediction=prediction ,prob=prob, file=st_image_path, image_urls=image_urls, wiki_url=wiki_url)

@app.route("/species")
def list_birds():
    """json_path = os.path.join(app.static_folder, "bird_image_database.json")
    with open(json_path, "r", encoding="utf-8") as f:
        birds = json.load(f)"""

    return render_template("species.html")

if __name__=="__main__":
    app.run(debug=True)
