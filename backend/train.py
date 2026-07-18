"""Train a research baseline from data/train and evaluate once on data/test."""
import json
from pathlib import Path
import numpy as np
import tensorflow as tf

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
OUT = ROOT / 'model_artifacts'
OUT.mkdir(exist_ok=True)
SEED, IMAGE_SIZE, BATCH_SIZE = 42, (224, 224), 16

common = dict(directory=DATA/'train', image_size=IMAGE_SIZE, batch_size=BATCH_SIZE,
              label_mode='binary', validation_split=.2, seed=SEED)
train = tf.keras.utils.image_dataset_from_directory(subset='training', **common)
valid = tf.keras.utils.image_dataset_from_directory(subset='validation', **common)
test = tf.keras.utils.image_dataset_from_directory(
    DATA/'test', image_size=IMAGE_SIZE, batch_size=BATCH_SIZE,
    label_mode='binary', shuffle=False)

augment = tf.keras.Sequential([
    tf.keras.layers.RandomRotation(.03), tf.keras.layers.RandomZoom(.08),
    tf.keras.layers.RandomTranslation(.03, .03)
])
model = tf.keras.Sequential([
    tf.keras.layers.Input((*IMAGE_SIZE, 3)), augment,
    tf.keras.layers.Rescaling(1/255),
    tf.keras.layers.Conv2D(32, 3, activation='relu'), tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'), tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Conv2D(128, 3, activation='relu'), tf.keras.layers.MaxPool2D(),
    tf.keras.layers.GlobalAveragePooling2D(), tf.keras.layers.Dropout(.35),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer=tf.keras.optimizers.Adam(3e-4), loss='binary_crossentropy',
              metrics=['accuracy', tf.keras.metrics.AUC(name='auc'),
                       tf.keras.metrics.Precision(name='precision'),
                       tf.keras.metrics.Recall(name='recall')])

labels = np.concatenate([y.numpy().ravel() for _, y in train])
counts = np.bincount(labels.astype(int), minlength=2)
class_weight = {i: len(labels)/(2*count) for i, count in enumerate(counts) if count}
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=4, restore_best_weights=True),
    tf.keras.callbacks.ReduceLROnPlateau(patience=2, factor=.3),
    tf.keras.callbacks.ModelCheckpoint(OUT/'pneumonia_cnn.keras', save_best_only=True)
]
model.fit(train, validation_data=valid, epochs=20, class_weight=class_weight, callbacks=callbacks)
metrics = model.evaluate(test, return_dict=True)
probabilities = model.predict(test, verbose=0).ravel()
truth = np.concatenate([y.numpy().ravel() for _, y in test]).astype(int)
predicted = (probabilities >= .5).astype(int)
metrics.update({
    'true_negative': int(((truth==0)&(predicted==0)).sum()),
    'false_positive': int(((truth==0)&(predicted==1)).sum()),
    'false_negative': int(((truth==1)&(predicted==0)).sum()),
    'true_positive': int(((truth==1)&(predicted==1)).sum()),
    'test_samples': int(len(truth)), 'threshold': .5, 'seed': SEED
})
(OUT/'evaluation.json').write_text(json.dumps(metrics, indent=2))
print(json.dumps(metrics, indent=2))
