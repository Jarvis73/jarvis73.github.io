---
layout: post
title: "聚类"
data: 2019-5-6 21:07:00
categories: 机器学习
mathjax: true
figure: 
author: Jarvis
meta: Post
---

* content
{:toc}

> 引言: 



<!-- <div class="polaroid">
    <img class="cool-img" src="/images/2018/12/FlowNet-4.jpg" FlowNet/>
    <div class="container">
        <a href="https://en.wikipedia.org/wiki/Optical_flow">Opical Flow</a>
    </div>
</div> -->

## Mean-Shift

Mean-Shift 聚类方法首先由 Fukunaga 于 1970's 提出, 从 1998 年起被广泛使用. 

### 密度估计

密度估计就是从一族离散的点中估计出这族点潜在的密度分布函数. 下图是一个二维上的点集.

<div class="polaroid">
    <img class="cool-img" src="/images/2019/05/cluster-1.jpg" Cluster/>
    <div class="container">
        <p>一个混合高斯模型(Mixture of Gaussian, MoG)产生的二维数据点</p>
    </div>
</div>

* 基于直方图的估计
* 最近邻估计
  
  $$
  \hat{p}(x) = \frac{#\{x_i\lvert\lVert x_i - x\rVert\leq\epsilon\}}{N}
  $$

* Parzen 估计
  原则: (1)每一个数据点都增加了其附近区域的密度估计, 如在一个固定半径的圆上均匀的提高概率 (2)更一般地, 使用缓慢增加的函数, 如高斯函数(称为核函数).
  
  <div class="polaroid">
    <img class="cool-img" src="/images/2019/05/cluster-0.jpg" Cluster/>
    <div class="container">
        <p>Parzen Example</p>
    </div>
  </div>

### 核密度估计 (Kernel Density Estimation, KDE)

可以想象成对于每一个数据点, 我们都给它分配一个核(函数). 实际上核函数就是一个权重函数, 核(kernel)是数学上一种优雅的叫法. 核函数有多种选择, 没有局限, 常用的是高斯核函数(Gaussian kernel).

多变量核密度估计函数如下:

$$
f(\mathbf{x}) = \frac{1}{nh^d}\sum_{i=1}^n\frac{1}{h}K\left(\frac{\mathbf{x}-\mathbf{x}_i}{h}\right).
$$

常用核函数:

* Gaussian 
  
  $$
  K_N = (2\pi)^{-d/2}\exp\left(-\frac12\lVert \mathbf{x}\rVert^2\right)
  $$

* Epanechnikov

  $$
  K_E = \frac34(1-\mathbf{x}^2), \quad \text{if } \lVert\mathbf{x}\rVert\leq 1
  $$

应用高斯核函数到上述 KDE 方程, 我们得到如下的图: 

* surface 图:

<div class="polaroid">
    <img class="cool-img" src="/images/2019/05/cluster-2.jpg" Cluster/>
    <div class="container">
        <p>Surface plot of the KDE with Gaussian kernel.</p>
    </div>
</div>

* contour 图:

<div class="polaroid">
    <img class="cool-img" src="/images/2019/05/cluster-3.jpg" Cluster/>
    <div class="container">
        <p>Contour plot of the KDE with Gaussian kernel and bandwidth=2.</p>
    </div>
</div>

### Mean-Shift 算法: 寻找一个分布离某一点最近的众数(mode)——局部众数(local mode)的方法.

假设: 数据量足够多的时候, 越接近"众数", 密度应该越大.

Mean-Shift 应用 KDE 的方法可以想象成数据点从它所在的位置迭代式地"爬山"到达最近的"山峰". 根据核函数**带宽(bandwidth)**的不同, 所找到的"山峰"位置和数量也可能不同. 一种极端情况是我们使用非常窄的带宽, 此时 KDE 会非常"稀碎", 从而产生过多的"山峰", 从而给出太多聚类簇. 另一种极端情况是带宽太宽, 会导致产生的"山峰"过少, 甚至最后只剩下一个"山峰", 即只剩一类. 一个小的带宽例子如下图所示.

<div class="polaroid">
    <img class="cool-img" src="/images/2019/05/cluster-4.jpg" Cluster/>
    <div class="container">
        <p>Contour plot of the KDE with Gaussian kernel and bandwidth=0.5</p>
    </div>
</div>

下面我们给出两个动画演示使用 Mean-Shift 算法产生的一个较好的聚类结果和一个较差的聚类结果.



## References

1. **Mean Shift Clustering**<br />
   Matt Nedrich<br />
   [[link]](https://spin.atomicobject.com/2015/05/26/mean-shift-clustering/). In network, 2015.
