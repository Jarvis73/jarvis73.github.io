---
layout: post
title: "numpy.ndarray 笔记"
date: 2020-8-4 12:15:00 +0800
author: Jarvis
meta: Wiki_Python
hidden: true
---

* content
{:toc}

这篇文章主要记录和讨论 `numpy.ndarray` 的一些实现细节和使用过程中需要注意的一些点. 这对理解高维矩阵--张量的实现和使用极其有用. 


## 1. 什么是 `numpy.ndarray`

## 2. `numpy.ndarray` 的实现机制


## 3. 共享内存的那些函数 (存在风险的函数)

* 切片操作

* `np.rot90()`

  通过修改 `strides` 参数实现.

