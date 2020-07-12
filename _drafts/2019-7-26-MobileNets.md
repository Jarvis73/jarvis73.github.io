---
layout: post
title: "Inception & Xception: Going Faster and Lighter"
date: 2019-07-26 16:13:00 +0800
categories: 深度学习
mathjax: true
figure: ./images/2019-7/ception.png
author: Jarvis
meta: Post
---

* content
{:toc}



## Inception 系列

Inception结构(V1)来自于论文[^1] , 该论文提出的 GoogLeNet 是2014年ILSVRC目标分类任务的冠军, 同时GoogLeNet成为了后来诸多模型的准线. 

### 1. Inception V1

该论文指出对于深度模型, 增大模型是一个较为简单的提升精度的方法, 如增加层数, 增加神经元的数量. 但是随之而来的是 (1) 过拟合的问题, (2) 更加消耗计算资源和储存资源. 解决这两个问题的一种基础的想法就是把全连接层甚至卷积层中的神经元连接减少, 即使其**稀疏化**. 但我们不希望使用无规则的稀疏化, 因为这样会使得稀疏矩阵的操作和稠密连接所差无几(通常只有有规律的稀疏矩阵才有高效的算法, 如三对角矩阵). 

GoogLeNet中使用的Inception结构如下图所示.

{% include image.html class="polaroid" url="2019-7/inception.png" title="Inception module with dimensionality reduction" %}

核心操作是把普通的卷积层变成了四路计算, 包含 $$ 1\times1 $$ , $$ 3\times3 $$ 和 $$ 5\times5 $$ 的卷积和一个最大池化的操作. $$ 1\times1 $$ 卷积用于整合细粒度信息(小感受野), 而 $$ 3\times3 $$ 和 $$ 5\times5 $$ 卷积用于抓取偏语义的信息(大感受野). 而叠加额外的 $$ 1\times1 $$ 卷积的目的是压缩中间层的通道数, 从而可以减少模型参数. 文中提到这里使用 $$ 1\times1 $$ 卷积的目的恰好和 Network in Network文中的用法相反.

### 2. GoogLeNet

GoogLeNet 是该论文中单独设计的神经网络模型, 包含了 2-5-2 共 9 个 Inception 模块, 同时在训练过程中使用深度监督策略, 第 3 和第 5 个 Inception 模块的输出各接一个分类器, 这两个分类器以 0.3 的权重加入到总的损失函数中训练. 推断时这两个额外的分类器弃去不用. 模型结构如下图所示.

{% include image.html class="polaroid" url="2019-7/googlenet.png" title="GoogLeNet Architecture" %}

### 3. Inception V2

Inception V2 是在 Batch Normalization 论文[^2]中提出的, 其对于 V1 版本的改进也就是 BN 的加入.

## Xception




## MobileNets V1

MobileNets 致力于协调神经网络速度与精度, 在尽可能的保持精度或者损失较少精度的前提下大幅度减少资源消耗
* 乘加操作 Mult-Adds 的数量: CPU 资源
* 模型参数 Parameters 的数量: 内存资源

### 主要方法

MobileNets 对普通 CNNs 的改进方向包含三个部分:

1. 使用深度可分离卷积 (depthwise separable convolution) 代替普通卷积
2. 减少模型通道数的 $$ alpha $$ 参数: 论文中称为 width multiplier
3. 减小图像大小的 $$ \rho $$ 参数: 论文中称为 resolution multiplier 

普通卷积计算 Mult-Adds 的次数为

$$
D_K \cdot D_K \cdot M \cdot N \cdot D_F \cdot D_F
$$

其中 $$ D_K $$ 是卷积核的边长, $$ D_F $$ 是特征图的边长, $$ M $$ 和 $$ N $$ 分别为输入输出的通道数.

深度可分离卷积计算 Mult-Adds 的次数为

$$
D_K \cdot D_K \cdot M \cdot D_F \cdot D_F + M \cdot N \cdot D_F \cdot D_F
$$

MobileNets 使用了一个序列化的网络主干, 使用步长为2的卷积代替池化. 具体结构见论文.

### 实验

* Conv 和 Depthwise Conv 比较

| Model          | ImageNet Accuracy | Million Mult-Adds | Million Parameters |
|:--------------:|:-----------------:|:-----------------:|:------------------:|
| Conv MobileNet | 71.7%             | 4866              | 29.3               |
| MobileNet      | 70.6%             | 569               | 4.2                |

精度掉了 1.1%, 模型参数缩减了86%, 计算量缩减了88%.

* Narrow 和 Shallow 比较

| Model                   | ImageNet Accuracy | Million Mult-Adds | Million Parameters |
|:-----------------------:|:-----------------:|:-----------------:|:------------------:|
| $$ \alpha=0.75 $$ MobileNet | 68.4%             | 325               | 2.6                |
| Shallow MobileNet       | 65.3%             | 307               | 2.9                |

对比减少通道数和减少网络层数发现, 在几乎同样的参数量和计算量的情况下, 减少通道数是更好的选择. 这也符合我们的直观.

* Width Multiplier (通道数)比较和 Resolution Multiplier (分辨率)比较

| Networks   | ImageNet Accuracy | Million Mult-Adds | Million Parameters |
|:------------------:|:-----------------:|:-----------------:|:------------------:|
| 1.0 MobileNet-224  | 70.6%             | 569               | 4.2                |
| 0.75 MobileNet-224 | 68.4%             | 325               | 2.6                |
| 0.5 MobileNet-224  | 63.7%             | 149               | 1.3                |
| 0.25 MobileNet-224 | 50.6%             | 41                | 0.5                |
| 1.0 MobileNet-192 | 69..1%            | 418               | 4.2                |
| 1.0 MobileNet-160 | 67.2%             | 290               | 4.2                |
| 1.0 MobileNet-128 | 64.4%             | 186               | 4.2                |

* 与其他模型的比较

|     Networks      | ImageNet Accuracy | Million Mult-Adds | Million Parameters |
| :---------------: | :---------------: | :---------------: | :----------------: |
| 1.0 MobileNet-224 |       70.6%       |        569        |        4.2         |
|     GoogLeNet     |       69.8%       |       1550        |        6.8         |
|      VGG 16       |       71.5%       |       15300       |        138         |
| 0.5 MobileNet-160 |       60.2%       |        76         |        1.32        |
|    Squeezenet     |       57.5%       |       1700        |        1.25        |
|      AlexNet      |       57.2%       |        720        |         60         |

MobileNet要比GoogleNet更好, 更快, 比 VGG 16 差一点, 但快得多, 也更节省内存.

* 在 COCO 目标检测上的结果要比 Deeplab 和 Inception 差得多, 尽管可以大幅度减少参数量和计算量, 但 mAP 有 2%~6% 的损失. 所以这一版的 MobileNet 在分类任务上有非常好的表现, 而在目标检测任务上的表现差强人意.


## 参考文献

[^1]:
    **Going Deeper with Convolutions**<br />
    Christian Szegedy, Wei Liu, Yangqing Jia, Pierre Sermanet, et al. <br />
    [[link]](https://arxiv.org/abs/1409.4842). In CVPR[C], 2015: 1-9.

[^2]:
    **Batch normalization: Accelerating deep network training by reducing internal covariate shift**<br />
    Sergey Ioffe, Christian Szegedy <br />
    [[link]](https://arxiv.org/abs/1502.03167). In arXiv, 1502.03167.
