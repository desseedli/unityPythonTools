import os
import csv

file_path = './csv_lua'
save_path = './lua'


# 不能使用CSV的公式 比如F5格子+1等
class LuaCodeGen:
    def IsInt(string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def IsFloat(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def HandleTypeIsListStr(string):
        res = ""
        if ';' in string:
            parts = string.split(';')
            for index, part in enumerate(parts):
                if ':' in part:
                    temp_res = LuaCodeGen.HandleTypeIsListStr(part)
                    res += temp_res
                    if not index == len(parts) - 1:
                        res += ','
                else:
                    if LuaCodeGen.IsInt(part) or LuaCodeGen.IsFloat(part):
                        res += part
                    else:
                        res += '\'' + part + '\''
                    if not index == len(parts) - 1:
                        res += ','
        elif ':' in string:
            parts = string.split(':')
            res += "{"
            for index, part in enumerate(parts):
                if LuaCodeGen.IsInt(part) or LuaCodeGen.IsFloat(part):
                    res += part
                    if not index == len(parts) - 1:
                        res += ','
            res += "}"
        elif '|' in string and ';' not in string and ':' not in string:
            res += "{{"
            if LuaCodeGen.IsInt(string) or LuaCodeGen.IsFloat(string):
                res += string
            res += "}}"
        else:
            if LuaCodeGen.IsInt(string) or LuaCodeGen.IsFloat(string):
                res += string
            else:
                res += '\'' + string + '\''
        return res

    # 代码生成函数
    @staticmethod
    def GenLuaCode():
        file_list = os.listdir(file_path)
        for file_name in file_list:
            if file_name.endswith('csv'):
                file_name_no_extension, extension = os.path.splitext(file_name)
                open_file_path = os.path.join(file_path, file_name)
                lua_content = "local " + file_name_no_extension + " ={\n"
                print("open_file_path:" + open_file_path)
                with open(open_file_path, 'r', encoding='utf-8') as csvfile:
                    csvreader = csv.reader(csvfile)
                    next(csvfile)
                    header = next(csvreader)
                    types = next(csvreader)

                    csvdictreader = csv.DictReader(csvfile, fieldnames=header)
                    for row_index, row_value in enumerate(csvdictreader, start=4):
                        lua_content += "[" + row_value[header[0]] + "] = {\n"
                        for index, value in enumerate(header):
                            type = types[index]
                            if type == "int":
                                if len(row_value[value]) == 0 :
                                    lua_content += "['" + value + "'] = 0" + ",\n"
                                else:
                                    lua_content += "['" + value + "'] = " + row_value[value] + ",\n"
                            elif type == "string":
                                lua_content += "['" + value + "'] = " + '\'' + row_value[value] + '\'' + ",\n"
                            elif type == "list":
                                lua_content += "['" + value + "'] = {"
                                lua_content += LuaCodeGen.HandleTypeIsListStr(row_value[value])
                                lua_content += "},\n"
                        lua_content += "},\n"
                    lua_content += "}\n"
                    lua_content += "return " + file_name_no_extension

                lua_file_name = os.path.join(save_path, file_name_no_extension)
                lua_file_name += '.lua'
                # print(lua_content)
                with open(lua_file_name, 'w', encoding='utf-8') as lua_file:
                    lua_file.write(lua_content)

        print("done")
# LuaCodeGen.GenLuaCode()
