import os
import sys
import getopt
import re

try:
    import chardet
except:
    import os
    os.system("pip install chardet")
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
    # 替换掉python或其他代码块中‘#’开头的注释
    md = re.sub("```.*?```", "", md, flags=re.S)
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
    if len(level_list) > 0:
        level_list_new = []
        top = level_list[0]
        temp_list = [top]
        for x in level_list[1:] :
            if x > top :
                temp_list.append(x)
            else :
                top = x
                level_list_new.append(temp_list)
                temp_list = [top]
        level_list_new.append(temp_list)

        result_list = []
        index = 0
        for temp_list in level_list_new :
            top = temp_list[0]
            last_tab_count = -1
            for x in temp_list :
                tab_count = x - top
                if tab_count - last_tab_count > 1:
                    tab_count = last_tab_count + 1
                last_tab_count = tab_count
                tabs = "\t" * tab_count
                result = tabs + "- [" + name_list[index] + "](#" + name_list[index] + ")"
                result_list.append(result)
                index += 1
    return '\n\n'.join(result_list) + '\n\n'

# 将新的markdown文件写入到原来的markdown文件
def write_to_file(result, file,):
    md = read_md(file)
    encoding = get_encoding(file)
    md_new = open(file, 'w', encoding=encoding)
    md_new.write(result + md)
    md_new.close()

# 解析参数
def get_args(argv):
    files = []
    replace = False
    try :
        # h表示帮助，f表示要转换的文件，r表示是否替换原文件
        opts, args = getopt.getopt(argv, "hf:r:", ["help", "file=", "replace="])
    except getopt.GetoptError :
        print("Error: main.py -f <file> -r <replace>")
        print("   or: main.py --file=<file> -replace=<replace>")
        sys.exit()

    for opt, arg in opts :
        if opt in ("-h", "--help") :
            print("main.py -f <file> -r <replace>")
            print("or: main.py --file=<file> -replace=<replace>")
            sys.exit()
        elif opt in ("-f", "--file") :
            arg = re.sub("\s", "", arg)
            files = re.split("[,，]", arg)
        elif opt in ("-r", "--replace") :
            if arg == "True":
                replace = True

    return files, replace


if __name__ == "__main__":
    argv = sys.argv[1:]
    files, replace = get_args(argv)
    for file in files:
        if os.path.exists(file) :
            md = read_md(file)
            level_list, name_list = get_level_name(md)
            if len(name_list) > 0 :
                result= get_result(level_list, name_list)
                if replace :
                    write_to_file(result, file)
                print(file, '\n\n', result)
            else :
                print(file, '\n\n', "No Title")
        else :
            print("Error: %s is not exist" % file)