# TensorFlow and tf.keras
import warnings
warnings.filterwarnings("ignore")

import tensorflow as tf
from tensorflow import keras
import sys
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator, load_img, image
import os
import pandas as pd 

TRAIN=False

# Show image in plot with true label vs predicted label
def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plt.grid(True)
  plt.xticks([])
  plt.yticks([])
  
  plt.imshow(img, cmap=plt.cm.binary)
  
  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'
  
  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

# Show bars with predictions
def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(True)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)
  
  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

def load_image(pathImg) :
    data = []
    full_size_image = cv2.imread(pathImg, 1)
    data.append(cv2.resize(full_size_image, (28,28), Image.ANTIALIAS))
    return data

# Get Fashion DataSet
fashion_mnist = keras.datasets.fashion_mnist

# Download DataSet
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# Labels
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Get values between 0 to 1 for Train Images
train_images = train_images / 255.0

# Get values between 0 to 1 for Test Images
test_images = test_images / 255.0

# Add an empty color dimension as the Convolutional net is expecting this
x_train = np.expand_dims(train_images, -1)
x_test = np.expand_dims(test_images, -1)

print(x_train.shape)

# We begin by defining the a empty stack. We'll use this for building our 
# network, later by layer.
model = tf.keras.models.Sequential()

# We start with a convolutional layer this will extract features from 
# the input images by sliding a convolution filter over the input image, 
# resulting in a feature map.
model.add(
    tf.keras.layers.Conv2D(
        filters=32, # How many filters we will learn 
        kernel_size=(3, 3), # Size of feature map that will slide over image
        strides=(1, 1), # How the feature map "steps" across the image
        padding='valid', # We are not using padding
        activation='relu', # Rectified Linear Unit Activation Function
        input_shape=(28, 28, 1) # The expected input shape for this layer
    )
) 

# The next layer we will add is a Maxpooling layer. This will reduce the 
# dimensionality of each feature, which reduces the number of parameters that 
# the model needs to learn, which shortens training time.
model.add(
    tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2), # Size feature will be mapped to
        strides=(2, 2) # How the pool "steps" across the feature
    )
)
          
# We'll now add a dropout layer. This fights overfitting and forces the model to 
# learn multiple representations of the same data by randomly disabling neurons 
# in the learning phase.
model.add(
    tf.keras.layers.Dropout(
        rate=0.25 # Randomly disable 25% of neurons
    )
)

# Output from previous layer is a 3D tensor. This must be flattened to a 1D 
# vector before beiung fed to the Dense Layers.
model.add(
    tf.keras.layers.Flatten()
)

# A dense (interconnected) layer is added for mapping the derived features 
# to the required class.
model.add(
    tf.keras.layers.Dense(
        units=128, # Output shape
        activation='relu' # Rectified Linear Unit Activation Function
    )
)

# Final layer with 10 outputs and a softmax activation. Softmax activation 
# enables me to calculate the output based on the probabilities. 
# Each class is assigned a probability and the class with the maximum 
# probability is the model’s output for the input.
model.add(
    tf.keras.layers.Dense(
        units=10, # Output shape
        activation='softmax' # Softmax Activation Function
    )
)

# Build the model
model.compile(
    loss=tf.keras.losses.sparse_categorical_crossentropy, # loss function
    optimizer=tf.keras.optimizers.Adam(), # optimizer function
    metrics=['accuracy'] # reporting metric
)

if TRAIN:
    # Train the CNN on the training data
    history = model.fit(
        
        # Training data : features (images) and classes.
        x_train, train_labels,
                        
        # number of samples to work through before updating the 
        # internal model parameters via back propagation.
        batch_size=256, 

        # An epoch is an iteration over the entire training data.
        epochs=10, 

        # The model will set apart his fraction of the training 
        # data, will not train on it, and will evaluate the loss
        # and any model metrics on this data at the end of 
        # each epoch. 
        validation_split=0.2, 

        verbose=1)
    model.save_weights("fashion/model.h5")
else:
    model.load_weights("fashion/model.h5")

test_filenames = os.listdir("fashion/images")
test_df = pd.DataFrame({
    'filename': test_filenames
})
nb_samples = test_df.shape[0]
test_gen = ImageDataGenerator(rescale=1./255)
test_generator = test_gen.flow_from_dataframe(
    test_df, 
    "fashion/images/", 
    x_col='filename',
    y_col=None,
    class_mode=None,
    target_size=(28,28),
    color_mode="grayscale",
    batch_size=15,
    shuffle=False
)
predict = model.predict_generator(test_generator, steps=np.ceil(nb_samples/15))
for idx, p in enumerate(predict):
    print("=========================================")
    print(class_names[np.argmax(p)])
    print(test_filenames[idx])
    print(np.argmax(p))
    print(p)