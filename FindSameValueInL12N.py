import os
import csv

read_csv_path = os.path.abspath("../../Content/Config/LocalizationCommon.csv")
write_csv_path = os.path.abspath("../Tools/replaceExcel/LocalizationCommon.csv")
res_write_path = os.path.abspath("../Tools/replaceExcel/duplicateL12N.txt")

count = 0
write_rows = []
save_unique_rows = []
remove_rows = []
dict_res = []
is_write = False
is_deal_with_xlsx = False

save_xlsx_folder_path = os.path.abspath("../Tools/replaceExcel")
os.makedirs(save_xlsx_folder_path, exist_ok=True)

input_is_write = input("是否生成duplicateL12N.txt?  Y or N\n")
if isinstance(input_is_write, str):
    if input_is_write.upper() == 'Y':
        is_write = True
    else:
        is_write = False
else:
    is_write = False

input_is_deal_with_xlsx = input("是否要处理xlsx和生成LocalizationCommon.csv文件?  Y or N\n")
if isinstance(input_is_deal_with_xlsx, str):
    if input_is_deal_with_xlsx.upper() == 'Y':
        is_deal_with_xlsx = True
    else:
        is_deal_with_xlsx = False
else:
    is_deal_with_xlsx = False

with open(read_csv_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[1] == '':
            count = count + 1
        else:
            write_rows.append(row)

print("empty content CN count", count)

key_counts = {}

with open(read_csv_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        key = row['简体']
        if key != '':
            if key in key_counts:
                key_counts[key] += 1
                remove_rows.append(row)
            else:
                key_counts[key] = 1
                save_unique_rows.append(row)

duplicate_keys = [key for key, count in key_counts.items() if count > 1]


def find_value(target_key):
    for row in save_unique_rows:
        if target_key == row['简体']:
            return row


count = 0
for row in remove_rows:
    count = count + 1
    res_row = find_value(row['简体'])
    data = {"replace_key": res_row['key']}
    row.update(data)
    data = {"need_check": "false"}
    row.update(data)
    dict_res.append(row)

if is_write:
    with open(res_write_path, "w", encoding='utf-8') as writer:
        for data in dict_res:
            writer.write(str(data))
            writer.write("\n")

if is_deal_with_xlsx:
    res_data = []
    for key_value in save_unique_rows:
        data = []
        for value in key_value.values():
            data.append(value)
        res_data.append(data)
    with open(write_csv_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(res_data)

print("need remove count:", count)
if is_write:
    print("export txt path:", res_write_path)
    print("done")
if is_deal_with_xlsx:
    print("export L12NCommon.csv path:", write_csv_path)
    print("LocalizationCommon.csv记得第一行加上key，手动添加，例如：key,简体，繁体...")
    print("start import")
    import ReplaceDuplicateKeyInL12NCommon
if not is_write and not is_deal_with_xlsx:
    print("done")
