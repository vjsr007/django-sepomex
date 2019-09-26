# load, split and scale the maps dataset ready for training
from os import listdir
from numpy import asarray
from numpy import vstack
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from numpy import savez_compressed

from numpy import load
from matplotlib import pyplot

CREATE_IMAGES = False
PLOT_SAMPLE = True
 
# load all images in a directory into memory
def load_images(path, size=(256,512)):
	src_list, tar_list = list(), list()
	# enumerate filenames in directory, assume all are images
	for filename in listdir(path):
		# load and resize the image
		pixels = load_img(path + filename, target_size=size)
		# convert to numpy array
		pixels = img_to_array(pixels)
		# split into satellite and map
		sat_img, map_img = pixels[:, :256], pixels[:, 256:]
		src_list.append(sat_img)
		tar_list.append(map_img)
	return [asarray(src_list), asarray(tar_list)]
 
if CREATE_IMAGES:
    # dataset path
    path = 'maps/train/'
    # load dataset
    [src_images, tar_images] = load_images(path)
    print('Loaded: ', src_images.shape, tar_images.shape)
    # save as compressed numpy array
    filename = 'maps_256.npz'
    savez_compressed(filename, src_images, tar_images)
    print('Saved dataset: ', filename)

# load the prepared dataset
if PLOT_SAMPLE:
    # load the face dataset
    data = load('maps_256.npz')
    src_images, tar_images = data['arr_0'], data['arr_1']
    print('Loaded: ', src_images.shape, tar_images.shape)
    # plot source images
    n_samples = 3
    for i in range(n_samples):
        pyplot.subplot(2, n_samples, 1 + i)
        pyplot.axis('off')
        pyplot.imshow(src_images[i].astype('uint8'))
    # plot target image
    for i in range(n_samples):
        pyplot.subplot(2, n_samples, 1 + n_samples + i)
        pyplot.axis('off')
        pyplot.imshow(tar_images[i].astype('uint8'))
    pyplot.show()