---
layout: post
title: "Tensorflow 自定义数据集 (Tensorflow-Datasets Customization, TFDS)"
date: 2020-11-25 10:57:00 +0800
categories: Tensorflow
figure: /images/2020-11/tensorflow-datasets.jpg
author: Jarvis
meta: Post
---

* content
{:toc}




Tensorflow 提供了一个 `tensorflow-datasets` 的 Python 库来方便地下载、加载和管理数据集 (下文把 Tensorflow-Datasets 缩写为 TFDS). 

{% include card.html type="info" content="由于在中国大陆范围内谷歌服务不可用, 该 API 在中国大陆需要使用代理来下载数据集." %}

## 1. 安装

```bash
pip install tensorflow-datasets
```

### 1.1 配置代理

- 选择任意的代理服务, 假设已经配置了 socks5 代理
- 安装 privoxy 之类的工具, 用于把 socks5 转换为 http, https 和 ftp.
- 运行任意涉及 `tensorflow_datasets` 中 `builder.download_and_prepare()` 语句的脚本时, 增加如下的环境变量:

```bash
export TFDS_HTTP_PROXY=http://127.0.0.1:8118
export TFDS_HTTPS_PROXY=http://127.0.0.1:8118
export TFDS_FTP_PROXY=http://127.0.0.1:8118
```

注意以上三个都要添加. 如果是希望仅对当前命令有效, 则可以直接添加到命令开头:

```bash
TFDS_HTTP_PROXY=http://127.0.0.1:8118 TFDS_HTTPS_PROXY=http://127.0.0.1:8118 TFDS_FTP_PROXY=http://127.0.0.1:8118 python demo.py
```

## 2. 使用内嵌数据 (在线下载)

TFDS 提供了丰富的内嵌数据集, 包括语音, 图像, 视频, 文本等, 例如知名的 mnist, cifar-10, cifar-100 等等. 

对于小型数据集, 我们可以直接使用 API 下载(只会下载一次, 再次调用时会使用缓存的数据集). 

{% include card.html type="info" content="在中国大陆的用户可能无法直接从谷歌云存储(Google Cloud Storage, GCS) 下载这些数据集, 需要在运行脚本时按照第1.1节的方法指定代理服务器." %}

```python
import tensorflow_datasets as tfds

# 指定要加载的数据集名称, split, 和数据下载解压后存放的位置.
datasets = tfds.load('mnist', 
                     split='train', 
                     data_dir='/data/tfds')
```

当然了也可以使用 `builder` API 获取数据集的详细信息:

```python
builder = tfds.builder('mnist', data_dir='/data/tfds')
builder.download_and_prepare()
print(builder.info)

datasets = builder.as_datasets(split='train')
```

关于内嵌数据更详细的用法, 请参看[官方文档](https://www.tensorflow.org/datasets).

## 3. 使用内嵌数据 (手动下载)

纯手动下载数据并使用 TFDS 加载是无法直接调用 API 做到的, 因为 TFDS 内嵌数据集的下载、解压、生成 TFRecord 是一气呵成的, 没有提供 API 来单独完成某一步. 因此这一节只讨论这几个步骤的结果, 从而我们找到数据后复制到其他设备的相应位置即可.

有些服务器在某些情况下可能无法使用代理, 这时候就需要本地下载好数据集后传到服务器上. 我们先需要对 TFDS 数据集的结构做一个分析. 一个完整的 TFDS 数据集包含以下几部分内容:

* 数据集名称 dataset_name: 如 cifar10
* 版本 version: 如 3.0.2
* 数据 data
* 数据信息 dataset info: 如 dataset_info.json
* 数据特征 dataset features: 如 image.image.json, label.label.json

下载的数据 TFDS 会自动进行处理并保存为 TFRecord 格式. 假设我们设置的数据文件夹为 `/data/tfds`, 那么

* 下载的数据保存在: `/data/tfds/downloads` (通常是压缩文件)
* 解压的数据保存在: `/data/tfds/downloads/extracted` 
* 处理过的数据保存在: `/data/tfds/<dataset_name>/<version>`

那么拷贝时我们只需要把处理过的数据(即 TFRecord 数据 + `dataset_info.json` + 其他 `*.json`)复制到目标设备的数据目录下即可. 然后在使用 TFDS 加载数据时设置不下载数据:

```python
datasets = tfds.load('mnist', 
                     split='train', 
                     data_dir='/data/tfds', 
                     download=False)
```

## 4. 使用自定义数据集

TFDS 也支持把我们自己的数据集构造为 TFDS 可以读取的格式, 这样就可以使用 TFDS 直接从本地硬盘读取了. 

首先根据模板自定义数据集的生成文件:

* 如果 `tensorflow_datasets <= 3.2.0`

```bash
python /<site-packages>/tensorflow_datasets/scripts/create_new_dataset.py \
  --dataset <dataset_name> \
  --type image   # text, audio, translation
```

* 如果 `tensorflow_datasets >= 4.0.0`

```bash
tfds --help

tfds new <dataset_name>
```

然后会产生下面的文件(或文件夹), 这个例子是用 `v3.1.0` 的版本生成的, `v4.0.0` 及以后的版本略有不同, 但可以举一反三.

```python
"""my_dataset dataset."""

import tensorflow_datasets.public_api as tfds

_CITATION = """ """

_DESCRIPTION = """ """

class MyDataset(tfds.core.GeneratorBasedBuilder):
  """TODO(my_dataset): Short description of my dataset."""

  # TODO(my_dataset): Set up version.
  VERSION = tfds.core.Version('0.1.0')

  def _info(self):
    # TODO(my_dataset): Specifies the tfds.core.DatasetInfo object
    return tfds.core.DatasetInfo(
        builder=self,
        # This is the description that will appear on the datasets page.
        description=_DESCRIPTION,
        # tfds.features.FeatureConnectors
        features=tfds.features.FeaturesDict({
            # These are the features of your dataset like images, labels ...
        }),
        # If there's a common (input, target) tuple from the features,
        # specify them here. They'll be used if as_supervised=True in
        # builder.as_dataset.
        supervised_keys=(),
        # Homepage of the dataset for documentation
        homepage='https://dataset-homepage/',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    # TODO(my_dataset): Downloads the data and defines the splits
    # dl_manager is a tfds.download.DownloadManager that can be used to
    # download and extract URLs
    path = dl_manager.download_and_extract('https://todo-data-url')

    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            # These kwargs will be passed to _generate_examples
           gen_kwargs={},
        ),
    ]

  def _generate_examples(self):
    """Yields examples."""
    # TODO(my_dataset): Yields (key, example) tuples from the dataset
    yield 'key', {}
```

其中包含三个主要的函数:

* `_info()`: 包含数据集的基本信息和每个数据样本的格式.
* `_split_generators()`: 数据集的下载和划分.
* `_generate_examples()`: 每个 split 的生成器, 每次生成一个样本

我们要做的就是把这个模板文件按照我们自己的数据集填写完毕. 填写的规则可以参考[官方文档](https://www.tensorflow.org/datasets/add_dataset). 

此外, 也可以进一步参考 `/<site-packages>/tensorflow_datasets/image_classification/cifar.py` 这类的例子. 

这里我们要注意, 要使用本地的数据集, 我们需要把上面代码中下载数据的部分改为直接从本地读取即可:

```python
# 把
path = dl_manager.download_and_extract('https://todo-data-url')
# 改为
path = "/path/to/your_dataset"
```

### 4.1 自定义数据集实例

下面给一个读取自定义数据集的一个例子. 该数据集为 PASCAL VOC 2012 数据集, 包含 20 个前景类别, 我们把包含第 1-5 类的图片作为测试数据, 把包含 6-20 类的图片作为训练数据, 打算使用自监督学习训练一个特征提取器. 因此我们需要创建两个只包含图像(不需要标签)的训练集和测试集, 代码如下:

```python
"""voc_fs dataset."""

import collections
from pathlib import Path

import tensorflow.compat.v1 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """ """

_DESCRIPTION = """
PASCAL VOC 2012 datasets for self-supervised learning.
Four splits:
     1 -  5:  aeroplane  bicycle  bird    boat    bootle 
     6 - 10:     bus       car    cat    chair     cow 
    11 - 15: diningtable   dog   horse  motorbike person 
    16 - 20:    plant     sheep   sofa   train     tv
"""


class VocFS(tfds.core.GeneratorBasedBuilder):
    """ PASCAL VOC 2012 datasets for self-supervised learning  """

    VERSION = tfds.core.Version('0.1.0')

    MANUAL_DOWNLOAD_INSTRUCTIONS = "Manually download VOC_FS"

    def _info(self):
        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION,
            features=tfds.features.FeaturesDict({
                "id": tfds.features.Text(),
                "image": tfds.features.Image(shape=(None, None, 3), 
                                             encoding_format='jpeg'),
            }),
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        voc_fs_path = "/data/VOCdevkit/VOC2012" / self.name / str(self.VERSION)

        train_ids = []
        for i in range(6, 21):
            ids = (voc_fs_path / f"Binary_map_aug/train/{i}.txt")\
                .read_text().strip().splitlines()
            ids = [voc_fs_path / f"JPEGImages/{id_}.jpg" for id_ in ids]
            train_ids.extend(ids)
        train_ids = list(set(train_ids))
    
        test_ids = []
        for i in range(1, 6):
            ids = (voc_fs_path / f"Binary_map_aug/val/{i}.txt")\
                .read_text().strip().splitlines()
            ids = [voc_fs_path / f"JPEGImages/{id_}.jpg" for id_ in ids]
            test_ids.extend(ids)
        test_ids = list(set(test_ids))

        return [
            tfds.core.SplitGenerator(name='train', gen_kwargs={ "ids": train_ids }),
            tfds.core.SplitGenerator(name='test', gen_kwargs={ "ids": test_ids }),
        ]

    def _generate_examples(self, ids):
        """Yields examples."""
        for index, id_ in enumerate(ids): 
            yield index, { 'id': id_.stem, 'image': str(id_) }
```

使用 TFDS 加载数据集:

```python
datasets = tfds.load('voc_fs', 
                     split='train', 
                     data_dir='/data/tfds', 
                     download=False)
```

其中第一次加载时 TFDS 会从自动生成 TFRecord 数据集并保存在 `/data/tfds/voc_fs/0.1.0` 目录下, 在第二次加载时就会直接读取了.
