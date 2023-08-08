import os

def findAllFilesWithSpecifiedSuffix(target_dir, target_suffix="torrent"):
    find_res = []
    target_suffix_dot = "." + target_suffix
    walk_generator = os.walk(target_dir)
    for root_path, dirs, files in walk_generator:
        if len(files) < 1:
            continue
        for file in files:
            file_name, suffix_name = os.path.splitext(file)
            if suffix_name == target_suffix_dot:
                find_res.append(os.path.join(root_path, file))
    return find_res

findRes = findAllFilesWithSpecifiedSuffix(os.path.dirname(__file__),"torrent")
for needRemoveFilePath in findRes :
    print(needRemoveFilePath)
    os.remove(needRemoveFilePath)   
os.system("pause")
