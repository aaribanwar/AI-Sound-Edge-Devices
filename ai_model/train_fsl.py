import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import numpy as np
import os
from episodic_data_generator import create_episodes # <-- Import from our newly named file

# ==============================================================================
# === STEP 1: LOAD THE META-TRAINING AND META-VALIDATION DATASETS =============
# ==============================================================================

# Define paths
OUTPUT_PATH = "datasets" # Update if your path is different

# Load the datasets we created in the preprocessing step
X_meta_train = np.load(os.path.join(OUTPUT_PATH, 'X_meta_train.npy'))
y_meta_train = np.load(os.path.join(OUTPUT_PATH, 'y_meta_train.npy'))
X_meta_val = np.load(os.path.join(OUTPUT_PATH, 'X_meta_val.npy'))
y_meta_val = np.load(os.path.join(OUTPUT_PATH, 'y_meta_val.npy'))

print("Meta-Train data shapes:", X_meta_train.shape, y_meta_train.shape)
print("Meta-Validation data shapes:", X_meta_val.shape, y_meta_val.shape)

# ==============================================================================
# === STEP 2: BUILD THE EMBEDDING MODEL ========================================
# ==============================================================================

def build_embedding_model(input_shape):
    """
    This is your CRNN model, but without the final classification layer.
    Its output is a 128-dimensional embedding vector.
    """
    model = models.Sequential(name="embedding_model")
    
    # CNN layers with BatchNormalization
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # Reshape for LSTM layers
    model.add(layers.Reshape((-1, 128)))
    model.add(layers.Bidirectional(layers.LSTM(128, return_sequences=True)))
    model.add(layers.Bidirectional(layers.LSTM(128)))

    # This is our final embedding layer
    model.add(layers.Dense(128, activation=None)) # No activation, just the raw vector
    # We remove the final Dropout and Dense classifier layers

    return model

# ==============================================================================
# === STEP 3: DEFINE THE PROTOTYPICAL LOSS FUNCTION ============================
# ==============================================================================

def prototypical_loss(support_embeddings, query_embeddings, support_labels, query_labels, n_way):
    """
    Calculates the prototypical loss and accuracy for a given episode.
    """
    # 1. Calculate Prototypes from the support set
    # Prototypes are the mean of the embeddings for each class
    prototypes = []
    for i in range(n_way):
        class_indices = tf.where(tf.equal(support_labels, i))
        class_embeddings = tf.gather(support_embeddings, class_indices)
        class_embeddings = tf.squeeze(class_embeddings, axis=1)
        prototypes.append(tf.reduce_mean(class_embeddings, axis=0))
    prototypes = tf.stack(prototypes)

    # 2. Calculate distances from query samples to prototypes
    # We use squared Euclidean distance for efficiency
    query_expanded = tf.expand_dims(query_embeddings, 1) # Shape: (q*n, 1, emb_dim)
    prototypes_expanded = tf.expand_dims(prototypes, 0)   # Shape: (1, n, emb_dim)
    
    distances = tf.reduce_sum(tf.square(query_expanded - prototypes_expanded), axis=2)
    
    # 3. Calculate loss using the standard, stable TensorFlow function
    # The "logits" are the negative distances.
    # We want to minimize distance, which is equivalent to maximizing negative distance.
    loss = tf.reduce_mean(
        tf.nn.sparse_softmax_cross_entropy_with_logits(logits=-distances, labels=query_labels)
    )

    # 4. Calculate accuracy
    predictions = tf.cast(tf.argmin(distances, axis=1), tf.int32)
    accuracy = tf.reduce_mean(tf.cast(tf.equal(predictions, query_labels), tf.float32))

    return loss, accuracy


# ==============================================================================
# === STEP 4: THE CUSTOM TRAINING LOOP =========================================
# ==============================================================================

# FSL Parameters
N_WAY = 5       # 5 classes per episode
K_SHOT = 5      # 5 examples per class for support
Q_QUERIES = 5   # 5 examples per class for querying
N_WAY_VAL = 2   # 2 classes per episode for VALIDATION (matches our 6:2:2 split)

# Training Parameters
TRAINING_STEPS = 5000
VALIDATION_FREQ = 100
VALIDATION_STEPS = 100 # How many episodes to average for validation score

# Model and Optimizer
input_shape = X_meta_train.shape[1:]
embedding_model = build_embedding_model(input_shape)
optimizer = optimizers.Adam(learning_rate=0.001)

# Create data generators
train_generator = create_episodes(X_meta_train, y_meta_train, N_WAY, K_SHOT, Q_QUERIES)
val_generator = create_episodes(X_meta_val, y_meta_val, N_WAY_VAL, K_SHOT, Q_QUERIES)

# --- Main Training Loop ---
print("\n🚀 Starting Few-Shot Learning Training...")
for step in range(TRAINING_STEPS):
    # Get a single episode from the training generator
    support_x, support_y, query_x, query_y = next(train_generator)

    with tf.GradientTape() as tape:
        # 1. Get embeddings for all samples in the episode
        support_embeddings = embedding_model(support_x, training=True)
        query_embeddings = embedding_model(query_x, training=True)

        # 2. Calculate loss and accuracy for the episode
        loss, acc = prototypical_loss(
            support_embeddings, query_embeddings, support_y, query_y, N_WAY
        )

    # 3. Apply gradients
    gradients = tape.gradient(loss, embedding_model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, embedding_model.trainable_variables))

    # Print training progress
    if (step + 1) % 100 == 0:
        print(f"Step {step+1}/{TRAINING_STEPS} -> Train Loss: {loss.numpy():.4f}, Train Acc: {acc.numpy():.4f}")

    # --- Validation Loop ---
if (step + 1) % VALIDATION_FREQ == 0:
    val_losses = []
    val_accs = []
    for _ in range(VALIDATION_STEPS):
        # ... code to get validation episode ...
        s_x_val, s_y_val, q_x_val, q_y_val = next(val_generator)

        # ... code to get embeddings ...
        s_embed_val = embedding_model(s_x_val, training=False)
        q_embed_val = embedding_model(q_x_val, training=False)

        # Calculate loss and accuracy using N_WAY_VAL
        val_loss, val_acc = prototypical_loss(
            s_embed_val, q_embed_val, s_y_val, q_y_val, N_WAY_VAL # <-- Use N_WAY_VAL here
        )
        val_losses.append(val_loss.numpy())
        val_accs.append(val_acc.numpy())
        
        # Print average validation performance
        print(f"--- Validation at Step {step+1} -> Val Loss: {np.mean(val_losses):.4f}, Val Acc: {np.mean(val_accs):.4f} ---")

# Save the final embedding model
embedding_model.save('fsl_embedding_model.h5')
print("\n✅ Training complete. Embedding model saved as 'fsl_embedding_model.h5'")