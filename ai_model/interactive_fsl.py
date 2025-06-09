import sounddevice as sd
import numpy as np
import tensorflow as tf
import librosa
import time
from scipy.io.wavfile import write as write_wav # Import for saving audio

# ==============================================================================
# === STEP 1: SETUP AND HELPER FUNCTIONS (with Debugging) ======================
# ==============================================================================

# --- Constants ---
TFLITE_MODEL_PATH = 'fsl_embedding_model.tflite'
SAMPLE_RATE = 22050
RECORDING_DURATION = 4
K_SHOTS = 5

# --- Load TFLite Model ---
print("🔄 Loading TFLite embedding model...")
try:
    interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("✅ TFLite model loaded successfully.")
except ValueError:
    print("\n❌ ERROR: Could not load 'fsl_embedding_model.tflite'.")
    exit()

# --- Helper Functions (Unchanged) ---
def preprocess_custom_sound(signal, sr=SAMPLE_RATE):
    input_shape = input_details[0]['shape']
    max_len, n_mfcc = input_shape[1], input_shape[2]
    if signal.ndim > 1: signal = signal.mean(axis=1)
    target_samples = sr * RECORDING_DURATION
    if len(signal) < target_samples: signal = np.pad(signal, (0, target_samples - len(signal)), 'constant')
    else: signal = signal[:target_samples]
    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfcc).T
    if len(mfcc) < max_len: mfcc = np.pad(mfcc, ((0, max_len - len(mfcc)), (0, 0)), mode='constant')
    return mfcc[:max_len, :][np.newaxis, ..., np.newaxis].astype(np.float32)

def get_embedding(processed_input_with_batch):
    interpreter.set_tensor(input_details[0]['index'], processed_input_with_batch)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])[0]

# --- Modified Record Audio Function ---
def record_audio(duration, sample_rate, filename="temp_recording.wav"):
    """Records audio and provides debugging info."""
    print("Get ready to record...")
    time.sleep(1); print("3..."); time.sleep(1); print("2..."); time.sleep(1); print("1..."); time.sleep(1)
    print(f"🔴 Recording for {duration} seconds!")
    
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    audio = audio.flatten()
    
    # --- DEBUGGING ---
    # 1. Check the volume
    avg_amplitude = np.abs(audio).mean()
    print(f"✅ Recording finished. Average Amplitude: {avg_amplitude:.4f}")
    
    # 2. Save the file to listen to it
    write_wav(filename, sample_rate, (audio * 32767).astype(np.int16))
    print(f"   Saved recording to '{filename}'")
    
    # Alert if volume is too low
    if avg_amplitude < 0.01:
        print("   ⚠️ WARNING: Audio volume is very low. Try getting closer to the mic or increasing mic gain in your OS settings.")

    return audio

# ==============================================================================
# === STEP 2: INTERACTIVE FEW-SHOT LEARNING ====================================
# ==============================================================================

def main():
    print("\n--- Interactive Few-Shot Sound Classifier (Debug Mode) ---")
    
    num_classes = int(input("How many new sound classes do you want to teach? "))
    class_names = [input(f"Enter name for class {i+1}: ").replace(" ", "_") for i in range(num_classes)]
    
    prototypes = {}

    print("\n--- Phase 1: Teaching the Model ---")
    for name in class_names:
        class_embeddings = []
        print(f"\nNow teaching '{name}'. Please provide {K_SHOTS} examples.")
        for i in range(K_SHOTS):
            input(f"Press Enter to start recording sample {i+1}/{K_SHOTS} for '{name}'...")
            filename = f"rec_{name}_{i+1}.wav"
            audio_sample = record_audio(RECORDING_DURATION, SAMPLE_RATE, filename)
            
            processed_audio = preprocess_custom_sound(audio_sample)
            embedding = get_embedding(processed_audio)
            class_embeddings.append(embedding)
        
        prototypes[name] = np.mean(class_embeddings, axis=0)
        print(f"✅ Prototype learned for '{name}'.")
        
    print("\n--- Phase 2: Classification ---")
    while True:
        input("\nPress Enter to record a new sound to classify...")
        query_filename = "query_recording.wav"
        query_audio = record_audio(RECORDING_DURATION, SAMPLE_RATE, query_filename)
        
        processed_query = preprocess_custom_sound(query_audio)
        query_embedding = get_embedding(processed_query)
        
        distances = {name: np.sum((query_embedding - proto)**2) for name, proto in prototypes.items()}
        predicted_class = min(distances, key=distances.get)
        
        print("\n--- Prediction ---")
        print(f"🎙️  Predicted Sound Class: >> {predicted_class} <<")
        print("\n(Lower distance is better)")
        for name, dist in sorted(distances.items(), key=lambda item: item[1]):
            print(f"  - Distance to '{name}': {dist:.2f}")

        if input("\nClassify another sound? (y/n): ").lower() != 'y':
            break

    print("\nExiting application. Goodbye!")

if __name__ == '__main__':
    main()