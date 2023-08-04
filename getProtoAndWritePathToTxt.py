import os
import glob
import hashlib

dir_path = os.path.abspath("../..")
write_path = os.path.abspath("../Tools/imagePathAndMd5.txt")
duplicate_images_path  = os.path.abspath("../Tools/duplicateImages.txt")

def get_image_files(dir_path):
    image_files = []

    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isdir(file_path):
            image_files.extend(get_image_files(file_path))
        elif os.path.isfile(file_path) and file_path.lower().endswith((".jpg", ".jpeg", ".png", ".tga")):
            image_files.append(file_path)
    return image_files

def get_file_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

image_files = get_image_files(dir_path)
black_list_md5 = []
duplicate_images_list = []
repeat_index = []
black_list_path = []
isPrint = False
repeat_count = 0

with open(write_path,"w") as writer:
    for img_file in image_files:
        file_md5 = get_file_md5(img_file)
        if file_md5 in black_list_md5:
            index = black_list_md5.index(file_md5)
            if not index in repeat_index:
                tempString = black_list_path[index] + "," + black_list_md5[index]
                if isPrint :    
                    print(tempString)
                repeat_count = repeat_count + 1
                duplicate_images_list.append(tempString)
                repeat_index.append(index)
            tempString = img_file + "," + file_md5
            if isPrint:  
                print(tempString)
            repeat_count = repeat_count + 1
            duplicate_images_list.append(tempString)
        else:
            black_list_path.append(img_file)
            black_list_md5.append(file_md5)

        writer.write(img_file)
        writer.write(",")
        writer.write(file_md5)
        writer.write("\n")

with open(duplicate_images_path,"w") as writer:
    for data in duplicate_images_list:
         writer.write(data)
         writer.write("\n")

print("found count is:" + str(repeat_count) + "\n")
print("done")

    
