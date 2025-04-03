# This script will:
# 1. Create a "datasets" folder (if not already present).
# 2. Download the dataset from the provided link.
# 3. Extract the dataset into the "datasets" folder.
# 4. Remove the compressed file after extraction to save space.
#
# ----------------- INSTRUCTIONS -----------------
# To use this script, follow these steps:
# 1. Open Git Bash in the project directory.
# 2. Run the following command to execute the script:
#    
#    ./setup.sh
#
# 3. The dataset will be downloaded and extracted automatically.
#!/bin/bash

# Define dataset directory and Google Drive link
DATASET_DIR="ai_model/datasets"
DOWNLOAD_LINK="https://drive.google.com/uc?id=1K_ZXIWCv8OoroccdfTQp_4ZO368Fznbz"

# Create the datasets folder if not exists
mkdir -p "$DATASET_DIR"

# Check if dataset is already downloaded
if [ ! -d "$DATASET_DIR" ] || [ -z "$(ls -A "$DATASET_DIR")" ]; then
    echo "Downloading dataset..."
    gdown "$DOWNLOAD_LINK" -O dataset.zip
    unzip dataset.zip -d "$DATASET_DIR"
    rm dataset.zip
    echo "Dataset downloaded and extracted!"
else
    echo "Dataset already exists."
fi
