import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.metrics import classification_report
import os

# Load preprocessed data (update paths accordingly)
X_train = np.load('datasets/X_train.npy')
X_test = np.load('datasets/X_test.npy')
y_train = np.load('datasets/y_train.npy')
y_test = np.load('datasets/y_test.npy')

# Define the model (CRNN: CNN + LSTM/GRU)
def build_model(input_shape, num_classes):
    model = models.Sequential()
    
    # CNN layers with BatchNormalization
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # LSTM layers (Bidirectional LSTM)
    model.add(layers.Reshape((-1, 128)))  # Reshape to feed into LSTM
    model.add(layers.Bidirectional(layers.LSTM(128, return_sequences=True)))
    model.add(layers.Bidirectional(layers.LSTM(128)))

    # Fully connected layers
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(num_classes, activation='softmax'))

    model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Model parameters
input_shape = X_train.shape[1:]  # Shape of input (time, features, 1)
num_classes = len(np.unique(y_train))  # Number of classes

# Build the model
model = build_model(input_shape, num_classes)

# Define callbacks
checkpoint = ModelCheckpoint('best_model.h5', save_best_only=True, monitor='val_loss', mode='min', verbose=1)
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test),
          callbacks=[checkpoint, early_stop])

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print(f"Test accuracy: {test_acc:.4f}")

# Save the model
model.save('sound_classification_model.h5')

# Convert model to TFLite for edge deployment
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Apply optimization
tflite_model = converter.convert()

# Save the TFLite model
with open('sound_classification_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("✅ Model saved and converted to TFLite format.")
