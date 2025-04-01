import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Set dataset path
DATASET_PATH = r"C:\Users\apeksha narayan\Desktop\MINI_PROJECT\ai_model\clips"

# Step 1: Check if the folder exists
if not os.path.exists(DATASET_PATH):
    print(f"❌ ERROR: Dataset folder not found at: {DATASET_PATH}")
    print("Please verify the path and try again.")
    exit()

print(f"✅ Dataset folder found: {DATASET_PATH}")

# Step 2: Get the list of labels (subfolders)
LABELS = [label for label in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, label))]

if not LABELS:
    print("❌ ERROR: No subfolders (labels) found in dataset.")
    exit()

print(f"✅ Found {len(LABELS)} labels: {LABELS}")

# Step 3: Create a folder to store spectrograms
SPECTROGRAM_PATH = os.path.join(DATASET_PATH, "spectrograms")
os.makedirs(SPECTROGRAM_PATH, exist_ok=True)

# Step 4: Convert each .wav file into a spectrogram
def generate_spectrogram(file_path, output_path):
    y, sr = librosa.load(file_path, sr=None)  # Load audio
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

    # Plot and save spectrogram
    plt.figure(figsize=(5, 4))
    librosa.display.specshow(spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title(os.path.basename(file_path))
    plt.tight_layout()
    
    plt.savefig(output_path)
    plt.close()

# Step 5: Process the first few files from each label
for label in LABELS:
    label_path = os.path.join(DATASET_PATH, label)
    spectrogram_label_path = os.path.join(SPECTROGRAM_PATH, label)
    os.makedirs(spectrogram_label_path, exist_ok=True)

    wav_files = [f for f in os.listdir(label_path) if f.endswith('.wav')]

    if not wav_files:
        print(f"⚠️ WARNING: No .wav files found in {label_path}")
        continue

    print(f"🎵 Processing {len(wav_files[:5])} files from label '{label}'...")

    for wav_file in wav_files[:5]:  # Process only first 5 files per label
        file_path = os.path.join(label_path, wav_file)
        output_path = os.path.join(spectrogram_label_path, wav_file.replace(".wav", ".png"))
        
        generate_spectrogram(file_path, output_path)

print("✅ Spectrogram generation completed! 🎉")
