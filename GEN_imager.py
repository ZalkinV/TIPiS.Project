import os
import shutil
import random

import numpy as np
import matplotlib.pyplot as plt



max_images_count = 4000
# Paths for input data
npy_files_path = "../set/"

# Paths for results
images_path = "../gan/"



def create_images(nodules_path, images_path_res, max_count):
    print("Start creating images!")

    handled_files_count = 0
    random_picked_files = os.listdir(nodules_path)
    random.shuffle(random_picked_files)
    for npy_file_name in random_picked_files:

        if (handled_files_count >= max_count):
            break
            
        if not os.path.exists(images_path_res):
            os.makedirs(images_path_res)

        npy_file = np.load(nodules_path + npy_file_name)
        image_name = images_path_res + npy_file_name.rsplit(".")[0] + ".png"
        plt.imsave(image_name, npy_file, cmap='gray')
        handled_files_count += 1

        if handled_files_count % (int(max_count / 10)) == 0:
            print("{}/{} images was created.".format(handled_files_count, max_count))

    print("Images for {} files from {} was created in {}!".format(handled_files_count, nodules_path, images_path_res))


if __name__ == "__main__":
    create_images(npy_files_path, images_path, max_images_count)
