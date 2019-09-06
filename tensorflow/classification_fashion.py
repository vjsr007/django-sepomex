# TensorFlow and tf.keras
import warnings
warnings.filterwarnings("ignore")

import cv2
import tensorflow as tf
from tensorflow import keras
import sys
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from keras.preprocessing import image

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

# Test Image
data = []
img = image.load_img('tensorflow/images/sneaker01.jpg', target_size=(28,28,1), grayscale=True)
img = image.img_to_array(img)
img = img/255
data.append(img)
train_image = np.array(data)
train_image = train_image.mean(axis=3)

print(train_image.shape)

# Labels
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Get values between 0 to 1 for Train Images
train_images = train_images / 255.0

# Get values between 0 to 1 for Test Images
test_images = test_images / 255.0

# Create Model
# Flatten: Input Images 28x28 to linear array(one dimention)
# ReLU: Rectified Linear Unit activation function, lineal tensor with 128 positive values or 128 neurons
# Softmax: Ten outputs with SUM equals to 1, MAX value is the predicted label
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

# Adam optimizer - changes weight values
# Categorical CrossEntropy it's used when with classifification problems, each result is only a label
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Trainig model with train images and their labels with five epochs
model.fit(train_images, train_labels, epochs=5)

# Made prediction with test images
predictions = model.predict(train_image)

print(predictions)

i = 0
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions, test_labels, train_image)
plt.subplot(1,2,2)
plot_value_array(i, predictions,  test_labels)
plt.show()

# https://www.analyticsvidhya.com/blog/2019/01/build-image-classification-model-10-minutes/
# https://becominghuman.ai/building-an-image-classifier-using-deep-learning-in-python-totally-from-a-beginners-perspective-be8dbaf22dd8
# https://medium.com/datadriveninvestor/deep-learning-techniques-for-text-classification-9392ca9492c7