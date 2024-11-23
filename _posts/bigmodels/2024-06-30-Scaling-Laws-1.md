---
layout: post
title: "大模型(一): Scaling Laws - OpenAI 提出的科学法则"
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

这些问题 OpenAI 在[《Scaling Laws for Neural Language Models》](https://arxiv.org/abs/2001.08361)中做了详细的实验和解答, 这些实验和想法为我们提供了非常多的研究思路.




## 预设条件

任何 Scaling laws 相关的公式都是不能直接套用的, 因为它们都是经验公式, 里面的数值和结论都依赖于实验的一系列前提条件. 因此我们有必要先把前提条件清楚地列出来, 以避免误用. 

* <span style="color:blue">模型结构</span> --- Transformer decoder 结构的模型.
* <span style="color:blue">训练数据</span> --- WebText2 数据集, BPE tokenization, 词表大小 $$n_{\text{vocab}}=50,257$$, 训练的上下文长度 $$n_{\text{ctx}}=1024$$. 关于训练数据的详细介绍参考原文 2.3 节, 这里不再赘述.
* <span style="color:blue">$$L$$ 损失</span> --- 交叉熵损失. 具体是指 LLM 的预测损失, 它计算的是上下文中所有 token 的平均交叉熵损失. 
* <span style="color:blue">$$N$$ 模型参数</span> --- 模型的参数量, 仅包含 Attention 层的 QKVO 的 Linear 参数和 FFN 的参数; 不包含词表 Embedding 层和位置编码的参数. 
* <span style="color:blue">$$C\approx 6NBS$$ 计算量</span> --- 模型计算量, 其中 $$B$$ 是训练的批大小, $$S$$ 是训练的步数(准确来说是梯度更新的次数). 详细计算参考[《Transformer 的参数量和计算量》](/2024/06/29/Training-Compute/). 注意这里的计算量不包含 embedding 的计算量. OpenAI 的文章中采用 PF-days 作为 $$C$$ 的单位, 它表示 $$1 \text{Peta flops} \times 1 \text{day} = 10^{15} \times 86400 = 8.64\times 10^{19}$$. 
* <span style="color:blue">$$D$$ 数据量</span> --- 数据集的大小, 以 token 为单位. 
* <span style="color:blue">$$B_{\text{crit}}$$</span> --- 临界批大小 - 使用临界批大小训练模型可以获得时间和计算效率上的平衡. 
* <span style="color:blue">$$C_{\text{min}}$$</span> --- 达到指定 loss 的最小计算量 (不包含 embedding). 这是采用一个远小于 $$B_{\text{crit}}$$ 的 batch size 训练模型时才能达到的. 
* <span style="color:blue">$$S_{\text{min}}$$</span> --- 达到指定 loss 的最小训练步数. 这是采用一个远大于 $$B_{\text{crit}}$$ 的 batch size 训练模型时才能达到的. 结合 $$C_{\text{min}}$$ 和 $$S_{\text{min}}$$ 其实我们可以发现它们是 $$B$$ 取两个极端时才能达到的. 
* <span style="color:blue">$$\alpha_X$$</span> --- Power law 的指数, 即 $$L(X) \propto 1/X^{\alpha_X} $$, 其中 $$X$$ 可以是任意的 $$N, D, C, B, S$$ 等.
* 其他假设
  * <span style="color:blue">$$d_{\text{model}} \gg n_{\text{ctx}} / 12$$</span> --- 即模型的维度远大于上下文长度的 1/12. 注意 1/12 包含了 $$d_{\text{ff}} = 4d_{\text{model}}$$ 的假设. 这里的假设我们在[《Transformer 的参数量和计算量》](/2024/06/29/Training-Compute/)一文中也有提到.
  * <span style="color:blue">Adam 优化器</span> --- 如果没有指明, 则训练 250K 步, 批大小 512, 序列长度 1024. 由于显存限制, 大于 1B 的模型采用 Adafactor 训练. 
  * <span style="color:blue">学习率</span> --- 采用 3000 步 warmup, cosine decay 到 0. 此外, 实验发现在前面给出的设置下, 不同的学习率对于最终的 loss 影响不大.
  * <span style="color:blue">正则化</span> --- 采用 10% 的 dropout. 

## 实验范围

实验范围也是个非常重要的因素, 它直接决定了所得出的结论的适用范围. OpenAI 的实验范围如下:

* <span style="color:blue">模型参数量</span> --- 从 768 到 1.5B (不包含 embedding).
* <span style="color:blue">数据量</span> --- 从 22M 到 23B tokens.
* <span style="color:blue">模型形状</span> --- 包含深度 $$n_{\text{layer}}$$, 宽度 $$d_{\text{model}}$$, attention head 数量 $$n_{\text{head}}$$, FFN 层的维度 $$d_{\text{ff}}$$ 等.
* <span style="color:blue">上下文长度</span> --- 绝大部分实验采用 1024. 
* <span style="color:blue">批大小</span> --- 绝大部分实验采用 512 (序列长度用1024, 相当于 $$512K = 2^{19}$$ tokens), 也有些变化涉及 $$B_{\text{crit}}$$ 的实验.

## Scaling Laws

<span style="color:red"><strong>
结论一: 当参数量 $$N$$ 固定时(不包含embed层), Transformer 的表现不太依赖形状超参的选择, 如 $$n_{\text{layer}}, d_{\text{ff}}, n_{\text{head}}$$.
</strong></span> 

{% include image.html class="polaroid" url="2024/06/conclusion-01.png" title="模型表现不太依赖结构超参" %}

如上图所示. 我们可以观察到:  
1. Feed-Forward Ratio ($$d_{\text{ff}} / d_{\text{model}}$$) 从 0.5 变化到 10 时, loss 变化幅度在 2% 范围内, 波动不大. 但是超过 10 之后loss 会有 2% ~ 8% 的上升, 这意味着 **Feed-Forward Ratio 不宜过大**. 该结论在 50M 参数的模型上进行实验的.   
2. Aspect Ratio ($$d_{\text{model}} / n_{\text{layer}}$$) 在 10 到 120 的范围时 loss 波动在 2% 以内, 该结论在 50M、274M、1.5B 参数的模型上进行实验的, 因此可靠度更高. 总体来说 **Aspect Ratio 在 100 左右效果最好** (loss 最低), 例如下图中 LLaMA 结构的设计也符合这个结论.   
3. Attention Head Dimension ($$d_{\text{model}} / n_{\text{head}}$$) 在 16 到 256 的范围时 loss 波动在 2% 以内, 该结论在 256、512、1024 三个 $$d_{\text{model}}$$ 的模型上进行实验的, 因此可靠度较高. 总体来说 **对于较大的 $$d_{\text{model}}$$, Attention Head Dimension 在 64 ~ 128 的效果较好** (loss 最低). 例如下图中 LLaMA 结构的设计均采用了 128 的 Attention Head Dimension.

{% include image.html class="polaroid" url="2024/06/llama_structure.png" title="LLaMA 结构参数" %}

---
<span style="color:red"><strong>
结论二: 模型参数量 $$N$$ (不含 embed) 服从 power law, 形式为 $$L(N)\approx(N_c/N)^{\alpha_N}$$.
</strong></span> 

这里 $$N_c$$ 是个常数, 没有实际含义. 这批实验覆盖了从 $$(n_{\text{layer}}, d_{\text{model}}) = (2, 128)$$ 的小模型到 $$(6, 4288)\sim(207, 768)$$ 的大模型. 

<span style="color:blue">这个 power law 的前提是模型均训练到收敛且没有过拟合 (即需要使用足够大的数据量来训练, 以确保不会过拟合)</span>, 除了最大的模型可能有一定的过拟合. 如图 3(c) 所示.

{% include image.html class="polaroid-small" url="2024/06/conclusion-02-01.png" title="模型参数的 power law" %}

图 4 说明了计算参数量时包含 embedding 会导致小参数模型拟合 power law 的效果变差. 因此我们在计算参数量时应该排除 embedding 的参数量. 

{% include image.html class="polaroid" url="2024/06/conclusion-02-02.png" title="embedding 参数对拟合 power law 的影响" %}

图 5 的左图说明了不同数据集拟合的参数 $$N$$ 的 power law 曲线接近, 这意味着 power law 有一定的泛化能力.   
图 5 右图的比较了在 WebText2 上训练, 一个大模型(虚线)和一群收敛的小模型(点)的 text loss 和泛化到其他数据集的 loss 的关系, 发现也符合 power law (能拟合成直线). 另外, 点几乎都落在对应的虚线上, 这表示测试 loss 直接能表现模型的泛化能力, 这与模型是否收敛无关. 在附录 D.8 的实验中也证明了泛化能力与模型层数无关 (相同参数量下, 10-100多层的模型表现差不多). 

{% include image.html class="polaroid" url="2024/06/conclusion-02-03.png" title="数据集对拟合的 power law 影响不大" %}

此外, 在论文的 3.2.1 节还验证了 Transformer 结构优于 LSTM. 后者不具备良好的 power law 拟合性质, 且在 token 序列中位置 100 以后得预测效果不佳. 此处不再赘述. 

---
<span style="color:red"><strong>
结论三: 训练数据量 $$D$$ 服从 power law, 形式为 $$L(D)\approx(D_c/D)^{\alpha_D}$$.</strong></span> 

这里 $$D_c$$ 是个常数, 没有实际含义. 如图 3(b) 所示. 这里实际上只需要一个实验, 这个实验使用大小为 $$(n_{\text{layer}}, d_{\text{model}}) = (36, 1280)$$ 的模型, 在 WebText2 上训练到 loss 不再下降为止. 

---
<span style="color:red"><strong>
结论四: 当 $$N$$ 和 $$D$$ 同时变化时, 满足 $$L(N, D)=\left[(N_c/N)^{\alpha_N/\alpha_D} + (D_c/D)\right]^{\alpha_D}$$.
</strong></span> 

注意这个公式是根据结论二和结论三造出来的, 它在造的时候使用了三个原则:

1. 改变词表大小或者 tokenization 的方式只会整体上影响 loss 的乘数项, 而不影响公式的形式. 反映在上面的公式中就是只影响 $$N_c, D_c$$ 的取值.
2. 固定 $$D$$, 令 $$N \rightarrow\infty$$, 那么 loss 会收敛到 $$L(D)$$; 固定 $$N$$, 令 $$D \rightarrow\infty$$, 那么 loss 会收敛到 $$L(N)$$.
3. $$L(N, D)$$ 需要在 $$D=\infty$$ 是解析的, 这样它能够在 $$1/D$$ 处进行级数展开. 关于这一点, 参考原文的 4.1 节和文章[《High-dimensional dynamics of generalization error in neural networks》](https://arxiv.org/abs/1710.03667) 进一步的理解. 

根据实验结果拟合得到的四个系数分别为: 

$$
\alpha_N=0.076,\quad \alpha_D=0.103,\quad N_c=6.4\times 10^{13},\quad D_c=1.8\times 10^{13}.
$$

{% include image.html class="polaroid" url="2024/06/conclusion-04-01.png" title="数据量和参数量同时变化对模型表现的影响" %}

如图 6(a) 所示, $$D$$ 比较大的时候, 和 $$N$$ 存在直线的 power law; 当 $$D$$ 较小时, 模型的表现会随着参数量增加先提升后过拟合. 

实验发现训练 22B 数据的时候, 除了最大的模型, 其他模型均未发现过拟合的现象, 因此可以把 22B 看做 $$D=\infty$$, 然后计算有限数据和无穷数据下 loss 的比值:

$$
\begin{align}
\delta L(N, D) &= \frac{L(N, D)}{L(N, \infty)} - 1 \\
&\approx \left(1 + \left(\frac{N}{N_c}\right)^{\frac{\alpha_N}{\alpha_D}}\frac{D_c}{D}\right)^{\alpha_D} - 1 \\
& \leq 0.02
\end{align}
$$

第二行是代入结论四的公式, 第三行是论文中(可能是通过实验)估计不同随机种子下的 loss 变化范围. 这样我们就能计算出给定 $$N$$ 的情况下为了不过拟合所需要的最少的数据量:

$$
D \geq \frac{N_c^{-\alpha_N/\alpha_D}D_c}{1.02^{1/\alpha_D} - 1}N^{\alpha_N/\alpha_D} \gtrsim (5.5\times 10^3)N^{0.74}
$$

如果把 22B 代入 $$D$$, 那么可以得到 $$N\approx 0.95\times 10^9 = 950M$$. 这意味着小于 950M 的模型在 22B 的数据上不会过拟合. 另外一个结论是<span style="color:blue">数据集的增长相比于模型参数增长是次线性的</span>. 此外文章中特别提醒, 这个关系并不是计算效率最优的训练策略. 此外, 正则化可能也不是最优的, 这可能影响该结论的系数.

---
<span style="color:red"><strong>
结论五: 训练最优的计算量 $$C_{\text{min}}$$ 服从 power law, 形式为 $$L(C_{\text{min}})\approx(C_c/C_{\text{min}})^{\alpha_C}$$.
</strong></span> 

这里 $$C_c$$ 是个常数. 如图 3(a) 所示. 这里分别用不同的参数量 $$N$$ 做了多个实验. 因为我们有 $$C=6NBS$$, 所以每选择一个 $$C$$, 就能根据不同的 $$N$$ 得到 $$S = C / 6NB$$ (即训练步数), 从而得到对应的 loss. 这样每个大小的模型都有一条关于 $$C$$ 的 loss 曲线, 绘制在图上, 发现可以得到一条包络线, 这个包络线在 xy 对数轴的图上是一条直线. 这意味着<span style="color:blue">给定不同的 $$C$$, 需要使用的模型大小和数据量是不同的.</span> 

注意这个 power law 是在固定一个 batch size $$B$$ 的前提下得到的, 那么拟合的这条直线可能并不是最优的. 那么如何计算更准确的 $$C_{\text{min}}$$ 呢? 我们需要接下来两个结论来解决这个问题.

---
<span style="color:red"><strong>
结论六: 参数量和最小训练步数满足 $$L(N, S_{\text{min}})=(N_c/N)^{\alpha_N} + (S_c/S_{\text{min}})^{\alpha_S}$$.
</strong></span> 

这里引入了**最小训练步数 $$S_{\text{min}}$$**的概念, 引入这个概念是因为论文中认为大多实验并没有使用一个**最优的 batch size** 来训练. 这要追溯到 2018年 OpenAI 的一篇文章[《An Empirical Model of Large-Batch Training》](http://arxiv.org/abs/1812.06162), 当时已经发现模型可以有效地用大 batch 训练, 而该文章发现不同 domain 下选择的 batch 可能会差几个数量级, 因此为了解决如何选择最好的 batch size 的问题提出了 **gradient noise scale** 的概念来预测不同 domain 下最大且可行的 batch size. 
