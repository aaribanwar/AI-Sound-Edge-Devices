import tensorflow as tf
import numpy as np
import os
import librosa

# ==============================================================================
# === STEP 1: SETUP AND HELPER FUNCTIONS =======================================
# ==============================================================================

# Define paths
TFLITE_MODEL_PATH = 'fsl_embedding_model.tflite'
DATASET_PATH = 'datasets'

# Load the TFLite model and allocate tensors
print("🔄 Loading TFLite embedding model...")
interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print("✅ TFLite model loaded.")

def preprocess_custom_sound(signal, sr=22050):
    """
    A helper function to preprocess a raw audio signal into the model's input format.
    """
    input_shape = input_details[0]['shape']
    max_len = input_shape[1]
    n_mfcc = input_shape[2]

    if len(signal) < sr * 4:
        signal = np.pad(signal, (0, sr*4 - len(signal)), 'constant')
    
    mfcc = librosa.feature.mfcc(y=signal[:sr*4], sr=sr, n_mfcc=n_mfcc).T
    
    if len(mfcc) < max_len:
        mfcc = np.pad(mfcc, ((0, max_len - len(mfcc)), (0, 0)), mode='constant')
    
    processed_input = mfcc[:max_len, :]
    processed_input = processed_input[np.newaxis, ..., np.newaxis].astype(np.float32)
    return processed_input

def get_embedding(processed_input_with_batch):
    """
    Gets a 128-dimension embedding vector from the TFLite model for a given input.
    """
    interpreter.set_tensor(input_details[0]['index'], processed_input_with_batch)
    interpreter.invoke()
    embedding = interpreter.get_tensor(output_details[0]['index'])[0]
    return embedding

# ==============================================================================
# === STEP 2: "ONBOARDING" - LEARNING NEW CLASSES FROM A FEW SHOTS =============
# ==============================================================================

print("\n🚀 Simulating application workflow...")
print("A 'user' wants to teach the app to recognize two new sounds.")

X_meta_test = np.load(os.path.join(DATASET_PATH, 'X_meta_test.npy'))
y_meta_test = np.load(os.path.join(DATASET_PATH, 'y_meta_test.npy'))
class_ids = np.unique(y_meta_test)

CLASS_NAMES = {class_ids[0]: "New Sound A", class_ids[1]: "New Sound B"}
K_SHOTS = 5

prototypes = {}

print(f"\nPart A: Creating Prototypes from {K_SHOTS} shots...")
for class_id, class_name in CLASS_NAMES.items():
    print(f"  Learning '{class_name}'...")
    
    support_set_indices = np.where(y_meta_test == class_id)[0][:K_SHOTS]
    support_set_samples = X_meta_test[support_set_indices]
    
    class_embeddings = []
    for sample in support_set_samples:
        # --- FIX IS HERE ---
        # We must add a batch dimension (of 1) to the single sample.
        sample_with_batch = sample[np.newaxis, ...].astype(np.float32)
        embedding = get_embedding(sample_with_batch)
        class_embeddings.append(embedding)
        
    prototypes[class_name] = np.mean(class_embeddings, axis=0)

print("✅ Prototypes created and stored.")

# ==============================================================================
# === STEP 3: "REAL-TIME" - CLASSIFYING A NEW SOUND ============================
# ==============================================================================

print("\nPart B: A new, unknown sound arrives. Let's classify it.")

query_sample_index = np.where(y_meta_test == class_ids[0])[0][K_SHOTS]
query_sample = X_meta_test[query_sample_index]
true_label_id = y_meta_test[query_sample_index]
true_label_name = CLASS_NAMES[true_label_id]

# --- FIX IS HERE ---
# 1. Get the embedding for the new sound, adding the batch dimension.
query_sample_with_batch = query_sample[np.newaxis, ...].astype(np.float32)
query_embedding = get_embedding(query_sample_with_batch)

# 2. Calculate the distance to each known prototype
distances = {}
for class_name, proto_vec in prototypes.items():
    dist = np.sum((query_embedding - proto_vec) ** 2)
    distances[class_name] = dist

# 3. The prediction is the class with the smallest distance
predicted_class = min(distances, key=distances.get)

print("\n--- Inference Result ---")
print(f"True Sound Class: \t'{true_label_name}'")
print(f"Predicted Sound Class: \t'{predicted_class}'")
print("\nDistances to Prototypes:")
for name, dist in distances.items():
    print(f"  - {name}: {dist:.2f}")

if predicted_class == true_label_name:
    print("\n🎉 Correct Prediction!")
else:
    print("\n⚠️ Incorrect Prediction.")