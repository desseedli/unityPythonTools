import os

waring = input("必须放在需要命名的文件夹下面,切勿直接运行")
startNum = input("please input start num:")

walk_generator = os.walk(os.path.dirname(os.path.abspath(__file__)))
for root_path, dirs, files in walk_generator:
     if len(files) < 1:
            continue
     for file in files:
          file_name, suffix_name = os.path.splitext(file)
          if suffix_name == '.py':
               continue
          intFileName = int(file_name)
          result = intFileName + int(startNum)
          os.rename(file,str(result).zfill(4) + suffix_name)
os.system("pause")
#os.path.isdir(path)
