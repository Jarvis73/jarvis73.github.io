---
layout: post
title: "生成模型指标 (Metrics of Generative Models)"
date: 2022-12-09 21:17:00 +0800
categories: 深度学习 生成模型
mathjax: true
author: Jarvis
meta: Post
---

* content
{:toc}

生成模型 (genrative model) 的生成结果通常没有直接的 ground truth 来计算样本的生成质量. 比如图像生成既要考虑生成图像的噪声要低, 清晰度要高, 同时生成的多样性要高. 我们可以直接找一些人来做图灵测试, 从而评估图像生成的效果, 但这样评估的成本显然是比较高的. 本文介绍几种论文中常用的近似指标 IS, FID, NLL. 既然是近似指标, 那么就说明, 这些指标好不代表生成的样本一定好, 它们仅仅是在一定程度上可以反映生成样本的质量. 



## Inception Score, IS

Salimans 等人在 2016 年 [《Improved Techniques for Training GANs》](http://arxiv.org/abs/1606.03498) 一文中提出了 **Inception Score** 来衡量生成模型的结果. 作者发现 $$\text{IS}$$ 的得分与人类评估的结果是匹配的不错的. $$\text{IS}$$ 的定义基于 Inception-V3 分类模型, 该模型是 Szegedy 等人在 2015 年 [《Rethinking the Inception Architecture for Computer Vision》](https://www.cv-foundation.org/openaccess/content_cvpr_2016/html/Szegedy_Rethinking_the_Inception_CVPR_2016_paper.html) 一文中提出的, 用于 ImageNet 1000 个类别的分类. 

假设我们在 ImageNet 上训练了一个生成模型 $$G$$, 那么 $$\text{IS}$$ 可以如下计算:

$$
    \begin{align}
        \text{IS} &= \exp(\mathbb{E}_{\bm{x}}\mathbb{KL}(p(y\vert\bm{x})\vert p(y))) \\
        &= \exp(\mathbb{E}_{\bm{x}}\mathbb{H}(p(y\vert\bm{x}), p(y)) - \mathbb{E}_{\bm{x}}\mathbb{H}(p(y\vert\bm{x}), p(y\vert\bm{x}))) \\
        &= \exp(\mathbb{H}(\mathbb{E}_{\bm{x}}[p(y\vert\bm{x})], p(y)) - \mathbb{E}_{\bm{x}}\mathbb{H}(p(y\vert\bm{x}), p(y\vert\bm{x}))) \\
        &= \exp(\underbrace{\mathbb{H}(p(y), p(y))}_{p(y) 的熵} - \mathbb{E}_{\bm{x}}\underbrace{\mathbb{H}(p(y\vert\bm{x}), p(y\vert\bm{x}))}_{p(y\vert\bm{x}) 的熵}) \\
    \end{align}
$$

这里的期望可以通过从生成模型中大量采样 $$\bm{x}\sim G$$ 来计算. $$p(y\vert\bm{x})$$ 是 Inception 模型把 $$\bm{x}$$ 分类为 ImageNet 1000 类的概率分布, 而 $$p(y)$$ 可以通过 $$\mathbb{E}_{\bm{x}}[p(y\vert\bm{x})]$$ 得到. 

前面提到生成图像时, 我们希望图像清晰和具有多样性. 假设图像中的物体容易分辨, 那么 Inception 模型给出的概率分布 $$p(y\vert\bm{x})$$ 应当把绝大部分概率集中到某一个类别, 从而熵较低; 假设大量生成的图像多样性很高, 那么这些图像的类别分布应该很均匀, 即 $$\mathbb{E}_{\bm{x}}[p(y\vert\bm{x})]=p(y)$$ 的熵会比较大. 因此, 我们的目标就是极大化 $$\text{IS}$$. 

{% include card.html type="info" content="$$\text{IS}$$ 的取值范围为 $$[1, N]$$, 其中 $$N$$ 为类别的数量." %}


举个例子, 先引入 `numpy` 并定义熵: 

```python
import numpy as np

# 定义熵
def H(dist, axis=-1, eps=1e-8):
    return -(dist * np.log(dist + eps)).sum(axis)
```

假设我们有一组 $$p(y\vert\bm{x})$$, 在理想最好的情况下, 我们有 (假设有 $$N=3$$ 个类别):

```python
p_yx = np.eye(3)
# array([[1., 0., 0.],
#        [0., 1., 0.],
#        [0., 0., 1.]])

# 计算 p_y
p_y = p_yx.mean(axis=0)
# array([0.33333333, 0.33333333, 0.33333333])

# 计算 IS
IS = np.exp(H(p_y) - H(p_yx).mean(0))
# 2.9999999400000017
```

可以看到以上的结果在误差范围内等于 $$3$$, 即为 $$\text{IS}(N=3)$$ 的最大值.

```python
p_yx = np.ones((3, 3)) / 3
# array([[0.33333333, 0.33333333, 0.33333333],
#        [0.33333333, 0.33333333, 0.33333333],
#        [0.33333333, 0.33333333, 0.33333333]])

# 计算 p_y
p_y = p_yx.mean(axis=0)
# array([0.33333333, 0.33333333, 0.33333333])

# 计算 IS
IS = np.exp(H(p_y) - H(p_yx).mean(0))
# 1.0
```

可以看到以上的结果等于 $$1$$, 即为 $$\text{IS}(N=3)$$ 的最小值.


## Fréchet Inception Distance, FID

区别于 IS 是在 Inception-V3 输出的分布上计算的, FID 是在高层特征上计算真假图片之间的距离. FID 是 Heusel 等人在 2017 年 [《GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium》](https://papers.nips.cc/paper/2017/hash/8a1d694707eb0fefe65871369074926d-Abstract.html) 一文中提出的用于衡量生成样本质量的指标. 其计算方式如下：

$$
    \text{FID} = \Vert \mu_r - \mu_g \Vert^2 + Tr\left( \Sigma_r + \Sigma_g - 2(\Sigma_r\Sigma_g)^{\frac12} \right)
$$

其中 $$\mu$$ 是经验均值, $$\Sigma$$ 是经验协方差, $$Tr$$ 为矩阵的迹, $$r$$ 是真实数据集, $$g$$ 是生成的数据集. 

实际操作中, 我们使用原始数据集中的 $$M$$ 张图片, 经过 Inception-V3 模型得到 $$M\times 2048$$ 的特征向量组成的矩阵. 然后用生成模型生成 $$N$$ 张图片, 经过 Inception-V3 模型得到 $$N\times 2048$$ 的特征向量组成的矩阵. 用这两个矩阵就可以计算 $$\mu_r, \Sigma_r, \mu_g, \Sigma_g$$, 然后套用上面的公式计算 FID 了. 

相比 IS 是用生成的数据跟 ImageNet 做比较, FID 是用生成的数据跟训练集做比较, 更合理一些. 
