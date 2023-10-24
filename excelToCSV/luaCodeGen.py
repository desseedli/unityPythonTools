import os
import csv
import math

file_path = './csv_lua'
save_path = './lua'

count_limit = 2000

class LuaCodeGen:
    def __init__(self):
        self.file_name_no_extension = ""
        self.csvdictreader = {}
        self.types = {}
        self.header = {}

    def create_lua_header(self, page_count):
        lua_file_name = os.path.join(save_path, self.file_name_no_extension)
        lua_file_name += '.lua'
        lua_content = "return function()\n"
        lua_content += "\tlocal " + self.file_name_no_extension + " = {}\n"
        lua_content += "\tfor i = 1, " + str(page_count) + " do\n"
        lua_content += "\t\tlocal cfg = InternalRequire('{}' ..i,true)\n".format(self.file_name_no_extension)
        lua_content += "\t\tfor k ,v in pairs(cfg) do\n"
        lua_content += "\t\t\t" + self.file_name_no_extension + "[k] = v\n"
        lua_content += "\t\tend\n"
        lua_content += "\tend\n"
        for page in range(1, page_count + 1):
            lua_content += "\tpackage.loaded['{}'] = nil\n".format(self.file_name_no_extension + str(page))
        lua_content += "\treturn " + self.file_name_no_extension + "\n"
        lua_content += "end"
        with open(lua_file_name, 'w', encoding='utf-8') as lua_file:
            lua_file.write(lua_content)

    def write_lua_content(self, startRow):
        lua_content = ""
        count = 0
        for row_index, row_value in enumerate(self.csvdictreader, start=startRow):
            if row_value[self.header[0]]:
                count += 1
                lua_content += "[" + row_value[self.header[0]] + "]={\n"
                for index, value in enumerate(self.header):
                    type = self.types[index]
                    if type == "int" or type == "float":
                        if len(row_value[value]) == 0:
                            lua_content += "['" + value + "']=0" + ",\n"
                        else:
                            lua_content += "['" + value + "']=" + row_value[value] + ",\n"
                    elif type == "string":
                        lua_content += "['" + value + "']=" + '\'' + row_value[value] + '\'' + ",\n"
                    elif type == "bool":
                        if len(row_value[value]) == 0:
                            lua_content += "['" + value + "']=false,\n"
                        else:
                            lua_content += "['" + value + "']=" + row_value[value] + ",\n"
                    elif type == "list" and len(row_value[value].strip()) != 0:
                        lua_content += "['" + value + "']={"
                        lua_content += self.handle_type_is_list_str(row_value[value])
                        lua_content += "},\n"
                lua_content += "},\n"
                if count >= count_limit:
                    return lua_content
        return lua_content

    def is_int(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def is_float(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def handle_type_is_list_str(self, string):
        res = ""
        if ';' in string:
            parts = string.split(';')
            for index, part in enumerate(parts):
                if ':' in part:
                    temp_res = self.handle_type_is_list_str(part)
                    res += temp_res
                    if not index == len(parts) - 1:
                        res += ','
                else:
                    if self.is_int(part) or self.is_float(part):
                        res += part
                    else:
                        res += '\'' + part + '\''
                    if not index == len(parts) - 1:
                        res += ','
        elif ':' in string:
            parts = string.split(':')
            res += "{"
            for index, part in enumerate(parts):
                if self.is_int(part) or self.is_float(part):
                    res += part
                    if not index == len(parts) - 1:
                        res += ','
            res += "}"
        elif '|' in string and ';' not in string and ':' not in string:
            res += "{{"
            if self.is_int(string) or self.is_float(string):
                res += string
            res += "}}"
        else:
            if self.is_int(string) or self.is_float(string):
                res += string
            else:
                res += '\'' + string + '\''
        return res

    # 代码生成函数
    def gen_lua_code(self):
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_list = os.listdir(file_path)
        for file_name in file_list:
            if file_name.endswith('csv'):
                self.file_name_no_extension, extension = os.path.splitext(file_name)
                open_file_path = os.path.join(file_path, file_name)
                print("open_file_path:" + open_file_path)

                with open(open_file_path, 'r', encoding='utf-8') as csvfile:
                    csvreader = csv.reader(csvfile)
                    row_count = sum(1 for _ in csvreader)
                    need_page = math.ceil(row_count / count_limit)

                    csvfile.seek(0)

                    csvreader = csv.reader(csvfile)
                    next(csvfile)
                    self.header = next(csvreader)
                    self.types = next(csvreader)
                    self.csvdictreader = csv.DictReader(csvfile, fieldnames=self.header)
                    if need_page == 1:
                        lua_content = "local " + self.file_name_no_extension + "={\n"
                        lua_content += self.write_lua_content(4)
                        lua_content += "}\n"
                        lua_content += "return " + self.file_name_no_extension

                        lua_file_name = os.path.join(save_path, self.file_name_no_extension)
                        lua_file_name += '.lua'
                        with open(lua_file_name, 'w', encoding='utf-8') as lua_file:
                            lua_file.write(lua_content)
                    elif need_page > 1:
                        self.create_lua_header(need_page)
                        for page in range(1, need_page + 1):
                            class_name = self.file_name_no_extension + str(page)
                            lua_content = "local " + class_name + " ={\n"
                            lua_content += self.write_lua_content((page - 1) * count_limit + 4)
                            lua_content += "}\n"
                            lua_content += "return " + self.file_name_no_extension + str(page)
                            lua_file_name = os.path.join(save_path, class_name)
                            lua_file_name += '.lua'
                            with open(lua_file_name, 'w', encoding='utf-8') as lua_file:
                                lua_file.write(lua_content)
        print("done")


#luaCodeGen = LuaCodeGen()
#luaCodeGen.gen_lua_code()
