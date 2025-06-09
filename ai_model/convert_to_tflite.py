import tensorflow as tf

# Define the paths
KERAS_MODEL_PATH = 'fsl_embedding_model.h5'
TFLITE_MODEL_PATH = 'fsl_embedding_model.tflite'

print(f"🔄 Loading Keras model from: {KERAS_MODEL_PATH}")

# Load the trained Keras model
model = tf.keras.models.load_model(KERAS_MODEL_PATH, compile=False)

# Create a TFLite converter object
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# --- START OF FIX ---
# This is the fix for the LSTM conversion error.
# It allows the converter to use select TensorFlow ops when a TFLite op is not available.
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,  # Enable TFLite builtin ops.
    tf.lite.OpsSet.SELECT_TF_OPS    # Enable select TensorFlow ops.
]
converter._experimental_lower_tensor_list_ops = False
# --- END OF FIX ---

# Apply default optimizations
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convert the model
tflite_model = converter.convert()

# Save the TFLite model to a file
with open(TFLITE_MODEL_PATH, 'wb') as f:
    f.write(tflite_model)

print(f"✅ Model converted successfully!")
print(f"TFLite model saved to: {TFLITE_MODEL_PATH}")