import random

rank5_file_path = 'D:\\rank5.txt'
num_iter = 24025
random_dict = {}
history_dict = {}
digit_count = {str(i): [0] * 5 for i in range(10)}

with open(rank5_file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        string = line.replace(" ", "").rstrip("\n")
        # print(string)
        if string in history_dict:
            history_dict[string] += 1
        else:
            history_dict[string] = 1
        for index, digit_char in enumerate(string):
            digit = int(digit_char)
            digit_count[str(digit)][index] += 1

for _ in range(num_iter):
    random_num = random.randint(0, 99999)
    random_num = str(random_num).zfill(5)
    if random_num in random_dict:
        random_dict[random_num] += 1
    else:
        random_dict[random_num] = 1

for key, value in history_dict.items():
    if value > 1:
        print(f"Key: {key}, Value: {value}")

'''
for digit, counts in digit_count.items():
    print(f"数字 {digit}: {counts}")
'''
