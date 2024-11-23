---
layout: post
title: "大模型(二): DeepMind 的 Scaling Laws 有什么不同?"
date: 2024-06-30 10:57:00 +0800
categories: 大模型
mathjax: true
author: Jarvis
meta: Post
---

* content
{:toc}

大模型时代, 在数十亿到数千亿的数据上训练一个十亿到千亿级别的模型成本是非常高的, 任何一次实验都意味着数百万的投入, 因此实验效果的可靠预测是一个绕不开的目标. 我们在训练一个大模型的时候, 往往需要回答下面的这些问题:

1. 模型的效果对哪些变量是强依赖的? 
2. 如果给你 X 张 GPU, Y 个月的时间, 你能训出一个什么效果的模型?
3. 如果给你把计算资源翻倍, 你能把效果提升到什么水平? 模型需要扩到多大? 数据需要加多少?
4. 模型训练多久就可以停下了?

这些问题 OpenAI 在《Scaling Laws for Neural Language Models》中做了详细的实验和解答, 这些实验和想法为我们提供了非常多的研究思路.




## OpenAI Scaling Laws

### 1. 预设条件

任何 Scaling laws 相关的公式都是不能直接套用的, 因为它们都是经验公式, 里面的数值和结论都依赖于实验的一系列前提条件. 因此我们有必要先把前提条件清楚地列出来, 以避免误用. 

* 模型结构 --- Transformer decoder 结构的模型.
* 训练数据 --- WebText2 数据集, BPE tokenization, 词表大小 $$n_{\text{vocab}}=50,257$$, 训练的上下文长度 $$n_{\text{ctx}}=1024$$.
* $$L$$ 损失 --- 交叉熵损失. 具体是指 LLM 的预测损失, 它计算的是上下文中所有 token 的平均交叉熵损失. 
* $$N$$ 模型参数 --- 模型的参数量, 仅包含 Attention 层的 QKVO 的 Linear 参数和 FFN 的参数; 不包含词表 Embedding 层和位置编码的参数. 
* $$C\approx 6NBS$$ 计算量 --- 模型计算量, 其中 $$B$$ 是训练的批大小, $$S$$ 是训练的步数(准确来说是梯度更新的次数). 详细计算参考[《Transformer 的参数量和计算量》](/2024/06/29/Training-Compute/). 注意这里的计算量不包含 embedding 的计算量. OpenAI 的文章中采用 PF-days 作为 $$C$$ 的单位, 它表示 $$1 \text{Peta flops} \times 1 \text{day} = 10^{15} \times 86400 = 8.64\times 10^{19}$$. 
* $$D$$ 数据量 --- 数据集的大小, 以 token 为单位. 
* $$B_{\text{crit}}$$ --- 临界批大小 - 使用临界批大小训练模型可以获得时间和计算效率上的平衡. 
* $$C_{\text{min}}$$ --- 达到指定 loss 的最小计算量 (不包含 embedding). 这是采用一个远小于 $$B_{\text{crit}}$$ 的 batch size 训练模型时才能达到的. 
* $$S_{\text{min}}$$ --- 达到指定 loss 的最小训练步数. 这是采用一个远大于 $$B_{\text{crit}}$$ 的 batch size 训练模型时才能达到的. 结合 $$C_{\text{min}}$$ 和 $$S_{\text{min}}$$ 其实我们可以发现它们是 $$B$$ 取两个极端时才能达到的. 
* $$\alpha_X$$ --- Power law 的指数, 即 $$L(X) \propto 1/X^{\alpha_X} $$, 其中 $$X$$ 可以是任意的 $$N, D, C, B, S$$ 等.
* 其他假设
  * $$d_{\text{model}} \gg n_{\text{ctx}} / 12$$, 即模型的维度远大于上下文长度的 1/12. 注意 1/12 包含了 $$d_{\text{ff}} = 4d_{\text{model}}$$ 的假设. 这里的假设我们在[《Transformer 的参数量和计算量》](/2024/06/29/Training-Compute/)一文中也有提到.

### 2. Scaling Laws







## DeepMind Scaling Laws

本文研究了在给定计算量(compute budget) 下, 训练 transformer 语言模型最优的模型尺寸(model size)和 token 数. 具体来说, 令 $$N$$ 表示模型参数量, $$D$$ 表示训练的 token 数, 在给定的训练资源下 (即 $$ FLOPs(N, D) = C $$), 我们希望寻找最优的 $$N, D$$ 来达到最优的预训练的 loss $$L(N, D)$$. 这个目标可以用公式表示为:

$$
    N_{opt}(C), D_{opt}(C) = \underset{N, D, 使得 FLOPs(N, D) = C}{\arg\min} L(N, D).
$$

函数 $$N_{opt}(C), D_{opt}(C)$$ 表示计算资源 $$C$$ 下最优的 $$N$$ 和 $$D$$. 

先抛出结论: **对于计算最优的训练, 模型大小和训练的 token 数应当同等倍数的缩放.**

本文采用了三种方法来验证. 

### 方法一: 固定模型大小, 变化训练的 token 数. 

如下图所示. 作者使用从 70M ~ 10B 大小的模型进行实验, 每个模型进行了四组实验, 在下面左图中, 绘制了 training loss 曲线. 对于每个 FLOPs, 取获得最小 loss 的那组实验, 这样根据不同的 FLOPs 就能获得一组实验点(模型大小以及训练到相应的 FLOPs 使用的 token 数量), 绘制在中间和右边图中. 另外还标注出了 Gopher 模型的计算量下对应的最优参数量是 67B, 最优 token 数量是 1.5T. 

{% include image.html class="polaroid" url="2024/06/training_curve_envelope.png" title="训练曲线包络线" %}

最终的拟合表达式为 $$N_{opt}\propto C^a, D_{opt}\propto C^b$$, 其中 $$a=0.50, b=0.50$$. 

### 方法二: IsoFLOPs, 利用 FLOPs 等值线

在这组实验中, 给定 9 个固定的 FLOPs (6x10e18 ~ 3x10e21), 变化模型大小来寻找最优的模型大小. 注意, $$N, D, C$$ 三个变量中给定两个, 另一个是能直接算出来的. 因此我们可以直接计算出对应的 token 数. (注意 FLOPs 和模型大小确定后, 训练步数也就确定了, 作者会设置学习率的 cosine schedule length 等于训练步数, 因为在附录B的实验中发现 length 设置过大会导致 loss 不是最优的.)

如下图所示, 在不同的 FLOPs 下(不同颜色的点), 变化模型尺寸得到的近似抛物线, 因此用抛物线来拟合这些点. 作者通过为不同的 FLOPs 选择不同的模型尺寸来确保这些点能覆盖抛物线的最低点. 这样对每种 FLOPs 可以选出最优的模型尺寸和相应的 token 数, 同样可以拟合 power law. 拟合得到的 $$a=0.49, b=0.51$$, 与方法一基本一致. 

{% include image.html class="polaroid" url="2024/06/isoflop_curve.png" title="IsoFLOP 曲线" %}

### 方法三: IsoLoss, Loss 的等值线

第三种方法想要把前面两种方法所有实验的损失和相关超参通过一个函数来拟合. 那么我们首先要确定一下这个函数的形式, 然后才能代入参数计算相关系数. 我们先给出这个函数:

$$
    \hat{L}(N, D) \triangleq E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}.
$$

为了估计这个函数中的参数 $$(A, B, E, \alpha, \beta)$$, 使用 Huber loss 并采用 L-BFGS 优化算法来拟合数据. Huber loss 对 outlier 不敏感, 文章中采用了 $$\delta=10^{-3}$$.

$$
    \min_{A,B,E,\alpha,\beta} \sum_i \text{Huber}_{\delta}(\log\hat{L}(N_i, D_i) - \log L_i).
$$

**Efficient Frontier.** 我么可以通过上面的优化方法在约束 $$\text{FLOPs}(N, D)\approx 6ND$$ 下得到 $$N_{opt}$$ 和 $$D_{opt}$$:

$$
N_{opt}(C) = G\left(\frac{C}6\right)^a,\quad D_{opt}(C)=G^{-1}\left(\frac{C}6\right)^b,
$$

其中, 

$$
G=\left(\frac{\alpha A}{\beta B}\right)^{\frac1{\alpha+\beta}},\quad a=\frac{\beta}{\alpha+\beta},\; b=\frac{\alpha}{\alpha+\beta}.
$$

拟合的函数 $$\hat{L}$$ 绘制在下图中, 蓝色的直线是最优算力下的模型. 即, 在每条 loss 等值线上, 蓝线上的点对应的模型是所需要算力最小的模型, 即我们认为的最优模型. 文中拟合出来 $$a=0.46, b=0.54$$. 

{% include image.html class="polaroid" url="2024/06/isoloss_curve.png" title="IsoLoss 曲线" %}
