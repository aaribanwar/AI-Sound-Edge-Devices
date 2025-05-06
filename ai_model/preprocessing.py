import os
import numpy as np
import pandas as pd
import librosa
import librosa.display
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Define audio augmentation pipeline
AUGMENT = Compose([
    AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.3),
    TimeStretch(min_rate=0.8, max_rate=1.25, p=0.3),
    PitchShift(min_semitones=-4, max_semitones=4, p=0.4),
    Shift(min_shift=-0.5, max_shift=0.5, p=0.2)
])

# Define paths and parameters
METADATA_PATH = r"C:\Users\aniru\OneDrive\Desktop\miniProject\AI-Sound-Edge-Devices\ai_model\datasets\UrbanSound8K\metadata\UrbanSound8K.csv"
DATASET_PATH = r"C:\Users\aniru\OneDrive\Desktop\miniProject\AI-Sound-Edge-Devices\ai_model\datasets\UrbanSound8K\audio"
OUTPUT_PATH = r"C:\Users\aniru\OneDrive\Desktop\miniProject\AI-Sound-Edge-Devices\ai_model\datasets"

SAMPLE_RATE = 22050
DURATION = 4  # seconds
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION

# Classes to augment
classes_to_augment = ['jackhammer', 'children_playing', 'engine_idling']

# Initialize lists to store MFCC features and labels
mfccs = []
labels = []

# Load metadata
metadata = pd.read_csv(METADATA_PATH)

print("🔄 Preprocessing audio files...")

# Loop through each row in the metadata
for index, row in tqdm(metadata.iterrows(), total=len(metadata)):
    file_path = os.path.join(DATASET_PATH, f"fold{row['fold']}", row['slice_file_name'])
    label = row['class']
    signal, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

    # Ensure the signal is of the correct length
    if len(signal) < SAMPLES_PER_TRACK:
        pad = SAMPLES_PER_TRACK - len(signal)
        signal = np.pad(signal, (0, pad))
    else:
        signal = signal[:SAMPLES_PER_TRACK]

    # Extract MFCC features from the original signal
    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=40)
    mfcc = mfcc.T  # Transpose to (time, features)
    mfccs.append(mfcc)
    labels.append(row['classID'])

    # Augment only the specified classes
    if label in classes_to_augment:
        for _ in range(2):  # Create two augmented examples per sample
            aug_signal = AUGMENT(samples=signal, sample_rate=sr)
            mfcc_aug = librosa.feature.mfcc(y=aug_signal, sr=sr, n_mfcc=40).T
            mfccs.append(mfcc_aug)
            labels.append(row['classID'])

# Pad MFCCs to equal length
max_len = max(m.shape[0] for m in mfccs)
X = np.array([np.pad(m, ((0, max_len - m.shape[0]), (0, 0)), mode='constant')
              for m in mfccs])
X = X[..., np.newaxis]  # Add channel dimension

y = np.array(labels)

# Save the processed data
np.save(os.path.join(OUTPUT_PATH, "X_data.npy"), X)
np.save(os.path.join(OUTPUT_PATH, "y_data.npy"), y)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)
np.save(os.path.join(OUTPUT_PATH, "X_train.npy"), X_train)
np.save(os.path.join(OUTPUT_PATH, "X_test.npy"), X_test)
np.save(os.path.join(OUTPUT_PATH, "y_train.npy"), y_train)
np.save(os.path.join(OUTPUT_PATH, "y_test.npy"), y_test)

print("✅ Preprocessing complete. Saved X_train, X_test, y_train, y_test to datasets folder.")
