---
layout: post
title: "Transformer 的参数量和计算量"
date: 2024-06-29 10:57:00 +0800
categories: Transformer 大模型
mathjax: true
author: Jarvis
meta: Post
---

* content
{:toc}

Transformer 的参数量和计算量是现在做大模型绕不开的一环. 我们采用 OpenAI 关于 Scaling Laws 一文《Scaling Laws for Neural Language Models》中的记号来总结一下. 



## 记号

* $$n_{\text{vocab}}$$ - 词表大小 (LLM 的词表)
* $$n_{\text{ctx}}$$ - 输入的上下文长度
* $$n_{\text{layer}}$$ - Transformer block 的数量, 也称为层数.
* $$d_{\text{model}}$$ - Transformer 的基本维度
* $$d_{\text{attn}}$$ - Attention 层内的维度
* $$d_{\text{ff}}$$ - FFN 层内的维度

## 参数量和计算量

| 层/算子 | 实现 | 参数量 | 计算量(per Token) |
|:------:|:-----:|:-----:|:-----:|
| Embed  | nn.Linear | $$(n_{\text{vocab}} + n_{\text{ctx}})d_{\text{model}}$$ | $$4d_{\text{model}}$$ |
| Attention | nn.Linear | $$4n_{\text{layer}}d_{\text{model}}d_{\text{attn}}$$ | $$8n_{\text{layer}}d_{\text{model}}d_{\text{attn}}$$ |
| FFN | nn.Linear | $$2n_{\text{layer}}d_{\text{model}}d_{\text{ff}}$$ | $$4n_{\text{layer}}d_{\text{model}}d_{\text{ff}}$$ |
| Total (Non-Embedding) | - | $$2n_{\text{layer}}d_{\text{model}}(2d_{\text{attn}} + d_{\text{ff}})$$ | $$4n_{\text{layer}}d_{\text{model}}(2d_{\text{attn}} + d_{\text{ff}})$$ |

## 参数量计算

### Embed 层

Embed 层就是个 `nn.Embedding()`, 它本身只包含一个 $$n_{\text{vocab}}\times d_{\text{model}}$$ 的参数矩阵, 用于把文本 tokens 映射为对应的 embedding. 假如使用可学习的位置编码, 那么还需要增加一组位置编码的参数 $$n_{\text{ctx}}\times d_{\text{model}}$$. 如果使用 RoPE 位置编码, 那么就不需要位置编码的参数. 总体来说, Embed 层的参数量(算上可学习的位置编码)为:

$$
(n_{\text{vocab}} + n_{\text{ctx}})d_{\text{model}}
$$

### Attention 层

Attention 层包含 QKV 的 Linear 层和输出的 Linear 层. 假设 Attention 层的维度为 $$d_{\text{attn}}$$, 那么 QKV 的 Linear 层的参数量为 $$3d_{\text{model}}d_{\text{attn}}$$, 输出的 Linear 层的参数量为 $$d_{\text{attn}}d_{\text{model}}$$. 因此 Attention 层的参数量为:

$$
4d_{\text{model}}d_{\text{attn}}
$$

### FFN 层

FFN 层包含两个 Linear 层, 假设 FFN 层的维度为 $$d_{\text{ff}}$$, 那么 FFN 层的参数量为 $$2d_{\text{model}}d_{\text{ff}}$$. 因此 FFN 层的参数量为:

$$
2d_{\text{model}}d_{\text{ff}}
$$

## 计算量计算

从前面的表中可以得到前向的计算量为 2 倍的参数量. 另外反向的计算量是前向的 2 倍, 那么总的计算量为 6 倍的参数量.
因此通常我们会用 $$6ND$$ 来表示计算量, 其中 $$N$$ 是模型的参数量, $$D$$ 是数据量(token 数\text{).}
