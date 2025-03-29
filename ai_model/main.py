#%% Load Libraries
import numpy as np
import tensorflow as tf

#%% Load Dataset
x_train = np.random.rand(100, 10)
y_train = np.random.randint(0, 2, size=(100,))

#%% Train Model
model = tf.keras.models.Sequential([...])
model.fit(x_train, y_train, epochs=10)

#%% Evaluate Model
model.evaluate(x_train, y_train)
