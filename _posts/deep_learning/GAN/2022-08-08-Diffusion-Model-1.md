---
layout: post
title: "生成扩散模型(一): 基础 (Generative Diffusion Model: Basic)"
date: 2022-08-08 10:08:00 +0800
categories: 深度学习 生成模型
mathjax: true
author: Jarvis
meta: Post
figure: /images/2022/08/diffusion-1.png
---

* content
{:toc}

说起生成模型, 我们最先想到的应该就是大名鼎鼎的 [GAN](http://papers.nips.cc/paper/5423-generative-adversarial-nets.pdf) 和 [VAE](https://arxiv.org/abs/1312.6114) 了. 其他还有一些小众的如 [Flow 模型](https://proceedings.mlr.press/v97/ho19a.html), [VQ-VAE](http://arxiv.org/abs/1711.00937) 等. 过去的八年里我们已经见识了深度生成模型在图像生成方面取得的进展, 如 [BigGAN](https://arxiv.org/abs/1809.11096). 近两年, 有另一个小众的------**生成扩散模型 (Diffusion Model)**------异军突起, 尤其是在 OpenAI 和 Google 把扩散模型和 Visual-Language 语言模型结合起来给出了惊人的 "文本 --> 图像" 生成效果之后. 




{% include image.html class="polaroid" url='2022/08/diffusion-1.png' title='DDPM 生成的人脸 和 DALLE-2 文本 -> 图像 生成的图像.' %}

扩散模型的理论有些繁琐, 这篇文章我们主要讨论 [DDPM](https://hojonathanho.github.io/diffusion/)[^6] 中给出的扩散模型, [苏剑林](https://spaces.ac.cn/)给出了一套更容易理解的观点, 本文的核心思想和主要的公式推导来源于[^1].

## 图像变成噪声

生成模型的一般思路是给一组随机噪声, 通过某种概率模型下的变换, 输出一张具有一定语义信息的图像. 但是由于噪声是高维分布随机采样来的, 而图像是高维空间里低维流形上的一个点, 直接建模从噪声到图像的变换目前来看是不可能的, 因为二者的差距太大了. 既然步子迈的太大了做不到, 那么我们是不是可以步子迈的小一点, 朝着一个目标一点一点前进呢? 如果从噪声一点点生成图像是不好想象的, 那反过来把图像变成噪声就显得很容易了, 我们只需要在图像上持续不断地撒上噪声, 最终整个图像都会毁掉, 变成一幅完整的噪声图像. 

{% include image.html class="polaroid" url='2022/08/diffusion-2.png' title='图像逐步加噪' %}

假设输入的图像为 $$x$$, 最终变成的噪声图像是 $$z$$, 通过 $$T$$ 步把图像变成噪声, 那么就有:

$$
x = x_0\rightarrow x_1\rightarrow x_2\rightarrow \cdots x_{T-1}\rightarrow x_T = z
$$

这样我们就把复杂的图像到噪声的变换过程拆成了一个个的小的步骤, 每个步骤 $$x_{t-1} \rightarrow x_t$$ 我们只需要加一点点噪声. 那么这个过程反过来就变成了 $$x_t\rightarrow x_{t-1}$$ 也就变成了只需要去一点点噪声. 这时候我们只需要学习一个可以去掉一点噪声的模型 $$x_{t-1} = \mu(x_t)$$, 然后反复地进行去噪 $$x_{T-1}=\mu(x_{T})$$, $$x_{T-2}=\mu(x_{T-1}), \dots$$ 就可以获得一幅具有语义信息的图像 $$x_0$$ 了. 

如何建模去噪模型 $$\mu(\cdot)$$ 呢? 我们首先考虑怎么加噪. 具体来说, 我们可以把加噪的过程看作图像和噪声 MixUp 的过程, 

$$
\label{eq:add_noise}
\pmb{x}_t = \alpha_t \pmb{x}_{t-1} + \beta_t\pmb{e}_t, \quad \pmb{e}_t\sim\mathcal{N}(\pmb{0}, \pmb{I}),
$$

其中 $$\alpha_t, \beta_t\gt0$$, 并且我们定义 $$\alpha_t^2 + \beta_t^2=1$$, 其中 $$\beta_t$$ 接近于 $$0$$, 这是合理的, 因为我们希望每次只增加少量噪声以简化建模过程. 平方和为 $$1$$ 这个约束一方面是为了控制加噪过程中数值的尺度, 另一方面可以简化计算 (马上就可以看到). 

反复迭代 \eqref{eq:add_noise} 式, 可以得到

$$
\begin{align} \nonumber
    \pmb{x}_t &= \alpha_t\pmb{x}_{t-1} + \beta_t\pmb{e}_t \\ \nonumber
              &= \alpha_t(\alpha_{t-1}\pmb{x}_{t-2} + \beta_{t-1}\pmb{e}_{t-1}) + \beta_t\pmb{e}_t \\ \nonumber
              &= \alpha_t\alpha_{t-1}\pmb{x}_{t-2} + \alpha_t\beta_{t-1}\pmb{e}_{t-1} + \beta_t\pmb{e}_t \\ \nonumber
              &= \dots \\ \label{eq:xt_x0}
              &= (\alpha_t\dots\alpha_1)\pmb{x}_0 + \underbrace{(\alpha_t\dots\alpha_2)\beta_1\pmb{e}_1 + (\alpha_t\dots\alpha_3)\beta_2\pmb{e}_2 + (\alpha_t)\beta_{t-1}\pmb{e}_{t-1} + \beta_t\pmb{e}_t}_{\text{记为} \pmb{\gamma}_t}
\end{align}
$$

上式中, $$\pmb{\gamma}_t$$ 是相互独立的 $$t$$ 个正态分布的噪声 $$(\alpha_t\dots\alpha_{i+1})\beta_i\pmb{e}_i\sim\mathcal{N}(\pmb{0},(\alpha_t\dots\alpha_{i+1})^2\beta_i^2\pmb{I}),\;\; i=1,\dots,t$$ 之和 (注意 $$i=t$$ 时没有 $$\alpha$$ 项.). 根据正态分布的叠加性, 可知 $$\pmb{\gamma}_t$$ 的均值为 $$\pmb{0}$$, 方差为 $$\sigma^2\pmb{I}$$. 根据前面的定义 $$\alpha_t^2 + \beta_t^2=1$$, 我们有

$$
\begin{align}
(\alpha_t\dots\alpha_2)^2\beta_1^2 + (\alpha_t\dots\alpha_3)^2\beta_2^2 + (\alpha_t)^2\beta_{t-1}^2 + \beta_t^2 &= \sigma^2 \\ \nonumber
\Rightarrow\quad (\alpha_t\dots\alpha_2)^2\beta_1^2 + (\alpha_t\dots\alpha_3)^2\beta_2^2 + (\alpha_t)^2\beta_{t-1}^2 - \alpha_t^2 &= \sigma^2 - 1 \\ \nonumber
\Rightarrow\quad (\alpha_t\dots\alpha_2)^2\beta_1^2 + (\alpha_t\dots\alpha_3)^2\beta_2^2 + (\alpha_t\alpha_{t-1})^2\qquad\; &= \sigma^2 - 1 \\ \nonumber
\cdots \\ \nonumber
\Rightarrow\quad (\alpha_t\dots\alpha_1)^2\qquad\qquad\qquad\qquad\qquad\qquad\qquad\quad\;\; &= \sigma^2 - 1
\end{align}
$$

因此, 方法化简为 $$\sigma^2 = 1 - (\alpha_t\cdots\alpha_1)^2$$. 那么 \eqref{eq:xt_x0} 式可以写为

$$ \label{eq:xt_x0_2}
\pmb{x}_t = \underbrace{(\alpha_t\dots\alpha_1)}_{\text{记为} \bar{\alpha_t}}\pmb{x}_0 + \underbrace{\sqrt{1 - (\alpha_t\cdots\alpha_1)^2}}_{\text{记为} \bar{\beta_t}}\bar{\pmb{e}}_t, \quad, \bar{\pmb{e}}_t\sim\mathcal{N}(\pmb{0}, \pmb{I}).
$$

那么, 当我们选择合适的 $$\alpha_t$$ 以及足够大的 $$T$$, 最终 $$\bar{\alpha}_t$$ 就会趋于 $$0$$, 这意味着图像信息最终消失, 全部转化为高斯噪声. 

{% include card.html type='info' content='注意 \eqref{eq:xt_x0_2} 式除了表示图像生成噪声的过程, 同时也给出了任意 $$t$$ 步后的加噪图像用原始图像 $$\pmb{x}_0$$ 表达的形式, 这对于后续模型训练很有帮助.' %}


## 损失函数计算

那么从噪声生成图像时, 如何训练 $$\pmb{x}_{t-1}=\pmb{\mu}(\pmb{x}_t)$$ 呢? 最直接的方法就是 $$L_2$$ 损失:

$$
\Vert \pmb{x}_{t-1} - \pmb{\mu}(\pmb{x}_t) \Vert_2^2.
$$

这时可以直接用神经网络建模 $$\pmb{\mu}(\cdot)$$, 考虑到 $$\pmb{x}_{t-1}$$ 和 $$\pmb{x}_t$$ 在加噪过程中是有关系的, 所以我们不妨展开一下. 首先式 \eqref{eq:add_noise} 可以写成 $$\pmb{x}_{t-1} = \frac1{\alpha_t}(\pmb{x}_t - \beta_t\pmb{e}_t)$$, 这启发我们可以把 $$\pmb{\mu}(\cdot)$$ 写为

$$ \label{eq:inference0}
\pmb{\mu}(\pmb{x}_t)=\frac1{\alpha_t}(\pmb{x}_t - \beta_t\pmb{\epsilon}_{\pmb{\theta}}(\pmb{x}_t, t)),
$$

其中 $$\pmb{\epsilon}_{\pmb{\theta}}(\pmb{x}_t, t)$$ 是我们用神经网络建模的对象, $$\theta$$ 表示模型参数, $$t$$ 为第几步, 模型从噪声生成图像, 因而依赖于 $$\pmb{x}$$. 这里引入 $$t$$ 是为每一步生成过程使用不同的生成模型, 通过共享模型参数, 可以把 $$t$$ 作为参数输入模型. 我们得到

$$
\Vert \frac1{\alpha_t}(\pmb{x}_t - \beta_t\pmb{e}_t) - \frac1{\alpha_t}(\pmb{x}_t - \beta_t\pmb{\epsilon}_{\theta}(\pmb{x}_t, t)) \Vert_2^2 = \frac{\beta_t^2}{\alpha_t^2}\Vert \pmb{e}_t - \pmb{\epsilon}(\pmb{x}_t, t) \Vert_2^2.
$$

因为这是损失函数, 我们忽略前面的系数 $$\frac{\beta_t^2}{\alpha_t^2}$$. 注意到现在损失函数中包含三个变量, 其中 $$\pmb{e}_t$$ 是服从标准正态分布的变量, $$\pmb{\epsilon}$$ 是神经网络模型, 只有 $$\pmb{x}_t$$ 是未知的, 需要通过 $$t$$ 步的加噪采样得到, 这样显得太过复杂. 回忆我们在上一节讨论加噪时, \eqref{eq:xt_x0_2} 式给出可以使用初始图像 $$\pmb{x}_0$$ 和服从正态分布的噪声 $$\bar{e}_t$$ 来表示 $$\pmb{x}_t$$, 因此我们可以把 \eqref{eq:xt_x0_2} 式代入损失函数得到

$$ \label{eq:loss_ori0}
\Vert \pmb{e}_t - \pmb{\epsilon}(\bar{\alpha}_t\pmb{x}_0 + \bar\beta_t \pmb{\bar{e}}_t, t) \Vert_2^2.
$$

上式存在一个问题, 由于 $$\pmb{e}_t$$ 和 $$\pmb{\bar{e}}_t$$ 不是相互独立的, 采样时会相互影响. 所以我们后退一步使用 $$\pmb{x}_{t-1}$$ 对应的 \eqref{eq:xt_x0_2} 式来避免上面的问题. 我们有

$$
\begin{align} \nonumber
    \pmb{x}_t &= \alpha_t\pmb{x}_{t-1} + \beta_t\pmb{e}_t \\ \nonumber
              &= \alpha_t(\bar\alpha_{t-1}\pmb{x}_0 + \bar\beta_{t-1}\pmb{\bar{e}}_{t-1}) + \beta_t\pmb{e}_t \\
              &= \bar\alpha_t\pmb{x}_0 + \alpha_t\bar\beta_{t-1}\pmb{\bar{e}}_{t-1} + \beta_t\pmb{e}_t.
\end{align}
$$

这样, 损失函数可以写为

$$ \label{eq:loss_ori1}
\Vert \pmb{e}_t - \pmb{\epsilon}(\bar\alpha_t\pmb{x}_0 + \alpha_t\bar\beta_{t-1}\pmb{\bar{e}}_{t-1} + \beta_t\pmb{e}_t, t) \Vert_2^2.
$$

对比 \eqref{eq:loss_ori0} 式和 \eqref{eq:loss_ori1} 式, 本质就就是把 $$\bar\beta_t\bar{\pmb{e}}_t$$ 替换为了 $$\alpha_t\bar\beta_{t-1}\pmb{\bar{e}}_{t-1} + \beta_t\pmb{e}_t$$, 但是这样就把一个正态分布采样变成了两个, 这可能会增大模型训练的难度. 而使用 \eqref{eq:loss_ori0} 式又会导致两个正态分布产生依赖无法采样, 那么有没有办法在 \eqref{eq:loss_ori0} 式中把 $$\pmb{e}_t$$ 替换成不和 $$\pmb{\bar{e}}_t$$ 直接依赖的正态分布呢? 

答案是可以的. 这里需要用到一个积分的技巧. 考虑如下两个式子是成立的 (正态分布的叠加性):

$$
\begin{align} \label{eq:uv1}
    \alpha_t\bar\beta_{t-1}\pmb{\bar{e}}_{t-1} + \beta_t\pmb{e}_t &= \bar\beta_t\pmb{u}, \quad \pmb{u}\sim\mathcal{N}(\pmb{0},\pmb{I}) \\ \label{eq:uv2}
    \beta_t\pmb{\bar{e}}_{t-1} - \alpha_t\bar\beta_{t-1}\pmb{e}_t &= \bar\beta_t\pmb{v}, \quad \pmb{v}\sim\mathcal{N}(\pmb{0},\pmb{I}),
\end{align}
$$

其中 $$\pmb{u}, \pmb{v}\sim\mathcal{N}(\pmb{0},\pmb{I})$$. 我们有 

$$  \nonumber
\pmb{uv}^\top = \frac1{\bar{\beta}_t^2}\left(\alpha_t\beta_t\bar\beta_{t-1}(\bar{\pmb{e}}_{t-1}^2 - \pmb{e}_t^2) + (\beta_t^2 - \alpha_t^2\bar\beta_{t-1}^2)\bar{\pmb{e}}_{t-1}\pmb{e}_t\right)
$$

由于 $$\bar{\pmb{e}}_{t-1}$$ 和 $$\pmb{e}_t$$ 是相互独立标准正态分布的, 所以 $$\bar{\pmb{e}}_{t-1}^2 - \pmb{e}_t^2$$ 和 $$\bar{\pmb{e}}_{t-1}\pmb{e}_t$$ 的期望均为 $$\pmb{0}$$, 所以 $$\mathbb{E}[\pmb{uv}^\top]=0$$, 因此 $$\pmb{u}$$ 和 $$\pmb{v}$$ 相互独立. [(证明)](https://stats.stackexchange.com/questions/250200/are-two-standard-normal-random-variables-always-independent).

求解 \eqref{eq:uv1} 和 \eqref{eq:uv2} 式得到

$$
\begin{align}
    \pmb{e}_t &= \frac{\beta_t\pmb{u} - \alpha_t\bar\beta_{t-1}\pmb{v}}{\bar\beta_t} \\
    \pmb{\bar{e}}_t &= \pmb{u}
\end{align}
$$

代入 \eqref{eq:loss_ori0}, 得到

$$
\begin{align} \nonumber
&\mathbb{E}_{\pmb{\bar{e}}_t,\pmb{e}_t\sim\mathcal{N}(\pmb{0},\pmb{I})} \left[\left\Vert \pmb{e}_t - \pmb{\epsilon_{\theta}}(\bar{\alpha}_t\pmb{x}_0 + \bar\beta_t\pmb{\bar{e}}_t, t) \right\Vert_2^2\right] \\ \nonumber
=&\mathbb{E}_{\pmb{u},\pmb{v}\sim\mathcal{N}(\pmb{0},\pmb{I})} \left[\left\Vert \frac{\beta_t\pmb{u} - \alpha_t\bar\beta_{t-1}\pmb{v}}{\bar\beta_t} - \pmb{\epsilon_{\theta}}(\bar{\alpha}_t\pmb{x}_0 + \bar\beta_t \pmb{u}, t) \right\Vert_2^2\right]  \nonumber \\ \nonumber
=& \frac{\beta_t^2}{\bar\beta_t^2}\mathbb{E}_{\pmb{u}\sim\mathcal{N}(\pmb{0},\pmb{I})} \left[\left\Vert \pmb{u} - \frac{\bar\beta_t}{\beta_t}\pmb{\epsilon_{\theta}}(\bar{\alpha}_t\pmb{x}_0 + \bar\beta_t \pmb{u}, t) \right\Vert_2^2\right] + C
\end{align}
$$

其中 $$C$$ 是一个常数. 把 $$\frac{\bar\beta_t}{\beta_t}$$ 吸收到模型 $$\pmb{\epsilon_{\theta}}$$ 里面, 上面的损失可以简化为

$$
\left\Vert \pmb{u} - \pmb{\epsilon_{\theta}}(\bar{\alpha}_t\pmb{x}_0 + \bar\beta_t \pmb{u}, t) \right\Vert_2^2
$$

上面就是论文 DDPM 中最终的损失函数.

## 噪声生成图像

模型训练完成后, 我们就可以使用 \eqref{eq:inference0} 进行推断了

$$
\pmb{x}_{t-1} = \frac1{\alpha_t}(\pmb{x}_t - \beta_t\pmb{\epsilon}_{\pmb{\theta}}(\pmb{x}_t, t)),
$$

如果要引入随机性, 需要加上一个噪声项

$$
\pmb{x}_{t-1} = \frac1{\alpha_t}(\pmb{x}_t - \beta_t\pmb{\epsilon}_{\pmb{\theta}}(\pmb{x}_t, t)) + \sigma_t\pmb{z}, \quad \pmb{z}\sim\mathcal{N}(\pmb{0},\pmb{I})
$$

通常我们可以令 $$\sigma_t=\beta_t$$, 即加噪和去噪的方差同步变化. 从随机噪声 $$\pmb{x}_T$$ 出发, 经过 $$T$$ 步迭代之后就可以得到最终生成出的图像. 

{% include image.html class="polaroid" url='2022/08/diffusion-3.png' title='DDPM 在 CIFAR10 上的生成过程' %}

## 讨论

在 DDPM 中, 一般设置 $$T=1000$$, 这导致 DDPM 的生成过程很慢, 因此后续很多工作致力于优化生成速度. 

超参数的设置, 

$$
\alpha_t = \sqrt{1 - \frac{0.02t}{T}}
$$

可以看到 $$\alpha_t$$ 是递减的. VAE 用欧氏距离重构时, 往往得到的结果比较模糊, 所以选择尽可能大的 $$T$$, 使得每次迭代的两步间距尽可能地小, 这样输入输出比较接近时欧氏距离带来的模糊问题可以得到有效的缓解. 

使用递减的 $$\alpha_t$$, 可以在迭代的前期图像信息比较多的时候 (用大的 $$\alpha_t$$) 保持两步间距更小, 随着迭代到后期, 图像信息渐渐消失, 噪声信息占主导的时候 (用小的 $$\alpha_t$$ ) 增大两步间距. 当然了, 可以一直使用较大的 $$\alpha_t$$, 但由于我们最终需要 $$\bar\alpha_t\approx0$$, 较大的 $$\alpha_t$$ 会导致需要更大的 $$T$$ 来收敛. 

在实现上, $t$ 是使用 Transformer 中的位置编码表示的, 直接加到了残差模块上去.

{% include image.html class="polaroid" url='2022/08/diffusion-4.png' title='DDPM 在 CelebA-HQ 256 × 256 上的生成结果' %}


## Reference

[^1]:
    **生成扩散模型漫谈（一）：DDPM = 拆楼 + 建楼**, 苏剑林, In 科学空间, 2022, [[html](https://spaces.ac.cn/archives/9119)]

[^2]:
    **生成扩散模型漫谈（二）：DDPM = 自回归式VAE**, 苏剑林, In 科学空间, 2022, [[html](https://spaces.ac.cn/archives/9152)]

[^3]:
    **生成扩散模型漫谈（三）：DDPM = 贝叶斯 + 去噪**, 苏剑林, In 科学空间, 2022, [[html](https://spaces.ac.cn/archives/9164)]

[^4]:
    **生成扩散模型漫谈（四）：DDIM = 高观点DDPM**, 苏剑林, In 科学空间, 2022, [[html](https://spaces.ac.cn/archives/9181)]

[^5]:
    **由浅入深了解Diffusion Model**, In 知乎专栏, 2022, [[html](https://zhuanlan.zhihu.com/p/525106459)]

[^6]:
    **Denoising Diffusion Probabilistic Models**, Jonathan Ho, Ajay Jain, Pieter Abbeel, In NeruIPS, 2020, [[Paper](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html), [WebSite](https://hojonathanho.github.io/diffusion/), [Official TF-1.15 Code](https://github.com/hojonathanho/diffusion), [3rd Party PyTorch Code](https://github.com/lucidrains/denoising-diffusion-pytorch)]


