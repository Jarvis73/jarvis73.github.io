---
layout: post
title: "GNNs: Graph Neural Networks"
date: 2019-3-7 21:04:00 +0800
categories: 机器学习
mathjax: true
figure: /images/2019-3/GNNs-head.jpg
author: Jarvis
meta: Post
---

* content
{:toc}



**Title:** Graph Neural Networks: A Review of Methods and Applications

## 1. Introduction

**图 (graph)** 是一种对**节点 (node)** 和**边 (edge)** 进行建模的结构, 这种结构的研究主要聚焦于节点分类, 链接预测和聚类上. **图神经网络 (graph neural networks, GNNs)** 则是图与神经网络的一种结合, 同时也是神经网络的一种推广 (从结构化数据到非结构化数据). GNNs 的想法来源于以下几个方面:

- 卷积神经网络 (CNN). CNN 的特点在于局部连接, 共享权重, 多层结构. 
- 图嵌入 (graph embedding). 学习使用低维向量表示图节点, 边和子图.

GNNs 的特点: 

* 忽略节点的输入次序. 即 GNNs 的输出不依赖于输入节点的顺序.
* 通过求邻居节点状态的加权和来更新节点的状态
* 可以探索神经**推理 (reasoning)**, 这是 CNN 难以做到的.

本文的目的是对不同的 GNNs 模型做一个较为全面的综述, 并对相关应用做一个系统的分类. 

第2节介绍 GNNs 的各种网络结构, 第3节介绍 GNNs 在结构化数据和非结构化数据上的应用, 第4节本文提出了四个 GNNs 中开放性的问题以供未来的研究参考, 第5节做一个总结.

## 2. Models

在 2.1 节介绍原始的 GNNs 结构及其局限性. 在 2.2 节给出集中变体以解决原始 GNNs 中的问题. 在 2.3 节给出三种一般性的框架: message passing neural network (MPNN), non-local neural network (NLNN) 和 graph network (GN). 以下是符号表

| 记号                   | 描述                             |
| ---------------------- | -------------------------------- |
| $\mathbb{R}^m$         | $m$ 维欧氏空间                   |
| $a, \mathbf{a}, \mathbf{A}$          | 标量, 向量, 矩阵                 |
| $\mathbf{A}^T$                | 矩阵转置                         |
| $\mathbf{I}_N$                | $N$ 维单位矩阵                   |
| $\mathbf{g}_{\theta}\star\mathbf{x}$ | $\mathbf{g}_{\theta}$ 与 $\mathbf{x}$ 卷积     |
| $N, N^v$               | 图中的节点数                     |
| $N^e$                  | 图中的边数                       |
| $\mathcal{N}_v$        | 节点 $v$ 的邻点集                |
| $\mathbf{a}_v^t$              | 节点 $v$ 在时间 $t$ 的向量 $\mathbf{a}$ |
| $\mathbf{h}_v$                | 节点 $v$ 的隐藏状态              |
| $\mathbf{h}_v^t$              | 节点 $v$ 在时间 $t$ 的隐藏状态   |
| $\mathbf{e}_{vw}$             | 节点 $v$ 到 $w$ 的边的特征       |
| $\mathbf{e}_k$                | 标签为 $k$ 的边的特征            |
| $\mathbf{o}_v^t$              | 节点 $v$ 的输出                  |
| $\sigma$               | sigmoid 函数                     |
| $\rho$                 | 非线性函数                       |
| $\odot$                | 逐点乘法                         |
| $\parallel$            | 向量拼接                         |

#### 2.1 GNNs

GNNs 的概念首先在[1]中提出, 把神经网络进行拓展以处理图中的数据. GNNs 的目标是学习图中每个节点的隐藏**状态嵌入 (state embedding)** $\mathbf{h}_v\in\mathbb{R}^s $ ,  这个隐藏状态包含了该节点的邻节点的信息. 节点 $v$ 的隐藏状态 $\mathbf{h}_v$ 是一个 $s$ 维的向量, 可以用于产生该节点的输出标签 $\mathbf{o}_v$. 令 $f$ 是一个方程, 称为**局部变换方程 (local transition function)**, 在所有节点中共享, 用于根据邻居节点的输入来更新节点状态. 令 $g$ 为**局部输出函数 (local output function)**, 产生节点输出. 公式表示如下

$$
\begin{align}
\mathbf{h}_v&=f(\mathbf{x}_v,\mathbf{x}_{co[v]},\mathbf{h}_{ne[v]},\mathbf{x}_{ne[v]}), \\
\mathbf{o}_v&=g(\mathbf{h}_v, \mathbf{x}_v),
\end{align}
$$

其中函数 $f$ 中的四个参数分别表示节点 $v$ 的特征, 边的特征, 状态和邻节点的状态. 



## Reference

1. **The graph neural network model**<br />
   F.Scarselli, M.Gori, A.C.Tsoi, M.Hagenbuchner, G.Monfardini<br />
   [[Link]](https://ieeexplore.ieee.org/abstract/document/4700287/). In IEEE TNN 2009, vol.20, no. 1, pp. 61–80, 2009.

