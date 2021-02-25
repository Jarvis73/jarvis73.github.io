---
layout: post
title: "数据增广 (Data Augmentation)"
date: 2021-01-02 19:51:00 +0800
categories: 深度学习
mathjax: true
# figure: /images/2020-12/WGAN-4.png
author: Jarvis
meta: Wiki_Deep Learning
---

* content
{:toc}



本文讨论深度学习中的数据增广(也叫数据增强, data augmentation)技术. 深度学习因其用于高效的用于特征提取的分层结构和大规模的数据集, 在计算机视觉领域大放异彩. 然而, 由于大规模模型的参数量达到了数千万到数十亿的级别, 并且数据集标签的搜集成本较高, 因此充分地使用数据增广和正则化技术是避免模型过拟合的有效途径. 本文主要讨论传统的数据增广技术和近几年新流行的技术.

首先导入所需要的库, 并读取一张图像:

<ul class="nav nav-tabs">
  <li class="active"><a data-tab href="#tabContent0-1">PyTorch</a></li>
  <li><a data-tab href="#tabContent0-2">Tensorflow</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane active" id="tabContent0-1" markdown="block">
```python
import torch
import torchvision
from PIL import Image

image = Image.open("example.png")
W, H, C = (*image.size, len(image.mode))
```
</div>
<div class="tab-pane" id="tabContent0-2" markdown="block">
```python
import tensorflow as tf
import tensorflow_addons as tfa

raw_data = tf.io.read_file("example.png")
image = tf.io.decode_png(raw_data)
H, W, C = image.shape
```
</div>
</div>

## 1. 传统数据增广技术

### 1.1 平移 (translating)

* **参数** $$ (a, b): -aW \leq x_t < aW, -bH \leq y_t < bH $$ 平移的距离和最大范围

<ul class="nav nav-tabs">
  <li class="active"><a data-tab href="#tabContent1-1">PyTorch</a></li>
  <li><a data-tab href="#tabContent1-2">Tensorflow</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane active" id="tabContent1-1" markdown="block">
```python
# image: PIL.Image [W, H, C] / torch.Tensor [C, H, W]
trans = transforms.Compose([torchvision.transforms.RandomAffine(translate=(a, b))])
image2 = trans(image)
```
</div>
<div class="tab-pane" id="tabContent1-2" markdown="block">
```python
# image: tf.Tensor, [H, W, C]
shifts = (tf.random.uniform([2]) - 0.5) * [2 * a * W, 2 * b * H]
image2 = tfa.image.translate(image, shifts)
```
</div>
</div>


### 1.2 翻转 (flipping)

* **参数** $$ p: $$ 翻转的概率

<ul class="nav nav-tabs">
  <li class="active"><a data-tab href="#tabContent2-1">PyTorch</a></li>
  <li><a data-tab href="#tabContent2-2">Tensorflow</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane active" id="tabContent2-1" markdown="block">
```python
# image: PIL.Image [W, H, C] / torch.Tensor [C, H, W]
trans = transforms.Compose([torchvision.transforms.RandomHorizontalFlip(p=p)])
image2 = trans(image)
```
</div>
<div class="tab-pane" id="tabContent2-2" markdown="block">
```python
# image: tf.Tensor, [H, W, C]
image2 = tf.image.random_flip_left_right(image)

```
</div>
</div>


### 1.3 缩放 (scaling)

* **参数** $$ (a, b): a \leq s \leq b $$ 缩放的尺度范围

<ul class="nav nav-tabs">
  <li class="active"><a data-tab href="#tabContent3-1">PyTorch</a></li>
  <li><a data-tab href="#tabContent3-2">Tensorflow</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane active" id="tabContent3-1" markdown="block">
```python
# image: PIL.Image [W, H, C] / torch.Tensor [C, H, W]
trans = transforms.Compose([
    torchvision.transforms.RandomAffine(scale=(a, b), resample=Image.NEAREST)])
image2 = trans(image)
```
</div>
<div class="tab-pane" id="tabContent3-2" markdown="block">
```python
# image: tf.Tensor, [H, W, C]
size = tf.cast(tf.random.uniform((), a, b) * [H, W], tf.int32)
image2 = tf.image.resize(
    image, size=size, method='nearest')
```
</div>
</div>


### 1.4 裁剪 (cropping)

* **参数** $$ (h, w): $$ 裁剪的大小

<ul class="nav nav-tabs">
  <li class="active"><a data-tab href="#tabContent4-1">PyTorch</a></li>
  <li><a data-tab href="#tabContent4-2">Tensorflow</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane active" id="tabContent4-1" markdown="block">
```python
# image: PIL.Image [W, H, C] / torch.Tensor [C, H, W]
trans = transforms.Compose([torchvision.transforms.RandomCrop(size=(h, w))])
image2 = trans(image)
```
</div>
<div class="tab-pane" id="tabContent4-2" markdown="block">
```python
# image: tf.Tensor, [H, W, C]
image2 = tf.image.random_crop(image, size=(h, w, C))

```
</div>
</div>

### 1.5 旋转 (rotating)

* **参数** $$ \theta: -d \leq \theta \leq d $$ 随机旋转的范围

<ul class="nav nav-tabs">
  <li class="active"><a data-tab href="#tabContent5-1">PyTorch</a></li>
  <li><a data-tab href="#tabContent5-2">Tensorflow</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane active" id="tabContent5-1" markdown="block">
```python
# image: PIL.Image [W, H, C] / torch.Tensor [C, H, W]
trans = transforms.Compose([torchvision.transforms.RandomRotation(degree=d)])
image2 = trans(image)
```
</div>
<div class="tab-pane" id="tabContent5-2" markdown="block">
```python
# image: tf.Tensor, [H, W, C]
degree = tf.random.uniform((), -d, d)
image2 = tfa.image.rotate(image, degree)
```
</div>
</div>


### 1.6 颜色扰动 (color jitter)

* **参数** $$ a: -a \leq \alpha \leq a $$ 随机亮度的变化范围
* **参数** $$ b: -b \leq \beta \leq b $$ 随机对比度的变化范围
* **参数** $$ c: -c \leq \gamma \leq c $$ 随机饱和度的变化范围

<ul class="nav nav-tabs">
  <li class="active"><a data-tab href="#tabContent6-1">PyTorch</a></li>
  <li><a data-tab href="#tabContent6-2">Tensorflow</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane active" id="tabContent6-1" markdown="block">
```python
# image: PIL.Image [W, H, C] / torch.Tensor [C, H, W]
trans = transforms.Compose([
    torchvision.transforms.ColorJitter(
        brightness=(a1, b1), contrast=(a2, b2), saturation=(a3, b3))])
image2 = trans(image)
```
</div>
<div class="tab-pane" id="tabContent6-2" markdown="block">
```python
# image: tf.Tensor, [H, W, C]
image2 = tf.image.random_brightness(image, a)
image3 = tf.image.random_contrast(image2, -b, b)
image4 = tf.image.random_saturation(image3, -c, c)

```
</div>
</div>

{% include card.html type="warning" content="PyTorch 和 Tensorflow 对 ColorJitter 的内部实现方式是不同的." %}


## 2. 其他数据增广技术

