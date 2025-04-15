import os
import numpy as np
import tensorflow as tf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

# Auto-detect base path (you can also hardcode if needed)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "datasets")
MODEL_PATH = os.path.join(BASE_PATH, "sound_classification_model.h5")
METADATA_PATH = os.path.join(DATA_PATH, "UrbanSound8K", "metadata", "UrbanSound8K.csv")

# Load data
X_test = np.load(os.path.join(DATA_PATH, "X_test.npy"))
y_test = np.load(os.path.join(DATA_PATH, "y_test.npy"))

# Load label names from metadata
metadata = pd.read_csv(METADATA_PATH)
class_labels = metadata["class"].unique()
class_labels.sort()  # Ensure consistent ordering

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Predict
y_pred = np.argmax(model.predict(X_test), axis=1)

# Classification Report
report = classification_report(y_test, y_pred, target_names=class_labels)
print("Classification Report:\n", report)

# Save report (optional)
with open(os.path.join(BASE_PATH, "classification_report.txt"), "w") as f:
    f.write(report)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_labels, yticklabels=class_labels)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()
