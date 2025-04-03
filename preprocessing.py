import os
import numpy as np
import librosa

DATASET_PATH = "datasets/audio_dataset"
OUTPUT_PATH = "datasets/"

def convert_to_spectrogram(file_path, n_mels=64, n_fft=1024, hop_length=512, fixed_width=128):
    y, sr = librosa.load(file_path, sr=16000)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    # Pad or truncate the spectrogram to have a fixed width
    if mel_spec_db.shape[1] < fixed_width:
        pad_width = fixed_width - mel_spec_db.shape[1]
        mel_spec_db = np.pad(mel_spec_db, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mel_spec_db = mel_spec_db[:, :fixed_width]

    return mel_spec_db

# Collect all WAV files
all_files = []
for root, _, files in os.walk(DATASET_PATH):
    for file in files:
        if file.endswith(".wav"):
            all_files.append(os.path.join(root, file))

all_files = all_files[:5000]  # Limit to 5000 samples
print(f"Found {len(all_files)} audio files.")

# Convert all audio files to spectrograms
spectrograms = [convert_to_spectrogram(f) for f in all_files]

# Convert to NumPy array with shape (5000, 64, 128, 1)
X_train = np.array(spectrograms)[..., np.newaxis]

print(f"Final dataset shape: {X_train.shape}")

# Save dataset
np.save(os.path.join(OUTPUT_PATH, "X_train.npy"), X_train)
print("Saved dataset as X_train.npy")
