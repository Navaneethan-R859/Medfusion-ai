import tensorflow as tf
import numpy as np
from PIL import Image
import os

class AutoPredictor:

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(BASE_DIR, "ml_models", "auto", "auto_classifier.keras")
        self.model = None
        self.class_names = ["bone_xray", "chest_xray", "skin"]
        self.IMG_SIZE = 224

    def _load_model(self):
        if self.model is None:
            self.model = tf.keras.models.load_model(self.model_path)

    def predict(self, image_path):
        self._load_model()

        img = Image.open(image_path).convert("RGB")
        img = img.resize((self.IMG_SIZE, self.IMG_SIZE))

        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        preds = self.model.predict(img_array)[0]

        index = np.argmax(preds)
        confidence = float(preds[index])

        return self.class_names[index], confidence