---
layout: post
title: "关于少样本学习的思考 (二) (Thinking About FSL 2)"
date: 2021-03-22 20:42:00 +0800
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

{% include image.html class="polaroid" url="2021-03/FSL-2.png" title="Rapid learning and feature reuse paradigms." %}

本文分析了 MAML 算法在 meta-testing 时有效的原因是内循环的快速学习还是重用了 meta-training 时学到的特征, 得到了如下结论:

* 在 MAML 训练完后, 测试时冻结 meta-learner (即禁用内循环); 然后使用特征相似度评估方法 (Canonical Correlation Analaysis, CCA) 检查内循环在测试时发生了多大的变动.

  * 结果显示实际上只有最后的 head layer 参数有显著的变化, 其他层的参数变动非常小. 说明了 MAML 的效果来源于 meta-learner 的特征重用.

* 基于该实验发现, 提出了 ANIL (Almost No Inner Loop) 的方法, 在训练和测试时移除绝大部分的内循环, 仅仅保留最后一层参数的内循环更新. 

  * 结果显示 ANIL 实现了和 MAML 一样的精度, 而训练和推断速度有了显著的提升.

  * <u>测试时</u> head layer 的内循环可以去掉而不影响精度, 称为 NIL (No Inner Loop).

  * <u>训练时</u> head layer 的内循环**不**可以去掉, 否则会显著影响精度.

