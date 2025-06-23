import gdown
import zipfile
import os
import tensorflow as tf

MODEL_DIR = "model1"
ZIP_PATH = "model1.zip"
FILE_ID = "1JZG3_Q73Ab16wV2VI-d-gqmPdYw-rakc"

def download_and_extract_model():
    if not os.path.exists(MODEL_DIR):
        print("Downloading model...")
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, ZIP_PATH, quiet=False)

        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(MODEL_DIR)

        os.remove(ZIP_PATH)
def load_custom_model():
    download_and_extract_model()
    model = tf.keras.Sequential([
        tf.keras.layers.TFSMLayer("model1/model1/", call_endpoint="serving_default", trainable=True)
    ])
    return model