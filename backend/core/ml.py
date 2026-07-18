import os
from pathlib import Path
import numpy as np
from PIL import Image

class ModelUnavailable(RuntimeError): pass

def predict(image_path:str):
    model_path=Path(os.getenv('MODEL_PATH','model_artifacts/pneumonia_cnn.keras'))
    if not model_path.exists():
        raise ModelUnavailable('No trained model is configured. Run the training pipeline first.')
    import tensorflow as tf
    model=tf.keras.models.load_model(model_path)
    image=Image.open(image_path).convert('RGB').resize((224,224))
    x=np.expand_dims(np.asarray(image,dtype=np.float32)/255.0,0)
    probability=float(model.predict(x,verbose=0)[0][0])
    return ('PNEUMONIA' if probability>=.5 else 'NORMAL', probability if probability>=.5 else 1-probability, model_path.name)
