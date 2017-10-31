---
layout: post
title: Python装饰器 (二)
data: 2017-10-31 20:20:00
categories: Python
tags: python语法 
---

* content
{:toc}

## Python 的类装饰器
通过在类的方法前面加装装饰器, 可以实现更丰富的类的方法和更简洁的用法.




### @property @name.setter

在 `python` 的类中可以直接把属性暴露在外面, 允许使用者直接查看或者修改, 但是这样就无法对属性设定限制:

```python
class Student(object):
    def __init__(self):
        self.score = 0

s = Student()
s.score = 1000
```

所以为了限制属性不能任意指定, 可以通过接口函数来对属性值进行检查:

```python
class Student(object):
    def __init__(self):
        self.score = 0

    def get_score(self):
        return self.score

    def set_score(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Score must be a integer or float.")
        if value < 0 or value > 100:
            raise ValueError("Score is between 0 and 100")
        self.score = value
```

```
>>> s = Student()
>>> s.set_score(60.5)
>>> s.get_score()
60.5
>>> s.set_score(1000)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 10, in set_score
ValueError: Score is between 0 and 100
```

但是上面要使用两个函数作为接口函数, 调用时十分不方便, 这时就可以使用 `property` 装饰器, 调用了该装饰器后会自动生成相应的 `setter` 装饰器:

```python
class Student(object):
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        'setting'
        if not isinstance(value, (int, float)):
            raise ValueError("Score must be a integer or float.")
        if value < 0 or value > 100:
            raise ValueError("Score is between 0 and 100")
        self._score = value
```

```
>>> s = Student()
>>> s.score
0
>>> s.score = 100
>>> s.score
100
>>> s.score = 1001
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 13, in score
ValueError: Score is between 0 and 100
```

如果在上面的类中不定义 `score.setter` 方法, 那么 `score` 就变成了一个只读属性. 