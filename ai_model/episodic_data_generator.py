import numpy as np

def create_episodes(X, y, n_way, k_shot, q_queries):
    """
    Creates a generator of episodes for N-way, K-shot, Q-query learning.

    Args:
      X: The input data (features).
      y: The labels.
      n_way: Number of classes per episode (N).
      k_shot: Number of support examples per class (K).
      q_queries: Number of query examples per class (Q).

    Yields:
      A tuple of (support_images, support_labels, query_images, query_labels).
    """
    # Group data by class
    data_by_class = {}
    for i, label in enumerate(y):
        if label not in data_by_class:
            data_by_class[label] = []
        data_by_class[label].append(X[i])

    class_list = list(data_by_class.keys())

    while True:
        # 1. Select N classes for the episode
        episode_classes = np.random.choice(class_list, size=n_way, replace=False)

        support_images = []
        support_labels = []
        query_images = []
        query_labels = []

        for i, class_id in enumerate(episode_classes):
            # 2. Select K+Q samples from the chosen class
            all_samples_for_class = data_by_class[class_id]
            selected_samples_indices = np.random.choice(
                len(all_samples_for_class), size=k_shot + q_queries, replace=False
            )

            # 3. Split into support and query sets
            support_indices = selected_samples_indices[:k_shot]
            query_indices = selected_samples_indices[k_shot:]

            # Add to support set
            support_images.extend([all_samples_for_class[j] for j in support_indices])
            # Use relative labels (0 to N-1) for the episode
            support_labels.extend([i] * k_shot)

            # Add to query set
            query_images.extend([all_samples_for_class[j] for j in query_indices])
            query_labels.extend([i] * q_queries)

        # Shuffle the query set to avoid implicit ordering
        shuffle_indices = np.random.permutation(len(query_images))
        query_images = np.array(query_images)[shuffle_indices]
        query_labels = np.array(query_labels)[shuffle_indices]

        yield (
            np.array(support_images),
            np.array(support_labels),
            query_images,
            query_labels,
        )