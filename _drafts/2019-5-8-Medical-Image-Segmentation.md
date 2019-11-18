---
layout: post
title: "Medical Image Segmentation"
data: 2019-5-9 9:50:00
categories: 图像处理
mathjax: true
figure: /images/2019-5/Graph-Cuts-0.png
author: Jarvis
meta: Post
---

* content
{:toc}

> 医学图像往往因为不同的模态、不同的解剖结构、不同的大小、不同的机器扫描、是否增强等因素， 使得医学图像的相关算法难以泛化到其他医学图像的数据集. 

## 基于规则的分割 (Rule-Based)

每个区域的图像特征符合一组启发式的规则.

* 阈值 (threshold): 全局阈值, 局部/自适应阈值
  * 区域生长 (region-growing): 种子点, 包含准则 (criterion)
* 区域分割和融合 (region split-and-merge): 把图像打散为一些区域, 然后按照规则合并或分割已有的区域

## 基于统计推断的分割 (Optimal Statistical Inference)


<div class="polaroid">
    <img class="cool-img" src="/images/2019-5/Graph-Cuts-2.png" Graph-Cuts/>
    <div class="container">
        <p>Graph-Cuts 示例</p>
    </div>
</div>

## 6. References

1. **U-net: Convolutional networks for biomedical image segmentation**<br />
   Olaf Ronneberger, Philipp Fischer, Thomas Brox. <br />
   [[link]](https://link.springer.com/chapter/10.1007/978-3-319-24574-4_28). In MICCAI, 2015.

