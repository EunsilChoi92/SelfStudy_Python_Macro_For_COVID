a = []

for i in range(1, 31):
    str_num = ""
    if i < 10:
        str_num = "0" + str(i)
    else:
        str_num = str(i)
    a.append(str_num)

print(a)