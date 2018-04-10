---
layout: post
title: Group Normalization 阅读笔记
date: 2018-04-10 10:49:00
categories: 深度学习
tags: Base
figure: /images/2018-4-10/normalization.png
---

* content
{:toc}

论文题目: Group Normalization

作者: Yuxin Wu, Kaiming He

研究机构: Facebook AI Research

时间: 2018.03.22



## 前言
批归一化 (Batch Normalization, BN)[1] 提出后, 在深度学习领域扮演了一个重要的归一化的角色. 深度学习中由于经常使用大数据作为训练集, 所以无法把所有训练数据一次性载入内存而产生了**批训练**的方法(梯度下降). 从统计学的角度我们认为神经网络的学习特征的过程是一个学习数据分布的过程, 如果每一批的训练数据彼此的分布差异较大, 那么网络就需要不断地去适应不同的分布, 导致学习速度慢, 最终训练结果的精度也不够好. 

但是 BN 也存在一些问题. 顾名思义, BN 的效果是依赖于**批**的, 批比较大时, 数据标准化的结果会与整个数据集更为接近; 批比较小时, 仍然会存在较大的局部偏差. 如图 1 所示, 随着批大小的减小, BN 的误差会快速增大, 尤其是极小的批(batch size = 1 ~ 4). 

<center>
<img src="/images/2018-4-10/error.png" width="600" /><br />
图 1: **ImageNet 分类误差 vs. 批大小.** 这是一个在 ImageNet 上使用 8 个 GPUs 训练的 ResNet-50 的模型, 在验证集上评估.
</center>

本文的想法来源于以前的特征提取方法比如 SIFT, HOG 等提取出的是 group-wise 的特征, 并涉及到了 group-wise 的标准化. 比如 方向梯度直方图 (Histogram of oriented gradient, HOG) 特征检测算法把图像分为了多个块, 每个块分为四个 cell, 在每个 cell 内统计梯度方向, 从而每个块可以获得一个 k 维的特征向量, 然后对每个特征向量进行标准化. 这是一种组标准化的思路, 本文借鉴后提出了在神经网络的张量上, 把多通道分成组, 实施组标准化. 目前已有的标准化方法有

* 批标准化 (Batch Norm, BN)
* 层标准化 (Layer Norm, LN)
* 实例标准化 (Instance Norm, IN)
* 权重标准化 (Weight Norm)

如图 2 所示. 

<center>
<img src="/images/2018-4-10/normalization.png" /><br />
图 2: **标准化方法**. N 表示 batch 轴, C 表示通道轴, H,W 表示空间轴
</center>

从图 2 可以看出 LN, IN 和 GN 都是在每个样本上单独计算的. 而 LN 和 IN 是 GN 的两种极端情况.

## Group Normalization
标准化的通用公式是
$$
\hat{x_i} = \frac1\sigma(x_i-\mu_i).
$$

其中 $x$ 是某层输出的特征. 在 2D 图像时, $i = (i_N, i_C, i_H, i_W)$. $\mu$ 和 $\sigma$ 是均值和标准差

$$
\mu_i = \frac1m\sum_{k\in \mathcal{S}_i}x_k, \qquad \sigma_i = \sqrt{\frac1m\sum_{k\in \mathcal{S}_i}(x_k - \mu_i)^2 + \epsilon},
$$

其中 $\epsilon$ 是一个小的常数. $\mathcal{S}_i$ 是计算均值和标准差的像素集合, 不同的标准化方法本质上也就是集合 $\mathcal{S}_i$ 的不同. 

| 标准化方法    | $\mathcal{S}_i$ 定义方式                                     | 解释                                                         |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Batch Norm    | $\mathcal{S}_i = \{k|k_C = i_C\}$                            | $i_C$(和 $k_C$) 表示沿着 $C$ 轴的指标. 左式的意思是同一个通道的像素在一起标准化. 即对于每个通道, BN 沿着 $(N, H, W)$ 轴计算 $\mu$ 和 $\sigma$ , 得到的形状为 $C$ . |
| Layer Norm    | $\mathcal{S}_i = \{k|k_N = i_N\}$                            | 对于每个样本, LN 沿着 $(C, H, W)$ 轴计算 $\mu$ 和 $\sigma$ , 得到的形状为 $N$. |
| Instance Norm | $\mathcal{S}_i = \{k|k_N = i_N, k_C = i_C\}$                 | 对每个样本每个通道, IN 沿着 $(H, W)$ 轴计算 $\mu$ 和 $\sigma$ , 得到的形状为 $N\times C$. |
| Group Norm    | $S_i = \{k|k_N = i_N, \lfloor\frac{k_C}{C/G}\rfloor = \lfloor\frac{i_C}{C/G}\rfloor\}$ | $G$ 表示分组的数量, 是一个预定义的超参数(一般选择 $G=32$). $C/G$ 是每个组的通道数, 第二个等式条件表示对处于同一组的像素计算均值和标准差. 最终得到的形状为 $N\times (C/G)$ . |

最后三种方法都会再做一个 scale 和 shift:
$$
y_i= \gamma\hat{x_i} + \beta
$$
其中 $\gamma$ 和 $\beta$ 是可学习的参数, 对于所有的四种情况其形状均为 $C$.

### 实现

论文给出的 Tensorflow 下的实现方法:

```python
def GroupNorm(x, gamma, beta, G, eps=1e-5):
    """ Implementation of group normalization
    
    Params
    ------
    `x`: input features with shape [N, C, H, W]
    `gamma`, `beta`: scale and shift, with shape [1, C, 1, 1]
    `G`: number of groups for GN
    """
    assert C % G == 0, "C should be divisible by G"
    
    N, C, H, W = x.shape.as_list()
    x = tf.reshape(x, [N, G, C//G, H, W])
    
    mean, var = tf.nn.moments(x, [2, 3, 4], keep_dims=True)
    x = (x - mean) / tf.sqrt(var + eps)
    x = tf.reshape(x, [N, C, H, W])
    
    return x * gamma + beta
```

但是在 Tensorflow 和 Pytorch 中的 BN 均使用了 Moving Average, 下面给出 Tensorflow 带 Moving Average 的实现方法:

```python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

def GroupNormalization(inputs, 
                       group, 
                       N_axis=0, 
                       C_axis=-1, 
                       momentum=0.9,
                       epsilon=1e-3,
                       training=False,
                       name=None):
    """ Group normalization implementation with tensorflow.

    As descriped in Wu's paper(http://arxiv.org/abs/1803.08494), we can implement a 
    group norm with existed batch norm routine.

    Params
    ------
    `inputs`: tensor input
    `group`: number of groups in group norm
    `N_axis`: axis number of batch axis
    `C_axis`: axis number of channel axis
    `momentum`: momentum used in moving average mean and moving average variance
    `epsilon`: a small value to prevent divided by zero
    `training`: either a Python boolean, or a Tensorflow boolean scalar tensor (e.g. a 
    placeholder). Whether to return the output in training mode or in inference mode.
    **Note:** make sure to set this parameter correctly, or else your training/inference
    will not work properly.
    `name`: string, the name of the layer

    Returns
    -------
    Output tensor.
    """
    with tf.variable_scope(name, "GroupNorm"):
        input_shape = inputs.get_shape().as_list()
        ndims = len(input_shape)
        if not isinstance(C_axis, int):
            raise ValueError('`C_axis` must be an integer. Now it is {}'.format(C_axis))
        for axis in [C_axis, N_axis]:
            if axis < 0:
                axis = ndims + axis
            if axis < 0 or axis >= ndims:
                raise ValueError('Invalid axis: %d' % axis)
        
        # Require C % G == 0
        if input_shape[C_axis] % group != 0 or input_shape[C_axis] < group:
            raise ValueError('`group` should less than C_shape and be dividable '
                             'by C_shape. `group` is %d and C_shape is %d'
                             % (group, input_shape[C_axis]))

        permutation = [N_axis, C_axis] + [i if i != C_axis and i != N_axis for i in range(ndims)]
        inputs = tf.transpose(inputs, perm=permutation)
        
        old_shape = inputs.get_shape().as_list()
        new_shape = [old_shape[0], group, old_shape[1] // group] + old_shape[2:]
        inputs = tf.reshape(inputs, shape=new_shape)

        outputs = tf.layers.batch_normalization(inputs,
                                                axis=[0, 1],
                                                momentum=momentum,
                                                epsilon=epsilon,
                                                training=training)
        
        outputs = tf.reshape(outputs, shape=old_shape)
        
        reverse_permutation = permutation
        for i, idx in enumerate(permutation):
            reverse_permutation[idx] = i
        outputs = tf.transpose(outputs, perm=reverse_permutation)

        return outputs
```

