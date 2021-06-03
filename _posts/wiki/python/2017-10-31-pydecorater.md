---
layout: post
title: Python装饰器
date: 2017-10-31 20:20:00 +0800
update: 2021-05-27
author: Jarvis
meta: Wiki_Python
hidden: true
---

* content
{:toc}


## 1. 通用装饰器 (同时支持带/不带参数)

通常如果我们想要一个装饰器同时支持带参数和不带参数, 需要编写两个函数来实现. 如下:

```python
def deco1(func):
    def new_func(*args, **kwargs):
        # do something
        print("No prefix.")
        return func(*args, **kwargs)
    return new_func

def deco2(prefix=None):
    def inner_deco(func):
        def new_func(*args, **kwargs):
            # do something with `prefix`
            print(f"Using prefix: {prefix}")
            return func(*args, **kwargs)
        return new_func
    return inner_deco

@deco1
def foo1():
    pass

@deco2(prefix='AAA')
def foo2():
    pass

foo1()
foo2()
```

为了简化代码, 我们可以利用 `wrapt.decorator` 来简化上面的代码:

```python
import wrapt
from functools import partial

@wrapt.decorator
def optional_kwargs_decorator(wrapped, instance=None, args=None, kwargs=None):
    if args:
        return wrapped(*args, **kwargs)
    else:
        return partial(wrapped, **kwargs)

@optional_kwargs_decorator
def deco(func, prefix=None):
    def new_func(*args, **kwargs):
        # do something with `prefix`
        if prefix is not None:
            print(f"Using prefix: {prefix}")
        else:
            print("No prefix.")
        return func(*args, **kwargs)
    return new_func

# 不带参数的装饰器, 注意是不加括号的
@deco
def foo1():
    pass

# 带参数的装饰器, 以函数的形式调用并传入参数
@deco(prefix='AAA')
def foo2():
    pass

foo1()
foo2()
```

注意上面这段代码中装饰器 `optional_kwargs_decorator` 如果被 `wrapt.decorator` 装饰了的话, 其签名是固定的. 

虽然上面的代码看起来更复杂了, 但我们额外定义的装饰器 `optional_kwargs_decorator` 是可以复用的, 它的功能就是令被它装饰的装饰器(这个例子里是 `deco`)可以同时以带参数和不带参数的形式使用, 而不需要编写两个函数.

{% include card.html type="info" title="提示" content="要注意区分不带参数的装饰器和带参数的装饰器. @deco 返回的是被装饰过的函数, 而 @deco(prefix='AAA') 实际上是个函数调用 deco(prefix='AAA'), 该函数返回一个装饰器." %}


## 2. 常用装饰器
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