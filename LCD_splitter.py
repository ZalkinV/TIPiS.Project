import os
import shutil



# Paths for input data
data_path = "./LCD_nodules/"
labels_files_names = ["traindatalabels.txt", "valdatalabels.txt", "testdatalabels.txt"]


# Paths for results
images_path_res = "./LCD_results/"
benign_dir_name = "benign/"
malignant_dir_name = "malignant/"



def create_dirs(dirs):
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)


def read_labels(file_path):
    labels_txt = {}
    with open(file_path, "r") as file:
        for line in file:
            line_parts = line.rstrip().split(" ")
            cur_file = line_parts[0]
            cur_label = int(line_parts[1])
            labels_txt[cur_file] = cur_label

    return labels_txt


def split_files(labels, images_path_res, benign_path_res, malignant_path_res):
    splitted_files_count = 0;

    # Предполгается, что у всех записей в labels одинаковая директория
    files_type = list(labels)[0].split("/")[0]
    files_path = data_path + files_type + "/"
    for file_name in os.listdir(files_path):
        if file_name.split(".")[-1] != "jpg":
            continue

        file_name_in_labels = files_type + "/" + file_name
        if labels.get(file_name_in_labels, None) is None:
            print("Warning: file {} was not found in labels so pass it.".format(file_name_in_labels))
            continue

        if labels[file_name_in_labels] == 0:
            copy_to_path = benign_path_res + files_type + "_" + file_name
        else:
            copy_to_path = malignant_path_res + files_type + "_" + file_name
        shutil.copyfile(files_path + file_name, copy_to_path)

        splitted_files_count += 1

    print("Files from {} was splitted: {}".format(files_path, splitted_files_count))


if __name__ == "__main__":
    benign_path_res = images_path_res + benign_dir_name
    malignant_path_res = images_path_res + malignant_dir_name

    create_dirs([images_path_res, benign_path_res, malignant_path_res])
    
    for labels_file_name in labels_files_names:
        labels = read_labels(data_path + labels_file_name)
        split_files(labels, images_path_res, benign_path_res, malignant_path_res)
