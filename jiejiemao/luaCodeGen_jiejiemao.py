import os
import csv
import math
import re

count_limit = 2000
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

ExportMode = {'Client':0, 'Server':1, 'Lua':2}

def print_error(message):
    print(RED +  message + RESET)

def print_green(message):
    print(GREEN + message + RESET)

def is_number_or_float(sample_str):
    ''' Returns True if the string contains only
        number or float '''
    if sample_str == "" or sample_str == " ":
        result = True
    else:
        try:
            float_value = float(sample_str)
            return True
        except ValueError:
            return False
            
    return result

def print_lua_table(data):
    result = ""
    if type(data) == list:
        result += "{"
        for item in data:
            result += print_lua_table(item) + ","
        result = result.rstrip(",")
        result += "}"
    else:
        if data == '':
            return r"''"
        else:
            return data
    return result

def convert_to_lua_table(data):
    lua_table = "{"
    
    for sublist in data:
        if sublist == "":
            lua_table += "'',"
        else:
            lua_table += "{"
            
            for item in sublist:
                lua_table += "{" + ",".join(item) + "},"
            
            lua_table = lua_table.rstrip(",")  # Remove trailing comma and space
            lua_table += "},"
    
    lua_table = lua_table.rstrip(",")  # Remove trailing comma and space
    lua_table += "}"
    
    return lua_table


def convert_to_python_list_vertical_bar(data):
    if data == "" or data == " ":
        return ""
    else:    
        split_list = data.split("|")
        if len(split_list) == 1:
            if not is_number_or_float(split_list[0]):
                data = "'" + data + "'"
            return data
        else:
            split_list = ["'" + s + "'" if not is_number_or_float(s) else s for s in split_list]
            return split_list

def convert_to_python_list_colon(data):
    if data == "" or data == " ":
        return ""
    else:
        split_list = data.split(":")
        if len(split_list) == 1:
            result = []
            l = convert_to_python_list_vertical_bar(split_list[0])
            if l == "":
                return ""
            else:
                ll = convert_to_python_list_vertical_bar(split_list[0])
                if type(ll) == list:
                    result.append(convert_to_python_list_vertical_bar(split_list[0]))
                    return result
                else:
                    return ll
        else:
            result = []
            for ele in split_list:
                result.append(convert_to_python_list_vertical_bar(ele))
            return result

def convert_to_python_list_semicolon(data):
    split_list = data.split(";")
    result = []
    for ele in split_list:
        result.append(convert_to_python_list_colon(ele))
    return result

def convert_to_python_list(data):
    fixlastsemicolon = False
    if len(data) > 0:
        if data[-1] == ";":
            data = data[:-1]
    return convert_to_python_list_semicolon(data);

class LuaCodeGen:
    def __init__(self):
        self.file_name_no_extension = ""
        self.csvdictreader = {}
        self.types = {}
        self.header = {}

    def create_lua_header(self, filename, page_count):
        lua_file_name = filename
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
                            if(row_value[value] == "True"):
                                lua_content += "['" + value + "']=" + "true" + ",\n"
                            elif(row_value[value] == "False"):
                                lua_content += "['" + value + "']=" + "false" + ",\n"
                            elif(row_value[value] == "true"):
                                lua_content += "['" + value + "']=" + "true" + ",\n"
                            elif(row_value[value] == "false"):
                                lua_content += "['" + value + "']=" + "false" + ",\n"
                            else:
                                print_error("Error: can not handle bool value " + row_value[value])
                    elif type == "list" and len(row_value[value].strip()) != 0:
                        lua_content += "['" + value + "']="
                        lua_content += self.handle_type_is_list_str(row_value[value])
                        lua_content += ",\n"
                    elif type == "enum":                        
                        lua_content += "['" + value + "']=Enum." + value + "." + row_value[value] + ",\n"
                        #print_error("can not handle enum " + value)
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
        fixlastsemicolon = False
        if len(string) > 0:
            if string[-1] == ";":
                fixlastsemicolon = True
                string = string[:-1]
        result = print_lua_table(convert_to_python_list(string))
        if fixlastsemicolon:
            return result[:-1] + "," + result[-1:]
        else:
            return result

    def gen_lua_code(self, csvfile, save_path):
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not csvfile:
            print_error("csv file is None")
            return
        self.file_name_no_extension, extension = os.path.splitext(os.path.basename(save_path))
        luafiles = []
        csvreader = csv.reader(csvfile)
        row_count = sum(1 for _ in csvreader)
        need_page = math.ceil((row_count - 3) / count_limit)
        csvfile.seek(0);
        next(csvfile)
        self.header = next(csvreader)
        self.types = next(csvreader)
        self.csvdictreader = csv.DictReader(csvfile, fieldnames=self.header)
        if need_page == 1:
            lua_content = "local " + self.file_name_no_extension + " = {\n"
            lua_content += self.write_lua_content(4)
            lua_content += "}\n"
            lua_content += "return " + self.file_name_no_extension

            lua_file_name = save_path
            with open(lua_file_name, 'w', encoding='utf-8') as lua_file:
                lua_file.write(lua_content)
            luafiles.append(lua_file_name)
        elif need_page > 1:
            self.create_lua_header(save_path, need_page)
            for page in range(1, need_page + 1):
                class_name = self.file_name_no_extension + str(page)
                lua_content = "local " + class_name + " = {\n"
                lua_content += self.write_lua_content((page - 1) * count_limit + 4)
                lua_content += "}\n"
                lua_content += "return " + self.file_name_no_extension + str(page)
                lua_file_name = os.path.join(directory, class_name)
                lua_file_name += '.lua'
                with open(lua_file_name, 'w', encoding='utf-8') as lua_file:
                    lua_file.write(lua_content)
                luafiles.append(lua_file_name)
        csvfile.close()
        return luafiles

#luaCodeGen = LuaCodeGen()
#luaCodeGen.gen_lua_code()
