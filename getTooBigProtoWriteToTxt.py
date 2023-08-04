import os
import importlib
import subprocess

dir_path = os.path.abspath("../../Content/Icons")
write_path = os.path.abspath("../Tools/tooBigImage.txt")
rate = 1

def check_and_install_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"模块 {module_name} 已安装")
    except ImportError:
        print(f"模块 {module_name} 未安装，正在安装...")
        try:
            subprocess.check_call(['pip', 'install', module_name])
            print(f"模块 {module_name} 安装成功")
        except subprocess.CalledProcessError:
            print(f"模块 {module_name} 安装失败")

check_and_install_module("pillow")
from PIL import Image

def get_image_files(dir_path):
    image_files = []
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isdir(file_path):
            image_files.extend(get_image_files(file_path))
        elif os.path.isfile(file_path) and file_path.lower().endswith((".jpg", ".jpeg", ".png", ".tga")):
            if os.path.getsize(file_path) > 1 * 1024 * 1024 * rate:
                image = Image.open(file_path)
                if image.width >= 400 and image.height >= 400:
                    image_files.append(file_path)            
    return image_files

image_files = get_image_files(dir_path)

with open(write_path,"w") as writer:
    for img_file in image_files:
        writer.write(img_file)
        writer.write("\n")



print("done")

    
