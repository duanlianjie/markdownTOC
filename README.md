- [markdownTOC](#markdownTOC)

	- [环境](#环境)

	- [运行](#运行)

	- [特殊情况考虑](#特殊情况考虑)

# markdownTOC

python脚本，用于生成markdown文件的TableOfContent，解决Github Flavored Markdown不支持[TOC]显示的问题

## 环境

```
python 3.6
chardet 3.0.4
```

## 运行

打开脚本所在目录的命令行，运行以下命令即可

```
# get help
python main.py -h
python main.py --help
# run the script
python main.py -f markdown.md[[,m1.md,m2.md,...] -r True]
python main.py -file=markdown.md[[,m1.md,m2.md,...] -replace=True]
```


- 多个文件时用,分割

- 默认生成新的markdown不覆盖原文件，添加参数replace=True将覆盖原文件

## 特殊情况考虑

- python代码中的注释避免当做标题处理

    - 通过正则表达式把代码块` ```xxx``` `都删除

- 标题级别大小乱序
    
    - 把标题分成多个部分来处理，每个部分具有这样的特征：第一个级别最高，后面的都能被递归拆成这样的部分。
        
        - 例如`[4,5,6,1,2,3,3,3,4,2]->[[4,5,6],[1,2,3,3,3,4,2]]`
    
    - 标题级别跳级的，将把跳级的标题看做上一个标题的下一级别。
        
        - 例如`[1,2,3,3,2,3,3,'5',4,4]`，为了能显示出来，将把5看做4
    
- 标题和`#`之间没有空格

    - 可以修剪
    
- 标题相同

    - 一样生成相同的锚点
       
- 标题是空白字符

    - 抛弃
    
- markdown文件没有任何标题
    
    - 不生成锚点

- 编码问题
    
    - 使用chardet检测编码，装包命令已经写在脚本中
    