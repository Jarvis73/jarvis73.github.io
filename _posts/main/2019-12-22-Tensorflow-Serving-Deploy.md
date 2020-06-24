---
layout: post
title: "Tensorflow 模型部署"
date: 2019-12-22 13:36:00 +0800
categories: Tensorflow
figure: ./images/2019-12/tfx-hero.svg
author: Jarvis
meta: Post
---

* content
{:toc}

> 训练好深度学习模型后可以通过 Tensorflow Extended (TFX) 把模型部署为服务方便地使用.




{% include image.html class="polaroid" url="2019-12/tfx-hero.svg" title="Tensowflow Extended (TFX)" %}

## 1. 导出模型 (TF-1.13 API)

Tensorflow 目前统一的导出模型 API 为 SavedModel, 导出模型会把参数和模型结构分开存放 (ONNX 转换过来的参数和模型结构是合并在一个文件里的). 假设我们已经有一组训练好的模型参数, 使用如下的示例代码导出为 SavedModel 格式:

```python
# Specify several directories
ckpt_dir = "runs/tag"
export_dir = "export_path/tag/1"
bs, h, w, c = 1, 224, 224, 3

with tf.Session(graph=tf.Graph()) as sess:
    serialized_tf_example = tf.placeholder(tf.string, name="tf_example")
    feature_configs = {"x": tf.FixedLenFeature(shape=[], dtype=tf.float32)}
    tf_example = tf.parse_example(serialized_tf_example, feature_configs)
    tf_example["x"] = tf.reshape(tf_example["x"], (bs, h, w, c))
    image = tf.identity(tf_example["x"], name="image")

    # Do inference ................
    # pred = model(image)
    # .............................

    saver = tf.train.Saver()
    ckpt = tf.train.latest_checkpoint(ckpt_dir)
    saver.restore(sess, ckpt)
    print("Model restored.")

    builder = tf.saved_model.builder.SavedModelBuilder(export_dir)
    tensor_info_image = tf.saved_model.utils.build_tensor_info(image)
    tensor_info_output = tf.saved_model.utils.build_tensor_info(pred)
    prediction_signature = (
        tf.saved_model.signature_def_utils.build_signature_def(
            inputs={'x': tensor_info_image},
            outputs={'pred': tensor_info_output},
            method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME))

    builder.add_meta_graph_and_variables(
        sess, [tf.saved_model.tag_constants.SERVING],
        signature_def_map={
            'serving_default':
                prediction_signature,
        })

    builder.save(as_text=True)
    print('Done exporting!')
```

保存下来的目录结构如下所示. 注意我们增加了 `1` 作为子目录, 方便进行版本控制, 这表示该文件夹下是版本 `1` 的模型. 其中参数的保存格式和我们训练时检查点的格式相同, 而模型是 `protobuf` 的格式保存的. `*.pbtxt` 表示保存为文本格式, `*.pb` 表示保存为二进制格式.

```
export_path/
└── tag
    └── 1
        ├── saved_model.pbtxt
        └── variables
            ├── variables.data-00000-of-00001
            └── variables.index
```

接下来对上面的代码进行分析. 为了服务端和客户端通信的方便, 客户端需要把待推断的数据通过 `protobuf` 编码为字符串, 从而服务端需要从字符串还原数据(如一幅图像). 因此构建的推断计算图入口为一个占位符接收字符串 `tf.string`, 并使用 `tf.FixedLenFeature()` 和 `tf.parse_example` 这两个 API 对 `protobuf` 格式的数据进行解码, 最后使用 `tf.reshape` 把数据重构为 4D 的张量用于神经网络. `tf.identity` 只是用于创建一个节点来标明图像, 无其他用处.

```python
serialized_tf_example = tf.placeholder(tf.string, name="tf_example")
feature_configs = {"x": tf.FixedLenFeature(shape=[], dtype=tf.float32)}
tf_example = tf.parse_example(serialized_tf_example, feature_configs)
tf_example["x"] = tf.reshape(tf_example["x"], (bs, h, w, c))
image = tf.identity(tf_example["x"], name="image")
```

得到图像之后就可以构建核心计算图, 并导入先前训练好的模型参数. 这一段可以灵活的使用 Tensorflow 的各种 API. 唯一要注意的是最好使用已经提供的网络层或数学函数, 而使用 `tf.py_func` 这类函数构造的层可能会出问题 (未研究过, 遇到再写). 

```python
pred = model(image)
saver = tf.train.Saver()
ckpt = tf.train.latest_checkpoint(ckpt_dir)
saver.restore(sess, ckpt)
print("Model restored.")
```

然后创建 `SavedModel` 构造器 `SavedModelBuilder`. 同时使用 `build_tensor_info` 函数获取输入和输出张量的协议. 协议的类型是 `tensorflow.core.protobuf.meta_graph_pb2.TensorInfo`, 可以直接打印出来查看.

```python
builder = tf.saved_model.builder.SavedModelBuilder(export_dir)
tensor_info_image = tf.saved_model.utils.build_tensor_info(image)
tensor_info_output = tf.saved_model.utils.build_tensor_info(pred)
print(tensor_info_image)

#　打印的结果
# name: "image:0"
# dtype: DT_FLOAT
# tensor_shape {
#   dim {
#     size: 1
#   }
#   dim {
#     size: 224
#   }
#   dim {
#     size: 224
#   }
#   dim {
#     size: 3
#   }
# }
```

创建模型签名. 然后使用 `builder` 把当前会话中的计算图, 参数和模型签名绑定.

```python
prediction_signature = (
    tf.saved_model.signature_def_utils.build_signature_def(
        inputs={'x': tensor_info_image},
        outputs={'pred': tensor_info_output},
        method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME))

builder.add_meta_graph_and_variables(
    sess, [tf.saved_model.tag_constants.SERVING],
    signature_def_map={
        'serving_default':
            prediction_signature,
    })
```

保存模型.

```python
builder.save(as_text=True)
print('Done exporting!')
```

## 2. 部署模型 (TF-2.0 API)

由于模型已经按照 `protobuf` 的格式保存, 因此我们可以用任意版本的 Tensorflow 使用. 这里我们直接采用 Tensorflow 2.0 的 API.

### 2.1 服务端

Tensorflow 可以部署为仅使用 CPU, 但没有意义. 因此只讨论 GPU 版本的部署. 由于 Tensorflow 官方强烈建议在 Docker 中使用 `Tensorflow Serving`, 而 Docker 中使用主机的 GPU 需要 `Nvidia-Docker` 的支持, 但 NVIDIA 官方表明不支持在 Windows 中使用 `Nvidia-Docker`, 因此基于 Tensorflow-GPU 的模型部署只能在 Linux 系统上进行了.

服务端部署支持两种 API:
* Client REST API
* gRPC API

第一种基于 Json 格式进行数据传输, 第二种基于 Google 的 `protobuf` 格式进行数据传输. 第一种在 [Tensorflow 官网](https://www.tensorflow.org/tfx/serving/docker)有介绍, 我们这里主要讨论第二种.

0. 更新 Nvidia 驱动到最新版本. 这一步可以避免很多麻烦.
1. 安装 Docker. [Link](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
2. 安装 nvidia-docker2. [Link](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0))
3. 重启 Docker. 

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```
4. 拉取 tensorflow-serving 容器

```bash
docker pull tensorflow/serving:latest-gpu
```

接下来我们下载 Tensorflow 官方提供的示例程序.

```bash
mkdir -p /tmp/tfserving
cd /tmp/tfserving
git clone https://github.com/tensorflow/serving
```

然后运行示例程序.

```bash
docker run --runtime=nvidia --rm -p 8500:8500 -p 8501:8501 -v "/tmp/tfserving/serving/tensorflow_serving/servables/tensorflow/testdata/saved_model_half_plus_two_gpu:/models/half_plus_two" -e MODEL_NAME=half_plus_two -t tensorflow/serving:latest-gpu &
```

其中端口 8501 用于 REST API, 8500 端口用于 gRPC API. 其他参数的含义参考 Docker 的文档, 本文不详细展开.

### 2.2 客户端

服务端启动之后, 可以通过网址

```
http://localhost:8501/v1/models/half_plus_two/metadata
```

来查看服务端是否正常开启, 该网址会显示模型签名 (参考上面构造签名的代码). 接下来编写基于 gRPC 数据传输格式的客户端程序.

```python
import grpc
import numpy as np
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

def client(numpy_array, host="localhost", port=8500):
    assert len(numpy_array.shape) == 4
    bs, h, w, c = numpy_array.shape

    channel = grpc.insecure_channel('{host}:{port}'.format(host=host, port=port))
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    request = predict_pb2.PredictRequest()
    request.model_spec.name = "half_plus_two"
    request.model_spec.signature_name = "serving_default"
    request.inputs['x'].CopyFrom(tf.make_tensor_proto(numpy_array, shape=[bs, h, w, c]))

    try:
        result = stub.Predict(request)
        output = np.array(result.outputs["pred"].int64_val).reshape(h, w)
    except Exception as e:
        print(e)
        output = None

    return result
```

### 2.3 使用老版本 NVIDIA 驱动

官方的 Docker `tensorflow/serving:latest-gpu` 是根据 10.1 版本的 CUDA 版本创建的, 只能用于高版本的显卡驱动. 有时不方便更新主机显卡驱动, 此时要想使用 `tensorflow/serving` 的 Docker 则需要创建自己的 Docker 镜像. 假设我们主机的显卡驱动是 396.36 版本 (对应的 CUDA 版本最高为 9.2.88, 为了保险我们准备使用 9.0 版本的 CUDA). 从 `tensorflow/serving` 的 [docker 工具页面]((https://github.com/tensorflow/serving/tree/master/tensorflow_serving/tools/docker)) 下载 `Dockerfile.devel-gpu` 和 `Dockerfile.gpu` 两个文件. 

修改 `Dockerfile.devel-gpu`:

```dockerfile
# 选择基础镜像, 基础镜像需要根据操作系统版本和选定的cuda版本选择. 
# 可使用的基础镜像可以从 [DockerHub](https://hub.docker.com/r/nvidia/cuda/tags) 查询
# FROM nvidia/cuda:10.0-base-ubuntu16.04 as base_build 修改为
FROM nvidia/cuda:9.0-base-ubuntu16.04 as base_build

# ......

# CUDNN 的版本不用改, 因为和 CUDA 9 是兼容的
ENV CUDNN_VERSION=7.4.1.5

# 然后把整个文档里的 10-0 和 10.0 全部修改为 9-0 和 9.0, 其他 CUDA 版本可以类似的修改.
```

修改完成后在终端使用 Dockerfile 构建镜像 (注意 docker build 命令末尾的点不能丢, 点表示构建路径为当前文件夹):

```bash
mkdir tfs-devel
mv Dockerfile.devel-gpu tfs-devel
cd tfs-devel
docker build -t tensorflow/serving:latest-devel-gpu-cuda9.0 .
```

接下来修改 `Dockerfile.gpu`:

```docker
ARG TF_SERVING_VERSION=latest
# 指定基础镜像为我们修改过的镜像
# ARG TF_SERVING_BUILD_IMAGE=tensorflow/serving:${TF_SERVING_VERSION}-devel-gpu
ARG TF_SERVING_BUILD_IMAGE=tensorflow/serving:${TF_SERVING_VERSION}-devel-gpu-cuda9.0

FROM ${TF_SERVING_BUILD_IMAGE} as build_image
# 类似的修改
# FROM nvidia/cuda:10.0-base-ubuntu16.04
FROM nvidia/cuda:9.0-base-ubuntu16.04

# 然后把整个文档里的 10-0 和 10.0 全部修改为 9-0 和 9.0, 其他 CUDA 版本可以类似的修改.
```

最后构建第二个镜像, 可以看到第二个镜像是在第一个镜像的基础上构建的. 仍然要注意最后的点.

```bash
mkdir tfs
mv Dockerfile.gpu tfs
cd tfs
docker build -t tensorflow/serving:latest-gpu-cuda9.0 .
```
