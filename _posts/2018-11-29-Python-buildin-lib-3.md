---
layout: post
title: Python库函数 (三) functools, itertools
date: 2018-11-29 19:15:00 +0800
author: Jarvis
meta: Wiki_Python
---

* content
{:toc}

# 标准库函数

* functools.reduce
* itertools.groupby




## functools

### reduce

`reduce()` 是 `functools` 中的一个比较常用的函数, 在 Python2 中是 build-in 函数, 而在 Python3 中被移至 `functools` 模块中. 它的作用是按照给定的规则(一个二元函数)对一个列表做维度压缩, 其定义为 `reduce(function, sequence, initial)`. 下面是一个简单的列表求和的例子

```python
a = [3, 2, 1, 4, 5]
result = reduce(lambda x, y: x + y, a, 0)
# 等价写法 1
result = reduce(sum, a, 0)
# 等价写法 2
result = sum(a)

print(result)
```

输出
```
15
```

与此类似的, Tensorflow 中许多基础的数学函数都是以`reduce`开头的, 如 `reduce_sum(), reduce_prod(), reduce_min()` 等. 下面是一个求列表最小值的例子

```python
a = [3, 2, 1, 4, 5]
result = reduce(lambda x, y: x if x <= y else y, a, 0x80000000)
# 等价写法 1
result = reduce(min, a, 0)
# 等价写法 2
result = min(a)
```

容易发现简单的函数直接使用是最简单的, 但是当我们需要更复杂的计算时使用 `reduce` 是一个更好的选择, 而不是使用 for 循环.


## itertools

### groupby

使用 `groupby` 往往是有很具体的目的, 比如输入一个数组, 按照其中的值输出一个分类的字典, 字典中包含了每个类别的元素在原始数组中的索引. `groupby` 的定义为 `groupby(iterable, key)`. 下面是一个具体的例子

```python
array = [1, 2, 2, 0, 0, 0, 1, 0, 2, 1]
gropuedLabels = dict((k, list(zip(*g))[1]) for k, g in groupby(sorted(zip(array, range(len(array))), key=lambda x: x[0]), key=lambda x: x[0]))
```

输出

```
{0: (3, 4, 5, 7), 1: (0, 6, 9), 2: (1, 2, 8)}
```

可以发现我们在使用 `groupby` 的时候先对原始数组做了排序, 这是 `groupby` 很坑的一点, 它只能对相邻的相同元素进行分组, 所以不相邻但值相同的元素仍然会被它划分为不同的组. 为了最后获取索引, 我们对数据和索引 `zip(array, range(len(array)))` 同时进行排序. 在例子中我们使用了 `groupby` 的 `key` 参数, 该参数输入一个函数, `groupby` 会先使用该函数映射原始数据后再进行分组.
