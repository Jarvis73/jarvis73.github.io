---
layout: post
title: "生成扩散模型(三): 灵活性和易处理性 (Generative Diffusion Model: Flexibility and Tractability)"
date: 2022-11-27 15:07:00 +0800
categories: 深度学习 生成模型
mathjax: true
author: Jarvis
meta: Post
---

* content
{:toc}

说起机器学习中使用概率模型建模复杂的数据集时, 要<span style="color:blue">同时满足概率模型的灵活性 (flexibility) 和易处理性 (tractability) 是一件十分困难的事情</span>. 如果想要用复杂的模型 $$\phi(\bm{x})$$ (比如深度神经网络) 提高建模的灵活性, 那么往往会牺牲易处理性, 因为为了获得数据的概率分布 $$p(\bm{x})=\frac{\phi(\bm{x})}{Z}$$, 需要计算标准化常数 $$Z$$, 然而这需要计算积分 $$Z=\int\phi(\bm{x})\text{d}x$$, 导致计算难度陡增, 需要用蒙特卡洛 (Monte Carlo, MC) 等耗时耗力的方法. 反之, 如果使用易处理的模型 (比如高斯分布) 拟合数据, 那么这类模型又难以描述分布十分复杂的数据.



而 Sohl-Dickstein 等人在 2015 年的工作[《Deep Unsupervised Learning using Nonequilibrium Thermodynamics》](https://proceedings.mlr.press/v37/sohl-dickstein15.html) 提出了一种新的模型 (也就是我们现在所熟知的扩散模型) 来解决上面不能两全的问题, 以同时追求灵活性和易处理性. 扩散模型源自于<span style="color:red">非平衡热力学 (non-equilibrium thermodynamics) </span>的现象, 即系统性地、缓慢地、一步一步地摧毁原始的数据分布 (也即**扩散过程**), 我们只需要去建模这个扩散过程的逆过程即可恢复数据分布. 

## 扩散概率模型

扩散模型有如下优点:

1. 模型结构是灵活的
2. 确定的采样过程
3. 易于和其他分布相乘 (比如计算后验分布时)
4. 模型的对数似然和每一步中间状态的概率分布都可以计算

## 前向过程

扩散模型的<span style="color:red">前向过程 (forward/inference process)</span> 中, 我们把原始的数据分布记为 $$q(\bm{x}_0)$$ (注意, 该分布是未知的, 我们只有一些从该分布中采样得到的样本, 即我们拿到的训练数据), 数据的分布在扩散过程中逐渐变成一个简单的(易处理的)分布 $$q(\bm{x}_T)$$, 其中 $$T$$ 是扩散的步数. 我们假设扩散过程是服从<span style="color:red">马尔科夫 (Markov)</span> 性质的, 即当前状态只跟上一个状态有关, 而与再早以前的状态无关. 前向过程可以表示为:

$$ \label{eq:forward}
    q(\bm{x}_{0:T})=q(\bm{x}_0)\prod_{t=1}^T q(\bm{x}_t\vert\bm{x}_{t-1}).
$$

其中的 $$q(\bm{x}_t\vert\bm{x}_{t-1})$$ 可以是高斯分布或者二项分布. 扩散最终的结果是一个标准高斯分布或二项分布. 

{% include card.html type="info" content="我们使用 $$p(\bm{x}_{0:T})$$ 表示随机变量 $$\bm{x}_0,\cdots,\bm{x}_T$$ 联合分布的密度函数." %}


## 反向过程

<span style="color:red">反向过程 (reverse process)</span> 通过训练可以描述前向过程的反向过程:

$$ \label{eq:backward}
    p(\bm{x}_{0:T})=p(\bm{x}_T)\prod_{t=1}^T p(\bm{x}_{t-1}\vert \bm{x}_t).
$$

当扩散步长 $$\beta$$ 足够小的时候, 其逆向过程也是一个高斯(二项)分布. 下文主要考虑高斯分布, 那么只需要考虑计算高斯分布的均值和方差(协方差矩阵)即可. 

特别地, 我们定义反向过程的起点等于前向过程的终点, 即 $$p(\bm{x}_T)=q(\bm{x}_T)$$.

## 模型概率

上面定义的扩散模型是一个隐变量模型, $$\bm{x}_1\cdots\bm{x}_T$$ 都属于隐变量, $$\bm{x}_0$$ 是观测变量, 那么对该隐变量模型联合分布的密度函数在所有隐变量上积分即可得到观测变量的边缘分布

$$
    p(\bm{x}_0) = \int d\bm{x}_{1:T}\,p(\bm{x}_{0:T}).
$$

这个积分是不易处理的, 我们可以把上面的式子变成反向过程和前向过程的相对概率

$$
    \begin{align}
        p(\bm{x}_0) &= \int d\bm{x}_{1:T}\,p(\bm{x}_{0:T}) \frac{q(\bm{x}_{1:T}\vert \bm{x}_0)}{q(\bm{x}_{1:T}\vert \bm{x}_0)} \\ \label{eq:model_prob_2}
        &= \int d\bm{x}_{1:T}\,q(\bm{x}_{1:T}\vert \bm{x}_0) \frac{p(\bm{x}_{0:T})}{q(\bm{x}_{1:T}\vert \bm{x}_0)} \\ \label{eq:model_prob_3}
        &= \int d\bm{x}_{1:T}\,q(\bm{x}_{1:T}\vert \bm{x}_0) \cdot p(\bm{x}_T) \prod_{t=1}^T\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_t\vert \bm{x}_{t-1})}.
    \end{align}
$$

其中式 \eqref{eq:model_prob_3} 是把式 \eqref{eq:forward} 和 \eqref{eq:backward} 代入式 \eqref{eq:model_prob_2} 得到的.

作者在这里说明了一下式 \eqref{eq:model_prob_3} 是易于处理的. 只需要计算 $$p(\bm{x}_T) \prod_{t=1}^T\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_t\vert \bm{x}_{t-1})}$$, 然后在所有的前向过程的路径 $$q(\bm{x}_{1:T}\vert\bm{x}_0)$$ 上求和 (相当于做积分) 即可. 特别地, 如果前向过程的步长 $$\beta$$ 是个无穷小量, 那么给定 $$\bm{x}_0$$ 只有一条确定的前向路径. 

## 训练模型

训练模型需要一个损失函数, 我们可以<u>极大化模型的对数似然 (log likelihood)</u>, 它相当于搜索能使得当前的观测样本出现概率最大的参数. $$N$$ 个观测变量 $$\{\bm{x}^{(i)}\}_{i=1}^N$$ 的对数似然计算方式如下:

$$
    \log \prod_{i=1}^N p_{\theta}(\bm{x}^{(i)}) = \sum_{i=1}^N\log  p_{\theta}(\bm{x}^{(i)})
$$

假设我们可以采样从数据分布 $$q(\bm{x}_0)$$ 采样到所有的值, 那么对数似然就是函数 $$\log p(\bm{x}_0)$$ 的期望, 用积分可以写为

$$
    \begin{align}
        L &= \int d\bm{x}_0 q(\bm{x}_0) \log p(\bm{x}_0) \\ \label{eq:log_likelihood}
        &= \int d\bm{x}_0 q(\bm{x}_0)\cdot \underline{\log\left[\int d\bm{x}_{1:T}\,q(\bm{x}_{1:T}\vert \bm{x}_0) \cdot p(\bm{x}_T) \prod_{t=1}^T\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_t\vert \bm{x}_{t-1})}\right]}
    \end{align}
$$

到这里没法直接往下用等式推导了. 但是我们可以利用 [琴生不等式 (Jensen's inequality)](https://en.wikipedia.org/wiki/Jensen%27s_inequality) 把对数符号拿到第二个积分符号里面. 

{% capture jensen_inequality %}
**一般陈述**: 过一个凸函数上任意两点所作割线一定在这两点间的函数图象的上方，即：

$$
    f(tx_1 + (1 - t)x_2) \leq tf(x_1) + (1 - t)f(x_2).
$$

其中 $$f(\cdot)$$ 为凸函数, 且 $$t\in[0, 1]$$. 琴生不等式有多种表述形式. 

**测度论下的概率形式的表述**: 假设 $$f(x)$$ 是个概率密度函数, 即满足 $$\int_{-\infty}^{\infty}f(x)dx=1$$. 如果 $$g$$ 是实值可测的函数, $$\phi$$ 是 $$g$$ 的值域上的一个<u>凸函数</u>, 那么有

$$
    \phi\left(\int_{\infty}^{\infty}dx f(x)g(x)\right) \leq \int_{\infty}^{\infty}dx f(x)\phi(g(x)).
$$

写成期望的形式为:

$$
    \phi\left(\mathbb{E}_{f(x)}[g(x)]\right) \leq \mathbb{E}_{f(x)}[\phi(g(x))]
$$
{% endcapture %}
{% include card.html type="info" title="琴生不等式 (Jensen's inequality) <a href=\"#jensen_inequality\">#</a>" content=jensen_inequality id="jensen_inequality" %}

我们对式 \eqref{eq:log_likelihood} 下划线的部分应用琴生不等式, 注意 $$\log$$ 是凹函数, 因此不等号要反过来. 从而我们有

$$
    \begin{align}
        L &\geq \int d\bm{x}_0 q(\bm{x}_0)\cdot \underline{\int d\bm{x}_{1:T}\,q(\bm{x}_{1:T}\vert \bm{x}_0) \cdot \log\left[p(\bm{x}_T) \prod_{t=1}^T\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_t\vert \bm{x}_{t-1})}\right]} \\ \label{eq:lower_bound}
        &= \int d\bm{x}_{0:T}\,q(\bm{x}_{0:T}) \cdot \log\left[p(\bm{x}_T) \prod_{t=1}^T\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_t\vert \bm{x}_{t-1})}\right] \triangleq K.
    \end{align}
$$

这样式 \eqref{eq:lower_bound} 就是 $$L$$ 的一个下界, 我们把这个下界记为 $$K$$. 

为了让这个下界更容易计算, 原文对 $$K$$ 做了一些拆解和变换 (论文附录 B). 首先<span style="color:red">论文中假定对于任意 $$t=1,\cdots,T$$, (交叉)熵</span> 

$$ \label{eq:assumption}\color{red}{
    \int d\bm{x}_t q(\bm{x}_t)\log q(\bm{x}_t) = \int d\bm{x}_t q(\bm{x}_t)\log p(\bm{x}_t) = -\mathbb{H}_p(\bm{x}_T) 
}
$$ 

<span style="color:red">是个常数. (为什么?)</span> 然后我们分别考虑 $$K$$ 的三个部分,

**第一部分: $$p(\bm{x}_T)$$ 的处理**

把 $$p(\bm{x}_T)$$ 分离出来, 有

$$
    \begin{align} \label{eq:tmp1}
        K &= \int d\bm{x}_{0:T}\,q(\bm{x}_{0:T}) \sum_{t=1}^T\log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_t\vert \bm{x}_{t-1})}\right] + \int d\bm{x}_T q(\bm{x}_T)\log p(\bm{x}_T) \\ \label{eq:tmp2}
        &= \sum_{t=1}^T\int d\bm{x}_{0:T}\,q(\bm{x}_{0:T})\log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_t\vert \bm{x}_{t-1})}\right] - \mathbb{H}_p(\bm{x}_T)
    \end{align}
$$

根据反向过程最后的规定, 前向过程的边际分布 $$q(\bm{x}_T)$$ 与反向过程的边际分布 $$p(\bm{x}_T)$$ 是相同的分布, 那么式 \eqref{eq:tmp1} 的最后一项交叉熵就可以写为 $$p(\bm{x}_T)$$ 的熵 $$\mathbb{H}_p(\bm{x}_T)$$ .

**第二部分: $$t=0$$ 时的边缘效应**

为了避免边缘效应 (具体是什么呢? 作者没有说), 我们定义反向过程的最后一步等于前向过程的第一步:

$$
    \begin{align}
        & p(\bm{x}_0, \bm{x}_1) = q(\bm{x}_0, \bm{x}_1) \\ \label{eq:item1}
        \Rightarrow\quad & \frac{p(\bm{x}_0\vert \bm{x}_1)}{q(\bm{x}_1\vert \bm{x}_0)} = \frac{q(\bm{x}_0)}{p(\bm{x}_1)}
    \end{align}
$$

然后我们可以把式 \eqref{eq:tmp2} 中 $$t=1$$ 的项分离出来:

$$
    \begin{align}
        &\int d\bm{x}_0 d\bm{x}_1\,q(\bm{x}_0,\bm{x}_1)\log\left[\frac{p(\bm{x}_0\vert\bm{x}_1)}{q(\bm{x}_1\vert \bm{x}_0)}\right] \\
        =& \int d\bm{x}_0 d\bm{x}_1\,q(\bm{x}_0,\bm{x}_1)\log\left[\frac{q(\bm{x}_0)}{p(\bm{x}_1)}\right] &  {\small 根据式 \eqref{eq:item1}} \\
        =& \int d\bm{x}_0\,q(\bm{x}_0)\log q(\bm{x}_0) - \int d\bm{x}_1\,q(\bm{x}_1)\log p(\bm{x}_1) \log  \\
        =& \mathbb{H}_p(\bm{x}_T) - \mathbb{H}_p(\bm{x}_T) & {\small 根据式 \eqref{eq:assumption}} \\
        =& 0
    \end{align}
$$

**第三部分: 重写后验概率 $$q(\bm{x}_{t-1}\vert\bm{x}_0)$$**

由于前向过程是马尔科夫过程, 所以可以把 $$\bm{x}_0$$ 作为条件直接加入 $$q(\bm{x}_t\vert \bm{x}_{t-1})$$, 我们有: 

$$
    \begin{flalign}
        K &= \sum_{t=2}^T\int d\bm{x}_{0:T}\,q(\bm{x}_{0:T})\log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_t\vert \bm{x}_{t-1},\bm{x}_0)}\right] - \mathbb{H}_p(\bm{x}_T) \\
        &= \sum_{t=2}^T\int d\bm{x}_{0:T}\,q(\bm{x}_{0:T})\log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_{t-1}\vert \bm{x}_t,\bm{x}_0)}\frac{q(\bm{x}_{t-1}\vert\bm{x}_0)}{q(\bm{x}_t\vert\bm{x}_0)}\right] - \mathbb{H}_p(\boldsymbol{x}_T) & {\small \text{Bayes }公式} \\
        &= \sum_{t=2}^T\int d\bm{x}_{0:T}\,q(\bm{x}_{0:T})\log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_{t-1}\vert \bm{x}_t,\bm{x}_0)}\right] + \sum_{t=2}^T[\mathbb{H}_q(\bm{x}_t\vert\bm{x}_0) - \mathbb{H}_q(\bm{x}_{t-1}\vert\bm{x}_0)] - \mathbb{H}_p(\boldsymbol{x}_T) \\
        &= \sum_{t=2}^T\int d\bm{x}_{0:T}\,q(\bm{x}_{0:T})\log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_{t-1}\vert \bm{x}_t,\bm{x}_0)}\right] + \mathbb{H}_q(\bm{x}_T\vert\bm{x}_0) - \mathbb{H}_q(\bm{x}_1\vert\bm{x}_0) - \mathbb{H}_p(\boldsymbol{x}_T) \\ \label{eq:before_final}
        &= \sum_{t=2}^T\int d\bm{x}_{0:T}\,q(\bm{x}_{0:T})\log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_{t-1}\vert \bm{x}_t,\bm{x}_0)}\right] + \mathbb{H}_q(\bm{x}_T\vert\bm{x}_0) - \mathbb{H}_q(\bm{x}_1\vert\bm{x}_0) - \mathbb{H}_p(\boldsymbol{x}_T)
    \end{flalign}
$$

我们对式 \eqref{eq:before_final} 的求和符号后单项的多元积分进行拆解, 有:

$$
    \begin{flalign}
        &\int d\bm{x}_{0:T}\,q(\bm{x}_{0:T})\log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_{t-1}\vert \bm{x}_t,\bm{x}_0)}\right] \\
        =& \int d\bm{x}_0 d\bm{x}_{t-1} d\bm{x}_t\,q(\bm{x}_0,\bm{x}_{t-1},\bm{x}_t)\log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_{t-1}\vert \bm{x}_t,\bm{x}_0)}\right] & {\small 除 \bm{x}_0, \bm{x}_{t-1}, \bm{x}_t 以外的变量积分为 1 } \\
        =& \int d\bm{x}_0 d\bm{x}_t\,q(\bm{x}_0,\bm{x}_t) \underbrace{\int d\bm{x}_{t-1}\,q(\bm{x}_{t-1}\vert \bm{x}_t,\bm{x}_0) \log\left[\frac{p(\bm{x}_{t-1}\vert\bm{x}_t)}{q(\bm{x}_{t-1}\vert \bm{x}_t,\bm{x}_0)}\right]}_{\text{负 KL 散度}} & {\small 条件概率} \\
    \end{flalign}
$$

所以式 \eqref{eq:before_final} 可以变为:

$$
    \begin{multline} \label{eq:final}
    K = -\sum_{t=2}^T\int d\bm{x}_0 d\bm{x}_t\,q(\bm{x}_0,\bm{x}_t)\mathbb{KL}\left(q(\bm{x}_{t-1}\vert\bm{x}_t,\bm{x}_0)\Vert p(\bm{x}_{t-1}\vert \bm{x}_t)\right) \\
     + \mathbb{H}_q(\bm{x}_T\vert\bm{x}_0) - \mathbb{H}_q(\bm{x}_1\vert\bm{x}_0) - \mathbb{H}_p(\boldsymbol{x}_T)
    \end{multline}
$$

现在式 \eqref{eq:final} 的每一项交叉熵和 KL 散度都是易处理的. 具体的处理方法我们将会在 [《生成扩散模型(四): 扩散模型和得分匹配》](/2022/11/28/Diffusion-Model-4/) 中给出.

在训练时, 作者把扩散步长 $$\beta_{2:T}$$ 作为可学习的参数, 并固定了第一步的步长 $$\beta_1$$ 为一个很小的数来避免过拟合. 从 $$q(\bm{x}_{1:T}\vert\bm{x}_0)$$ 中采样的样本对于 $$\beta_{1:T}$$ 的依赖可以使用 [《变分自编码器 (VAE)》](https://arxiv.org/abs/1312.6114) 中的重参数化技巧作为额外的随机变量来计算.
