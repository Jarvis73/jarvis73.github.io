---
layout: post
title: Python库函数 (一) logging
date: 2017-10-31 20:26:00
author: Jarvis
meta: Wiki_Python
---

* content
{:toc}

# 标准库函数

* logging.Handler, logging.Formatter

**Update 2018-4-14:** add some functions to `logger`




## logging

### getLogger FileHandler StreamHandler

`logging` 是个用来定义输出的模块, `print` 函数只能指定一个输出, 有时候我们既想在终端输出, 也想保存在文件中, 一种方法是同时使用 `print` 和文件操作的 `write` 函数来进行, 而 `logging` 则可以很优雅的定制双输出方式. 代码如下

```python
import os
import logging
from time import time, strftime, localtime
from datetime import datetime

levels = [logging.NOTSET,
          logging.DEBUG,
          logging.INFO,
          logging.WARNING,
          logging.ERROR,
          logging.CRITICAL]

def create_logger(log_file=None, file_=True, console=True, 
                  withtime=False, file_level=2, console_level=2):
    if file_:
        prefix = strftime('%Y%m%d%H%M%S', localtime(time()))
        if log_file is None:
            log_file = os.path.join(os.path.dirname(__file__), prefix)
        elif withtime:
            log_file = os.path.join(os.path.dirname(log_file), prefix + "_" + os.path.basename(log_file))

        if os.path.exists(log_file):
            os.remove(log_file)

    logger = logging.getLogger()
    logger.setLevel(levels[0])

    formatter = logging.Formatter("%(message)s")

    if file_:
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(levels[file_level])
        file_handler.setFormatter(formatter)
        # Register handler
        logger.addHandler(file_handler)

    if console:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(levels[console_level])
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# Using
logger = create_logger()
logger.info('Some messages')
logger.debug('Debug infomation')
logger.error('Some errors')
```

输出


```
# Console
Some messages
Some errors
```

```
# File 20171119020228.log
Some messages
Some errors
```

注意以下几点:

* 不指定文件名时使用当前日期和时间自动生成文件名比如 `20171119020228.log`
* `setlevel()` 函数用来设置记录信息的级别, 在 `logging` 模块中总共有六级信息, 分别是
  * CRITICAL
  * ERROR
  * WARNING
  * INFO
  * DEBUG
  * NOTSET

  等级从高到低, 设置为某一等级的意思是低于该等级的信息将不会显示, 比如我们上面设置了等级为 `INFO`, 那么 `logger.debug('message')` 的信息将不会被记录下来.
* 使用 `logging.FileHandler()` 创建文件句柄, 使用 `logging.StreamHandler()` 创建控制台句柄.
* 使用 `logging.Formatter()` 创建信息格式化方式, 其中 `%(message)s` 是 `python` 中的格式化字符串, 一般来说 `%s` 表示字符串, 可以使用 `'%s - %s' % (name1, name2)` 这样的形式(元组)来为格式化字符串传值. 而 `%(message)s` 的方式可以为该格式化字符串指定名称 `message`, 这样可以通过字典来传值, 比如 `'%(message)s - %(name)s' % {'message': msg, 'name': name}`.

### Formatter

有时候我们希望 `logger` 的输出有一定的格式, 那么就可以使用 `logging.Formatter` 类来指定. 自动识别的格式有如下几种, 其他的请参考 ![Python API Doc](https://docs.python.org/3.6/library/logging.html?highlight=logging%20formatter#logrecord-attributes).

| 属性名 | 格式 | 描述 |
|:------|:----|:-----|
| `asctime` | `%(asctime)s` | 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒 |
| `levelname` | `%(levelname)s` | 日志级别, 英文单词 |
| `levelno` | `%(levelno)s` | 日志级别, 数字 |
| `message` | `%(message)s` | 输出的消息 |
| `msecs` | `%(msecs)d` | 时间的毫秒数 |
| `name` | `%(name)s` | Logger 的名字 |

举个例子, 假如格式化字符串为

```python
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
```

那么 `logger.info('Some message')` 会输出 `2017-11-19 15:54:12,345 INFO Some message` 这样的信息. 

下面给出一个实例, 用来得到和 `tensorflow` 类似下面这样的输出消息格式

```
2017-11-19 02:02:37.110996: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.1 instructions, but these are available on your machine and could speed up CPU computations.
2017-11-19 02:02:37.111027: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.2 instructions, but these are available on your machine and could speed up CPU computations.
2017-11-19 02:02:37.111033: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX instructions, but these are available on your machine and could speed up CPU computations.
2017-11-19 02:02:37.111055: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX2 instructions, but these are available on your machine and could speed up CPU computations.
2017-11-19 02:02:37.111060: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use FMA instructions, but these are available on your machine and could speed up CPU computations.
2017-11-19 02:02:37.823554: I tensorflow/core/common_runtime/gpu/gpu_device.cc:955] Found device 0 with properties: 
name: GeForce GTX 1080 Ti
major: 6 minor: 1 memoryClockRate (GHz) 1.582
pciBusID 0000:86:00.0
Total memory: 10.91GiB
Free memory: 10.76GiB
2017-11-19 02:02:37.823608: I tensorflow/core/common_runtime/gpu/gpu_device.cc:976] DMA: 0 
2017-11-19 02:02:37.823624: I tensorflow/core/common_runtime/gpu/gpu_device.cc:986] 0:   Y 
2017-11-19 02:02:37.823642: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1045] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX 1080 Ti, pci bus id: 0000:86:00.0)
```

我们看到这里的时间是以小数点加三位毫秒和三位微秒数字结尾的, 并且级别信息为单个字母. 可以通过重载 `logging.Formatter()` 类来实现

```python
import logging

class MyFormatter(logging.Formatter):
    converter = datetime.fromtimestamp

    # Here the `record` is a LogRecord obejct
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s

def create_logger(...):
    ...
    ...

    formatter = MyFormatter("%(asctime)s: %(levelname).1s %(message)s")
    ...
    ...
    return logger
```

其中 `%(levelname).1s` 表示只输出字符串的第一个字符.

### Stream

有时候我们不用 `print()` 来打印信息, 而需要 `pprint.pprint()` 这样的函数来打印格式化的信息, 一般来说 `pprint` 函数也是直接打印到控制台的, 如果要控制打印位置, 则需要添加参数. 此时我们可以按照如下的方式使用我们的 `logger` :

```python
from pprint import pprint

some_message = "123456"

# print 函数
for handler in logger.handlers:
    print(some_message, file=handler.stream)

# pprint 函数
for handler in logger.handlers:
    pprint(some_message, stream=handler.stream)
```
