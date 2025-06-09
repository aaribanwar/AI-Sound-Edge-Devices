import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import os
from episodic_data_generator import create_episodes
from train_fsl import prototypical_loss # We can reuse the loss function for its accuracy calculation

# ==============================================================================
# === STEP 1: LOAD THE TEST DATA AND THE TRAINED EMBEDDING MODEL =============
# ==============================================================================

# Define paths
OUTPUT_PATH = "datasets" # Update if your path is different
MODEL_PATH = "fsl_embedding_model.h5"

# Load the meta-test dataset
print("🔄 Loading meta-test data and trained model...")
X_meta_test = np.load(os.path.join(OUTPUT_PATH, 'X_meta_test.npy'))
y_meta_test = np.load(os.path.join(OUTPUT_PATH, 'y_meta_test.npy'))

# Load the saved embedding model
# We add compile=False because we are not going to train it further.
embedding_model = load_model(MODEL_PATH, compile=False)
print("✅ Data and model loaded successfully.")

# ==============================================================================
# === STEP 2: SET UP AND RUN THE EVALUATION ====================================
# ==============================================================================

# Evaluation Parameters
# These can be different from training. This is a typical "2-way, 5-shot" evaluation.
N_WAY_TEST = 2  # Number of classes in the test set
K_SHOT_TEST = 5 # How many examples of each new class we get to "learn" from
Q_QUERIES_TEST = 10 # How many examples we test on
EVALUATION_EPISODES = 1000 # Number of episodes to average for a stable result

print(f"\n🚀 Starting evaluation: {N_WAY_TEST}-way, {K_SHOT_TEST}-shot with {Q_QUERIES_TEST} queries per class.")

# Create the data generator for the test set
test_generator = create_episodes(X_meta_test, y_meta_test, N_WAY_TEST, K_SHOT_TEST, Q_QUERIES_TEST)

# --- Main Evaluation Loop ---
test_accuracies = []
for i in range(EVALUATION_EPISODES):
    # Get a single test episode
    support_x, support_y, query_x, query_y = next(test_generator)
    
    # Get embeddings for all samples in the episode (no training)
    support_embeddings = embedding_model(support_x, training=False)
    query_embeddings = embedding_model(query_x, training=False)

    # Calculate the accuracy for this single episode
    # We can reuse our loss function because it also returns accuracy
    _, acc = prototypical_loss(
        support_embeddings, query_embeddings, support_y, query_y, N_WAY_TEST
    )
    test_accuracies.append(acc.numpy())

    # Print progress
    if (i + 1) % 100 == 0:
        print(f"  Completed {i+1}/{EVALUATION_EPISODES} episodes...")

# ==============================================================================
# === STEP 3: REPORT THE FINAL RESULTS =========================================
# ==============================================================================

# Calculate mean accuracy and a 95% confidence interval
mean_accuracy = np.mean(test_accuracies)
std_accuracy = np.std(test_accuracies)
confidence_interval = 1.96 * std_accuracy / np.sqrt(EVALUATION_EPISODES)

print("\n🎉 Evaluation Complete!")
print("=" * 30)
print(f"Average Test Accuracy: {mean_accuracy:.4f}")
print(f"95% Confidence Interval: {mean_accuracy:.4f} ± {confidence_interval:.4f}")
print("=" * 30)