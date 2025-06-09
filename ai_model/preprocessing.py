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
METADATA_PATH = "./datasets/UrbanSound8K/metadata/UrbanSound8K.csv"
DATASET_PATH = "./datasets/UrbanSound8K/audio"
OUTPUT_PATH = "./datasets"


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

# Convert lists to numpy arrays
X = np.array(mfccs)
y = np.array(labels)

# Reshape X for the model
max_len = max(m.shape[0] for m in mfccs)
X_padded = np.array([np.pad(m, ((0, max_len - m.shape[0]), (0, 0)), mode='constant') for m in mfccs])
X_padded = X_padded[..., np.newaxis] # Add channel dimension

print("✅ Preprocessing complete.")
print(f"Shape of X: {X_padded.shape}")
print(f"Shape of y: {y.shape}")

# Define the split of classes for meta-learning
# You can change these class IDs based on your preference
all_class_ids = np.unique(y)
np.random.shuffle(all_class_ids) # Shuffle for a random split

meta_train_classes = all_class_ids[:6]
meta_val_classes = all_class_ids[6:8]
meta_test_classes = all_class_ids[8:]

print(f"\nMeta-Train Class IDs: {meta_train_classes}")
print(f"Meta-Val Class IDs: {meta_val_classes}")
print(f"Meta-Test Class IDs: {meta_test_classes}")

# Function to split the data based on class IDs
def split_data_by_classes(X, y, class_ids):
    indices = np.isin(y, class_ids)
    return X[indices], y[indices]

# Create the data splits
X_meta_train, y_meta_train = split_data_by_classes(X_padded, y, meta_train_classes)
X_meta_val, y_meta_val = split_data_by_classes(X_padded, y, meta_val_classes)
X_meta_test, y_meta_test = split_data_by_classes(X_padded, y, meta_test_classes)


# Save the new FSL datasets
print("\n💾 Saving datasets for Few-Shot Learning...")
np.save(os.path.join(OUTPUT_PATH, "X_meta_train.npy"), X_meta_train)
np.save(os.path.join(OUTPUT_PATH, "y_meta_train.npy"), y_meta_train)
np.save(os.path.join(OUTPUT_PATH, "X_meta_val.npy"), X_meta_val)
np.save(os.path.join(OUTPUT_PATH, "y_meta_val.npy"), y_meta_val)
np.save(os.path.join(OUTPUT_PATH, "X_meta_test.npy"), X_meta_test)
np.save(os.path.join(OUTPUT_PATH, "y_meta_test.npy"), y_meta_test)

print("✅ FSL data saved successfully.")


# We are keeping this function as it might be useful later for single predictions
def preprocess_custom_sound(audio, sr=22050, max_len=max_len):
    audio = audio.flatten()
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T
    mfcc = np.pad(mfcc, ((0, max_len - mfcc.shape[0]), (0, 0)), mode='constant')
    return mfcc[np.newaxis, ..., np.newaxis]
