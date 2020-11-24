---
layout: post
title: "Python 相关配置"
date: 2020-11-24 16:33:00 +0800
categories: Config
figure: /images/2020-11/python.png
author: Jarvis
meta: Post
---

* content
{:toc}




{% include card.html type="info" content="本文仅考虑 Python3." %}

## 1. 配置国内镜像

### 1.1 pip 清华镜像

(pypi 镜像每 5 分钟同步一次)

#### 临时使用

```bash
# 清华源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple <some-package>
# 阿里云源
pip install -i https://mirrors.aliyun.com/pypi/simple/ <some-package>
```

#### 设为默认

```bash
# 升级 pip 到最新的版本 (>=10.0.0) 后进行配置
pip install pip -U
# 清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 阿里云源
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```


### 1.2 Conda 清华镜像

参考链接 [https://mirror.tuna.tsinghua.edu.cn/help/anaconda/](https://mirror.tuna.tsinghua.edu.cn/help/anaconda/)

#### 临时使用

```bash
conda install -c https://mirrors.tuna.tsinghua.edu.cn/anaconda <package_name>
```

#### 设为默认

Linux / Windows 系统: 在 `~/.condarc` 中填入源. 可以从下面选择北外源或者清华源.


* 北外源

```
channels:
  - defaults
show_channel_urls: true
channel_alias: https://mirrors.bfsu.edu.cn/anaconda
default_channels:
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/main
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/free
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/r
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/pro
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.bfsu.edu.cn/anaconda/cloud
  msys2: https://mirrors.bfsu.edu.cn/anaconda/cloud
  bioconda: https://mirrors.bfsu.edu.cn/anaconda/cloud
  menpo: https://mirrors.bfsu.edu.cn/anaconda/cloud
  pytorch: https://mirrors.bfsu.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.bfsu.edu.cn/anaconda/cloud
```

* 清华源

```
channels:
  - defaults
show_channel_urls: true
channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

## 2. 创建虚拟环境

### 2.1 conda

首推的虚拟环境管理工具. 使用 conda 来安装包(而非 pip). <br />查找库的链接: [https://anaconda.org/](https://anaconda.org/)<br />
<br />注意 conda 源的python包和pip源的python包是不通用的, 有事可以混合安装, 但容易出现依赖错误.<br />(有时候涉及到一些C++库如cuda的时候, 或者一些只在pip中存在的库需要同时用两种工具安装包的时候, 可能会出现各种奇怪的依赖错误导致环境创建失败.)

```bash
# 创建 conda 环境
conda create -n OpenCV-4.2.0-py3

# 激活 conda 环境
# For linux
source activate OpenCV-4.2.0-py3
# For windows
activate OpenCV-4.2.0-py3

# 在虚拟环境中安装 python 包
conda install numpy
# 虚拟环境中尽量不使用pip, 除非万不得已. pip和conda安装的包的兼容性很差.
pip install numpy

# 退出虚拟环境
# For linux
source deactivate
# For windows
deactivate
```

### 2.2 virtualenv
conda 安装环境不成功的第二选择. 

virtualenv也是个python的第三方库, 用于管理虚拟环境, 但仍然使用pip来安装包.

```bash
# 需要先在默认环境中安装该库
pip install virtualenv

# 创建一个独立的 python 环境. 这样就在当前目录下创建了一个venv文件夹, 其中包含了一个最小的python
virtualenv venv

# 也可以指定 python 版本
virtualenv venv -p python3.6

# 激活环境
source venv/bin/activate
```


### 2.3 venv

{% include card.html type="info" content="貌似不能指定 python版本, 所以暂不推荐, 这里只做记录" %}

以编译OpenCV为例, 创建一个 Python 虚拟环境:

```bash
# 创建虚拟环境所在的文件夹
mkdir ~/venv; cd ~/venv

# 创建名为 OpenCV-4.2.0-py3 的虚拟环境
python3 -m venv OpenCV-4.2.0-py3

# 以下可选, 为激活虚拟环境创建短命令
# echo "# Virtual Environment Wrapper" >> ~/.bashrc
# echo "alias workoncv-$cvVersion=\"source $cwd/OpenCV-$cvVersion-py3/bin/activate\"" >> ~/.bashrc
# 或者直接激活
source ~/venv/OpenCV-4.2.0-py3/bin/activate

# 在虚拟环境中安装python包
pip install numpy matplotlib

# 退出虚拟环境
deactivate
```

## 3. 环境的导出和安装

### 3.1 pip

```bash
# 导出库到文件
pip freeze > requirements.txt

# 从文件中安装库
pip install -r requirements.txt
```

### 3.2 conda

```bash
# 导出库到文件
conda list -e > requirements.txt

# 从文件中安装库
conda install --file requirements.txt
```
上面的安装方法仅限于常规安装. 有一些第三方channel和pip安装的库无法用此法安装, 只能导出. 为此, 我们可以选择导出整个环境.

```bash
# 导出环境到文件
conda env export > env.yml

# 从文件创建环境
conda env create -f env.yml
```


## 3. Python 基本库
### 3.1 文档

- [Python3-cookbook](https://python3-cookbook.readthedocs.io/zh_CN/latest/index.html) 中文译本



## 4. Python 第三方库

<div class="table-responsive">
<table class="table-striped table-hover table-auto">
  <thead>
      <tr>
        <td>名称</td>
        <td style="min-width: 250px">安装方式</td>
        <td>功能</td>
      </tr>
    </thead>
    <tbody>
    <tr>
        <td>tqdm</td>
        <td>conda install tqdm<br/>pip install tqdm</td>
        <td>提供进度条</td>
    </tr>
    <tr>
        <td>numpy</td>
        <td>conda install numpy<br/>pip install numpy</td>
        <td>提供多维数组的计算, 底层用C语言实现, 保证了效率. 是大量科学计算库的依赖库.</td>
    </tr>
    <tr>
        <td>matplotlib</td>
        <td>conda install matplotlib<br/>pip install matplotlib</td>
        <td>提供二维和三维的绘图功能</td>
    </tr>
    <tr>
        <td>scipy</td>
        <td>conda install scipy<br/>pip install scipy</td>
        <td>提供基于numpy的科学计算/数值计算功能<br/>提供scipy.ndimage进行高维图像/张量处理</td>
    </tr>
    <tr>
        <td>pandas</td>
        <td>conda install pandas<br/>pip install pandas</td>
        <td>结构化数据处理库, 基于Series和DataFrame两个数据结构进行数据处理. 适用于多类型结构化的数据, 可以与Excel的操作模式进行类比.</td>
    </tr>
    <tr>
        <td>opencv</td>
        <td>conda install opencv</td>
        <td>OpenCV C++ 的 Python 包装</td>
    </tr>
    <tr>
        <td>skimage</td>
        <td>conda install scikit-image</td>
        <td>用于图像处理的库, 部分功使用的是scipy.ndimage</td>
    </tr>
    <tr>
        <td>tensorflow</td>
        <td>pip install tensorflow<br/>pip install tensorflow-gpu</td>
        <td>一个基于静态图/动态图的用于机器学习/深度学习的分布式框架, Python包装, 依赖于 cudatoolkit和cudnn</td>
    </tr>
    <tr>
        <td>pytorch</td>
        <td>见官网</td>
        <td>一个基于动态图的用于机器学习/深度学习的框架, 依赖于 cudatoolkit 和 cudnn</td>
    </tr>
    <tr>
        <td>cudatoolkit</td>
        <td>conda install cudatoolkit</td>
        <td>cuda 工具箱, 配合tensorflow/pytorch使用</td>
    </tr>
    <tr>
        <td>cudnn</td>
        <td>conda install cudnn</td>
        <td>cudnn 工具箱, 配合tensorflow/pytorch使用, 依赖于 cudatoolkit</td>
    </tr>
    <tr>
        <td><a target="_blank" href="https://sacred.readthedocs.io/en/stable/index.html">Sacred</a></td>
        <td>pip install sacred</td>
        <td>实验工具, 用于配置, 组织, 记录和保证实验的可复现性. 鼓励实验的模块化和可配置性. 大量使用装饰器实现基本功能.</td>
    </tr>
    <tr>
        <td>nibabel</td>
        <td>pip install nibabel</td>
        <td>用于简单的医学图像读写</td>
    </tr>
    <tr>
        <td>simpleitk</td>
        <td>conda install simpleitk -c simpleitk</td>
        <td>强大的医学图像处理库, ITK C++ 的 Python 包装.</td>
    </tr>
    </tbody>
</table>
</div>



## 5. Python 编辑器/IDE

### 5.1 VSCode

链接: [https://code.visualstudio.com/](https://code.visualstudio.com/)

介绍: 微软推出的多语言编辑器, 当然也支持 Python, 相比于大型 IDE, VSCode 是轻量级工具(但插件装多了也会变慢). 

使用: 安装 VSCode, 从 VSCode 的插件市场安装 `Python` 插件

{% include card.html type="warning" content="避免使用默认的 python 语言解析服务器, 因为每次打开 VSCode 都要下载, 非常慢. 可以从插件市场安装微软提供的替代品 `Pylance` 插件." %}

### 5.2 PyCharm

链接: [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/)

介绍: 功能强大的 Python IDE, 支持功能完善的智能感知, 并自动生成缺失的 API 接口文档. 支持远程ssh连接, 远程同步文件, 远程运行程序. 教育优惠可以免费试用专业版.

