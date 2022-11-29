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
    \bm{z} = \text{Encoder}(\bm{x}) \\
    \bar{\bm{x}} = \text{Decoder}(\bm{z})
\end{align}
$$

其中 encoder 和 decoder 通常可以用神经网络来建模, 而神经网络中输入和输出的中间过程是黑盒模型, 缺乏好的解释. 那么我们想到就像加噪/去噪那样, 可以对编码和解码的过程拆解为一个个小步骤, 每个小步骤用更简单的模型来表达, 同时我们把编码和解码的过程定义为加噪和去噪的过程, 从而让每个小步骤的输入和输出具有更好的解释性

$$
\begin{align}
    \text{Encoder: } \bm{x} = \bm{x}_0 \rightarrow \bm{x}_1 \rightarrow \cdots \bm{x}_{T-1} \rightarrow \bm{x}_T = \bm{z} \\
    \text{Decoder: } \bm{z} = \bm{x}_T \rightarrow \bm{x}_{T-1} \rightarrow \cdots \bm{x}_1 \rightarrow \bm{x}_0 = \bm{x} \\
\end{align}
$$

[前一篇文章](/2022/08/08/Diffusion-Model-1/)我们定义加噪的时候, 是把图像分解为带噪图像和噪声的加权和. 本文用更一般的概率分布的形式来表达, 即一步编码为 $$p(\bm{x}_t\vert\bm{x}_{t-1})$$, 一步解码为 $$q(\bm{x}_{t-1}\vert\bm{x}_t)$$. 同时我们假设上面的每一步分解过程只依赖于前一步的结果, 这在随机过程中也被称为[马尔可夫性质](https://en.wikipedia.org/wiki/Markov_property). 有了这个假设, 我们就可以把编解码过程中所有输出的联合分布表示为

$$
\begin{align}
p(\bm{x}_0,\bm{x}_1,\cdots,\bm{x}_T) &= p(\bm{x}_T\vert\bm{x}_{T-1})\cdots p(\bm{x}_2\vert\bm{x}_1)p(\bm{x}_1\vert\bm{x}_0)p(\bm{x}_0) \\
q(\bm{x}_0,\bm{x}_1,\cdots,\bm{x}_T) &= q(\bm{x}_0\vert\bm{x}_{1})\cdots q(\bm{x}_{T-2}\vert\bm{x}_{T-1})q(\bm{x}_{T-1}\vert\bm{x}_T)q(\bm{x}_T) \\
\end{align}
$$

其中 $$p(\bm{x}_0)$$ 就是数据分布, $$q(\bm{x}_T)$$ 就是编码输出分布. 

## 损失函数计算

同样的输出 ($$\bm{x}_0,\bm{x}_1,\cdots,\bm{x}_T$$), 两种不同的模型来表示, 因此我们可以通过极小化两个联合分布的 [KL 散度](/2018/09/18/Information-Theory/)来优化模型参数

$$ \label{eq:kl0}
\mathbb{KL}(p\Vert q)=\int p(\bm{x}_T\vert\bm{x}_{T-1})\cdots p(\bm{x}_1\vert\bm{x}_0)p(\bm{x}_0) \log\frac{p(\bm{x}_T\vert\bm{x}_{T-1})\cdots p(\bm{x}_1\vert\bm{x}_0)p(\bm{x}_0)}{q(\bm{x}_0\vert\bm{x}_{1})\cdots q(\bm{x}_{T-1}\vert\bm{x}_T)q(\bm{x}_T)}d\bm{x}_0\cdots d\bm{x}_T
$$

单步编码从加噪的角度来看就是 $$\bm{x}_t = \alpha_t\bm{x}_{t-1} + \beta_t\bm{e}_t, \; \bm{e}_t\sim\mathcal{N}(\bm{0},\bm{I})$$. 如果我们把等号右侧看作一个整体的分布的话, 那么就可以看作已知 $$\bm{x}_{t-1}$$ 时 $$\bm{x}_t$$ 的条件分布
$$p(\bm{x}_t\vert \bm{x}_{t−1}) := \mathcal{N}(\bm{x}_t; \alpha_t\bm{x}_{t−1},\beta_t^2\bm{I})$$. 反过来, $$q(\bm{x}_{t-1}\vert\bm{x}_t)$$ 则建模成了可学习的正态分布 $$\mathcal{N}(\bm{x}_{t-1};\bm{\mu}(\bm{x}_t), \sigma_t^2\bm{I})$$. 其中 $$\alpha_t,\beta_t,\sigma_t$$ 都是超参数. 解码过程建模成了可学习的正态分布, 这一点跟[《变分自动编码器 (VAE)》](https://arxiv.org/abs/1312.6114) 是类似的. 但与 VAE 不同的是, DDPM 为了简化计算过程放弃了建模方差, 只建模了均值. 

由于分布 $$p(\bm{x}_t\vert \bm{x}_{t−1})$$ 都是固定的, 因此 \eqref{eq:kl0} 式作为损失函数时可以丢掉 $$p\log p$$ 的项, 从而有

$$
-\int p(\bm{x}_T\vert\bm{x}_{T-1})\cdots p(\bm{x}_1\vert\bm{x}_0)p(\bm{x}_0) \left[ \log q(\bm{x}_T) + \sum_{t=1}^T \log q(\bm{x}_{t-1}\vert\bm{x}_t) \right] d\bm{x}_0\cdots d\bm{x}_T
$$

其中 $$q(\bm{x}_T)$$ 也没有可训练的参数, 所以上式进一步简化为

$$
-\sum_{t=1}^T \int p(\bm{x}_T\vert\bm{x}_{T-1})\cdots p(\bm{x}_1\vert\bm{x}_0)p(\bm{x}_0) \log q(\bm{x}_{t-1}\vert\bm{x}_t) d\bm{x}_0\cdots d\bm{x}_T
$$

下面我们考虑求和号里面的每一项

$$
\begin{align} \nonumber
& -\int p(\bm{x}_T\vert\bm{x}_{T-1})\cdots p(\bm{x}_1\vert\bm{x}_0)p(\bm{x}_0) \log q(\bm{x}_{t-1}\vert\bm{x}_t) d\bm{x}_0\cdots d\bm{x}_T \\ \nonumber
=& -\int p(\bm{x}_t\vert\bm{x}_{t-1})\cdots p(\bm{x}_1\vert\bm{x}_0)p(\bm{x}_0) \log q(\bm{x}_{t-1}\vert\bm{x}_t) d\bm{x}_0\cdots d\bm{x}_t\\ \label{eq:goal}
=& -\int p(\bm{x}_t\vert\bm{x}_{t-1})p(\bm{x}_{t-1}\vert\bm{x}_0)p(\bm{x}_0) \log q(\bm{x}_{t-1}\vert\bm{x}_t) d\bm{x}_0 d\bm{x}_{t-1} d\bm{x}_t 
\end{align}
$$

其中第一个等号是因为 $$q(\bm{x}_{t-1}\vert\bm{x}_t)$$ 只依赖到 $$\bm{x}_t$$, 因此 $$\bm{x}_{t+1}$$ 到 $$\bm{x}_T$$ 的联合分布可以直接积分为 $$1$$. 第二个等号的积分为

$$
\begin{align} \nonumber
\int p(\bm{x}_{t-1}\vert\bm{x}_{t-2})\cdots p(\bm{x}_1\vert\bm{x}_0) d\bm{x}_1\cdots d\bm{x}_{t-2} &= p(\bm{x}_{t-1}\vert\bm{x}_0) \\
&= \mathcal{N}(\bm{x}_{t-1};\bar\alpha_{t-1}\bm{x}_0, \bar\beta_{t-1}^2\bm{I})
\end{align}
$$

其中第二个等号的计算可以借助 [《生成扩散模型(一): 基础》](/2022/08/08/Diffusion-Model-1/#mjx-eqn-eq%3Axt_x0_2) 中的公式 [(5)](/2022/08/08/Diffusion-Model-1/#mjx-eqn-eq%3Axt_x0_2) $$\bm{x}_t = \bar{\alpha}_t\bm{x}_0 + \bar\beta_t\bm{e}_t$$ 把 $$t$$ 换为 $$t-1$$ 然后改写成分布的形式得到. 

此时我们分解一下上面的优化目标 \eqref{eq:goal} 式, 有

$$
\begin{align}
p(\bm{x}_t\vert\bm{x}_{t-1}) &\Rightarrow \bm{x}_{t−1}=\frac1{\alpha_t}(\bm{x}_t−\beta_t\bm{\varepsilon}_t)  \\
p(\bm{x}_{t-1}\vert\bm{x}_0) &\Rightarrow \bm{x}_{t−1}=\bar\alpha_t\bm{x}_0+\bar\beta_t\bm{\varepsilon}_{t−1} \\
-q(\bm{x}_{t-1}\vert\bm{x}_t) &\Rightarrow \frac1{2\sigma_t^2}\Vert \bm{x}_{t-1} - \bm\mu(\bm{x}_t) \Vert_2^2 \\
\bm{\mu}(\bm{x}_t) &= \frac1{\alpha_t}(\bm{x}_t−\beta_t\bm{\epsilon}_{\theta}(\bm{x}_t,t))
\end{align}
$$

接下来按照[损失函数计算](/2022/08/08/Diffusion-Model-1/#%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0%E8%AE%A1%E7%AE%97) 一节的内容即可完成推导.



## Reference

[^1]:
    **生成扩散模型漫谈（二）：DDPM = 自回归式VAE**, 苏剑林, In 科学空间, 2022, [[html](https://spaces.ac.cn/archives/9152)]

[^2]:
    **Denoising Diffusion Probabilistic Models**, Jonathan Ho, Ajay Jain, Pieter Abbeel, In NeruIPS, 2020, [[Paper](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html), [WebSite](https://hojonathanho.github.io/diffusion/), [Official TF-1.15 Code](https://github.com/hojonathanho/diffusion), [3rd Party PyTorch Code](https://github.com/lucidrains/denoising-diffusion-pytorch)]