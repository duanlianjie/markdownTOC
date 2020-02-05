- [markdownTOC](#markdownTOC)

	- [运行](#运行)

	- [特别情况考虑](#特别情况考虑)

# markdownTOC

python脚本，用于生成markdown文件的TableOfContent，解决Github Flavored Markdown不支持[TOC]显示的问题

## 运行

打开脚本所在目录的命令行，运行以下命令即可，生成新的markdown将覆盖原文件

`python main.py markdown.md [...]`

> **markdown.md替换为要生成TOC的markdown文件路径，后面可跟多个文件同时生成**

## 特别情况考虑

- 标题级别大小乱序

    - 把标题分出多个递增部分来处理

- 标题和`#`之间没有空格

    - 可以修剪
    
- 标题相同

    - 一样生成相同的锚点
       
- 标题是空白字符

    - 抛弃
    
- 没有任何标题
    
    - 不生成锚点

- 编码问题
    
    - 使用chardet检测编码，装包命令已经写在脚本中
    