import os
from kaggle.api.kaggle_api_extended import KaggleApi

try:
    print("Authenticating Kaggle API...")
    api = KaggleApi()
    api.authenticate()
    print("Authentication successful!")

    dataset = "zfturbo/audioset"
    download_path = "datasets/audio_dataset"

    print(f"Creating directory: {download_path}")
    os.makedirs(download_path, exist_ok=True)

    print(f"Downloading {dataset} to {download_path}...")
    api.dataset_download_files(dataset, path=download_path, unzip=True)
    print("Download complete!")

except Exception as e:
    print("Error:", e)
