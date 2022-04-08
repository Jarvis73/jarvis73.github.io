---
layout: post
title: 如何选择神经网络的超参数 第一部分 --- 学习率, 批大小, 动量和权重衰减
date: 2018-04-20 10:49:00 +0800
categories: 深度学习
tags: Base
mathjax: true
figure: /images/2018-4-20/Figure2.png
---

* content
{:toc}

论文: A Disciplined Apporach to Neural Network Hyper-Parameters: Part 1 - Learning Rate, Batch Size, Momentum and Weight Decay


## 1. 引言

神经网络的训练目前仍然是一种黑色的艺术(black art), 需要数年的经验积累来选择**最优的超参数**, **正则化方法**和**网络结构**, 而这三者都是高度非线性, 高度耦合的. 目前使用的参数搜索方法主要有:

*   网格搜索
*   随机搜索

而这二者均是费时费力的, 好的训练时间和网络表现均强烈依赖于好的参数. 



## 2. 关注验证损失的高效性

本文中我们均使用**验证损失**这个词来表示神经网络训练过程中在验证集上的损失. 

通过在训练早期监测验证损失, 我们就可以获取足够的信息来调整网络结构, 超参数, 而不必做完整的网格/随机搜索.


<img src="/images/2018/04/Figure1.png" />
<center><em>图 1: 训练损失, 验证精度, 验证损失和泛化误差的比较表明在训练过程中验证损失可以反映出额外的信息而在其他三者都无法看出的. 该曲线来自于 resnet-56 的结构在 cifar-10 数据集上不同学习率下几个指标的走势图.</em></center><br />

从图 1 中我们可以看到在黑色方框中的验证损失显示出学习率在 0.01~0.04 的时候存在过拟合的迹象. 我们可以看到该信息只能从验证损失中看到. 如果我们用验证误差减去训练误差(即泛化误差), 那么过拟合的信息在泛化误差曲线中就基本上看不出了. 从这个小栗子中我们可以看出这个网络结构存在过拟合的能力, 训练初期太小的学习率就会导致过拟合. 

**评论 1:** <span style="color:red">验证损失是网络收敛性的一个很好的指示器</span>

### 2.1 欠拟合与过拟合的权衡

概念:

*   **欠拟合:** 当模型容量不足时, 会造成训练损失和验证损失都无法下降的情况
*   **过拟合:** 当模型容量太大时, 会导致拟合训练集太过而使得泛化误差增大 

欠拟合和过拟合的关系如图 2 所示.

<figure>
<img src="/images/2018/04/Figure2.png"/>
<figcaption>图 2: 欠拟合与过拟合之间的权衡关系. 横轴的模型复杂度表示模型容量. 最优的模型复杂度落在欠拟合和过拟合之间.</figcaption>
</figure>



<style type="text/css">
figure {
    display: block;
    width: 600px;
    margin-left: auto;
    margin-right: auto;
}
figure img {
    vertical-align: top;
}
figure figcaption {
    width: 600px;
    text-align: center;
}
</style>