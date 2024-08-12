import tensorflow as tf
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.layers import (
    Conv2D,
    Dense,
    Dropout,
    GlobalAveragePooling2D,
    MaxPooling2D,
)
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2

from options import CLASS_NAMES, TARGET_SIZE


def sequential_model():
    model = Sequential(
        [
            Conv2D(
                64,
                (3, 3),
                activation="relu",
                input_shape=(*TARGET_SIZE, 3),
                kernel_regularizer=l2(0.001),
            ),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation="relu", kernel_regularizer=l2(0.001)),
            MaxPooling2D(2, 2),
            Conv2D(256, (3, 3), activation="relu", kernel_regularizer=l2(0.001)),
            MaxPooling2D(2, 2),
            GlobalAveragePooling2D(),
            Dense(512, activation="relu", kernel_regularizer=l2(0.001)),
            Dropout(0.5),
            Dense(len(CLASS_NAMES), activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    return model


def mobilenet_model():
    FROZEN_START = 5  # Start freezing by the layer
    FROZEN_STOP = 38  # Stop freezing at the layers

    model = MobileNet(
        weights="imagenet", include_top=False, input_shape=(*TARGET_SIZE, 3), alpha=0.25
    )
    for layer in model.layers[FROZEN_START:FROZEN_STOP]:
        layer.trainable = True

    # Add new layers on top of the model
    x = model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation="relu", kernel_regularizer=l2(0.001))(x)
    x = Dropout(0.5)(x)  # Dropout for regularization
    predictions = Dense(
        len(CLASS_NAMES), activation="sigmoid", kernel_regularizer=l2(0.001)
    )(x)

    # This is the model we will train
    model = Model(inputs=model.input, outputs=predictions)

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy", "auc"],
    )

    return model


def model_load(path):
    print(f"Loading model from {path}")
    model = tf.keras.models.load_model(path)
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy", "auc"],
    )
    return model


def model_store(model, path):
    model.save(path)


def model_convert(model, path):
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    with open(path, "wb") as f:
        f.write(tflite_model)
