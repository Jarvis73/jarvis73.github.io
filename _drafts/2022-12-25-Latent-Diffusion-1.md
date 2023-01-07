---
layout: post
title: "潜空间扩散模型 (Latent Diffusion Models, LDM)"
date: 2022-12-25 15:04:00 +0800
categories: 深度学习 生成模型
mathjax: true
author: Jarvis
meta: Post
---

* content
{:toc}

原始的扩散模型有一个显著的特点, 就是正向和反向过程都是在原始图像空间中进行的, 这也导致了扩散模型非常吃显存并且耗时. Rombach 等人在 CVPR 2022 的 [《High-Resolution Image Synthesis with Latent Diffusion Models》](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html) 一文中提出了**潜空间扩散 (latent diffusion model, LDM)** 的方法, 其核心思想在于把图像空间上做扩散改为<u>在一个预训练的自编码器的潜空间 (latent space) 做扩散</u>. 因为潜空间通常是比图像空间更低维度的空间, 这样做的好处是在同样地计算量下可以生成更高分辨率的图像, 或者生成同样质量的图像时可以显著地减少计算量. 




## 特征降维

既然在原始图像空间计算量很大, 那么 LDM 首先把原始图像 (特征维度 $$H\times W\times 3$$) 映射为低维表示 $$h\times w\times c$$, 同时希望低维表示和原始图像有尽可能相同语义信息.

> perceptually equivalent to the image space

使用 Esser 等人在 CVPR 2021 的 [《Taming transformers for high-resolution image synthesis》](https://openaccess.thecvf.com/content/CVPR2021/html/Esser_Taming_Transformers_for_High-Resolution_Image_Synthesis_CVPR_2021_paper.html?ref=https://githubhelp.com) 一文中提出的方法训练一个自动编码器 (autoencoder).

原始图像与低维表示的下采样比例 $$f=H/h=W/w$$ 通常为 2 的幂次 $$f=2^m,\;m\in\mathbb{N}$$. 

为了避免潜空间的方差过大不受约束, 提供了两种潜空间正则化方式:

1. $$KL\text{-}reg.$$ 在潜变量和标准正态分布之间施加一个小的 KL 散度惩罚. (类似于 [VAE](https://arxiv.org/abs/1312.6114))
2. $$VQ\text{-}reg.$$ 在解码器中引入了[向量量化层 (vector quantization, VQ)](https://proceedings.neurips.cc/paper/2017/hash/7a98af17e63a0ac09ce2e96d03992fbc-Abstract.html). 

## 潜空间扩散

{% include image.html class="polaroid-small" url="2022/12/latent-diffusion.png" title="潜空间扩散模型 Latent Diffusion Models" %}

根据 [《生成扩散模型(四): 扩散模型和得分匹配》](/2022/11/29/Diffusion-Model-4/), 在图像空间中扩散模型的损失函数为

$$
    L_{\text{DM}} = \mathbb{E}_{\bm{x},\bm{\epsilon}\sim\mathcal{N}(\bm{0},\bm{I}),t}\left[\Vert\bm{\epsilon}-\bm{\epsilon}_{\theta}(\bm{x}_t,t)\Vert_2^2\right].
$$

那么 LDM 的损失函数可以表示为:

$$
    L_{\text{LDM}} = \mathbb{E}_{\mathcal{E}(\bm{x}),\bm{\epsilon}\sim\mathcal{N}(\bm{0},\bm{I}),t}\left[\Vert\bm{\epsilon}-\bm{\epsilon}_{\theta}(\bm{z}_t,t)\Vert_2^2\right].
$$

其中 $$\mathcal{E}(\bm{x})$$ 为特征降维中得到的编码器, $$\bm{z}_t$$ 可以从编码器中得到.

## 条件控制

**Cross-Attention 方法**

上述的生成模型只能生成随机的样本, 为了控制生成样本的类别等, 可以把额外的条件信息 $$y$$ 嵌入扩散模型的神经网络中. 

LDM 在 U-Net 中增加了一个条件控制的接口, 这个接口通过生成特征和条件信息之间的 Cross-Attention 机制 $$\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V$$ 来实现, 其中:

$$
    Q=W_Q^{(i)}\phi_i(z_t),\; K=W_K^{(i)}\tau_{\theta}(y),\; V=W_V^{(i)}\tau_{\theta}(y).
$$

其中 $$i$$ 表示第几个注意力头, $$\phi_i(z_t)$$ 表示 U-Net 的中间特征, $$\tau_{\theta}(y)$$ 是条件信息 $$y$$ 中间表示. 带条件信息的损失函数可表示为:

$$
    L_{\text{LDM}} = \mathbb{E}_{\mathcal{E}(\bm{x}),y,\bm{\epsilon}\sim\mathcal{N}(\bm{0},\bm{I}),t}\left[\Vert\bm{\epsilon}-\bm{\epsilon}_{\theta}(\bm{z}_t,t,\tau_{\theta}(y))\Vert_2^2\right].
$$


