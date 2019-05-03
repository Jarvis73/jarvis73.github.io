---
layout: post
title: "Graph Cuts for Segmentation"
data: 2019-5-1 16:10:00
categories: 图像处理
mathjax: true
figure: /images/2019-5/Graph-Cuts-0.png
author: Jarvis
meta: Post
---

* content
{:toc}




**Title:** Interactive Graph Cuts for Optimal Boundary & Region Segmentation of Object in N-D Images

**Author:** Yuri Y. Boykov, Marie-Pierre Jolly

> 本文是基于 Graph-Cuts 进行自然图像/医学图像分割的一篇奠基之作, 许多常用的图割方法(如 GrabCut)是基于本文而设计的. 本文的两名作者均来自于西门子公司研究中心.

## 1. Introduction

图割法是计算机视觉领域分割任务常用的方法. 本文提出了**交互式图割法**, 同时结合**软约束(soft constraint)**和**硬约束(hard constraint)**明确地定义损失函数, 并得到全局最优解. 

考虑任意一个点的集合 $\mathcal{P}$ 和点对的集合 

$$
\mathcal{N}:=\{(p,q)\lvert (p,q)=(q,p),\; p, q\in\mathcal{P}\}. 
$$

令 $A=(A_1, \cdots, A_p, \cdots, A_{\lvert\mathcal{P}\rvert})$ 表示二值向量, 元素 $A_p$ 代表集合 $\mathcal{P}$ 中像素 $p$ 的一种赋值(0或1, 前景或背景), 从而 $A$ 即表示一种分割. 那么我们加在分割 $A$ 的边界和区域上的软约束可以表示为损失函数 $E(A)$ :

$$
E(A) := \lambda R(A) + B(A),
$$

其中

$$
\begin{align}
R(A) &:= \sum_{p\in\mathcal{P}}R_p(A_p) \\
B(A) &:= \sum_{(p,q)\in\mathcal{N}}B_{(p,q)}\cdot\delta(A_p\cdot A_q),
\end{align}
$$

且

$$
\delta(A_p, A_q)=
\begin{cases}
1 & \text{if } A_p\neq A_q \\
0 & \text{otherwise}.
\end{cases}
$$

区域项 $R(A)$ 表示给像素 $p$ 赋以"前景"或"背景"的惩罚, 边界项 $B(A)$ 中 $B_{(p, q)}\geq0$ 表示对像素 $p$ 和 $q$ 取值不连续性的惩罚, 取值越接近则 $B_{(p, q)}$ 越大, 反之越小. 

## 2. Graph Cuts and Computer Vision

无向图 $\mathcal{G}=<\mathcal{V, E}>$ 定义为一族顶点 $\mathcal{V}$ 和连接这些点的边 $\mathcal{E}$ . 每条边 $e\in\mathcal{E}$ 都被赋予非负的权重(损失) $w_e$ . 我们引入两个特殊的顶点称为**端点(terminals)**, 他们和图中所有其他点相连, 但彼此不直接相连. 一个**割(cut)**是边集的一个子集 $C\in\mathcal{E}$ 使得图中的两个端点被分离开 $\mathcal{G}(C):=<\mathcal{V, E}\backslash C>$ . 在组合优化中我们一般把割的损失定义为边上损失的和

$$
\lvert C\rvert := \sum_{c\in C}w_e.
$$

图割法求解优化目标(最小割)的方法是使用**最大流最小割定理**, 即求解最小割等价于求解最大流. 另外, 有两个端点的图的最小割有更高效的(低阶)多项式时间算法求解.  

## 3. Segmentation Technique

假设 $\mathcal{O}$ 和 $\mathcal{B}$ 表示已经被用户标记为"(目标)object"和"(背景)background"像素的集合, 那么有 $\mathcal{O}\in\mathcal{P}$ 和 $\mathcal{B}\in\mathcal{P}$ 并且 $\mathcal{O}\cap\mathcal{B}=\emptyset$ . 我们的目标是计算公式(2)满足硬约束

$$
\begin{align}
\forall p\in\mathcal{O},\qquad & A_p = \text{"obj"} \\
\forall p\in\mathcal{B},\qquad & A_p = \text{"backround"}.
\end{align}
$$

的全局最优解. 从图像构建图如下图所示.

<div class="polaroid-small">
    <img class="cool-img" src="/images/2019-5/Graph-Cuts.png" Graph-Cuts/>
    <div class="container">
        <p>A simple 2D segmentation example for a 3x3 image.</p>
    </div>
</div>

### 3.1 Details

图 $\mathcal{G}=<\mathcal{V, E}>$ , 其中顶点包括图像中的像素点和两个端点(源点 $S$ 和汇点 $T$), 所以有 

$$
\mathcal{V} = \mathcal{P}\cup\{S, T\}.
$$

边集包括两种类型的边: (1) *n-links* (neighborhood links) 和 *t-links* (terminal links). 每个像素点 $p$ 都关联了边 $(p, S)$ 和 $(p, T)$ . 集合 $\mathcal{N}$ 中的邻居像素 $(p, q)$ 都关联了一条 n-link. 所以有

$$
\mathcal{E} = \mathcal{N}\bigcup_{p\in\mathcal{P}}\{(p, S), (p, T)\}.
$$

为了清晰, 我们把不同类型边的权重列在下面的表格中

<table>
   <thead>
     <tr>
      <td>edge</td>
      <td>weight(cost)</td>
      <td>for</td>
     </tr>
    </thead>
   <tbody>
   <tr>
      <td>$(p, q)$</td>
      <td>$B_{(p, q)}$</td>
      <td>$(p, q)\in\mathcal{N}$</td>
   </tr>
   <tr>
      <td rowspan="3">$\{p, S\}$</td>
      <td>$\lambda\cdot R_p(\text{"bkg"})$</td>
      <td>$p\in\mathcal{P},\;p\notin\mathcal{O}\cup\mathcal{B}$</td>
   </tr>
   <tr>
      <td>$K$</td>
      <td>$p\in\mathcal{O}$</td>
   </tr>
   <tr>
      <td>$0$</td>
      <td>$p\in\mathcal{B}$</td>
   </tr>
   <tr>
      <td rowspan="3">$\{p, T\}$</td>
      <td>$\lambda\cdot R_p(\text{"obj"})$</td>
      <td>$p\in\mathcal{P}, \;p\notin\mathcal{O}\cup\mathcal{B}$</td>
   </tr>
   <tr>
      <td>$0$</td>
      <td>$p\in\mathcal{O}$</td>
   </tr>
   <tr>
      <td>$K$</td>
      <td>$p\in\mathcal{B}$</td>
   </tr>
   </tbody>
</table>

其中

$$
K = 1 + \max_{p\in\mathcal{P}}\sum_{q:(p, q)\in\mathcal{N}}B_{(p, q)}.
$$

### 3.2 Min-Cut

我们想要的最小割 $C$ 应该满足以下条件:

* 在每个像素点 $p$ 上只有一条 t-link 属于 $C$ 
* $(p, q)\in C$ 当且仅当 $p, q$ 连接到不同的端点
* 如果 $p\in\mathcal{O}$ , 则 $(p, T)\in C$ 
* 如果 $p\in\mathcal{B}$ , 则 $(p, S)\in C$ 

## 4. Examples

从用户标记的像素中提取直方图作为密度分布的先验 $Pr(I\lvert\mathcal{O})$ 和 $Pr(I\lvert\mathcal{B})$ . 那么区域惩罚可以写为

$$
\begin{align}
R_p(\text{"obj"})&=-\ln Pr(I_p\lvert\mathcal{O}) \\
R_p(\text{"bkg"})&=-\ln Pr(I_p\lvert\mathcal{B}).
\end{align}
$$

而边界惩罚使用 *ad-hoc* 函数

$$
B_{\{p, q\}}\propto\exp\left(-\frac{(I_p-I_q)^2}{2\sigma^2}\right)\cdot\frac1{dist(p, q)}.
$$

注意: 在 2D 图像中使用 8-neighborhood, 在 3D 图像中使用 26-neighborhood.

