---
layout: demo
title: "机器学习实验管理 (ML Experiment Management)"
date: 2020-11-19 22:59:00 +0800
categories: Tools 可视化
figure: /images/2020-11/MLM-1.png
author: Jarvis
meta: Post
---

<style>
    .logo {
        width: 130px;
    }
    .logo img {
        height: 50px;
        object-fit: contain;
    }
    .logo:hover {

    }
    .table td {
        vertical-align: middle;
        text-align: center;
    }
    thead {
        font-weight: bold;
    }
    td {
        background-color: #fff;
    }
    thead td {
        background-color: #eee;
        color: #000;
    }

    .carousel-indicators {
        background-color: rgba(0, 0, 0, 0.2); 
        width: 15%; 
        margin-left: -7.5%;
    }

    .slide {
        width: 95%;
        margin: auto;
    }
</style>




随着深度学习的发展, 机器学习实验的超参数越来越多, 实验的准确复现仍然存在困难, 科研合作时实验的管理存在困难, 科研到生产的衔接导致了大量零碎的代码片段难以整合. 因此, 为了解决超参数的选择和对比, 实验的复现, 代码和实验的管理, 多人协作, 以及从科研到生产的版本控制等问题, 机器学习实验管理平台应运而生. 目前流行的管理平台有 TensorBoard, wandb.ai, allegro trains, mlflow, sacred 等等. 他们整体上功能类似, 但又各有千秋. 本文期望对流行的机器学习实验管理平台做一个详尽的对比, 并给出各自平台的亮点和不足, 从而为读者选择平台时提供一个参考.

我们下面讨论九个机器学习实验管理工具. (点击Logo进入项目主页)

<table class="table table-hover">
    <thead>
        <tr>
            <td style="min-width: 50px;">编号</td>
            <td>框架</td>
            <td>年份</td>
            <td style="min-width: 80px;">开源</td>
            <td>公司</td>
            <td style="min-width: 200px;">特性</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td><div class="logo"><a target="_blank" href="https://www.tensorflow.org/tensorboard/get_started?hl=zh-cn"><img src="/images/2020-11/tensorboard.svg" alt="TensorBoard" /></a></div></td>
            <td>2017</td>
            <td><a href="https://github.com/tensorflow/tensorboard">Github</a></td>
            <td>Google Inc.</td>
            <td>跟踪实验指标, 可视化模型图, 嵌入, 语音展示, 图像展示, 其他插件</td>
        </tr>
        <tr>
            <td>2</td>
            <td><div class="logo"><a target="_blank" href="https://github.com/IDSIA/sacred"><img src="/images/2020-11/sacred.png" alt="Sacred" style="padding: 10px;" /></a></div></td>
            <td>2014</td>
            <td><a href="https://github.com/IDSIA/sacred">Github</a></td>
            <td>IDSIA</td>
            <td>配置、组织、记录和复制计算实验, 开销小, 鼓励实验的模块化和可配置性</td>
        </tr>
        <tr>
            <td>3</td>
            <td><div class="logo"><a target="_blank" href="https://neptune.ai/"><img src="/images/2020-11/neptune.png" alt="Neptune" /></a></div></td>
            <td>2016</td>
            <td><a href="https://github.com/neptune-ai">Github</a></td>
            <td>Neptune Labs Inc.</td>
            <td>轻量级的实验管理工具</td>
        </tr>
        <tr>
            <td>4</td>
            <td><div class="logo"><a target="_blank" href="https://losswise.com/"><img src="/images/2020-11/losswise.svg" alt="LossWise" style="padding: 10px;" /></a></div></td>
            <td>2018</td>
            <td>-</td>
            <td>Mathpix Inc.</td>
            <td>简单的API, 记录参数、图像、日志, 整合统计指标</td>
        </tr>
        <tr>
            <td>5</td>
            <td><div class="logo" style="background-color: #1e2388; border-radius: 5px;"><a target="_blank" href="https://guild.ai/"><img src="/images/2020-11/guild.svg" alt="Guild" style="padding: 15px; background-color: #1e2388;" /></a></div></td>
            <td>2019</td>
            <td><a href="https://github.com/guildai/guildai">Github</a></td>
            <td>TensorHub Inc.</td>
            <td>跟踪实验, 自动管线, 微调参数</td>
        </tr>
        <tr>
            <td>6</td>
            <td><div class="logo" style="background-color: #010029; border-radius: 5px;"><a target="_blank" href="https://allegro.ai/"><img src="/images/2020-11/allegro.svg" alt="Allegro" style="padding: 11px; background-color: #010029;"  /></a></div></td>
            <td>2019</td>
            <td><a href="https://github.com/allegroai/trains">Github</a></td>
            <td>Allegro AI</td>
            <td>端到端企业级平台, 可管理机器学习和深度学习产品的生命周期</td>
        </tr>
        <tr>
            <td>7</td>
            <td><div class="logo" style="background-color: #0a2240; border-radius: 5px;"><a target="_blank" href="https://mlflow.org/"><img src="/images/2020-11/mlflow.png" alt="mlflow" style="padding: 12px; background-color: #0a2240;"  /></a></div></td>
            <td>2018</td>
            <td><a href="https://github.com/mlflow/mlflow/">Github</a></td>
            <td>LF Proj. LLC.</td>
            <td>兼容任意机器学习库、语言, 可多人协作, 可以拓展到Spark</td>
        </tr>
        <tr>
            <td>8</td>
            <td><div class="logo" style="background-color: #000; border-radius: 5px;"><a target="_blank" href="https://www.wandb.com/"><img src="/images/2020-11/wandb-logo.svg" alt="Weights & Biases" style="padding: 10px; background-color: #000;"/></a></div></td>
            <td>2017</td>
            <td>-</td>
            <td>Weights and Biases Inc.</td>
            <td>跟踪、比较、可视化机器学习实验, 可协作, 企业支持</td>
        </tr>
        <tr>
            <td>9</td>
            <td><div class="logo" style="background-color: #2a2564; border-radius: 5px;"><a target="_blank" href="https://www.comet.ml/site/"><img src="/images/2020-11/comet.png" alt="Comet" style="padding: 8px; background-color: #2a2564;"/></a></div></td>
            <td>2017</td>
            <td>-</td>
            <td>Comet ML Inc.</td>
            <td>跟踪、比较、解释和优化实验和模型</td>
        </tr>
    </tbody>
</table>

## 0. Overview

下面的表格从整体上给出了九种框架主要功能的对比:

* [ √ ] 表示库本身有该功能
* [ 空格 ] 表示库本身没有该功能
* [ * ] 表示还有更多
* [ ? ] 表示未知
* [ $ ] 表示收费

<table class="table table-hover table-bordered table-striped">
    <thead>
        <tr>
            <td>功能</td>
            <td><a target="_blank" href="https://www.tensorflow.org/tensorboard/get_started?hl=zh-cn">TensorBoard</a></td>
            <td><a target="_blank" href="https://github.com/IDSIA/sacred">Sacred</a></td>
            <td><a target="_blank" href="https://neptune.ai/">Neptune</a></td>
            <td><a target="_blank" href="https://losswise.com/">LossWise</a></td>
            <td><a target="_blank" href="https://guild.ai/">Guild</a></td>
            <td><a target="_blank" href="https://allegro.ai/">Allegro</a></td>
            <td><a target="_blank" href="https://mlflow.org/">mlflow</a></td>
            <td><a target="_blank" href="https://www.wandb.com/">W & B</a></td>
            <td><a target="_blank" href="https://www.comet.ml/site/">Comet</a></td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>标量</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>比较</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>资源信息</td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>资源监控</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>源码</td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>计算图</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td>✔</td>
        </tr>
        <tr>
            <td>二进制</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>图像</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>数据分布</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>嵌入</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td>✔</td>
        </tr>
        <tr>
            <td>音频</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td>✔</td>
        </tr>
        <tr>
            <td>后端</td>
            <td></td>
            <td><a href="https://www.mongodb.com/try/download/community">MongoDB</a>
                <p>Neptune*</p></td>
            <td>✔</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>前端</td>
            <td>✔</td>
            <td><a href="https://github.com/vivekratnavel/omniboard">Omniboard</a>
                <p>Neptune*</p></td>
            <td>✔</td>
            <td>✔</td>
            <td>✔<p>TensorBoard</p></td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>前端评级</td>
            <td>✩✩</td>
            <td>✩✩</td>
            <td>✩✩✩</td>
            <td>✩✩✩</td>
            <td>✩</td>
            <td>✩✩✩✩</td>
            <td>✩✩</td>
            <td>✩✩✩✩✩</td>
            <td>✩✩✩✩✩</td>
        </tr>
        <tr>
            <td>参数管理</td>
            <td></td>
            <td>✩✩✩✩✩</td>
            <td>✩✩✩</td>
            <td>✩</td>
            <td>✩✩</td>
            <td>✩✩</td>
            <td>✩✩</td>
            <td>✩✩✩</td>
            <td>✩✩✩</td>
        </tr>
        <tr>
            <td>云服务</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>云空间</td>
            <td></td>
            <td></td>
            <td>100G</td>
            <td>?</td>
            <td></td>
            <td></td>
            <td></td>
            <td>100G</td>
            <td>100G</td>
        </tr>
        <tr>
            <td>本地部署</td>
            <td>✔</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔$</td>
        </tr>
        <tr>
            <td>团队协作</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>插件</td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>参数调优</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td></td>
            <td></td>
            <td>✔</td>
            <td>✔</td>
        </tr>
        <tr>
            <td>商业支持</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td>✔$</td>
            <td>✔$</td>
        </tr>
        <tr>
            <td>内部支持<p>的框架</p></td>
            <td>Tensorflow<p>PyTorch</p></td>
            <td></td>
            <td>Keras<p>Tensorflow</p><p>PyTorch</p><p>Sacred</p><p>mlflow*</p></td>
            <td>Keras</td>
            <td>Keras<p>Tensorflow</p><p>PyTorch</p><p>sklearn</p><p>MXNet</p><p>XGBoost</p></td>
            <td>Keras<p>Tensorflow</p><p>PyTorch</p><p>sklearn</p><p>MXNet</p><p>Caffe2*</p></td>
            <td>Keras<p>Tensorflow</p><p>PyTorch</p><p>sklearn</p><p>XGBoost*</p></td>
            <td>Keras<p>Tensorflow</p><p>PyTorch</p><p>sklearn</p><p>XGBoost*</p></td>
            <td>Keras<p>Tensorflow</p><p>PyTorch</p><p>sklearn</p><p>MXNet</p><p>Caffe2*</p></td>
        </tr>
    </tbody>
</table>

{% include card.html type="info" content="<strong>内部支持的框架</strong>指的是库内部做了相应适配, 未写出的框架可以通过编码来向管理工具传输数据." %}

{% include card.html type="info" content="上面的表格仅仅是我试用过后的发现的功能, 可能不全. 其中 TensorBoard 和 Sacred 是我使用较多的, 功能描述基本没有问题. 同时表格中的所有评价都是我短时间接触后的主观感受, 不代表实际使用的情况." %}

## 1. TensorBoard

Tensorboard 是谷歌在推出 Tensorflow 之后发布的一款用于展示实验过程中的标量(losses, metrics)、图像、数据分布、计算图等内容的可视化工具. 

<div id="slide_sacred" class="carousel slide" data-ride="carousel">
  <!-- 圆点指示器 -->
  <ol class="carousel-indicators">
    <li data-target="#slide_sacred" data-slide-to="0" class="active"></li>
    <li data-target="#slide_sacred" data-slide-to="1"></li>
    <li data-target="#slide_sacred" data-slide-to="2"></li>
    <li data-target="#slide_sacred" data-slide-to="3"></li>
    <li data-target="#slide_sacred" data-slide-to="4"></li>
    <li data-target="#slide_sacred" data-slide-to="5"></li>
  </ol>

  <!-- 轮播项目 -->
  <div class="carousel-inner">
    <div class="item active">
      {% include image.html class="polaroid-center" url="2020-11/tensorboard-1.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/tensorboard-2.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/tensorboard-3.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/tensorboard-4.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/tensorboard-5.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/tensorboard-6.png" %}
    </div>
  </div>
</div>

## 2. Sacred

Sacred是可帮助研究人员配置、组织、记录和复制实验的工具. 它旨在完成研究人员需要围绕实际实验进行的所有繁琐的日常工作. Sacred 有一下几个设计目的:

* 跟踪实验的所有参数
* 轻松进行不同设置的实验
* 将单个运行的配置保存在数据库中
* 重现结果

<div id="slide_sacred" class="carousel slide" data-ride="carousel">
  <!-- 圆点指示器 -->
  <ol class="carousel-indicators">
    <li data-target="#slide_sacred" data-slide-to="0" class="active"></li>
    <li data-target="#slide_sacred" data-slide-to="1"></li>
    <li data-target="#slide_sacred" data-slide-to="2"></li>
    <li data-target="#slide_sacred" data-slide-to="3"></li>
  </ol>

  <!-- 轮播项目 -->
  <div class="carousel-inner">
    <div class="item active">
      {% include image.html class="polaroid-center" url="2020-11/sacred-2.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/sacred-5.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/sacred-3.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/sacred-4.png" %}
    </div>
  </div>
</div>

## 3. Neptune

<div id="slice_neptune" class="carousel slide" data-ride="carousel">
  <!-- 圆点指示器 -->
  <ol class="carousel-indicators">
    <li data-target="#slice_neptune" data-slide-to="0" class="active"></li>
    <li data-target="#slice_neptune" data-slide-to="1"></li>
    <li data-target="#slice_neptune" data-slide-to="2"></li>
  </ol>

  <!-- 轮播项目 -->
  <div class="carousel-inner">
    <div class="item active">
      {% include image.html class="polaroid-center" url="2020-11/neptune-1.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/neptune-2.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/neptune-3.png" %}
    </div>
  </div>
</div>

## 4. Losswise

* 支持与 Github 集成, 使用私有 GPU 直接运行 Github 的分支. 

{% include image.html class="polaroid-center" url="2020-11/losswise-1.png" %}

## 5. Guild

* 与 Tensorboard 做了集成

<div id="slice_guild" class="carousel slide" data-ride="carousel">
  <!-- 圆点指示器 -->
  <ol class="carousel-indicators">
    <li data-target="#slice_guild" data-slide-to="0" class="active"></li>
    <li data-target="#slice_guild" data-slide-to="1"></li>
  </ol>

  <!-- 轮播项目 -->
  <div class="carousel-inner">
    <div class="item active">
      {% include image.html class="polaroid-center" url="2020-11/guild-1.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/guild-2.png" %}
    </div>
  </div>
</div>

## 6. Allegro Trains

* 没找到实验源码的保存位置
* 没有云端服务, 只能本地部署


<div id="slide_allegro" class="carousel slide" data-ride="carousel">
  <!-- 圆点指示器 -->
  <ol class="carousel-indicators">
    <li data-target="#slide_allegro" data-slide-to="0" class="active"></li>
    <li data-target="#slide_allegro" data-slide-to="1"></li>
    <li data-target="#slide_allegro" data-slide-to="2"></li>
    <li data-target="#slide_allegro" data-slide-to="3"></li>
    <li data-target="#slide_allegro" data-slide-to="4"></li>
  </ol>

  <!-- 轮播项目 -->
  <div class="carousel-inner">
    <div class="item active">
      {% include image.html class="polaroid-center" url="2020-11/allegro-1.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/allegro-2.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/allegro-3.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/allegro-4.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/allegro-5.png" %}
    </div>
  </div>
</div>

## 7. mlflow

* 支持模型部署

<div id="slide_mlflow" class="carousel slide" data-ride="carousel">
  <!-- 圆点指示器 -->
  <ol class="carousel-indicators">
    <li data-target="#slide_mlflow" data-slide-to="0" class="active"></li>
    <li data-target="#slide_mlflow" data-slide-to="1"></li>
  </ol>

  <!-- 轮播项目 -->
  <div class="carousel-inner">
    <div class="item active">
      {% include image.html class="polaroid-center" url="2020-11/mlflow-1.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/mlflow-2.png" %}
    </div>
  </div>
</div>

## 8. Weights & Biases

Weights & Biases 帮助你记录机器学习项目的过程。利用我们的工具记录运行过程中的超参数和输出指标，然后将结果可视化并做比较，便捷地与同事分享结果。

* 有中文文档
* 功能强大, 可以免费本地部署

<div id="slide_wb" class="carousel slide" data-ride="carousel">
  <!-- 圆点指示器 -->
  <ol class="carousel-indicators">
    <li data-target="#slide_wb" data-slide-to="0" class="active"></li>
    <li data-target="#slide_wb" data-slide-to="1"></li>
    <li data-target="#slide_wb" data-slide-to="2"></li>
    <li data-target="#slide_wb" data-slide-to="3"></li>
    <li data-target="#slide_wb" data-slide-to="4"></li>
  </ol>

  <!-- 轮播项目 -->
  <div class="carousel-inner">
    <div class="item active">
      {% include image.html class="polaroid-center" url="2020-11/wb-1.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/wb-2.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/wb-3.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/wb-4.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/wb-5.png" %}
    </div>
  </div>
</div>



## 9. Comet

我们发现有了个 Neptune (海王星), 所以我们叫 Comet (彗星). (不是, 我瞎说的. 实在是主页没有几句话简介.)

* 功能强大, 可以付费本地部署

<div id="slide_comet" class="carousel slide" data-ride="carousel">
  <!-- 圆点指示器 -->
  <ol class="carousel-indicators">
    <li data-target="#slide_comet" data-slide-to="0" class="active"></li>
    <li data-target="#slide_comet" data-slide-to="1"></li>
  </ol>

  <!-- 轮播项目 -->
  <div class="carousel-inner">
    <div class="item active">
      {% include image.html class="polaroid-center" url="2020-11/comet-1.png" %}
    </div>
    <div class="item">
      {% include image.html class="polaroid-center" url="2020-11/comet-2.png" %}
    </div>
  </div>
</div>
