---
layout: post
title: "关于少样本学习的思考 (二) (Thinking About FSL 2)"
date: 2021-03-22 17:28:00 +0800
categories: 深度学习 少样本学习
mathjax: true
figure: /images/2021-03/FSL-1.png
author: Jarvis
meta: Post
---


* content
{:toc}




## 1. (ICLR 2020) A Baseline for Few-Shot Image Classification

本文指出, 当前的 FSL 方法尽管通过复杂的设计来提取特征, 但都没有从本质上提高 FSL 的精度, 如下图所示. SOTA 方法尽管看起来在提高平均精度, 但并没有缩小 95% 置信区间的范围. 本文提出了一个非常简单的基于 transductive fine-tuneing 的方法, 超过了其他复杂设计的 SOTA 方法, 并希望作为 FSL 新的 baseline 方法.

{% include image.html class="polaroid" url="2021-03/FSL-1.png" title="Are we making progress?" %}

**Transductive learning (直推学习)** 是相对于 **inductive learning (归纳学习)** 来说的. 
* Inductive learning 是指从训练集中归纳出一定的规则(模型), 然后把该规则应用到测试数据上得到结果; 
* Transductive learning 指的是直接从训练数据和测试数据中直推出测试的结果, 因此 transductive learning 中是允许测试样本参与模型的构建的.

本文引入了 **semi-supervised learning (半监督学习)** 的方法, 通过惩罚待测试样本的 **Shannon Entropy (香农熵)** 来实现 transductive learning.

### 1.1 方法

令 $$ z(x;\theta)\in \mathbb{R}^{\vert C_m\vert} $$ 为 backbone 的 logits, 这里的 backbone 包括了 feature extractor 和 classifier. 本文新增一个 classifier 用于分类:

$$
\mathbb{R}^{\vert C_t\vert} \ni z(x;\Theta) =w\frac{z(x;\theta)_+}{\Vert z(x;\theta)_+\Vert} + b,
$$

其中 $$ w $$ 使用 support image 的 logits 归一化后的向量来初始化, $$ b $$ 初始化为 0, $$ (\cdot)_+ $$ 表示 ReLU 激活. 

* Transductive Fine-Tuning

在交叉熵损失上增加一项香农熵:

$$
\Theta^* = \underset{\Theta}{\arg\min}\frac{1}{N_s}\sum_{(x,y)\in\mathcal{D}_s}-\log p_{\Theta}(y\vert x) + \frac{1}{N_q}\sum_{(x,y)\in\mathcal{D}_q}\mathbb{H}(p_{\Theta}(\cdot\vert x)).
$$

其中第一项是交叉熵, 使用 support images/labels 来优化, 第二项是香农熵, 使用 query images 来优化.


## 2. (ICLR 2020) Rapid Learning or Feature Reuse? Towards Understanding the Effectiveness of MAML


