---
layout: post
title: "Medical Image Segmentation"
data: 2019-5-9 9:50:00
categories: 图像处理
mathjax: true
figure: /images/2019-5/Graph-Cuts-0.png
author: Jarvis
meta: Post
---

* content
{:toc}

> 医学图像往往因为不同的模态、不同的部位、不同的大小、不同的像素间隔、不同的增强序列等因素， 使得医学图像的相关算法难以泛化到其他医学图像的数据集. 因此, 一个统一的、有效的处理流程是必要的.




## 1. 医学图像简介

(待补充).

## 2. 预处理(Preprocessing)

### 2.1 图像标准化(Normalization)

记图像为 $I$.

| 模态 | 处理方法 |
| 非 CT | $\frac{I - \text{mean}(I)}{\sqrt{\text{Var}(I)}}$ |
| CT  | ? |

### 2.2 像素间隔(Voxel Spacing)

每个轴收集训练集中所有的 voxel spacing, 取中位数作为目标 voxel spacing. 然后对所有数据进行三次样条插值. 

特别地, 对于平面外(out-of-plane)的像素间隔超过平面内(in-plane)像素间隔3倍的插值可能会出现伪影, 这种情况下平面外插值使用最近邻插值. 对于对应的分割标注, 每个标注使用线性插值.

## 3. 训练过程

### 3.1 模型结构

U-Net[1]是医学图像分割常用的神经网络结构. 通常使用时对原始模型有如下修改:

* 使用带 padding 的卷积(Convolution)以获得与输入同样大小的输出
* 使用 Instance normalization
* 使用 Leaky ReLU 代替 ReLU (可选)

### 3.2 神经网络超参数

模型超参数的选择取决于数据集. 

* 对于 patch size 和 batch size 的平衡, 更倾向于大的 patch size 以充分利用上下文信息, 但要求 batch size 至少为 2. 
* 池化次数的选择: 池化直到 spatial size 小于等于 4.
* 第一层卷积使用 30 个卷积核, 每次池化后翻倍
* 3D U-Net 的使用 (未完待续)

训练超参数的选择:

* 使用五折交叉验证
* 250 个 batches 定义为 1 个 epoch
* 使用交叉熵和 Dice 的和作为损失函数
* 使用 Adam 优化器, 初始学习率 $3e-4$, $L_2$ 正则化系数 $3e-5$ 
* 训练损失的指数移动平均在30个 epoch 里不再改善时学习率下降, 因子为 0.2 
* 训练在学习率小于 $1e-6$ 或超过 1000 个 epochs 时停止

<div class="polaroid">
    <img class="cool-img" src="/images/2019-5/Graph-Cuts-2.png" Graph-Cuts/>
    <div class="container">
        <p>Graph-Cuts 示例</p>
    </div>
</div>

## 6. References

1. **U-net: Convolutional networks for biomedical image segmentation**<br />
   Olaf Ronneberger, Philipp Fischer, Thomas Brox. <br />
   [[link]](https://link.springer.com/chapter/10.1007/978-3-319-24574-4_28). In MICCAI, 2015.

