# preprocess_us8k.py
import os
import numpy as np
import pandas as pd
import librosa
from tqdm import tqdm

# Constants
BASE_DIR = "datasets/UrbanSound8K"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
METADATA_PATH = os.path.join(BASE_DIR, "metadata", "UrbanSound8K.csv")
OUTPUT_PATH = "datasets"
SAMPLE_RATE = 22050
N_MELS = 64
N_FFT = 1024
HOP_LENGTH = 512
FIXED_WIDTH = 128

def extract_mel_spectrogram(file_path):
    y, sr = librosa.load(file_path, sr=SAMPLE_RATE, mono=True)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=N_FFT,
                                               hop_length=HOP_LENGTH, n_mels=N_MELS)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    # Pad or truncate to fixed width
    if mel_spec_db.shape[1] < FIXED_WIDTH:
        pad_width = FIXED_WIDTH - mel_spec_db.shape[1]
        mel_spec_db = np.pad(mel_spec_db, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mel_spec_db = mel_spec_db[:, :FIXED_WIDTH]

    return mel_spec_db

def preprocess_data():
    metadata = pd.read_csv(METADATA_PATH)

    X = []
    y = []

    print("Processing audio files...")
    for index, row in tqdm(metadata.iterrows(), total=len(metadata)):
        fold = f"fold{row['fold']}"
        file_name = row['slice_file_name']
        class_id = row['classID']
        file_path = os.path.join(AUDIO_DIR, fold, file_name)

        try:
            mel_spec = extract_mel_spectrogram(file_path)
            X.append(mel_spec)
            y.append(class_id)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    X = np.array(X)[..., np.newaxis]  # Shape: (N, 64, 128, 1)
    y = np.array(y)  # Shape: (N,)

    print(f"Final dataset shape: X={X.shape}, y={y.shape}")

    # Save
    np.save(os.path.join(OUTPUT_PATH, "X.npy"), X)
    np.save(os.path.join(OUTPUT_PATH, "y.npy"), y)
    print("Saved X.npy and y.npy")

if __name__ == "__main__":
    preprocess_data()
