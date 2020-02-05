import chardet

# 获取file的编码
def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']

# 读取file
def read_md(file):
    encoding = get_encoding(file)
    f = open(file, encoding=encoding)
    md = f.read()
    return md

# 从读取的markdown获取标题级别列表level_list和标题名字列表name_list
def get_level_name(md):
    md_list = md.split('\n')
    title_list = [string for string in md_list if string.startswith('#')]

    level_list = []
    name_list = []
    for string in title_list:
        level = string.count('#')
        name = string.strip('#').strip()
        if name != '':
            level_list.append(level)
            name_list.append(name)
    return level_list, name_list

# 从level_list和name_list获取标题的锚点列表result_list
def get_result(level_list, name_list):
    # 把level_list分割为递增的几部分，用'#'做分割标记
    # 例如[1, 2, 3, 4, 4, 4, 3, 3, 2, 4, 5] -> [1, 2, 3, 4, 4, 4, '#', 3, 3, '#', 2, 4, 5]
    temp = level_list[0]
    i = 0
    for x in level_list[1:]:
        if x < temp:
            i = i + 1
            level_list.insert(i, '#')
        temp = x
        i = i + 1
    # 根据level_list获取每个标题的锚点result_list
    result_list = []
    name_index = 0
    tab = 0 # 制表符的数目
    for i, x in enumerate(level_list):
        if x != '#':
            tab_string = "\t" * tab
            result = tab_string + "- [" + name_list[name_index] + "](#" + name_list[name_index] + ")"
            result_list.append(result)
            if i + 1 != len(level_list) and level_list[i] != level_list[i + 1]:
                tab = tab + 1
            name_index = name_index + 1
        else:
            tab = 0
            continue
    return result_list

# 将新的markdown文件写入到原来的markdown文件
def write_to_file(result_list, file):
    result = '\n\n'.join(result_list) + '\n\n'
    md = read_md(file)

    encoding = get_encoding(file)
    md_new = open(file, 'w', encoding=encoding)
    md_new.write(result + md)
    md_new.close()
    return result


if __name__ == "__main__":
    import sys
    file = sys.argv[1]

    md = read_md(file)
    level_list, name_list = get_level_name(md)
    result_list = get_result(level_list, name_list)
    result =  write_to_file(result_list, file)
    print(result)