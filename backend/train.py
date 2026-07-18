"""Train a baseline CNN from data/train/{NORMAL,PNEUMONIA} and evaluate on data/test."""
from pathlib import Path
import tensorflow as tf
DATA=Path('data'); OUT=Path('model_artifacts'); OUT.mkdir(exist_ok=True)
train=tf.keras.utils.image_dataset_from_directory(DATA/'train',image_size=(224,224),batch_size=16,label_mode='binary')
valid=tf.keras.utils.image_dataset_from_directory(DATA/'val',image_size=(224,224),batch_size=16,label_mode='binary')
model=tf.keras.Sequential([tf.keras.layers.Rescaling(1/255,input_shape=(224,224,3)),tf.keras.layers.Conv2D(16,3,activation='relu'),tf.keras.layers.MaxPool2D(),tf.keras.layers.Conv2D(32,3,activation='relu'),tf.keras.layers.MaxPool2D(),tf.keras.layers.Conv2D(64,3,activation='relu'),tf.keras.layers.GlobalAveragePooling2D(),tf.keras.layers.Dropout(.3),tf.keras.layers.Dense(1,activation='sigmoid')])
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy',tf.keras.metrics.AUC(name='auc')])
callbacks=[tf.keras.callbacks.EarlyStopping(patience=3,restore_best_weights=True),tf.keras.callbacks.ModelCheckpoint(OUT/'pneumonia_cnn.keras',save_best_only=True)]
model.fit(train,validation_data=valid,epochs=20,callbacks=callbacks)
if (DATA/'test').exists(): print(model.evaluate(tf.keras.utils.image_dataset_from_directory(DATA/'test',image_size=(224,224),batch_size=16,label_mode='binary'),return_dict=True))
