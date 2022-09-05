---
layout: post
title: "Ubuntu 安装 NVIDIA 驱动和 CUDA"
date: 2022-09-04 14:56:00 +0800
categories: Config
author: Jarvis
meta: Wiki_Ubuntu
hidden: true
---

* content
{:toc}

记录一下 Ubuntu Server 配置 Nvidia 驱动.



## 安装 NVIDIA 驱动

```bash
# 惯例, 更新源
sudo apt update

# 安装 `ubuntu-drivers`
sudo apt install ubuntu-drivers-common

# 查看设备 (⌐■_■)
ubuntu-drivers devices

# Outputs:
# ......
# driver   : nvidia-driver-515-server - distro non-free
# driver   : nvidia-driver-515 - distro non-free recommended
# ......

# 找到包含 recommended 的那行, 就是目前最新版的驱动
# 安装驱动, 我们选择安装 server 版
sudo apt install nvidia-driver-515-server

```

安装完成后执行 `nvidia-smi` 会显示

```
NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver. Make sure that the latest NVIDIA driver is installed and running.
```

只要重启一下服务器就好啦.

## 安装 CUDA

注意这里是指在系统目录中安装 CUDA 做公共使用, 通常安装于 `/usr/lib/cuda`. 当我们使用 Conda 环境的的时候, 可以选择在虚拟环境中安装额外的 cudatoolkit, 这样 python 环境可以不适用系统目录的 CUDA 而使用虚拟环境中的.

首先在 [https://developer.nvidia.com/cuda-toolkit-archive](https://developer.nvidia.com/cuda-toolkit-archive) 查找需要的 CUDA 版本, 然后用以下命令安装 (注意替换为自己选择版本的链接).

```bash
wget https://developer.download.nvidia.com/compute/cuda/11.4.0/local_installers/cuda_11.4.0_470.42.01_linux.run
sudo sh cuda_11.4.0_470.42.01_linux.run
```


