---
layout: post
title: "PyTorch 训练慢的问题"
date: 2021-06-09 17:25:00 +0800
categories: PyTorch
author: Jarvis
meta: Post
mathjax: true
---

* content
{:toc}

本文记录了使用 PyTorch 训练模型时张量不连续导致速度极慢的问题.



## 张量不连续导致训练慢

今天遇到的一个用 PyTorch 训练模型慢的原因是张量不连续的问题. 张量不连续时 PyTorch 有可能报如下的警告

```text
Warning: Mixed memory format inputs detected while calling the operator. The operator will output channels_last tensor even if some of the inputs are not in channels_last format. (function operator())
```

但比较坑的是也可能不报, 这就导致在 debug 的时候一开始并没有注意到时张量不连续的问题. PyTorch 的张量像 numpy 数组一样支持在不改变底层数据存储的前提下, 改变张量的形状、提取子张量、改变轴的顺序等操作. 若数据存储的顺序和轴的顺序不一致时, 就可能会导致张量不连续的问题. 当然了这个问题并不总是会导致错误, 但仍然值得关注. 

拿这次遇到的问题来举例. 我们通常使用 PyTorch 自带的 `torch.utils.data.Dataset` 和 `torch.utils.data.DataLoader` 来构造数据加载器. 通过继承 `Dataset`, 自己实现 `__init__()`, `__len__()` 和 `__getitem__()` 即可. 在 `__getitem__()` 中, 通常会有这样的数据读取和预处理过程:

```python
class MyDataset(Dataset):
    def __init__(self, data_list):
        self.files = data_list
	
    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):
        filename = self.files(index)

        image1 = np.array(Image.open(filename))
        image2 = augmentation(image1)
        image3 = image2.transpose(2, 0, 1)          # (1)
        image = torch.from_numpy(image3).float()    # (2)
        return image
```

上面的代码中:

* (1) 处的轴重排是把 HWC 变为 CHW 以符合 PyTorch 轴的顺序, 注意**此时 `image3` 已经是不连续数组了**. 
* (2) 处的代码是把 `np.ndarray` 转为 `torch.Tensor`, 由于 `torch.from_numpy()` 输出的 `torch.Tensor` 和输入的 `np.ndarray` 是共享内存的, **所以 `image` 是不连续张量**.

然后我们还会使用 `DataLoader` 来构造数据生成器, 且生成的是一个一个 batch 的数据,

```python
dataset = MyDataset(data_list)
dataloader = DataLoader(dataset, 
                        batch_size=4, 
                        shuffle=True, 
                        num_workers=4, 
                        drop_last=True, 
                        pin_memory=True)

for image in dataloader:
    prob = train_step(image)                        # (3)
    # ......
```

* (3) 处的 `image` 的是一个 batch 的数据, 尺寸为 `[B, 3, H, W]`. 注意, **此处的 `image` 已经是一个连续的张量了**, 所以应该是 `DataLoader` 对每一个图像做了重排, 所以正常情况下我们就可以拿 `image` 去训练了.

今天遇到的问题是, 我在 `train_step()` 额外输入了其他的原始数据, 并且在 `train_step()` 中做了数据预处理, 其中包括了 `transpose` 操作, 导致数据不连续. 然后 `torch.from_numpy()` 转为张量后仍然是不连续的, 此时送入网络训练就特别慢了, 大约慢了 20 倍. 解决问题只需要把数据强制连续了就可以了,

```python
# Numpy 下操作
print(array.flags['C_CONTIGUOUS'])
array_1 = np.ascontiguousarray(array)
print(array_1.flags['C_CONTIGUOUS'])

# PyTorch 下操作
print(tensor.is_contiguous())
tensor_1 = tensor.contiguous()
print(tensor_1.is_contiguous())
```

关于更详细的数据连续性的解释, 可以参考[知乎文章](https://zhuanlan.zhihu.com/p/64551412). 

## 关于时间的测量

在 PyTorch 中测量时间时, 由于 CUDA 是并行跑的, 所以之间测量 `train_step()` 中的代码运行时间可能不准确, 需要在测量时间前后加一句 CUDA 同步.

```python
torch.cuda.synchronize()
```

可以使用我封装好的 `Timer` 类的实例来方便的测量时间([Github](https://github.com/Jarvis73/Helper/blob/main/helper/timer.py)). 使用方法如下,

```python
timer = Timer()

with timer.start(sync=True):
    prob = model(image)

print(f"Elapse: {timer.diff:.2f}s")
```

{% capture content_name %}
I am plain text.   
I am **Strong**.   
I am `code`.  
I am inline formula $$ \alpha $$ .

I am block formula:

$$
\mathcal{L} = \frac12(a - b)^2
$$

Block code:

```python
from functools import partial
```

List:
* 1
* 2
{% endcapture %}
{% include card.html type='info' content=content_name %}
