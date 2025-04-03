import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, LSTM, Dense, TimeDistributed, Reshape

# Step 1: Load Preprocessed Dataset
print("Loading dataset...")
X_train = np.load("datasets/X_train.npy")
print(f"Loaded dataset shape: {X_train.shape}")  # Should print (5000, 64, 128, 1)

# Step 2: Define the CNN + LSTM Model
model = Sequential([
    # CNN layers
    Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(64, 128, 1)),
    MaxPooling2D((2, 2)),

    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),

    Flatten(),
    
    # Reshape to fit LSTM input (time steps, features)
    Reshape((64, -1)),

    # LSTM layer
    LSTM(128, return_sequences=False),

    # Fully connected layer
    Dense(64, activation='relu'),
    Dense(10, activation='softmax')  # Assuming 10 classes for classification
])

# Step 3: Compile the Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 4: Train the Model
print("Starting training...")
model.fit(X_train, np.random.rand(5000, 10), epochs=10, batch_size=32)  # Replace with actual labels

# Step 5: Save the Model
model.save("cnn_lstm_sound.h5")
print("Model training complete. Saved as cnn_lstm_sound.h5")  