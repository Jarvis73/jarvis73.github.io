---
layout: post
title: Tensorflow 模型的保存和恢复
data: 2017-11-18 17:26:00
categories: Tensorflow
tags: tensorflow
---

* content
{:toc}

这篇文章主要记录一下tensorflow中模型的创建保存和恢复, 另外还涉及到框架下一些内建函数的使用方法. 

# 模型的保存

模型保存使用函数 `tf.train.Saver()`, 

# 内建函数的使用

## NewCheckpointReader

当我们已经有了保存好的模型时, 一般会有如下四个文件:

* checkpoint
* model.ckpt-1234.data-00000-of-00001
* model.ckpt-1234.index
* model.ckpt-1234.meta

可以通过以下方法查看模型中所有的变量:

```python
import tensorflow as tf
reader = tf.train.NewCheckpointReader("D:/Logging/SA/train/model.ckpt-1234")
variables = reader.get_variable_to_shape_map()
for ele in variables:
    print(ele)
```
