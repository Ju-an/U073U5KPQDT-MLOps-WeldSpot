import os
import io
import matplotlib.pyplot as plt
from datetime import datetime
import tensorflow as tf
import numpy as np
from options import CLASS_NAMES, TRAIN_EPOCHS, TRAINING_VERBOSITY
from service.training_configuration import get_device

def model_training(model, train_data, validation_data, epochs=TRAIN_EPOCHS):
    # strategy = tf.distribute.OneDeviceStrategy(device='/gpu:0')
    # with strategy.scope():

    log_dir = os.path.join("logs", "fit", datetime.now().strftime("%Y%m%d-%H%M%S"))
    tensorboard_tracking = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_auc',  # Monitor validation AUC
        mode='max',         # Stop when the AUC stops increasing
        patience=18,        # Number of epochs with no improvement after which training will be stopped
        restore_best_weights=True  # Restore model weights from the epoch with the best AUC
    )
    device = get_device()
    print(f"Training on {device}")
    with tf.device(device):
        training = model.fit(
            train_data,
            epochs=epochs,
            validation_data=validation_data,
            callbacks=[early_stopping, tensorboard_tracking],
            verbose = TRAINING_VERBOSITY
        )
        return training

def measure_performance(model, test_data, type="test"):
    log_dir = os.path.join("logs", "predict")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{type}_{timestamp}.png"
    file_path = os.path.join(log_dir, filename)

    file_writer = tf.summary.create_file_writer(log_dir)
    test_loss, test_acc, test_auc = model.evaluate(test_data)
    print(f'Test accuracy: {test_acc}, Test AUC: {test_auc}, Test loss: {test_loss}')

    predictions = model.predict(test_data)
    y_pred = [CLASS_NAMES[prediction.argmax()] for prediction in predictions]
    y_pred_indices = [CLASS_NAMES.index(pred) for pred in y_pred]
    y_true = test_data.classes
    conf_matrix = tf.math.confusion_matrix(y_true, y_pred_indices).numpy()
    # Log confusion matrix as an image
    figure = plot_confusion_matrix(conf_matrix, class_names=CLASS_NAMES)
    plot_to_image(figure, file_path)
    cm_image = tf.image.decode_png(tf.io.read_file(file_path), channels=4)
    cm_image = tf.expand_dims(cm_image, 0)
    with file_writer.as_default():
        tf.summary.image("Confusion Matrix", cm_image, step=0)

    # Calculate average AUC
    auc_per_class = []
    for i in range(len(CLASS_NAMES)):
        true_positives = conf_matrix[i, i]
        false_positives = conf_matrix[:, i].sum() - true_positives
        false_negatives = conf_matrix[i, :].sum() - true_positives
        true_negatives = conf_matrix.sum() - (true_positives + false_positives + false_negatives)

        if true_positives + false_negatives > 0 and true_negatives + false_positives > 0:
            sensitivity = true_positives / (true_positives + false_negatives)
            specificity = true_negatives / (true_negatives + false_positives)
            auc = (sensitivity + specificity) / 2
            auc_per_class.append(auc)

    average_auc = sum(auc_per_class) / len(auc_per_class) if auc_per_class else 0
    return average_auc

def plot_confusion_matrix(cm, class_names):
    figure = plt.figure(figsize=(8, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)

    # Normalize the confusion matrix.
    cm = np.around(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], decimals=2)

    # Use white text if squares are dark; otherwise black.
    threshold = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        color = "white" if cm[i, j] > threshold else "black"
        plt.text(j, i, cm[i, j], horizontalalignment="center", color=color)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return figure

def plot_to_image(figure, file_path):
    # Save the plot to a PNG file.
    plt.savefig(file_path, format='png')
    # Closing the figure prevents it from being displayed directly inside the notebook.
    plt.close(figure)
