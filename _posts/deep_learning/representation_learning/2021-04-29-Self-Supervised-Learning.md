---
layout: post
title: "自监督学习(Self-Supervised Learning, SSL)"
date: 2021-04-29 19:13:00 +0800
update: 2021-06-03
categories: 深度学习
mathjax: true
figure: ./images/2021-04/SSL-02.png
author: Jarvis
meta: Post
---

* content
{:toc}



## 摘要

* MoCo
* SimCLR
* SwAV
* BYOL
* MoCo V3

排行榜: [https://paperswithcode.com/sota/self-supervised-image-classification-on](https://paperswithcode.com/sota/self-supervised-image-classification-on)

## Self-Supervised Learning

自监督学习 vs 无监督学习:
* 无监督学习指的是不使用标签来从数据集中学习特征的学习方法
* 自监督学习指的是从数据集中自定义新的 pretext task (包括 samples 和 labels) 来完成预训练

1. (Method 1) 自监督学习是无监督学习的一种, 都是为了从数据 $$ x $$ 中生成 **有代表性的特征** $$ h = f(x) $$, 用于下游任务. 那么什么是有代表性的特征?

在无监督学习中, 有一些的研究认为, 如果可以从 $$ h $$ 中很好的恢复 $$ x = g(h) $$ 的话, 那么 $$ h $$ 就是有代表性的特征. 由此, 出现了大量的生成式方法, 比如 AutoEncoder, 这类模型希望从低维特征 $$ h $$ 中生成的样本尽可能地与原始样本相同, 即:

$$
\min\mathcal{L}_1(g(f(x)), x)
$$

但是生成式方法需要构造一个额外的生成器 $$ g $$, 这会存在一些问题, 比如需要两个模型, 生成的样本不尽如人意等. (待补充) 

因此人们开始思考是否有其他路径来判断 $$ h $$ 是否为有代表性的特征, 于是人们做出了一些妥协的选择: 

2. (Method 2) 使用 $$ h $$ 可以完成特定的下游任务, 如预测空间位置, 预测部分样本, 执行拼图任务等等. 这类方法需要增加分类器或回归器 $$ p $$ 执行预测任务, 即

$$
\min\mathcal{L}_2(p(f(x)), y)
$$

3. (Method 3) 如果当样本进行一些变换时, $$ h $$ 能够保持不变, 那么就认为 $$ h $$ 就是有代表性的特征. 前面两种方法都是在输出空间进行比较, 而这第三种方法是在特征空间中进行比较:

$$
\min\mathcal{L}_3(f(x), f(x^+))
$$

其中 $$ x^+ $$ 是 $$ x $$ 的一个变换. 

## Contrastive Learning

但是这第三种方法有个缺点---会产生平凡解, 即模型永远都把所有的样本映射到同一个点上. 这就意味着, 我们不仅要把相似的样本在特征空间中映射到尽量接近的位置, 还要让不相似的样本映射到尽量远的位置, 这就导出了对比学习 (Contrastive Learning):

$$
\min\mathcal{L}_3(f(x), f(x^+)) - \mathcal{L}_4(f(x), f(x^-))
$$

如果我们把这样的无监督学习过程看做一种降维的话, 这样的学习方法还有几个好处, (1) 不需要在输入空间构造度量函数, (2) 只需要样本的邻接关系, (3) 学习到的映射可以直接应用于新的数据点而不需要额外的先验知识.

## Deep InfoMax

微软: **Learning deep representations by mutual information estimation and maximization**[^1]

应用对比学习, 通过最大化 $$ h $$ 和 $$ x $$ 的互信息, 并且最小化 $$ h $$ 和负样本 $$ x' $$ 的互信息来训练.

$$
\min - T(x, h) + \log\sum_{x'}e^{T(x', h)}
$$

{% include image.html class="polaroid" url="2021-04/SSL-01.png" title="Deep InfoMax"  %}

## MoCo

FAIR: **Momentum Contrast for Unsupervised Visual Representation Learning**[^2]

作者假设从更多的负样本中可以学到更好的特征, 因此维护了个比 batch size 更大的查询字典, 并使用动量来保持字典中键的一致性.

$$
\begin{align}
\theta_q &\leftarrow \theta_q - \eta\nabla f_q(x) \\
\theta_k &\leftarrow m\theta_k + (1-m)\theta_q
\end{align}
$$

其中 $$ \theta_k, \theta_q $$ 分别是字典分支和查询分支的编码器参数.

{% include image.html class="polaroid" url="2021-04/SSL-02.png" title="MoCo"  %}


## SimCLR

Google Brain: **A Simple Framework for Contrastive Learning of Visual Representations**[^3]

本文贡献: (1) 组合使用多种 data augmentation 很关键, (2) 表示层和对比学习损失层之间增加一个线性层很关键, (3) 大 batch size 和更多的 epochs 很关键.

$$
\min-\log\frac{\exp(s_{i,j}/\tau)}{\sum_{k=1}^{2N}\mathbf{1}_{[k\neq i]}\exp(s_{i,j}/\tau)}
$$

{% include image.html class="polaroid" url="2021-04/SSL-03.png" title="SimCLR"  %}

## SwAV

FAIR: **Unsupervised Learning of Visual Features by Contrasting Cluster Assignments**[^4]

基于聚类的自监督方法. 构造一个"交换的"预测问题:

$$
\mathcal{L}(z_t, z_s) = \ell(z_t, q_s) + \ell(z_s, q_t)
$$

$$
\ell(z_t, q_s) = -\sum_k q_s^{(k)}\log p_t^{(k)}, \qquad p_t^{(k)}=\frac{\exp\left(\frac{1}{\tau}z_t^Tc_k\right)}{\sum_{k'}\exp\left(\frac{1}{\tau}z_t^Tc_{k'}\right)}
$$

{% include image.html class="polaroid" url="2021-04/SSL-04.png" title="SwAV"  %}

## BYOL

DeepMind: **Bootstrap Your Own Latent A New Approach to Self-Supervised Learning**[^5]

不使用负样本. 有人发现实际还是隐式的用了负样本, 在 $$ q_{\theta} $$ 里面用了 Batch Normalization. 后来作者又发了一篇 arxiv, 把 BN 换成了 Group Normalization + Weights Standardization, 可以达到和 BYOL 接近的精度.

$$
\mathcal{L}=\Vert q_{\theta}(z_{\theta}) - z_{\xi}' \Vert_2^2
$$

$$
\theta \leftarrow \text{Optimizer}(\theta, \nabla_{\theta}\mathcal{L}, \eta) \qquad \xi \leftarrow \xi + (1 − \tau)\theta
$$

{% include image.html class="polaroid" url="2021-04/SSL-05.png" title="BYOL"  %}

## SimCLR V2

Google Brain: **Big Self-Supervised Models are Strong Semi-Supervised Learners**[^6]

1. ResNet-50 --> ResNet-50 (2x) --> ResNet-50 (4x) --> ResNet-152 (3x, Seletive Kernel)
2. SimCLR 使用了两层 projection head, SimCLR V2 增加到三层, 并且使用第一层的输出作为最终的结果
3. 加入 MoCo 的机制

## MoCo V3

FAIR: **An Empirical Study of Training Self-Supervised Vision Transformers**[^7]

使用了 Visual Transformers, 使用了 InfoNCE 损失：

$$
\mathcal{L}_q = -\frac{\exp(q\cdot k^+/\tau)}{\exp(q\cdot k^+/\tau) + \sum_{k^-}\exp(q\cdot k^+/\tau)}
$$


{% include image.html class="polaroid" url="2021-04/SSL-06.png" title="Visual Transformers, ViT"  %}


## 参考文献

[^1]:
    **Learning deep representations by mutual information estimation and maximization**<br /> 
    R Devon Hjelm, Alex Fedorov, Samuel Lavoie-Marchildon, Karan Grewal, Phil Bachman, Adam Trischler, Yoshua Bengio<br />
    [[html]](https://openreview.net/forum?id=Bklr3j0cKX) In ICLR 2018

[^2]:
    **Momentum Contrast for Unsupervised Visual Representation Learning**<br />
    Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, Ross Girshick<br />
    [[html]](https://openaccess.thecvf.com/content_CVPR_2020/html/He_Momentum_Contrast_for_Unsupervised_Visual_Representation_Learning_CVPR_2020_paper.html) In CVPR, 2020

[^3]:
    **A Simple Framework for Contrastive Learning of Visual Representations**<br />
    Ting Chen, Simon Kornblith, Mohammad Norouzi, Geoffrey Hinton<br />
    [[html]](http://proceedings.mlr.press/v119/chen20j.html) In ICML, 2020

[^4]:
    **Unsupervised learning of visual features by contrasting cluster assignments**<br />
    Mathilde Caron, Ishan Misra, Julien Mairal, Priya Goyal, Piotr Bojanowski, Armand Joulin<br /> 
    [[pdf]](https://proceedings.neurips.cc/paper/2020/file/70feb62b69f16e0238f741fab228fec2-Paper.pdf) In NeurIPS, 2020

[^5]:
    **Bootstrap Your Own Latent - A New Approach to Self-Supervised Learning**<br />
    Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec, Pierre Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires, Zhaohan Guo, Mohammad Gheshlaghi Azar, Bilal Piot, koray kavukcuoglu, Remi Munos, Michal Valko<br />
    [[html]](https://papers.nips.cc/paper/2020/hash/f3ada80d5c4ee70142b17b8192b2958e-Abstract.html) In NeurIPS, 2020

[^6]:
    **Big Self-Supervised Models are Strong Semi-Supervised Learners**<br /> 
    Ting Chen, Simon Kornblith, Kevin Swersky, Mohammad Norouzi, Geoffrey Hinton<br />
    [[pdf]](https://proceedings.neurips.cc/paper/2020/file/fcbc95ccdd551da181207c0c1400c655-Paper.pdf) In NeurIPS, 2020

[^7]:
    **An Empirical Study of Training Self-Supervised Vision Transformers**<br />
    Xinlei Chen, Saining Xie, Kaiming He<br /> 
    [[html]](http://arxiv.org/abs/2104.02057) In arXiv:2104.02057
