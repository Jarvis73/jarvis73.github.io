---
layout: post
title: "大模型(三): 基础大模型 (AweSome Foundation Models)"
date: 2024-11-12 16:20:00 +0800
categories: 大模型
author: Jarvis
meta: Post
---

* content
{:toc}

基础大模型论文列表

## 生成

[2024 - Fluid](#fluid)  
[2022 - MIM Scaling Laws](#masked-image-modeling-scaling-laws)

## 理解

[2023 - SAM](#sam)  
[2021 - CLIP](#clip)  
[2021 - Florence](#florence)  

## 生成 + 理解

[2024 - Emu3](#emu3)  
[2024 - Show-o](#show-o)  
[2024 - Transfusion](#transfusion)  
[2024 - Chameleon](#chameleon)  
[2024 - Survey: Unifying Und&Gen in AR](#survey-unifying-undgen-in-ar)  
[2023 - DreamLLM](#dreamllm)  

## 2024 年

### Fluid

**Fluid: Scaling Autoregressive Text-to-image Generative Models with Continuous Tokens** 单位: Google DeepMind, MIT

[[PDF](http://arxiv.org/abs/2410.13863)]

探讨了 Autoregressive 模型在连续 token 和离散 token, random order 和 raster order 上训练的效果和 scaling 能力. 评估指标上连续 token + random order 效果最好.

{% include image.html class="polaroid" url="2024/11/fluid.png" title="Autoregressive models with different orders." %}

### Emu3

**Emu3: Next-Token Prediction is All You Need** 单位: BAAI

[[PDF](http://arxiv.org/abs/2409.18869)] [[Project](https://emu.baai.ac.cn/about)] [[GitHub](https://github.com/baaivision/Emu3)]

使用 Next Token Prediction 训练理解生成的统一模型, 完成理解和图、视频生成等任务. 自己训练了基于 SBER-MoVQGAN 的图+视频统一的 tokenizer.

{% include image.html class="polaroid" url="2024/11/emu3.png" title="Emu3" %}


### Show-o

**Show-o: One Single Transformer to Unify Multimodal Understanding and Generation** 单位: NUS, 字节

[[PDF](http://arxiv.org/abs/2408.12528)] [[Project](https://showlab.github.io/Show-o/)] [[GitHub](https://github.com/showlab/Show-o)] [[HuggingFace](https://huggingface.co/spaces/showlab/Show-o)]

图像部分采用 Mask Image Modeling 和 Full Attention 的方案训练, 文本部分采用 Next Token Prediction 和 Causal Attention 的方案训练. 自己训练了一个 MAGVITv2 作为 tokenizer. 

{% include image.html class="polaroid" url="2024/11/show-o.png" title="Show-o 结构" %}
{% include image.html class="polaroid" url="2024/11/show-o2.png" title="Show-o 不同任务的序列构造" %}
{% include image.html class="polaroid" url="2024/11/show-o3.png" title="Show-o Attention Mask 构造" %}


### Transfusion

**Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model** 单位: Meta, Waymo

[[PDF](http://arxiv.org/abs/2408.11039)] 

图像部分采用 VAE 编码到隐空间, 用 diffusion 的方式训练; 文本部分采用 Next Token Prediction 训练. 

{% include image.html class="polaroid" url="2024/11/transfusion.png" title="Transfusion" %}


### Chameleon

**Chameleon: Mixed-Modal Early-Fusion Foundation Models** 单位: Meta

[[PDF](http://arxiv.org/abs/2405.09818)] 

使用 Next Token Prediction 训练生成理解统一的模型. 自己训练了基于 Make-a-Scene 的 tokenizer. 训练数据包含文本、图文对、图文交织.

{% include image.html class="polaroid" url="2024/11/chameleon.png" title="Chameleon" %}


### Survey: Unifying Und&Gen in AR

**Towards Unifying Understanding and Generation in the Era of Vision Foundation Models: A Survey from the Autoregression Perspective** 单位: 北大, 清华

[[PDF](http://arxiv.org/abs/2410.22217)]

综述统一理解和生成的基于 AutoRegressive 范式的工作.

{% include image.html class="polaroid" url="2024/11/survey_ar_undgen.png" title="Vision Tokenizers 分类" %}
{% include image.html class="polaroid" url="2024/11/survey_ar_undgen2.png" title="Autoregression 结构分类" %}


## 2023 年

### DreamLLM

**DreamLLM: Synergistic Multimodal Comprehension and Creation** 单位: 西安交大, 旷视

[[PDF](https://arxiv.org/abs/2309.11499)] [[Project](https://dreamllm.github.io/)] [[GitHub](https://github.com/RunpeiDong/DreamLLM)]

协同的多模态理解和生成.

{% include image.html class="polaroid" url="2024/11/dreamLLM.png" title="DreamLLM" %}


### SAM

**Segment Anything** 单位: Meta

[[PDF](https://arxiv.org/abs/2304.02643)] [[Project](https://segment-anything.com/)] [[GitHub](https://github.com/facebookresearch/segment-anything)]

SAM 交互分割模型, 分割一切

{% include image.html class="polaroid" url="2024/11/sam.png" title="SAM" %}

## 2022 年

### Masked Image Modeling Scaling Laws

**On Data Scaling in Masked Image Modeling** 单位: 清华, 西安交大, MSRA

[[PDF](https://arxiv.org/abs/2206.04664)]

(1) Mask modeling 需要大数据; (2) 训练的久一点会更好; (3) Validation loss 是个很好的评估下游任务性能的指标. 

{% include image.html class="polaroid" url="2024/11/mlm_scaling.png" title="Masked Modeling Scaling Laws" %}


## 2021 年

### CLIP

**Learning Transferable Visual Models From Natural Language Supervision** 单位: OpenAI

[[PDF](http://arxiv.org/abs/2103.00020)] [[Project](https://openai.com/index/clip/)] [[GitHub](https://github.com/OpenAI/CLIP)] [[HuggingFace](https://huggingface.co/docs/transformers/model_doc/clip)]

CLIP 是一个图文的多模态模型, 对图像和文本通过对比学习联合训练实现图文对齐.

{% include image.html class="polaroid" url="2024/11/clip.png" title="CLIP" %}


### Florence

**Florence: A New Foundation Model for Computer Vision** 单位: Microsoft 

[[PDF](http://arxiv.org/abs/2111.11432)]

统一视觉理解任务到 **空间-时间-模态** 三个维度, 完成所有视觉的理解任务. 

{% include image.html class="polaroid-small" url="2024/11/florence.png" title="Florence" %}


