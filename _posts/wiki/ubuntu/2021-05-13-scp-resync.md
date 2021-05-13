---
layout: post
title: scp/rsync 命令
date: 2021-05-13 14:37:00 +0800
author: Jarvis
meta: Wiki_Ubuntu
hidden: true
---

* content
{:toc}




## 1. 简介

`scp` 是基于 ssh 协议的远程复制命令; `rsync` 是远程同步命令, 可选择基于 ssh 协议.

* `scp` 既可以在本地和远程之间复制, 也可以在远程和远程之间复制; `rsync` 只能在本地和远程之间复制.

* `rsync` 的一个非常好用的地方是支持断点续传, 这在传输大文件(图像数据集)的时候十分有用.

## 2. `scp` 基本用法

```bash
# 本地文件复制到远程
scp {{path/to/local_file}} {{remote_host}}:{{path/to/remote_file}}

# 指定远程端口
scp -P {{port}} {{path/to/local_file}} {{remote_host}}:{{path/to/remote_file}}

# 远程文件复制到本地
scp {{remote_host}}:{{path/to/remote_file}} {{path/to/local_directory}}

# 远程文件夹复制到本地
scp -r {{remote_host}}:{{path/to/remote_directory}} {{path/to/local_directory}}

# 以本地为桥梁, 在两个远程之间复制文件
scp -3 {{host1}}:{{path/to/remote_file}} {{host2}}:{{path/to/remote_directory}}
```

scp 也支持 ssh 的 config 文件中的 host, 以及 -i 参数.

## 3. `rsync` 基本用法

```bash
# 本地文件复制到远程
rsync {{path/to/local_file}} {{remote_host}}:{{path/to/remote_directory}}

# 远程文件复制到本地
rsync {{remote_host}}:{{path/to/remote_file}} {{path/to/local_directory}}

# 复制文件, 以归档(a) (保护属性) 和压缩(z) 模式, 输出信息(v) 和 人类可读(h)的进度条(P):
rsync -azvhP {{path/to/local_file}} {{remote_host}}:{{path/to/remote_directory}}

# 远程文件夹复制到本地
rsync -r {{remote_host}}:{{path/to/remote_directory}} {{path/to/local_directory}}

# 远程文件夹的内容(不包括文件夹本身)复制到本地
rsync -r {{remote_host}}:{{path/to/remote_directory}}/ {{path/to/local_directory}}

# 识别软连接(l), 忽略已经复制的文件, 除非更新(u):
rsync -rauL {{remote_host}}:{{path/to/remote_file}} {{path/to/local_directory}}
```

## 4. 常用用法

* 相比于 `scp`, `rsync` 最大的优点是可以断点续传, 因此在传输大文件时应该优先选用 `rsync`.

```bash
# 通过 ssh 复制文件, 显示进度条
rsync -P --rsh=ssh {{path/to/local_file}} {{path/to/remote_directory}}
```
