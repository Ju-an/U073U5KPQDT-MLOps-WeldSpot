
import tensorflow as tf
from options import CLASS_NAMES

def train_model(model, train_data, validation_data, epochs):
    # strategy = tf.distribute.OneDeviceStrategy(device='/gpu:0')
    # with strategy.scope():
    # TODO: Fix overfitting doing following steps:
    # 1. Regularization: Consider adding regularization techniques such as dropout, L2 regularization, or data augmentation to reduce overfitting.
    # 2. Learning Rate: Experiment with different learning rates. Sometimes a lower learning rate can help the model generalize better.
    # 3. Early Stopping: Use early stopping to prevent the model from overfitting by monitoring the validation loss and stopping training when it stops improving.
    # Train
    training = model.fit(
        train_data,
        # steps_per_epoch= 31, # train_generator.samples // batch,
        epochs=epochs,
        validation_data=validation_data,
        # validation_steps= 6, # validation_generator.samples // batch,
    )
    return training

def measure_performance(model, test_data):
    test_loss, test_acc, test_auc = model.evaluate(test_data)
    print(f'Test accuracy: {test_acc}, Test AUC: {test_auc}, Test loss: {test_loss}')
    # TODO: Use tensorboard to visualize the training, validation, test and evaluation performance metrics
    predictions = model.predict(test_data)
    y_pred = [CLASS_NAMES[prediction.argmax()] for prediction in predictions]
    y_pred_indices = [CLASS_NAMES.index(pred) for pred in y_pred]
    y_true = test_data.classes
    conf_matrix = tf.math.confusion_matrix(y_true, y_pred_indices).numpy()
