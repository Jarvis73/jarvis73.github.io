---
layout: post
title: Jupyter Notebook转pdf的脚本
date: 2017-10-16 17:58 +0800
categories: Python
excerpt: 用python写的一个很简单的脚本, 把.ipynb文件转换为pdf文件
author: Jarvis
meta: Post
---

* content
{:toc}

+-+-+-+-

## 使用环境

1. Win10 64位系统 (在windows系统上进行了测试)
2. texlive2015 (这里主要需要的是xelatex工具, 保证电脑可以正常使用xelatex编译tex文档)
3. Anaconda (主要使用了jupyter的nbconvert工具)

## 脚本

### **主程序**:

```python
import sys
import os

def change(name):
    with open(name, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open(name, "w", encoding="utf-8") as f:
        for line in lines:
            if "Colors for the hyperref package" in line:
                line = "\t% ======================= Added by Jarvis =====================\n\t\\usepackage{framed}\n\t\\usepackage{color}\n\t\\definecolor{shadecolor}{rgb}{0.97,0.97,0.97}\n\t% ======================= Added by Jarvis =====================" + line
            if "\\begin{Verbatim}" in line:
                line = "\\begin{shaded}\n" + line
            elif "\\end{Verbatim}" in line:
                line = line + "\\end{shaded}"
            f.write(line)

def main():
    fname = sys.argv[1]
    
    # 把ipynb转为tex
    os.system("jupyter nbconvert --to latex \"{}\"".format(fname))
    name = fname[0:-6]
    os.system("echo Compailing tex to pdf......")
    
    # 为代码块添加背景
    change(name + '.tex')

    # 编译tex文件得到pdf
    os.system("xelatex.exe -synctex=1 -interaction=nonstopmode \"{}\".tex > nul".format(name))

    # 删除多余的中间文件
    os.remove("{}.tex".format(name))
    os.remove("{}.aux".format(name))
    os.remove("{}.log".format(name))
    os.remove("{}.out".format(name))
    os.remove("{}.synctex.gz".format(name))
    os.system("echo Finished!")
```

解释: main函数中首先使用`jupyter nbconvert --to latex xxx.ipynb`命令把`.ipynb`文件转化为`.tex`文件; 然后再调用`xelatex`对`latex`文件进行编译. 
change函数对`nbconvert`转换得到的`latex`中代码环境做了一点修改, 即给代码块添加了统一的背景, 更容易与文档内容区分. 最后把`latex`生成的多余文件删除(扫尾了).


### **安装程序 (便于使用)**

```python
from setuptools import setup

setup(
    name = 'nb2pdf',
    py_modules = ['nb2pdf'],
    entry_points = {
        'console_scripts':['nb2pdf=nb2pdf:main']
    }
)
```

简单的`python`模块安装程序, 就不解释了. 


## 使用方法

安装完毕后在待转换的notebook文档的目录下打开命令行, 执行命令`nb2pdf xxx.ipynb`后即可得到pdf文件. 注意: 文件名包含空格时要加双引号, 即`nb2pdf "xxx.ipynb"`. 
