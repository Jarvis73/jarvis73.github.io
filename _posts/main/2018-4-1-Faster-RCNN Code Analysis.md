---
layout: post
title: Faster R-CNN(Tensorflow) 源码解析
date: 2018-04-01 18:24:00 +0800
categories: 深度学习
figure: /images/2018-4-1/faster-rcnn.png
author: Jarvis
meta: Post
---

* content
{:toc}

以下代码来源于[Faster RCNN](https://github.com/endernewton/tf-faster-rcnn). 由于该代码太长, 所以这里做个注释, 即是为了自己理清思路, 也是为了改写时方便.

源码运行入口在 `./tf-faster-rcnn/experiments/scripts/train_faster_rcnn.sh`  

python 程序入口在 `./tf-faster-rcnn/tools/trainval_net.py`





## 1. 数据预处理 + 输入层

目前数据工厂里支持的数据集有

* VOC: 2007, 2012
* COCO: 2014, 2015

### 1.1 数据预处理

该程序支持同时使用多个数据集, 首先对多个数据集 (字符串, 用加号连接) 进行预处理:

```python
imdb, roidb = combined_roidb(args.imdb_name)
```

获取单个数据集, 这里的 `imdb` 是由匿名函数生成的类 `pascal_voc` 或者类 `coco` 的一个实例.

```python
imdb = get_imdb(imdb_name)
```

以 `pascal_voc 2007` 为例, 给出该数据集的目录树

```
tf-faster-rcnn/data/VOCdevkit2007
└── VOC2007
    ├── Annotations
    |   ├── 000001.xml
    |   ├── ...
    |   └── 009963.xml
    ├── ImageSets
    │   ├── Layout
    │   │   ├── test.txt
    │   │   ├── train.txt
    │   │   ├── trainval.txt
    │   │   └── val.txt
    │   ├── Main
    │   │   ├── aeroplane_test.txt
    │   │   ├── aeroplane_train.txt
    │   │   ├── aeroplane_trainval.txt
    │   │   ├── aeroplane_val.txt
    │   │   ├── ...
    │   │   ├── test.txt
    │   │   ├── train.txt
    │   │   ├── trainval.txt
    │   │   └── val.txt
    │   └── Segmentation
    │       ├── test.txt
    │       ├── train.txt
    │       ├── trainval.txt
    │       └── val.txt
    ├── JPEGImages
    ├── SegmentationClass
    └── SegmentationObject
```

类 `pascal_voc` , 该类继承自类 `imdb` , `imdb` 是所有数据集的公共类.

#### 1.1.1 类 `pascal_voc` 

* `self._year` 为数据集的年份
* `self._image_set` 取值于 `['tran', 'val', 'trainval', 'test']` .
* `self._devkit_path`  数据根目录: `./tf-faster-rcnn/data/VOCdevkit2007/` 
* `self._data_path`  数据目录: `./tf-faster-rcnn/data/VOCdevkit2007/VOC2007`  
* `self._classes`  元组, 背景的类别名称总是在第 0 个位置
* `self._class_to_ind`  字典, 类别到数字的映射
* `self._image_ext`  图像的后缀
* `self._image_index`  列表, 该数据集中每幅图像的编号
* `self._roidb_handler`  两种选择, `gt_roidb` 或 `rpn_roidb` .
* `self.roidb` 边界框数据库, 等于下面 `gt_roidb` 函数的返回值


**获得 ground truth 感兴趣区域的数据库, 并保存为 `pkl` 格式的文件** 

如果已经存在数据库, 则直接返回存在的数据库, 否则生成新的数据库. 下面的 `self._load_pascal_annotation()` 使用图像的编号从 xml 文件中读取相应的标注 (标注文件的名称与图像标号一致), 该函数返回一个字典, 包含如下键值对:

* `boxes`  二维数组, `shape = [num_objs, 4]` , 4 表示边界框是左上和右下两点的坐标
* `gt_classes`  一维数组, `shape = [num_objs]` 
* `gt_overlaps`  二维数组, `shape = [num_objs, num_cls]` , 每一行表示一个物体, 表示该物体的列对应的值设为 1.0, 其他均为 0.
* `seg_areas`  一维数组, `shape = [num_objs]` , 边界框包含区域的面积

```python
def gt_roidb(self):
    """
    Return the database of ground-truth regions of interest.

    This function loads/saves from/to a cache file to speed up future calls.
    """
    cache_file = os.path.join(self.cache_path, self.name + '_gt_roidb.pkl')
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as fid:
            try:
                roidb = pickle.load(fid)
            except:
                roidb = pickle.load(fid, encoding='bytes')
        print('{} gt roidb loaded from {}'.format(self.name, cache_file))
        return roidb

    # a dict consists of bounding boxes an  objects of one image
    gt_roidb = [self._load_pascal_annotation(index) for index in self.image_index]
    with open(cache_file, 'wb') as fid:
        pickle.dump(gt_roidb, fid, pickle.HIGHEST_PROTOCOL)
    print('wrote gt roidb to {}'.format(cache_file))

    return gt_roidb
```

#### 1.1.2 数据处理 

1. 获取 `pascal_voc` 类的一个实例, `imdb = get_imdb(imdb_name)`  
2. 设置建议方法 `imdb.set_proposal_method(cfg.TRAIN.PROPOSAL_METHOD)` , 有 `gt` 和 `rpn` 两种选择
3. 获取 roidb (即为 labels)
   * 添加反转后的边界框 `imdb.append_flipped_images` 
   * 准备训练数据 `rdl_roidb.prepare_roidb(imdb)` . 这一步为 roidb 列表中的每个字典添加了部分键:
     * `image`  图像路径
     * `width`  图像宽度
     * `height`  图像高度
     * `max_classes`  一维数组, `shape = [num_objs]` , 每一行表示与该边界框重合度最高的物体类别(由于这里是使用的 ground truth, 所以这里的类别就是该物体自己的类别)
     * `max_overlaps`  一维数组, `shape = [num_objs]` ,  每个值这里都为 1, 表示每个物体的边界框与某个物体的边界框(包括它自己的) 最大的重叠度为 1. 这两个指标在使用 ground truth rois 的时候是没用的, 因为取值都为 1, 没有实用价值. 当我们使用 `rpn` 的建议方法时应该就会有用了.

### 1.2 输入层

#### 1.2.1 类  `ROIDataLayer`

输入 ground truth rois 的层, 使用 `self.forward()` 方法来获取下一个小批. 其中涉及到一个函数 `get_minibatch()` 用于把小批的 `roidb[i]` (也就是一小批字典) 中的边界框信息提取出来并整合为输入的格式. 

##### `get_minibatch()`

返回网络输入的一个小批, 是一个字典:

* `data`: 三维数组, 形状为 `[num_img, h, w, 3]`. 神经网络的图像输入, 此处的 `num_img=1` 

* `gt_boxes`: 边界框, 形状为 `[num_gt_indexs, 5]` 

* `im_info`: 图像信息, 三个元素, 前两个元素为最终输入图像的高和宽, 第三个元素为原始图像缩放为当前图像的比例


##### `_get_image_blob()`



## 2. 神经网络构建 ---- `network.py`

先列出一些变量含义:

|    变量    | 含义                                 |
| :------: | ---------------------------------- |
| `img_bs` | 输入图像的 batch size, 代码中 `img_bs = 1` |
| `tri_bs` | 训练 Fast RCNN 所用 `rois` 的批大小        |
|   `h`    | 主干网络头部输出的特征图的高度                    |
|   `w`    | 主干网络头部输出的特征图的宽度                    |
|   `A`    | 在上述特征图上的每个点产生 `A` 个 anchor         |
|   `K`    | 多目标检测任务的种类数, 背景也算一类                |

下面给出 `class Network` 的变量列表, 一级列表均为字典, 二级列表为字典的键:

* `self._predictions` 
  * `rpn_cls_score`  RPN 网络二分类的的得分, 未经过 `softmax` 层, `shape = [img_bs, h, w, A*2]` 
  * `rpn_cls_score_reshape`  RPN 网络二分类的得分, 未经过 `softmax` 层, `shape = [img_bs, A*h, w, 2]`  
  * `rpn_cls_prob`  RPN 网络二分类的概率, 经过了 `softmax` 层, `shape = [img_bs, A*h, w, 2]` 
  * `rpn_cls_pred`  RPN 网络二分类的预测结果, `shape = [img_bs*A*h*w]` 
  * `rpn_bbox_pred`  RPN 网络边界框回归的预测结果, `shape = [img_bs, h, w, A*4]` 
  * `cls_score`  Fast RCNN 网络多分类的得分, 未经过 `softmax` 层, `shape = [tri_bs, K]` 
  * `cls_pred`  Fast RCNN 网络多分类的预测及过, `shape = [tri_bs]` 
  * `cls_prob`  Fast RCNN 网络多分类的概率, 经过了 `softmax` 层, `shape = [tri_bs, K]` 
  * `bbox_pred`  Fast RCNN 网络边界框回归的预测结果, `shape = [tri_bs, K*4]`  
  * `rois`  RPN 网络 (代替 Selective Search) 产生的感兴趣区域, 可直接用于训练 Fast RCNN 部分, `shape = [tri_bs, 5]` . 这里的 `5` 表示 `[img_index, x1, y1, x2, y2]` .
* `self._anchor_targets` 
  * `rpn_labels`  RPN 网络二分类的稀疏 ground truth, `shape = [img_bs, 1, A*h, w]` 
  * `rpn_bbox_targets`  RPN 网络边界框回归的 ground truth, `shape = [img_bs, h, w, A*4]` 
  * `rpn_bbox_inside_weights`  RPN 网络边界框回归的权重, `shape = [img_bs, h, w, A*4]` . 
  * `rpn_bbox_outside_weights`  RPN 网络边界框回归的权重, `shape = [img_bs, h, w, A*4]` . 计算光滑化的 `L1` 损失时内部权重与 `bbox_labels` 和 `bbox_targets` 的差相乘, 外部权重与 `L1` 损失相乘. 代码中内部损失已经弃用 (权重设置为了 `[1.0, 1.0, 1.0, 1.0]`) .
* `self._proposal_targets` 
  * `rois`  从 `self._predictions`  的 `rois` 中采样出的 `TRAIN.BATCH_SIZE` 个样本
  * `labels`  Fast RCNN 网络多分类的稀疏 ground truth, `shape= [tri_bs, 1]` 
  * `bbox_targets`  Fast RCNN 网络边界框回归的 ground truth, `shape = [tri_bs, K*4]` 
  * `bbox_inside_weights`  Fast RCNN 网络边界框回归的权重, `shape = [tri_bs, K*4]` 
  * `bbox_outside_weights` Fast RCNN 网络边界框回归的权重, `shape = [tri_bs, K*4]` . 内外权重与上面类似, 不再赘述. 
* `self._losses` 
  * `rpn_cross_entropy`  RPN 网络二分类的交叉熵损失
  * `rpn_loss_box`  RPN 网络边界框回归的光滑化 `L1` 损失
  * `cross_entropy`  Fast RCNN 网络多分类的交叉熵损失
  * `loss_box`  Fast RCNN 网络边界框回归的光滑化 `L1` 损失
  * `total_loss` 包含了以上四项损失以及权重/偏置的 `L2` 正则化的总损失
* `self._layers` 
  * `head`  主干网络的头部输出
* `self._act_summaries` (该变量是一个列表)
  * `net`  主干网络的头部输出
  * `rpn`  RPN 网络使用 `3x3` 卷积代替滑窗全连接层的输出
* `self._score_summaries` 
  * `self._anchor_targets`  
  * `self._proposal_targets`  
  * `self._predictions`  
* `self._event_summaries`  
  * `self._losses`  

### 2.1 网络输入

```python
self._image = tf.placeholder(tf.float32, shape=[1, None, None, 3])	# [bs, h, w, c]
self._im_info = tf.placeholder(tf.float32, shape=[3])	# [h, w, image_scale]
self._gt_boxes = tf.placeholder(tf.float32, shape=[None, 5])
```

*   Faster RCNN 由于其网络结构的特殊性, 输入 `_image` 仅允许 `batch size = 1` ; 但也得益于网络结构, 接受不同大小图片的输入. 
*   `_im_info` 有三个元素, 前两个元素为最终输入图像的高和宽, 第三个元素为原始图像缩放为当前图像的比例
*   而另一个输入 `_gt_boxes` 为边界框, 第 0 维对应当前输入图像中要寻找的物体的数量, 第 1 维的值为 5, 对应 $[t_x, t_y, t_w, t_h, label]$. 这里的 `label` 是该物体的编号值.


---

下面的部分主要分析各个**网络层 ---- `self._build_network()`**  

1. 定义权重/偏置的初始化器以及正则化器 ---- `initializer & regularizer`
2. 输入图像 --> 主干网络前端 ---- `self._image_to_head()` 
3. 计算 anchors (即在网格上计算所有的 anchors, 每个格点 A 个) ---- `self._anchor_component()`
4. 主干网络前端 --> 区域建议 ---- `self._region_proposals()` 
5. 区域建议 --> roi pooling 层 ---- `self._crop_pool_layer()` 
6. roi pooling 层 --> 主干网络尾部 ---- `self._head_to_tail()` 
7. 主干网络尾部 --> 预测输出 ---- `self._region_classification()`

**其中 2 是共享网络 (Faster R-CNN 原文中是共享的, 该代码中已经合并为同一个网络); 3, 4 属于 RPN 网络部分; 5, 6, 7 属于 Fast R-CNN 部分** . 接下来对每个部分进行详细的解析. 

---


### 2.2 构建网络 ---- 主干部分 `self._image_to_head()` 

`Network` 类是一个基类, 构建网络的主干部分要求由继承 `Network` 的类来实现. 

使用了 Tensorflow 的一个 contribution ---- `slim` , 可以大幅简化 Tensorflow 网络构建过程. 以 VGG16为例:

```python
with tf.variable_scope(self._scope, self._scope, reuse=reuse):
  net = self._image
  net = slim.repeat(net, 2, slim.conv2d, 64, [3, 3], trainable=False, scope='conv1')
  net = slim.max_pool2d(net, [2, 2], padding='SAME', scope='pool1')
  net = slim.repeat(net, 2, slim.conv2d, 128, [3, 3], trainable=False, scope='conv2')
  net = slim.max_pool2d(net, [2, 2], padding='SAME', scope='pool2')
  net = slim.repeat(net, 3, slim.conv2d, 256, [3, 3], trainable=is_training, scope='conv3')
  net = slim.max_pool2d(net, [2, 2], padding='SAME', scope='pool3')
  net = slim.repeat(net, 3, slim.conv2d, 512, [3, 3], trainable=is_training, scope='conv4')
  net = slim.max_pool2d(net, [2, 2], padding='SAME', scope='pool4')
  net = slim.repeat(net, 3, slim.conv2d, 512, [3, 3], trainable=is_training, scope='conv5')

  self._act_summaries.append(net)
  self._layers['head'] = net
```

注意这里的前两个 repeat 块都设置了 `trainable = False` . 

### 2.3 构建网络 ---- RPN 部分, 计算 Anchors `self._anchor_component()`    

函数 `self._anchor_component()` 计算得到特征图上所有 Anchors 的坐标 (注意, anchors 是在特征图上计算的, 但是该函数返回的坐标是 anchor 在原始图像上的坐标), 函数内部定义了两个成员变量:

* `self._anchors` 形状为 `[w*h*3*3, 4]` 
* `self._anchor_length` 一个整数, 值为 `w * h * 3 * 3` 

由于要在每个位置产生 A 个 anchors, 所以可以只计算以左上角的点为中心的 A 个 anchors, 然后在二维网格上平移即可得到所有的 anchors. 下面的代码用于计算左上角的点为中心的 A 个 anchors:

```python
def generate_anchors(base_size=16, ratios=[0.5, 1, 2],
                     scales=2 ** np.arange(3, 6)):
    """
    Generate anchor (reference) windows by enumerating aspect ratios X
    scales wrt a reference (0, 0, 15, 15) window.
    """

    base_anchor = np.array([1, 1, base_size, base_size]) - 1
    ratio_anchors = _ratio_enum(base_anchor, ratios)
    #                                 h : w
    # [[ -3.5   2.   18.5  13. ]    0.5 : 1
    #  [  0.    0.   15.   15. ]      1 : 1
    #  [  2.5  -3.   12.5  18. ]]     2 : 1
    
    anchors = np.vstack([_scale_enum(ratio_anchors[i, :], scales)
                         for i in range(ratio_anchors.shape[0])])

    return anchors
```

这里给出 A = 3x3 的一个例子, 下表列出这 9 个 anchors 的详细信息

| No.  | h * scales, w * scales    | ratio   | scales | shape      | Approx area       |
| ---- | ------------------------- | ------- | ------ | ---------- | ----------------- |
| 1    | [ -84.  -40.   99.   55.] | 0.5 : 1 | 8      | [ 96, 184] | (16x16) x (8x8)   |
| 2    | [-176.  -88.  191.  103.] | 0.5 : 1 | 16     | [192, 368] | (16x16) x (16x16) |
| 3    | [-360. -184.  375.  199.] | 0.5 : 1 | 32     | [384, 736] | (16x16) x (32x32) |
| 4    | [ -56.  -56.   71.   71.] | 1 : 1   | 8      | [128, 128] | (16x16) x (8x8)   |
| 5    | [-120. -120.  135.  135.] | 1 : 1   | 16     | [256, 256] | (16x16) x (16x16) |
| 6    | [-248. -248.  263.  263.] | 1 : 1   | 32     | [512, 512] | (16x16) x (32x32) |
| 7    | [ -36.  -80.   51.   95.] | 2 : 1   | 8      | [176,  88] | (16x16) x (8x8)   |
| 8    | [ -80. -168.   95.  183.] | 2 : 1   | 16     | [352, 176] | (16x16) x (16x16) |
| 9    | [-168. -344.  183.  359.] | 2 : 1   | 32     | [704, 352] | (16x16) x (32x32) |

然后使用把这 9 个 anchors 在二维网格上平移得到所有位置的所有 anchors. 这里的 anchors 是绝对位置, 总共有 $K \times A = (w \times h) \times (n \times n) $ 个, 所以最终是一个形状为 $[k \times A, 4]$ 的数组. 这里的 width 和 height 均为最后一个卷积输出的特征图的尺寸, 即 RPN 网络会在该特征图上滑动.

```python
A = anchors.shape[0]    # A = 9
shift_x = np.arange(0, width) * feat_stride
shift_y = np.arange(0, height) * feat_stride
shift_x, shift_y = np.meshgrid(shift_x, shift_y)

# ravel(): Return a flattened array.
# shift length of [x1, y1, x2, y2]
shifts = np.vstack((shift_x.ravel(), shift_y.ravel(),
                    shift_x.ravel(), shift_y.ravel())).transpose()
K = shifts.shape[0] # w * h
# width changes faster, so here it is H, W, C
anchors = anchors.reshape((1, A, 4)) + shifts.reshape((1, K, 4)).transpose((1, 0, 2))
anchors = anchors.reshape((K * A, 4)).astype(np.float32, copy=False)
```

### 2.4 构建网络 ---- RPN 部分, 计算区域建议 `self._region_proposal()` 

#### 2.4.1 网络结构

使用卷积代替全连接来加快计算速度. 第一个 `slim.conv2d` 使用 3x3 的卷积核来代替在 3x3 的 window 中的全连接操作, 得到 `cfg.RPN_CHANNELS` 维 (比如 512) 的向量 (实际上是 height x width x 512 的张量). 后面的两个 `slim.conv2d` 分别得到 `2A` 个分类结果和 `4A` 个 BBox 回归系数. 

```python
rpn = slim.conv2d(net_conv, cfg.RPN_CHANNELS, [3, 3], 
                  trainable=is_training,
                  weights_initializer=initializer,
                  scope="rpn_conv/3x3")
self._act_summaries.append(rpn)
# [bs, h, w, 9*2]
rpn_cls_score = slim.conv2d(rpn, self._num_anchors * 2, [1, 1], 
                            trainable=is_training,
                            weights_initializer=initializer,
                            padding='VALID', 
                            activation_fn=None, 
                            scope='rpn_cls_score')
...
...
...
# [bs, h, w, 9*4]
rpn_bbox_pred = slim.conv2d(rpn, self._num_anchors*4, [1, 1],
                            trainable=is_training,
                            weights_initializer=initializer,
                            padding='VALID', 
                            activation_fn=None, 
                            scope='rpn_bbox_pred')
```

---

#### 计算 RPN 的建议区域 (proposals), 以及训练 RPN 部分的预测 (pred) 和标签 (label)

这一部分比较繁杂, 需要计算的指标比较多, 下面先列举一下:

1. RPN 给出的建议区域, 形状应与 [num_rois, 5] 匹配 ---- `rois` (形状为 [2000, 5])
2. RPN 给出的建议区域的得分, 形状应与 [num_rois] 匹配 ---- `rois_scores` (形状为 [2000])
3. 预测的分类输出, 形状应与 [1, h, w, 9, 2] 匹配 ---- `rpn_cls_prob` (形状为 [1, h, w, 9x2])
4. 预测的回归输出, 形状应与 [1, h, w, 9, 4] 匹配 ---- `rpn_bbox_pred` (形状为 [1, h, w, 9x4])
5. ground truth 分类 label, 形状应与 [1, h, w, 9, 2] 匹配 ---- `rpn_labels` (形状为 [1, 1, 9xh, w])
6. ground truth 回归 label, 形状应与 [1, h, w, 9, 4] 匹配 ---- `rpn_bbox_targets` (形状为 [1, h, w, 9x4])

这里的**形状匹配**是指形状各个维度匹配即可, 实际的形状可能略有不同, 由于 tensorflow 不支持 五维及以上的数组, 所以需要使用四位数组来*周旋*. 

---

#### 2.4.2 分类指标

对二分类 (是/不是物体) 结果使用 softmax 得到

* 二分类概率值 `rpn_cls_prob` ---- 计算损失的指标, 第一个值表示不是物体的概率, 第二个表示是物体的概率.
* 概率高的类别 `rpn_cls_pred` ---- 预测结果(是/不是物体).

```python
# change it so that the score has 2 as its channel size
# [bs, h*9, w, 2]
rpn_cls_score_reshape = self._reshape_layer(rpn_cls_score, 2, "rpn_cls_score_reshape")  
rpn_cls_prob_reshape = self._softmax_layer(rpn_cls_score_reshape, "rpn_cls_prob_reshape")
rpn_cls_pred = tf.argmax(tf.reshape(rpn_cls_score_reshape,[-1,2]),axis=1, name="rpn_cls_pred")
# [bs, h, w, 2*9]
rpn_cls_prob = self._reshape_layer(rpn_cls_prob_reshape, self._num_anchors*2, "rpn_cls_prob") 
```

####2.4.3 获取 2000 个建议区域  `proposal_layer.py` 

```python
rois, roi_scores = self._proposal_layer(rpn_cls_prob, rpn_bbox_pred, "rois")
```

该函数使用所有 anchors 的*类别预测*结果与*边界框预测*结果作为输入, 返回应用 NMS 后的少量 anchors. 下面详述该函数的具体实现.

首先使用 `anchors` 和 `rpn_bbox_pred` 计算 BBox 回归修正后的 anchors 的四个坐标值. 然后把超出图像边界的推荐框裁剪到图像边界. 这里出现的函数 

* `bbox_transform_inv(boxes, delta)` 表示对 anchor 平移 delta 后得到预测的边界框, 而
* `bbox_trainsform(ex_rois, gt_rois)` 表示使用 anchor 和 ground truth bbox 计算四个变换参数

```python
proposals = bbox_transform_inv(anchors, rpn_bbox_pred)
proposals = clip_boxes(proposals, im_info[:2])
```

然后按照每个区域被认为是物体的得分高低进行排序, 选出前 `pre_nms_topN ` 个区域 (大约 12000 个). 

```python
order = scores.ravel().argsort()[::-1]
if pre_nms_topN > 0:
    order = order[:pre_nms_topN]
proposals = proposals[order, :]
scores = scores[order]
```

再应用 `NMS` (非极大抑制) 从每一批重合度最高的区域中选出并保留得分最高的一个, 最后保留 `post_nms_topN` 个区域 (大约 2000 个) 即为我们最终的感兴趣区域 `rois`. 

```python
keep = nms(np.hstack((proposals, scores)), nms_thresh)

# Pick th top region proposals after NMS
if post_nms_topN > 0:
    keep = keep[:post_nms_topN]
proposals = proposals[keep, :]
scores = scores[keep]
```

现在的 `proposals` 只有 4 列, 但是我们最后的 `rois` 是 5 列, 实际上最后又添加了一列图像的指标, 由于我们这里仅支持每一小批单幅图像, 所以在第一列添加 `index = 0` (这里添加的原因可能是为了适应原来的 Fast R-CNN 的代码, 在 Fast R-CNN 中是每一小批两幅图片的, 不过我并未看过 Fast R-CNN 的代码, 仅是猜测).

```python
# Only support single image as input
batch_inds = np.zeros((proposals.shape[0], 1), dtype=np.float32)
blob = np.hstack((batch_inds, proposals.astype(np.float32, copy=False)))
```

#### 2.4.4 回归指标

##### 2.4.4.1 计算每个 anchor 的 label 值 `anchor_target_layer.py`  

这一步要给 `self._anchors` 中的所有 anchor 赋以一个 label 值: 

* 1 : 正样本
* 0 : 负样本
* -1 : 非样本, 不用于训练

首先从所有的 $K\times A\times n\times n$ 个 anchors 中筛掉超出图像边界的, 注意这里是筛掉, 而不是裁剪到边界. 

```python
# allow boxes to sit over the edge by a small amount
_allowed_border = 0

# only keep anchors inside the image
inds_inside = np.where(
    (all_anchors[:, 0] >= -_allowed_border) &
    (all_anchors[:, 1] >= -_allowed_border) &
    (all_anchors[:, 2] < im_info[1] + _allowed_border) &  # width
    (all_anchors[:, 3] < im_info[0] + _allowed_border)  # height
)[0]

# keep only inside anchors
anchors = all_anchors[inds_inside, :]
```

然后计算所有的 anchors 和 ground truth anchors 之间的重叠 (overlaps). 这里的重叠是一个二维数组, 形状为 [N, K] , 这里 N 是边界筛选后 anchors 的数量, K 是 gt anchors 的数量.

* `argmax_overlaps` : 对每个 anchor 选择一个与其重叠最高的 gt anchor 的 index, N 维向量, 取值于 [0, K - 1]
* `max_overlaps` : 上述 index 对应的 overlaps, N 维向量
* `gt_argmax_overlaps` : 对每个 gt anchor 选择一个与其重叠最高的 anchor 的 index, K 维向量, 取值于 [0, N - 1]
* `gt_max_overlaps` : 上述 index 对应的 overlaps, K 维向量

```python
# overlaps between the anchors and the gt boxes
# overlaps (ex, gt)
overlaps = bbox_overlaps(np.ascontiguousarray(anchors, dtype=np.float),
        			     np.ascontiguousarray(gt_boxes, dtype=np.float))
argmax_overlaps = overlaps.argmax(axis=1)
max_overlaps = overlaps[np.arange(len(inds_inside)), argmax_overlaps]   # N
gt_argmax_overlaps = overlaps.argmax(axis=0)
gt_max_overlaps = overlaps[gt_argmax_overlaps, np.arange(overlaps.shape[1])]  # K
```

正样本:

* 所有 anchors 中, 与 gt anchor 重叠最高的 anchor (即重叠矩阵中每一列选一个), 有 K 个
* 与任一个 gt anchor 重叠超过阈值 IOU 的 anchor (即重叠矩阵中按行筛选)

```python
labels[gt_argmax_overlaps] = 1
labels[max_overlaps >= cfg.TRAIN.RPN_POSITIVE_OVERLAP] = 1
```

负样本:

这里的 `cfg.TRAIN.RPN_CLOBBER_POSITIVES` 看起来没什么用, 一般来说正例的阈值要比反例的阈值高, 所以这里负样本在正样本之前赋值或之后赋值都不影响.

```python
if cfg.TRAIN.RPN_CLOBBER_POSITIVES:
    # assign bg labels last so that negative labels can clobber positives
    labels[max_overlaps < cfg.TRAIN.RPN_NEGATIVE_OVERLAP] = 0
```

接下来如果得到的正样本数量超过了每批中需要的正样本数量, 则从其中随机选出需要的数量, 剩下的赋以 `label = -1` 即可, 负样本类似筛选, 但要与正样本数量互补.

```python
num_fg = int(cfg.TRAIN.RPN_FG_FRACTION * cfg.TRAIN.RPN_BATCHSIZE)
fg_inds = np.where(labels == 1)[0]
if len(fg_inds) > num_fg:
    disable_inds = npr.choice(
        fg_inds, size=(len(fg_inds) - num_fg), replace=False)
    labels[disable_inds] = -1

num_bg = cfg.TRAIN.RPN_BATCHSIZE - np.sum(labels == 1)
......
```

##### 2.4.4.2 计算 bbox 的 label 值 `bbox_transform.py` 

只需要应用论文中的四个公式即可, 这里 `bbox_targets` 的形状与 `labels` 相同也是 `N`:

```python
bbox_targets = _compute_targets(anchors, gt_boxes[argmax_overlaps, :])
```

##### 2.4.4.3 为正负样本给定权重

这里的权重分为两种:

* 第一种是一致权重 (uniform weight), 正负样本都除以总的样本数 
* 第二种是非一致权重, 正样本权重为 $p/num(pos)$ , 负样本权重为 $(1-p)/num(neg)$ .

```python
bbox_outside_weights = np.zeros((len(inds_inside), 4), dtype=np.float32)
if cfg.TRAIN.RPN_POSITIVE_WEIGHT < 0:
    # uniform weighting of examples (given non-uniform sampling)
    num_examples = np.sum(labels >= 0)
    positive_weights = np.ones((1, 4)) * 1.0 / num_examples
    negative_weights = np.ones((1, 4)) * 1.0 / num_examples
else:
    assert ((cfg.TRAIN.RPN_POSITIVE_WEIGHT > 0) & (cfg.TRAIN.RPN_POSITIVE_WEIGHT < 1))
    positive_weights = (cfg.TRAIN.RPN_POSITIVE_WEIGHT / np.sum(labels == 1))
    negative_weights = ((1.0 - cfg.TRAIN.RPN_POSITIVE_WEIGHT) / np.sum(labels == 0))
bbox_outside_weights[labels == 1, :] = positive_weights
bbox_outside_weights[labels == 0, :] = negative_weights
```

最后由于 `labels` 和 `bbox_targets` 均是 N 个 anchors 的 (筛去超出边界的), 需要反映射到原始 anchors 上 (未筛选过的), 所以最后使用 `_unmap(data, count, inds, fill=0)` 函数进行反向映射, 这里不再赘述.

### 2.5 构建网络 ---- Fast RCNN 部分

#### 2.5.1 计算用于 Fast RCNN 的 ROIs 及其 Labels ---- `proposal_target_layer.py`

这里就承接了 Fast RCNN 的部分, 使用 RPN 产生的 2000 个 proposals 代替 Selective Search 产生的区域, 然后从这 2000 个中选择 `cfg.TRAIN.BATCH_SIZE` 个作为训练的一批. 

```python
num_images = 1
rois_per_image = cfg.TRAIN.BATCH_SIZE / num_images
fg_rois_per_image = np.round(cfg.TRAIN.FG_FRACTION * rois_per_image)

# Sample rois with classification labels and bounding box regression
# targets
labels, rois, roi_scores, bbox_targets, bbox_inside_weights = _sample_rois(
    all_rois, all_scores, gt_boxes, fg_rois_per_image,
    rois_per_image, _num_classes)
```

下面详述函数 `_sample_rois()` 的细节.  首先使用 `bbox_overlaps()` 函数计算 proposals 和 gt boxes 的重叠矩阵. 然后对每一个 proposals, 获得与其重叠最大的 gt boxes 的指标和重叠值, 将该 gt boxes 的 label 作为该 proposal 的 label.

```python
# overlaps: (rois x gt_boxes)
overlaps = bbox_overlaps(
    np.ascontiguousarray(all_rois[:, 1:5], dtype=np.float),
    np.ascontiguousarray(gt_boxes[:, :4], dtype=np.float))
gt_assignment = overlaps.argmax(axis=1)
max_overlaps = overlaps.max(axis=1)
labels = gt_boxes[gt_assignment, 4]
```

然后使用 Fast RCNN 中建议的阈值: 

* 25% 的前景 (u ≥ 1) 从与 ground truth 的 IoU 重叠超过 0.5 的推荐区域中选择
* 75% 的背景 (u = 0) 从 IoU 在 [0.1, 0.5) 的区域中选取

这里的 25% 对应于上面的 `cfg.TRAIN_FG_FRACTION`. 

```python
fg_inds = np.where(max_overlaps >= cfg.TRAIN.FG_THRESH)[0]
bg_inds = np.where((max_overlaps < cfg.TRAIN.BG_THRESH_HI) &
                   (max_overlaps >= cfg.TRAIN.BG_THRESH_LO))[0]
```

对 Fast RCNN 原始版本微调, 确保可以得到固定数量的样本

```python
if fg_inds.size > 0 and bg_inds.size > 0:
    fg_rois_per_image = min(fg_rois_per_image, fg_inds.size)    
    fg_inds = npr.choice(fg_inds, size=int(
        fg_rois_per_image), replace=False)
    bg_rois_per_image = rois_per_image - fg_rois_per_image
    to_replace = bg_inds.size < bg_rois_per_image
    bg_inds = npr.choice(bg_inds, size=int(
        bg_rois_per_image), replace=to_replace)
elif fg_inds.size > 0:
    to_replace = fg_inds.size < rois_per_image
    fg_inds = npr.choice(fg_inds, size=int(
        rois_per_image), replace=to_replace)
    fg_rois_per_image = rois_per_image
elif bg_inds.size > 0:
    to_replace = bg_inds.size < rois_per_image
    bg_inds = npr.choice(bg_inds, size=int(
        rois_per_image), replace=to_replace)
    fg_rois_per_image = 0
else:
    import pdb
    pdb.set_trace()
```

把正负样本的指标合并, 并把负样本的类别设为 0 . 得到 `rois` 和 `roi_scores` :

```python
# The indices that we're selecting (both fg and bg)
keep_inds = np.append(fg_inds, bg_inds)
# Select sampled values from various arrays:
labels = labels[keep_inds]
# Clamp labels for the background RoIs to 0
labels[int(fg_rois_per_image):] = 0
rois = all_rois[keep_inds]
roi_scores = all_scores[keep_inds]
```

最后使用四个公式计算回归的偏移, 形状为 [N, 5], 其中的 5 表示 [class, tx, ty, th, tw]:

```python
bbox_target_data = _compute_targets(rois[:, 1:5],
         							gt_boxes[gt_assignment[keep_inds], :4], labels)
```

然后把 label 的形状重构一下, 变成 [N, 4xK], K 是类别数这样每行就只有 4 个值有意义

```python
bbox_targets, bbox_inside_weights = _get_bbox_regression_labels(bbox_target_data, num_classes)
```

该层最终返回如下:

* `rois`  形状为 [bs, 5], 第一列为 0
* `roi_scores`  形状为 [bs]
* `labels`  形状为 [bs, 1]
* `bbox_targets`  形状为 [bs, 4xK], K 为类别数
* `bbox_inside_weights`  形状为 [bs, 4xK]
* `bbox_outside_weights`  形状为 [bs, 4xK]


#### 2.5.2 ROI Pooling 层 `_crop_pool_layer()` 

我们现在有了 `rois` , 其坐标是在原始图像下的, 而 ROI Pooling 是在特征图上进行的, 所以先要转换坐标, 这里是直接除以 `_image_to_head` 所下采样的倍数. `bottom` 是指 `_image_to_head` 的输出.

```python
height = (tf.to_float(bottom_shape[1]) - 1.) * np.float32(self._feat_stride[0])
width = (tf.to_float(bottom_shape[2]) - 1.) * np.float32(self._feat_stride[0])
x1 = tf.slice(rois, [0, 1], [-1, 1], name="x1") / width
y1 = tf.slice(rois, [0, 2], [-1, 1], name="y1") / height
x2 = tf.slice(rois, [0, 3], [-1, 1], name="x2") / width
y2 = tf.slice(rois, [0, 4], [-1, 1], name="y2") / height
```

由于反向传播通过 ROI Pooling 层时不需要传播到 ROIs , 所以直接阻止梯度沿 ROIs 继续传播, 同时可以节省时间:

```python
bboxes = tf.stop_gradient(tf.concat([y1, x1, y2, x2], axis=1))
```

接下来使用 tensorflow 中的 `tf.image.crop_and_resize()` 函数来提取 ROIs. 该函数参数如下:

* `image`  4D 的待裁剪张量
* `boxes`  裁剪框, 形状为 [num_boxes, 4]
* `box_ind`  框的指标, 用于指示第 `i` 个框属于第几张输入的图, 形状为 [num_boxes], (由于我们每次使用一张图, 所以该向量全为 0).
* `crop_size`  两个元素, `size = [crop_height, crop_width]` . 所有用 `boxes` 裁出来的块都会 resize 到该大小.
* `method`  resize 的方法, 默认为双线性.

返回值:

* 4-D 张量, 形状为 `[num_boxes, crop_height, crop_width, depth]` .

这里把 `crop_size` 设置为需要的两倍大, 最后采用一个 `max_pooling` .

```python
pre_pool_size = cfg.POOLING_SIZE * 2
crops = tf.image.crop_and_resize(bottom, 
                                 bboxes, 
                                 tf.to_int32(batch_ids), 
                                 [pre_pool_size, pre_pool_size], 
                                 name="crops")
slim.max_pool2d(crops, [2, 2], padding='SAME')
```

#### 2.5.3 头到尾部分 `self._head_to_tail()` 

这一段为 Fast RCNN 网络结构中的 FCs 的部分

```python
with tf.variable_scope(self._scope, self._scope, reuse=reuse):
  pool5_flat = slim.flatten(pool5, scope='flatten')
  fc6 = slim.fully_connected(pool5_flat, 4096, scope='fc6')
  if is_training:
      fc6 = slim.dropout(fc6, keep_prob=0.5, is_training=True, scope='dropout6')
  fc7 = slim.fully_connected(fc6, 4096, scope='fc7')
  if is_training:
      fc7 = slim.dropout(fc7, keep_prob=0.5, is_training=True, scope='dropout7')
```

#### 2.5.4 区域分类+回归部分 `self._region_classification()` 

这一段是 Fast RCNN 网络结构中的 Outputs 部分

```python
cls_score = slim.fully_connected(fc7, self._num_classes,
                                 weights_initializer=initializer,
                                 trainable=is_training,
                                 activation_fn=None, scope='cls_score')
cls_prob = self._softmax_layer(cls_score, "cls_prob")
cls_pred = tf.argmax(cls_score, axis=1, name="cls_pred")
bbox_pred = slim.fully_connected(fc7, self._num_classes * 4,
                                 weights_initializer=initializer_bbox,
                                 trainable=is_training,
                                 activation_fn=None, scope='bbox_pred')
```

## 3. 损失计算 ---- `self._add_losses()`

总共有五项损失:

* RPN, 类别损失, 使用交叉熵

```python
rpn_cls_score = tf.reshape(self._predictions['rpn_cls_score_reshape'], [-1, 2])
rpn_label = tf.reshape(self._anchor_targets['rpn_labels'], [-1])
rpn_select = tf.where(tf.not_equal(rpn_label, -1))
rpn_cls_score = tf.reshape(tf.gather(rpn_cls_score, rpn_select), [-1, 2])
rpn_label = tf.reshape(tf.gather(rpn_label, rpn_select), [-1])
rpn_cross_entropy = tf.reduce_mean(
    tf.nn.sparse_softmax_cross_entropy_with_logits(logits=rpn_cls_score,
                                                   labels=rpn_label))
```

* RPN, 边界框损失, 使用光滑化的 `L1` 损失函数:

$$
\text{smooth}_{L_1}(x) = \left\{
\begin{array}{ll}
\frac{\sigma^2}{2}x^2 & \text{if } \lvert x\rvert < \frac1{\sigma^2} \\
\lvert x\rvert-\frac1{2\sigma^2} & \text{otherwise,}
\end{array}\right.
$$

```python
rpn_bbox_pred = self._predictions['rpn_bbox_pred']
rpn_bbox_targets = self._anchor_targets['rpn_bbox_targets']
rpn_bbox_inside_weights = self._anchor_targets['rpn_bbox_inside_weights']
rpn_bbox_outside_weights = self._anchor_targets['rpn_bbox_outside_weights']
rpn_loss_box = self._smooth_l1_loss(rpn_bbox_pred, 
                                    rpn_bbox_targets,
                                    rpn_bbox_inside_weights,
                                    rpn_bbox_outside_weights, 
                                    sigma=sigma_rpn, 
                                    dim=[1, 2, 3])
```

* RCNN, 类别损失

```python
cls_score = self._predictions["cls_score"]
label = tf.reshape(self._proposal_targets["labels"], [-1])
cross_entropy = tf.reduce_mean(
    tf.nn.sparse_softmax_cross_entropy_with_logits(logits=cls_score, 
                                                   labels=label))
```

* RCNN, 边界框损失

```python
bbox_pred = self._predictions['bbox_pred']
bbox_targets = self._proposal_targets['bbox_targets']
bbox_inside_weights = self._proposal_targets['bbox_inside_weights']
bbox_outside_weights = self._proposal_targets['bbox_outside_weights']
loss_box = self._smooth_l1_loss(
    bbox_pred, bbox_targets, bbox_inside_weights, bbox_outside_weights)
```

* 权重正则化损失

```python
regularization_loss = tf.add_n(tf.losses.get_regularization_losses(), 'regu')
```

## 4. 收集摘要用于 Tensorboard

摘要内容包括:

* `self._add_gt_image_summary()`  带有边界框的 ground truth 图片 ---- `tf.summary.image`
* `self._event_summaries()`  损失 ---- `tf.summary.scalar`
* `self._score_summaries()`  得分 ---- `tf.summary.histogram`
* `self._act_summaries()`  特征图的稀疏度 ---- `tf.summary.histogram & tf.summary.scalar` 
* `self._train_summaries()`  权重/偏置 ---- `tf.summary.histogram` 


## 5. 求解器 ---- `SolverWrapper`

**参数:**

* `sess`: 用于训练的 tensorflow 会话
* `network`: 主干网络类的对象, 可从 `/lib/nets/` 中选取
* `imdb`: 图像数据库类的对象, 可从 `/lib/datasets/` 中选取
* `roidb`: 感兴趣区域数据库, 一个列表, 其中的元素为字典, 每个元素包含了一个目标的边界框等信息
* `valroidb`: 用于验证的感兴趣区域数据库
* `output_dir`: 保存中间结果的文件夹
* `tbdir`: 保存摘要的文件夹, 用于 tensorboard
* `pretrained_model`: 与训练模型, 可选

**变量:**

* `self.net`: 主干网络
* `self.imdb`
* `self.roidb`
* `self.valroidb`
* `self.output_dir`
* `self.tbdir`
* `self.tbvaldir`: 验证时保存摘要的文件夹
* `self.pretrained_model`
* `self.data_layer`: ROIDataLayer 类的对象, 由 roidb 产生, 用于提供训练用的数据
* `self.data_layer_val`
* `self.optimizer`: 优化器
* `self.saver`: 检查点储存器
* `self.writer`: 摘要储存器
* `self.valwriter`: 验证集摘要储存器

### 方法

##### `snapshot(self, sess, iter)`

保存 tensorflow 的检查点, numpy 的随机数状态, 以及训练集和验证机的当前状态. 保存两类文件:

* Tensorflow 的检查点文件 (.ckpt)
* Numpy 的转储文件 (.pkl)

##### `from_snapshot(self, sess, sfile, nfile)`

从检查点载入权重

##### `remove_snapshot(self, np_paths, ss_paths)`

删除旧的检查点, 早于 `__C.TRAIN.SNAPSHOT_KEPT` 数量的检查点被删除

##### `find_previous(self)`

查找所有已保存的检查点

##### `initialize(self, sess)`

初始化检查点的路径列表, 从预训练的模型中载入权重.

##### `restore(self, sess, sfile, nfile)`

从检查点载入权重和学习率

#####`construct_graph(self, sess)`

构建全部的计算图, 包括

* 神经网络结构
* 定义学习率
* 定义优化器
* 定义训练/验证摘要储存器 (writer)

##### `train_model(self, sess, max_iters)`

* 创建训练数据读取层和验证数据读取层
* 构建计算图
* 载入检查点
* 迭代训练, 保存检查点, 中间输出
* 训练完毕, 保存最后一步输出
* 关闭储存器 (writer)

