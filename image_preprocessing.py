import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
def preprocess_image(image):
    IMG_SIZE = (299, 299)

    # Create ImageDataGenerator (no augmentation, just preprocessing)
    datagen  = ImageDataGenerator()

    # Load images from folder
    image = cv2.resize(image, IMG_SIZE)
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    # Use ImageDataGenerator to preprocess
    img_gen = datagen.flow(img_array ,batch_size=1)
    return next(img_gen)