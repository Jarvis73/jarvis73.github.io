---
layout: post
title: "生成扩散模型(四): 扩散模型和得分匹配 (Generative Diffusion Model: Diffusion Matching and Score Matching)"
date: 2022-11-29 14:01:00 +0800
categories: 深度学习 生成模型
mathjax: true
author: Jarvis
meta: Post
---

* content
{:toc}

我们在[《生成扩散模型(三): 灵活性和易处理性》](/2022/11/27/Diffusion-Model-3/)一文中讨论了生成扩散模型对前向过程和反向过程的建模, 以及训练模型时所使用的极大化似然函数的推导. 然而先前的扩散模型的生成效果仍然有限, Ho 等人在 DDPM 一文 [《Denoising Deffision Probabilistic Models》](https://arxiv.org/abs/2006.11239) 中指出扩散模型实际上可以生成更高质量的样本. 同时, 扩散模型在选择特定超参数的情况下与 [去噪得分匹配 (denoising score matching)]() 的训练过程和基于 [退火的朗之万动力学(annealed Langevin dynamics)]() 的采样过程是等价的.



## 背景回顾

**反向过程** $$\newcommand{\xx}{\bm{x}} \newcommand{\pt}{p_{\theta}} \newcommand{\mt}{\bm{\mu}_{\theta}} \newcommand{\st}{\bm{\Sigma}_{\theta}}$$ 

扩散模型是个隐变量模型 $$p_{\theta}(\xx_0)\triangleq\int p_{\theta}(\xx_{0:T})d\xx_{1:T}$$, 其中 $$\xx_0 \sim q(\xx_0)$$ 是观测变量, $$\xx_1,\cdots,\xx_T$$ 是隐变量. 其反向过程 $$p_{\theta}(\xx_{0:T})$$ 是一个马尔科夫链, 从状态 $$p(\xx_T)=\mathcal{N}(\xx_T;\bm{0},\bm{I})$$ 开始, 转移变换 $$p_{\theta}(\xx_{t-1}\vert\xx_t)$$ 通过神经网络学习出来, 其中 $$\theta$$ 是模型参数:

$$
    \pt(\xx_T)\prod_{t=1}^T\pt(\xx_{t-1}\vert\xx_t), \quad \pt(\xx_{t-1}\vert\xx_t) \triangleq\mathcal{N}(\xx_{t-1};\mt(\xx_t,t),\st(\xx_t, t)).
$$

这里的转移变换 $$\pt(\xx_{t-1}\vert\xx_t)$$ 定义为正态分布, 其均值向量 $$\mt(\xx_t,t)$$ 和协方差矩阵 $$\st(\xx_t, t)$$ 是我们需要通过模型得到的.

**前向过程**

扩散模型区别于其他隐变量模型的地方在于隐变量的后验概率 $$q(\xx_{1:T}\vert\xx_0)$$ 也定义为一个马尔科夫链 (称为扩散过程或者正向过程), 其转移变换为在数据上不断增加方差为 $$\beta_1,\cdots,\beta_T$$ 的高斯噪声:

$$ \label{eq:transform}
    q(\xx_{1:T}\vert\xx_0) \triangleq \prod_{t=1}^T q(\xx_t\vert\xx_{t-1}), \quad q(\xx_t\vert\xx_{t-1}) \triangleq \mathcal{N}(\xx_t;\sqrt{1-\beta_t}\xx_{t-1}, \beta_t\bm{I}).
$$

注意这里 $$\beta_t$$ 是接近于 0 的数, 所以正向过程每次只增加一点点高斯噪声, 这有利于模型的学习(只学习简单的去噪任务, 训练可以变得更容易).

前向过程有个特点是, 给定任意 $$\xx_0$$, 我们可以直接计算出任意时刻 $$t$$ 的条件边际分布 $$q(\xx_t\vert\xx_0)$$. 不妨把式 \eqref{eq:transform} 的递推式利用[《重参数化技巧》](/2022/09/05/Normal-Distribution/#重参数化技巧)写为

$$ \label{eq:reparam}
    \xx_t = \sqrt{\alpha_t}\xx_{t-1} + \sqrt{1-\alpha_t}\bm{\epsilon}_t, \quad \alpha_t \triangleq 1 - \beta_t, \quad \bm{\epsilon}_t\in\mathcal{N}(\bm{0}, \bm{I}).
$$

注意 $$q(\xx_t\vert\xx_{t-1})$$ 的定义方式使得重参数化后 $$\xx_{t-1}$$ 和 $$\bm{\epsilon}$$ 的系数的平方和为 $$1$$. 这样的定义方式可以便于我们后续的推导. 由此我们可以对式 \eqref{eq:reparam} 自行迭代得到

$$
    \begin{align}
        \xx_t &= \sqrt{\alpha_t}\xx_{t-1} + \sqrt{1-\alpha_t}\bm{\epsilon}_t \\
        &= \sqrt{\alpha_t}(\sqrt{\alpha_{t-1}}\xx_{t-2} + \sqrt{1-\alpha_{t-1}}\bm{\epsilon}_{t-1}) + \sqrt{1-\alpha_t}\bm{\epsilon}_t \\
        &= \sqrt{\alpha_t\alpha_{t-1}}\xx_{t-2} + \underline{\sqrt{\alpha_t(1-\alpha_{t-1})}\bm{\epsilon}_{t-1} + \sqrt{1-\alpha_t}\bm{\epsilon}_t} \\
        &= \sqrt{\alpha_t\alpha_{t-1}}\xx_{t-2} + \sqrt{1-\alpha_{t-1}\alpha_t}\bm{\epsilon}' & {\small 正态分布随机变量的和} \\
        &= \cdots \\
        &= \sqrt{\alpha_t\alpha_{t-1}\cdots\alpha_1}\xx_0 + \sqrt{1-\alpha_t\alpha_{t-1}\cdots\alpha_1}\bm{\epsilon} & {\small 一直迭代直到 \xx_0} \\ \label{eq:xt_x0}
        &= \sqrt{\bar{\alpha}_t}\xx_0 + \sqrt{1-\bar{\alpha}_t}\bm{\epsilon} & {\small \bar{\alpha}_t\triangleq \alpha_t\alpha_{t-1}\cdots\alpha_1}
    \end{align}
$$

注意上面划线的部分, 两个服从正态分布的独立随机变量的和仍是个正态分布, 我们不妨把它记为 $$\bm{\epsilon}'$$. 其均值仍为 $$0$$ , 方差为

$$
    \begin{align}
        & \left(\sqrt{\alpha_t(1-\alpha_{t-1})}\right)^2 + \left(\sqrt{1-\alpha_t}\right)^2 \\
        =& \alpha_t - \alpha_t\alpha_{t-1} + 1 - \alpha_t \\
        =& 1 - \alpha_{t-1}\alpha_t
    \end{align}
$$

详见[《正态分布随机变量的和》](/2022/09/05/Normal-Distribution/#正态分布随机变量的和).

根据式 \eqref{eq:xt_x0}, 反向重参数化后我们有

$$ \label{eq:xt_x0_dist}
    q(\xx_t\vert\xx_0) = \mathcal{N}(\xx_t;\sqrt{\bar{\alpha}_t}\xx_0, (1-\bar{\alpha}_t)\bm{I}).
$$

这样我们可以直接根据定义的 $$\beta_t$$ 序列和采样的 $$\xx_0$$, 一次性采样得到 $$\xx_t$$. 

**优化目标**

与 Sohl-Dickstein 在 2015 年的工作相同 (见 [《生成扩散模型(三): 灵活性和易处理性》](/2022/11/27/Diffusion-Model-3/#%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B)), DDPM 的优化目标是<u>极小化<strong>负</strong>对数似然</u>:

$$
    \begin{align}
        &\mathbb{E}_{q(\xx_0)}[-\log\pt(\xx_0)] \\
        =\;& \mathbb{E}_{q(\xx_0)}\left[-\log\int\pt(\xx_{0:T})d\xx_{1:T}\right] & {\small 边际分布 \rightarrow 联合分布} \\
        =\;& \mathbb{E}_{q(\xx_0)}\left[-\log\int\frac{\pt(\xx_{0:T})}{q(\xx_{1:T}\vert\xx_0)}\cdot q(\xx_{1:T}\vert\xx_0)d\xx_{1:T}\right] & {\small 分子分母同乘以前向过程} \\
        =\;& \mathbb{E}_{q(\xx_0)}\left[-\log\mathbb{E}_{q(\xx_{1:T}\vert\xx_0)}\left[\frac{\pt(\xx_{0:T})}{q(\xx_{1:T}\vert\xx_0)}\right] \right] & {\small 积分写成期望} \\
        \leq\;& \mathbb{E}_{q(\xx_0)}\left[\mathbb{E}_{q(\xx_{1:T}\vert\xx_0)}\left[-\log\frac{\pt(\xx_{0:T})}{q(\xx_{1:T}\vert\xx_0)}\right] \right] & {\small 琴生不等式} \\
        =\;& \mathbb{E}_{q(\xx_{1:T})}\left[-\log\frac{\pt(\xx_{0:T})}{q(\xx_{1:T}\vert\xx_0)}\right]
    \end{align}
$$

其中的小于等于号是根据 [琴生不等式(Jensen's inequality)](/2022/11/27/Diffusion-Model-3/#jensen_inequality) 的期望形式得到的.

到了这一步, Sohl-Dickstein 是根据交叉熵为常数进行推导的, 最后是以 KL 散度和熵的形式表达的. 而 DDPM 中的推导略有不同 (附录A), 最终为

$$
    \begin{multline} \label{eq:obj}
        \mathbb{E}_{q(\xx_0)}[\underbrace{\mathbb{KL}(q(\xx_T\vert\xx_0)\Vert p(\xx_T))}_{L_T}] \\
        + \sum_{t=2}^T\mathbb{E}_{q(\xx_0,\xx_t)}[\underbrace{\mathbb{KL}(q(\xx_{t-1}\vert\xx_t,\xx_0)\Vert \pt(\xx_{t-1}\vert\xx_t))}_{L_{t-1}}] \\
         - \mathbb{E}_{q(\xx_1)}[\underbrace{\log\pt(\xx_0\vert\xx_1)}_{L_0}]
    \end{multline}
$$

注意论文中把三个期望统一写成了 $$\mathbb{E}_q$$ 了, 会让人比较困惑, 我们这里还是分开写.

下面我们考虑式 \eqref{eq:obj} 中各项的易处理性. $$L_T$$ 的 $$q(\xx_T\vert\xx_0)$$ 和 $$p(\xx_T)$$ 都有确切表达式; $$L_0$$ 中的 $$\pt(\xx_0\vert\xx_1)$$ 可以由模型给出; $$L_{1:T-1}$$ 中的 $$\pt(\xx_{t-1}\vert\xx_t)$$ 也可以由模型给出, 最后只剩 $$q(\xx_{t-1}\vert\xx_t,\xx_0)$$. 我们发现, 尽管 $$q(\xx_{t-1}\vert\xx_t)$$ 是不易处理的 (用 Bayes 公式变换得到 $$q(\xx_{t-1}\vert\xx_t)=\frac{q(\xx_t\vert\xx_{t-1})p(\xx_{t-1})}{p(\xx_t)}$$, 但 $$p(\xx_t)$$ 和 $$p(\xx_{t-1})$$ 都不易获得), 但我们知道如果以 $$\xx_0$$ 为条件的话, $$p(\xx_t\vert\xx_0)$$ 和 $$p(\xx_{t-1}\vert\xx_0)$$ 都是有确切表达式的 (式 \eqref{eq:xt_x0} 或 \eqref{eq:xt_x0_dist}). 因此我们考虑用 Bayes 公式来计算:

$$
    \begin{align}
        q(\xx_{t-1}\vert\xx_t,\xx_0) &= \frac{q(\xx_t\vert\xx_{t-1},\xx_0)q(\xx_{t-1}\vert\xx_0)}{p(\xx_t\vert\xx_0)} \\  \label{eq:xtm1_xt_x0}
        &= \frac{q(\xx_t\vert\xx_{t-1})q(\xx_{t-1}\vert\xx_0)}{q(\xx_t\vert\xx_0)} & {\small 前向过程是马尔科夫的, \xx_0 可以省略}
    \end{align}
$$

下面我们把式 \eqref{eq:transform} 和式 \eqref{eq:xt_x0_dist} 高斯分布的密度函数代入式子 \eqref{eq:xtm1_xt_x0} 得到:

$$
    \begin{align}
        & q(\xx_{t-1}\vert\xx_t,\xx_0) = \frac{q(\xx_t\vert\xx_{t-1})q(\xx_{t-1}\vert\xx_0)}{q(\xx_t\vert\xx_0)} \\ \label{eq:density}
        &= C_1\cdot\exp\left(-\frac12\left(
            \frac{\Vert\xx_t-\sqrt{1-\beta_t}\xx_{t-1}\Vert^2}{\beta_t}
            + \frac{\Vert\xx_{t-1}-\sqrt{\bar{\alpha}_{t-1}}\xx_0\Vert^2}{1-\bar{\alpha}_{t-1}}
            - \frac{\Vert\xx_t-\sqrt{\bar{\alpha}_t}\xx_0\Vert^2}{1-\bar{\alpha}_t}
        \right)\right) \\
        &\triangleq C_2\cdot\exp\left(-\frac{(\xx_{t-1} - \tilde{\bm{\mu}}_t)^2}{2\tilde{\beta}_t}\right)
    \end{align}
$$

可以看到式 \eqref{eq:density} 除去常数 $$C_1$$, 指数和 $$-\frac12$$, 里面的部分是 $$\xx_{t-1}$$ 的二次函数, 这符合正态分布的形式, 所以我们直接通过待定系数法可以解出 $$\tilde{\bm{\mu}}_t$$ 和 $$\tilde{\beta}_t$$ 的表达式如下 (注意用到了前面定义的 $$\alpha_t=1-\beta_t$$ 和 $$\bar{\alpha}_t=\bar{\alpha}_{t-1}\cdot\alpha_t$$):

$$ \label{eq:tilde_mu_t}
    \tilde{\bm{\mu}}_t = \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\xx_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t}\xx_0, \quad \tilde{\beta}_t = \frac{1-\bar{\alpha}_{t - 1}}{1-\bar{\alpha}_t}\beta_t
$$

因此我们有

$$
    q(\xx_{t-1}\vert\xx_t,\xx_0) = \mathcal{N}(\xx_{t-1}; \tilde{\bm{\mu}}_t(\xx_t,\xx_0), \tilde{\beta}_t\bm{I})
$$


## 扩散模型和去噪得分匹配

扩散模型在实现时需要定义一些东西: (1) 前向过程的方差序列 $$\beta_t$$, (2) 模型结构, (3) 反向过程高斯模型的参数化方式. 本文从去噪得分匹配模型得到启发, 给出了一种更实用的训练目标. 下面依次讨论式 \eqref{eq:obj} 的三个部分 $$L_0, L_{1:T-1}$$, 和 $$L_T$$ . 

**前向过程和 $$L_T$$**

DDPM 中固定了方差序列 $$\beta_t$$ 为常量 (Sohl-Dickstein 使用的是可训练的序列). 此外, 从式 \eqref{eq:obj} 中我们可以看到这一项的 KL 散度计算不依赖于任何的参数 ($$q(\xx_T\vert\xx_0)$$ 是预定义好的前向过程, $$p(\xx_T)$$ 是标准正态分布), 因此损失函数中可以直接去掉这一项.

**反向过程和 $$L_{1:T-1}$$**

现在考虑 $$\pt(\xx_{t-1}\vert\xx_t)=\mathcal{N}(\xx_{t-1};\mt(\xx_t,t),\st(\xx_t,t))$$ 在 $$1<t<T$$ 时模型的定义方式. 

首先, DDPM 中把协方差矩阵 $$\st(\xx_t,t)\triangleq\sigma_t^2\bm{I}$$ 定义仅依赖时间步 $$t$$ 的常量. 作者实验了 $$\sigma^2_t=\beta_t$$ 和 $$\sigma^2_t=\tilde{\beta}_t$$ 这两种策略, 发现效果差不多. 特别地, 这两种情况分别是 $$\xx_0\sim\mathcal{\bm{0},\bm{I}}$$ 和 $$\xx_0$$ 只有一个点这两种情况的最优解, 这两种 $$\sigma^2$$ 的选择实际上对应了反向过程熵上下界. 

其次, 我们考虑均值向量 $$\mt(\xx_t,t)$$. 由于 $$q(\xx_{t-1}\vert\xx_t,\xx_0)$$ 和 $$\pt(\xx_{t-1}\vert\xx_t))$$ 都是正态分布, 根据 [《正态分布的 KL 散度》](/2022/09/05/Normal-Distribution/#正态分布的-kl-散度), 我们有

$$ \label{eq:L_tm1}
    L_{t-1} = \mathbb{E}_{q(\xx_0,\xx_t)}\left[\frac1{2\sigma^2_t}\Vert \tilde{\bm{\mu}}_t(\xx_t,\xx_0) - \mt(\xx_t,t) \Vert^2\right] + C
$$

其中 $$C$$ 是只跟方差有关的一个常数, 不依赖于 $$\theta$$. 所以我们可以把模型定义为 $$\mt$$, 然后来预测 $$\tilde{\bm{\mu}}_t$$. 但是这样我们需要同时采样 $$\xx_0$$ 和 $$\xx_t$$ 才能得到 $$\tilde{\bm{\mu}}_t$$ (式 \eqref{eq:tilde_mu_t}), 涉及到两次随机采样, 这样会使得模型训练变得困难. 我们注意到 $$\xx_0$$ 可以用 $$\xx_t$$ 表示, 因此把式 \eqref{eq:xt_x0} 做个变形得到 

$$
    \xx_0=\frac1{\sqrt{\bar{\alpha}_t}}(\xx_t - \sqrt{1-\bar{\alpha}_t}\bm{\epsilon}),
$$

然后代入式 \eqref{eq:tilde_mu_t}, 有

$$
    \tilde{\bm{\mu}}_t(\xx_t,\xx_0) = \frac1{\sqrt{\alpha}_t}\left(\xx_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\bm{\epsilon}\right).
$$

而 $$\mt$$ 也依赖于 $$\xx_t$$, 那么如果定义为跟上式一样的形式, 即

$$ \label{eq:before_sampling}
    \mt(\xx_t,t) = \frac1{\sqrt{\alpha}_t}\left(\xx_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\bm{\epsilon}_{\theta}(\xx_t,t)\right).
$$

那么式 \eqref{eq:L_tm1} 就可以变成:

$$
    L_{t-1} = \mathbb{E}_{q(\xx_0),\bm{\epsilon}\sim\mathcal{N}(\bm{0},\bm{I})}\left[\frac{\beta_t^2}{2\sigma^2_t\alpha_t(1-\bar{\alpha}_t)}\Vert \bm{\epsilon} - \bm{\epsilon}_{\theta}(\xx_t,t) \Vert^2\right] + C.
$$

从而这一项损失可以变为

$$ \label{eq:L_tm1_final}
    \mathbb{E}_{q(\xx_0),\bm{\epsilon}\sim\mathcal{N}(\bm{0},\bm{I})}\left[\frac{\beta_t^2}{2\sigma^2_t\alpha_t(1-\bar{\alpha}_t)}\Vert \bm{\epsilon} - \bm{\epsilon}_{\theta}(\sqrt{\bar{\alpha}_t}\xx_0 + \sqrt{1-\bar{\alpha}_t}\bm{\epsilon},t) \Vert^2\right].
$$

注意上式中的两处 $$\bm{\epsilon}$$ 都是从 $$\xx_0$$ 生成 $$\xx_t$$ 时加的随机噪声, 因此它们可以用一次相同的采样. 

**去噪得分匹配**

现在我们需要的结论都有了, 再看一下和去噪得分匹配的关系. 我们考虑反向过程, 在给定 $$\xx_t$$ 时, 我们采样 $$\xx_{t-1}\sim \pt(\xx_{t-1}\vert\xx_t)$$ 的过程 (经过重参数化) 其实就是计算式 \eqref{eq:before_sampling} 加上一个高斯噪声, 即

$$ \label{eq:sampling}
    \xx_{t-1} = \frac1{\sqrt{\alpha}_t}\left(\xx_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\bm{\epsilon}_{\theta}(\xx_t,t)\right) + \sigma_t\bm{z},\quad \bm{z}\sim\mathcal{N}(\bm{0},\bm{I}).
$$

如果我们把 $$\bm{\epsilon}_{\theta}$$ 看作学习数据分布的梯度的话, 那么这个过程就和朗之万动力学采样类似了. 同时, 式 \eqref{eq:L_tm1_final} 的形式和多尺度噪声下的去噪得分匹配的形式也是一样的. 

**数据缩放, 反向过程解码器和 $$L_0$$**

由于后面直接把 $$L_0$$ 近似简化了, 并且效果不错. 所以这部分略显复杂的近似方案就略去了.

## 损失函数

DDPM 把最终的训练损失函数简化为

$$ \label{eq:loss}
    L_{\text{simple}}(\theta) \triangleq \mathbb{E}_{t,q(\xx_0),\bm{\epsilon}\sim\mathcal{N}(\bm{0},\bm{I})}\left[\Vert \bm{\epsilon} - \bm{\epsilon}_{\theta}(\sqrt{\bar{\alpha}_t}\xx_0 + \sqrt{1-\bar{\alpha}_t}\bm{\epsilon},t) \Vert^2\right]
$$

其中 $$t=1,2,\cdots,T$$. 那么 $$t=1$$ 的情况就对应了 $$L_0$$ 中的复杂的近似方案; $$1<t\leq T$$ 就对应了 $$L_{1:T-1}$$ 的情况, 而 $$L_T$$ 由于没有可训练的参数, 直接略去了. 

注意式子 \eqref{eq:loss} 相比于 \eqref{eq:L_tm1_final} 还去掉了系数 $$\frac{\beta_t^2}{2\sigma^2_t\alpha_t(1-\bar{\alpha}_t)}$$, 这样带来的效果就相当于使用 $$\bm{\epsilon}_{\theta}$$ 重构 $$\bm{\epsilon}$$ 时对不同的时间步 $$t$$ 使用了不同的权重. DDPM 中对这些参数的设置使得, 在 $$t$$ 较小时权重也较小, 从而可以让模型重点优化更困难的去噪步 ($$t$$ 比较大的时候, 即模型从高斯噪声初步生成目标轮廓的时候). 

## 算法总结

* 准备数据集: 相当于准备了 $$q(\xx_0)$$ 的一组子集
* 构建模型, 论文中采用改进的 U-Net 结构: 相当于建模了 $$\bm{\epsilon}_{\theta}(\cdot, \cdot)$$ 
* 执行训练循环:

> $$\text{for } \_ \text{ in range(total_steps)}:$$  
> $$\quad \xx_0\sim q(\xx_0)$$   
> $$\quad t\sim \text{Uniform}(\{1,\dots,T\})$$   
> $$\quad \bm{\epsilon}\sim\mathcal{N}(\bm{I},\bm{I})$$   
> $$\quad $$ 梯度更新:  
> $$\qquad \nabla_{\theta}\Vert \bm{\epsilon} - \bm{\epsilon}_{\theta}(\sqrt{\bar{\alpha}_t}\xx_0 + \sqrt{1-\bar{\alpha}_t}\bm{\epsilon},t) \Vert^2 \qquad$$   (式 \eqref{eq:loss})   

* 生成模型采样:

> $$\xx_T\sim\mathcal{N}(\bm{0},\bm{I})$$  
> $$\text{for } t \text{ in range} (T, 0):$$  
> $$\quad \bm{z}\sim\mathcal{N}(\bm{0},\bm{I}) \text{ if } t > 1, \text{ else } \xx_z=0$$   
> $$\quad \xx_{t-1} = \frac1{\sqrt{\alpha}_t}\left(\xx_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\bm{\epsilon}_{\theta}(\xx_t,t)\right) + \sigma_t\bm{z} \qquad$$   (式 \eqref{eq:sampling})   
> $$\text{Return } \xx_0$$ 
