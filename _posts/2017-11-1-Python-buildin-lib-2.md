---
layout: post
title: Python库函数 (二) collections
date: 2017-11-1 19:00:00 +0800
author: Jarvis
meta: Wiki_Python
---

* content
{:toc}

# 标准库函数

* collections.namedtuple




## collections

### namedtuple

这是标准库 `collections` 的一个函数 `namedtupe`, 可以用来容易地创建一个简单的类, 示例如下

```python
from collections import namedtuple

# 创建一个Dog类
Dog = namedtuple('Dog', ['name', 'weight', 'owner'])
rex = Dog('rex', 30, 'Bob')
print(rex)
```

输出

```
Dog(name='rex', weight=30, owner='Bob')
```
