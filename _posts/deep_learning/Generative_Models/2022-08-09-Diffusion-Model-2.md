---
layout: post
title: "生成扩散模型(二): VAE 观点 (Generative Diffusion Model: From the Perspective of VAE)"
date: 2022-08-09 18:11:00 +0800
categories: 深度学习 生成模型
mathjax: true
author: Jarvis
meta: Post
---

* content
{:toc}

我们在前面一篇文章[《生成扩散模型(一): 基础》](/2022/08/08/Diffusion-Model-1/)中通过迭代式的图像加噪和去噪的角度分析了生成扩散模型, 并最终推导出了和 DDPM 论文中一样的损失函数. 如果我们把图像加噪的过程看作编码, 把去噪的过程看作解码, 那么这两个过程合起来就可以看作一个[自动编码器 (autoencoder)](https://en.wikipedia.org/wiki/Autoencoder). 



本文就从自动编码器的角度重新审视 DDPM[^2] 中的扩散模型, 同时本文的内容主要来自于[^1]. 

## 从单步到多步

自动编码器包含编码器 (encoder) 和解码器 (decoder) 两部分, 即

$$
\begin{align}
    \pmb{z} = \text{Encoder}(\pmb{x}) \\
    \bar{\pmb{x}} = \text{Decoder}(\pmb{z})
\end{align}
$$

其中 encoder 和 decoder 通常可以用神经网络来建模, 而神经网络中输入和输出的中间过程是黑盒模型, 缺乏好的解释. 那么我们想到就像加噪/去噪那样, 可以对编码和解码的过程拆解为一个个小步骤, 每个小步骤用更简单的模型来表达, 同时我们把编码和解码的过程定义为加噪和去噪的过程, 从而让每个小步骤的输入和输出具有更好的解释性

$$
\begin{align}
    \text{Encoder: } \pmb{x} = \pmb{x}_0 \rightarrow \pmb{x}_1 \rightarrow \cdots \pmb{x}_{T-1} \rightarrow \pmb{x}_T = \pmb{z} \\
    \text{Decoder: } \pmb{z} = \pmb{x}_T \rightarrow \pmb{x}_{T-1} \rightarrow \cdots \pmb{x}_1 \rightarrow \pmb{x}_0 = \pmb{x} \\
\end{align}
$$

[前一篇文章](/2022/08/08/Diffusion-Model-1/)我们定义加噪的时候, 是把图像分解为带噪图像和噪声的加权和. 本文用更一般的概率分布的形式来表达, 即一步编码为 $p(\pmb{x}_t\vert\pmb{x}_{t-1})$, 一步解码为 $q(\pmb{x}_{t-1}\vert\pmb{x}_t)$. 同时我们假设上面的每一步分解过程只依赖于前一步的结果, 这在随机过程中也被称为[马尔可夫性质](https://en.wikipedia.org/wiki/Markov_property). 有了这个假设, 我们就可以把编解码过程中所有输出的联合分布表示为

$$
\begin{align}
p(\pmb{x}_0,\pmb{x}_1,\cdots,\pmb{x}_T) &= p(\pmb{x}_T\vert\pmb{x}_{T-1})\cdots p(\pmb{x}_2\vert\pmb{x}_1)p(\pmb{x}_1\vert\pmb{x}_0)p(\pmb{x}_0) \\
q(\pmb{x}_0,\pmb{x}_1,\cdots,\pmb{x}_T) &= q(\pmb{x}_0\vert\pmb{x}_{1})\cdots q(\pmb{x}_{T-2}\vert\pmb{x}_{T-1})q(\pmb{x}_{T-1}\vert\pmb{x}_T)q(\pmb{x}_T) \\
\end{align}
$$

其中 $p(\pmb{x}_0)$ 就是数据分布, $q(\pmb{x}_T)$ 就是编码输出分布. 

同样的输出 ($\pmb{x}_0,\pmb{x}_1,\cdots,\pmb{x}_T$), 两种不同的模型来表示, 因此我们可以通过极小化两个联合分布的 [KL 散度](/2018/09/18/Information-Theory/)来优化模型参数

$$ \label{eq:kl0}
\mathbb{KL}(p\Vert q)=\int p(\pmb{x}_T\vert\pmb{x}_{T-1})\cdots p(\pmb{x}_1\vert\pmb{x}_0)p(\pmb{x}_0) \log\frac{p(\pmb{x}_T\vert\pmb{x}_{T-1})\cdots p(\pmb{x}_1\vert\pmb{x}_0)p(\pmb{x}_0)}{q(\pmb{x}_0\vert\pmb{x}_{1})\cdots q(\pmb{x}_{T-1}\vert\pmb{x}_T)q(\pmb{x}_T)}d\pmb{x}_0\cdots d\pmb{x}_T
$$

单步编码从加噪的角度来看就是 $\pmb{x}_t = \alpha_t\pmb{x}_{t-1} + \beta_t\pmb{e}_t, \; \pmb{e}_t\sim\mathcal{N}(\pmb{0},\pmb{I})$. 如果我们把等号右侧看作一个整体的分布的话, 那么就可以看作已知 $\pmb{x}_{t-1}$ 时 $\pmb{x}_t$ 的条件分布
$p(\pmb{x}_t\vert \pmb{x}_{t−1}) := \mathcal{N}(\pmb{x}_t; \alpha_t\pmb{x}_{t−1},\beta_t^2\pmb{I})$. 反过来, $q(\pmb{x}_{t-1}\vert\pmb{x}_t)$ 则建模成了可学习的正态分布 $\mathcal{N}(\pmb{x}_{t-1};\pmb{\mu}(\pmb{x}_t), \sigma_t^2\pmb{I})$. 其中 $\alpha_t,\beta_t,\sigma_t$ 都是超参数. 解码过程建模成了可学习的正态分布, 这一点跟[《变分自动编码器 (VAE)》](https://arxiv.org/abs/1312.6114) 是类似的. 但与 VAE 不同的是, DDPM 为了简化计算过程放弃了建模方差, 只建模了均值. 

由于分布 $p(\pmb{x}_t\vert \pmb{x}_{t−1})$ 都是固定的, 因此 \eqref{eq:kl0} 式作为损失函数时可以丢掉 $p\log p$ 的项, 从而有

$$
-\int p(\pmb{x}_T\vert\pmb{x}_{T-1})\cdots p(\pmb{x}_1\vert\pmb{x}_0)p(\pmb{x}_0) \left[ \log q(\pmb{x}_T) + \sum_{t=1}^T \log q(\pmb{x}_{t-1}\vert\pmb{x}_t) \right] d\pmb{x}_0\cdots d\pmb{x}_T
$$

其中 $q(\pmb{x}_T)$ 也没有可训练的参数, 所以上式进一步简化为

$$
-\sum_{t=1}^T \int p(\pmb{x}_T\vert\pmb{x}_{T-1})\cdots p(\pmb{x}_1\vert\pmb{x}_0)p(\pmb{x}_0) \log q(\pmb{x}_{t-1}\vert\pmb{x}_t) d\pmb{x}_0\cdots d\pmb{x}_T
$$

下面我们考虑求和号里面的每一项

$$
\begin{align} \nonumber
& -\int p(\pmb{x}_T\vert\pmb{x}_{T-1})\cdots p(\pmb{x}_1\vert\pmb{x}_0)p(\pmb{x}_0) \log q(\pmb{x}_{t-1}\vert\pmb{x}_t) d\pmb{x}_0\cdots d\pmb{x}_T \\ \nonumber
=& -\int p(\pmb{x}_t\vert\pmb{x}_{t-1})\cdots p(\pmb{x}_1\vert\pmb{x}_0)p(\pmb{x}_0) \log q(\pmb{x}_{t-1}\vert\pmb{x}_t) d\pmb{x}_0\cdots d\pmb{x}_t\\ \label{eq:goal}
=& -\int p(\pmb{x}_t\vert\pmb{x}_{t-1})p(\pmb{x}_{t-1}\vert\pmb{x}_0)p(\pmb{x}_0) \log q(\pmb{x}_{t-1}\vert\pmb{x}_t) d\pmb{x}_0 d\pmb{x}_{t-1} d\pmb{x}_t 
\end{align}
$$

其中第一个等号是因为 $q(\pmb{x}_{t-1}\vert\pmb{x}_t)$ 只依赖到 $\pmb{x}_t$, 因此 $\pmb{x}_{t+1}$ 到 $\pmb{x}_T$ 的联合分布可以直接积分为 $1$. 第二个等号的积分为

$$
\begin{align} \nonumber
\int p(\pmb{x}_{t-1}\vert\pmb{x}_{t-2})\cdots p(\pmb{x}_1\vert\pmb{x}_0) d\pmb{x}_1\cdots d\pmb{x}_{t-2} &= p(\pmb{x}_{t-1}\vert\pmb{x}_0) \\
&= \mathcal{N}(\pmb{x}_{t-1};\bar\alpha_{t-1}\pmb{x}_0, \bar\beta_{t-1}^2\pmb{I})
\end{align}
$$

其中第二个等号的计算可以借助 [《生成扩散模型(一): 基础》](/2022/08/08/Diffusion-Model-1/#mjx-eqn-eq%3Axt_x0_2) 中的公式 (5) $\pmb{x}_t = \bar{\alpha}_t\pmb{x}_0 + \bar\beta_t\pmb{e}_t$ 把 $t$ 换为 $t-1$ 然后改写成分布的形式得到. 

此时我们分解一下上面的优化目标 \eqref{eq:goal} 式, 有

$$
\begin{align}
p(\pmb{x}_t\vert\pmb{x}_{t-1}) &\Rightarrow \pmb{x}_{t−1}=\frac1{\alpha_t}(\pmb{x}_t−\beta_t\pmb{\varepsilon}_t)  \\
p(\pmb{x}_{t-1}\vert\pmb{x}_0) &\Rightarrow \pmb{x}_{t−1}=\bar\alpha_t\pmb{x}_0+\bar\beta_t\pmb{\varepsilon}_{t−1} \\
p(\pmb{x}_0)                   &\Rightarrow \\ 
-q(\pmb{x}_{t-1}\vert\pmb{x}_t) &\Rightarrow \frac1{2\sigma_t^2}\Vert \pmb{x}_{t-1} - \pmb\mu(\pmb{x}_t) \Vert_2^2 \\
\pmb{\mu}(\pmb{x}_t) &= \frac1{\alpha_t}(\pmb{x}_t−\beta_t\pmb{\varepsilon}_t)
\end{align}
$$




<br/>
<br/>
<br/>
<br/>
<br/>
<br/>


[^1]:
    **生成扩散模型漫谈（二）：DDPM = 自回归式VAE**, 苏剑林, In 科学空间, 2022, [[html](https://spaces.ac.cn/archives/9152)]

[^2]:
    **Denoising Diffusion Probabilistic Models**, Jonathan Ho, Ajay Jain, Pieter Abbeel, In NeruIPS, 2020, [[Paper](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html), [WebSite](https://hojonathanho.github.io/diffusion/), [Official TF-1.15 Code](https://github.com/hojonathanho/diffusion), [3rd Party PyTorch Code](https://github.com/lucidrains/denoising-diffusion-pytorch)]