---
layout: post
title: Python 科学计算
date: 2019-6-9 12:15:00 +0800
author: Jarvis
meta: Wiki_Python
---

* content
{:toc}

> Python 表示矩阵主要使用的是 `Numpy` 包, 其常用的科学计算函数主要包含在 `Numpy.linalg` 和 `Scipy.linalg` 中.

## 矩阵分解

* **奇异值分解(singular value decomposition, SVD)**: $S$ 对角阵, 元素为奇异值; $U$ 和 $V$ 为正交阵, 列向量为奇异向量

  ```python
  # LAPACK routine `_gesdd`
  u, s, vh = numpy.linalg.svd(A, full_matrices=True, compute_uv=True)
  ```

* **QR 分解**: $Q$ 为正交矩阵, $R$ 为上三角阵

  ```python
  # LAPACK routines dgeqrf, zgeqrf, dorgqr, and zungqr.
  q, r = numpy.linalg.qr(A, mode='reduced')
  ```

* **LU 分解**: $L$ 为下三角阵, $U$ 为上三角阵

  ``python
  p, l, u = scipy.linalg.lu(A, permute_l=False, overwrite_a=False, check_finite=True)
  ```
  
  有时候矩阵 $A$ 没有 LU 分解, 比如 $A$ 的第一个元素为0, 且 $A$ 是可逆矩阵. 此时需要对 $A$ 的行进行重排, 因此需要增加一个置换矩阵 $P$ , 从而变为 **PLU 分解**.

