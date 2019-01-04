---
layout: post
title: "DeepLab: Segmentation Network"
data: 2019-1-2 21:04:00
categories: 深度学习
mathjax: true
figure: /images/2019-1/DeepLabv2-1.jpg
author: Jarvis
meta: Post
---

* content
{:toc}



## 1. ICLR 2015: Semantic Image Segmentation with Deep Convolutional Nets and Fully Connected CRFs

**作者**: Liang-Chieh Chen(UCLA), George Papandreou(Google Inc.), Iasonas Kokkinos(CentraleSuplec and INRIA), Kevin Murphy(Google Inc.), Alan L. Yuille(UCLA)

`DeepLab V1` 贡献:
* 速度: 引入空洞卷积(`atrous` 卷积)提高处理速度(8fps)
* 准确度: PASCAL VOC-2012 分割任务上取得 start-or-the-art (test set: 71.6%), 超过第二名7.2%
* 简单性: 仅包含 (1) DCNN (2) CRFs 两个步骤

### Atrous/Hole Convolution

在 VGG-16 模型中原始图像共下采样 5 次, 缩小为输入图像的 $1/32$. 本文目标是语义分割, 而缩小 32 倍的图像无法准确的定位分割的各部分, 而直接减少 VGG-16 的两个 block 又会影响特征的提取, 因此引入空洞卷积既能增大感受野, 也能减少下采样的次数. 一维的空洞卷积如下图所示.

<div class="polaroid">
    <img class="cool-img" src="/images/2019-1/DeepLabv1-1.jpg" DeepLabv1/>
    <div class="container">
        <p>Atrous Convolution</p>
    </div>
</div>

其卷积方式就是在卷积核中引入"空洞", 使得不增加卷积核参数的情况下能够扩大卷积核的感受野, 用公式表示为(二维情况)

$$
y(i, j) = \sum_{m = 1}^M\sum_{n = 1}^Nx(i + dm, j + dn)w(m, n),
$$

其中 $M, N$ 是卷积核两个维度上的长度, $d > 1$ 时为空洞卷积, $d = 1$ 时为普通卷积.

代码实现中 VGG-16 最后两个 MaxPooling 层步长改为 1, 最后三个卷积层改为 $2\times$ 空洞卷积, 第一个全连接层改为 $4\times$ 空洞卷积, 使用 $4\times4$ 的卷积核(在精度略微损失(损失了0.5)的前提下相比原来 $7\times7$ 的卷积核速度翻倍).

### CRFs 恢复边界细节

在分类精度和定位精度上有一个自然的 trade-off, 网络越深, 下采样的次数越多, 分类的精度就越高, 同时损失的位置信息也越多. 目前文献中针对该问题有三类主流的方法:
1. 利用多个网络层的信息
2. 采用超像素表示
3. 全连接 CRFs<sup>2</sup> (这也是本文使用的方法)

### 实验结果

最终实验中最好的配置 `DeepLab-CRF-LargeFOV` (val set: mIOU = 67.64%)为 $3\times3$ 的卷积核, $12\times$ 的空洞卷积, 参数量最少, 精度与 $7\times7$ 的卷积核相同, 速度接近前者的 3.5 倍. 此外本文实验中还引入了 multi-scale 的策略(FCN 的做法, 把多个层次的特征图上采样后), 也提升了一定的精度(`DeepLab-MSc-CRF-LargeFOV` val set: mIOU=68.70%).


## 2. TPAMI 2017: DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs

**作者**: Liang-Chieh Chen, George Papandreou, Iasonas Kokkinos, Kevin Murphy, Alan L. Yuille

`DeepLab V2` 主要贡献:
* 提出膨胀空间金字塔池化(atrous spatial pyramid pooling, ASPP)

### 多尺度图像表示

多尺度是目前针对同时有大目标和小目标物体的一种比较流行的策略.

本文试验了两种利用多尺度图像特征的方法:
1. 相当于标准的多尺度处理
2. 提出了 ASPP 结构

**标准的多尺度处理**: 并行输入多个尺度的图像(经过缩放的), 并行的 DCNN 之间共享参数. 为了产生最终的结果, 多个尺度的输出经过双线性插值为原始图像的大小, 然后进行融合, 融合的方式选择 `max()` 函数.

**ASPP**: 结构如下图所示, 使用不同的膨胀率使得网络提取到不同尺度的信息.

<div class="polaroid">
    <img class="cool-img" src="/images/2019-1/DeepLabv2-2.jpg" DeepLabv2/>
    <div class="container">
        <p>Atrous Spatial Pyramid Pooling</p>
    </div>
</div>

使用了 ASPP 结构的 DeepLab 网络称为 `DeepLab-ASPP`, 其中 ASPP 结构增加在了最后一个池化层(已修改步长为 1)之后, 如图所示.

<div class="polaroid">
    <img class="cool-img" src="/images/2019-1/DeepLabv2-3.jpg" DeepLabv2/>
    <div class="container">
        <p>DeepLab-ASPP</p>
    </div>
</div>

### 实验结果

仍然在最后增加 CRFs 修整边界, 以 Resnet-101 作为主干网络, `DeepLab-ASPP-CRFs` 达到了 mIOU=79.7% 的精度.



## Reference

1. [Semantic Image Segmentation with Deep Convolutional Nets and Fully Connected CRFs](https://arxiv.org/abs/1412.7062)
2. [Efficient Inference in Fully Connected CRFs with Gaussian Edge Potentials](https://arxiv.org/abs/1210.5644)
3. [DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs](https://arxiv.org/abs/1606.00915)
