import os
import shutil

import numpy as np
import matplotlib.pyplot as plt



# Paths for input data
nodules_path = "./GAN_nodules/"
labels_file_path = "./GAN_nodules/full_label.csv"


# Paths for results
nodules_paths_res = ["./GAN_results/benign/",
                 "./GAN_results/malignant/",]

images_path_res = "./GAN_results/images/"



def create_dirs(dirs):
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)


def read_labels(file_path):
    labels_csv = {}
    with open(file_path, "r") as file:
        header = file.readline().rstrip()
        for line in file:
            cur_id, cur_label = line.rstrip().split(",")
            labels_csv[cur_id] = int(cur_label)

    return labels_csv


def split_files(nodules_all_path, labels, benign_path_res, malignant_path_res):
    splitted_files_count = 0;
    for file_name in os.listdir(nodules_all_path):
        if file_name.split(".")[-1] != "npy":
            continue

        patient_name = file_name.split("_")[0]
     
        if labels[patient_name] == 0:
            copy_to_path = malignant_path_res + file_name
        else:
            copy_to_path = benign_path_res + file_name
        shutil.copyfile(nodules_all_path + file_name, copy_to_path)
        
        splitted_files_count += 1

    print("Files was splitted: {}".format(splitted_files_count))


def create_images(nodules_paths):
    for nodules_path in nodules_paths:

        handled_files_count = 0
        nodule_type = nodules_path.rstrip("/").split("/")[-1]
        for npy_file_name in os.listdir(nodules_path):

            patient_name = npy_file_name.split("_")[0]
            image_path = images_path_res + nodule_type + "/"
            
            if not os.path.exists(image_path):
                os.makedirs(image_path)

            npy_file = np.load(nodules_path + npy_file_name)
            for slice_number in range(len(npy_file)):
                image_name = image_path + patient_name + "_" + str(slice_number) + ".png"
                plt.imsave(image_name, npy_file[slice_number], cmap='gray')
            handled_files_count += 1

        print("Images for {} files in {} was created!".format(handled_files_count, nodules_path))


if __name__ == "__main__":
    create_dirs([nodules_paths_res[0], nodules_paths_res[1], images_path_res])
    labels = read_labels(labels_file_path)
    split_files(nodules_path, labels, nodules_paths_res[0], nodules_paths_res[1])
    create_images(nodules_paths_res)
