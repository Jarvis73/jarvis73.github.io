---
layout: post
title: Tensorflow 数据集 (Tensorflow Datasets)
date: 2020-11-25 10:57:00 +0800
categories: Tensorflow
figure: /images/2020-11/tensorflow-datasets.jpg
author: Jarvis
meta: Post
---

* content
{:toc}




Tensorflow 提供了一个 `tensorflow-datasets` 的 Python 库来方便地下载、加载和管理数据集. 

{% include card.html type="info" content="由于在中国大陆范围内谷歌服务不可用, 该 API 在中国大陆需要使用代理来下载数据集." %}

## 1. 安装

```bash
pip install tensorflow-datasets
```

### 1.1 配置代理

- 选择任意的代理服务, 假设已经配置了 socks5 代理
- 安装 privoxy 之类的工具, 用于把 socks5 转换为 http, https 和 ftp.
- 运行任意涉及 `tensorflow_datasets` 中 `builder.download_and_prepare()` 语句的脚本时, 增加如下的环境变量:

```bash
export TFDS_HTTP_PROXY=http://127.0.0.1:8118
export TFDS_HTTPS_PROXY=http://127.0.0.1:8118
export TFDS_FTP_PROXY=http://127.0.0.1:8118
```

注意以上三个都要添加. 如果是希望仅对当前命令有效, 则可以直接添加到命令开头:

```bash
TFDS_HTTP_PROXY=http://127.0.0.1:8118 TFDS_HTTPS_PROXY=http://127.0.0.1:8118 TFDS_FTP_PROXY=http://127.0.0.1:8118 python demo.py
```

