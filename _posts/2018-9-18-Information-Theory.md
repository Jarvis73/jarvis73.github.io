---
layout: post
title: "机器学习(一): 信息论初步"
data: 2018-09-18 21:28:00
categories: 机器学习
mathjax: true
figure: /images/MLPP/Shannon.jpg
author: Jarvis
meta: Post
---

* content
{:toc}

我们通常提到信息论(information theorey)时一般在谈论如何以更紧凑的方式表示数据(比如**数据压缩**或**源编码**), 或者在数据传输和存储时减少误差. 乍一看和机器学习及概率论并无关系, 但他们有着密切的联系. 比如在压缩数据时, 往往使用短的编码词编码高频词汇, 长的编码词编码低频词汇; 反之解码时需要一个好的概率模型来确定哪种原始组合的概率更高.



<div class="polaroid">
    <img class="cool-img" src="/images/MLPP/Shannon.jpg" Shannon/>
    <div class="container">
        <p>Claude Shannon 1916-2001. <a href="https://www.chalmers.se/en/areas-of-advance/ict/events/shannon-centennial/Pages/shannon.aspx">Picture source</a></p>
    </div>
</div>

## 1. 熵

>   **定义:** 分布为 $p$ 的随机变量 $X$ 的熵是不确定性的一种度量, 记为 $\mathbb{H}(X)$ 或 $\mathbb{H}(p)$ . 特别的, 对一个有着 $K$ 个取值的离散随机变量, 熵可以定义为
>
>   $$
>   \mathbb{H}(X)\triangleq-\sum_{k=1}^Kp(X=k)\log{p(X=k)}
>   $$
>

**定理:** $\mathbb{H}(X)\leq K$, 当且仅当 $X$ 是离散均匀分布时等号成立.

该定理可以作为下面信息不等式的推论得出. 从定理中容易知道离散分布的最大熵为 $\mathbb{H}(X)=\log{K}$ . 特别地, $K=2$ 时得到**二值熵** $\mathbb{H}(X)=-(\theta\log{\theta}+(1-\theta)\log{(1-\theta)})$ , 其中 $\theta$ 为成功概率(相应的 $1-\theta$ 为失败概率). 

## 2. KL 散度

一个通常用于度量两个概率分布 $p$ 和 $q$ 的差异大小的指标就是 **KL 散度(Kullback-Leibler divergence)** 或称为**相对熵**. 

>   **定义:** 离散形式
>
>   $$
>   \mathbb{KL}(p\lVert q)\triangleq\sum_{k=1}^Kp_k\log{\frac{p_k}{q_k}}
>   $$
>
>   连续形式
>
>   $$
>   \mathbb{KL}(p\lVert q)\triangleq\int_{\Omega} p(x)\log{\frac{p(x)}{q(x)}}\,dx
>   $$
>

注意, KL 散度不是对称的, 所以并不是一种距离度量. 把 KL 散度展开为两项

$$
\mathbb{KL}(p\lVert q)=\sum_kp_k\log{p_k} - \sum_kp_k\log{q_k} = -\mathbb{H}(p) + \mathbb{H}(p, q)
$$

其中我们把 $\mathbb{H}(p, q)$ 称为**交叉熵**. 交叉熵是使用模型 $q$ 编码来自于分布 $p$ 的数据所需要的平均位数, 从而"正规"熵 $\mathbb{H}(p)=\mathbb{H}(p, p)$ 即是使用正确模型编码所需要的位数, 所以 KL 散度可以理解为使用模型 $q$ 编码来自于分布 $p$ 的数据所<font color="red">额外</font>需要的位数. 

**定理(信息不等式):** $\mathbb{KL}(p\lVert q)\geq 0$, 当且仅当 $p=q$ 时等号成立.

可利用 Jensen 不等式

$$
f\left(\sum_{i=1}^n\lambda_ix_i\right)\leq\sum_{i=1}^n\lambda_if(x_i).
$$

证明上述定理, 证明略. 

## 3. 互信息

考虑随机变量 $X$ 和 $Y$, 如果我们想知道这两者之间的关联性有多强, 一个直接的方法是计算他们的相关系数. 但是相关系数所反应的随机变量的相关性存在局限性, 如下图所示

<div class="polaroid">
    <img class="cool-img" src="https://upload.wikimedia.org/wikipedia/commons/0/02/Correlation_examples.png" Correlation Examples/>
    <div class="container">
        <p>Correlation Examples</p>
    </div>
</div>

相关性相同的随机变量可以有着千奇百怪且截然不同的分布. 因此我们引入**互信息(mutual information, MI)**

>   **定义:** 对随机变量 $X$ 和 $Y$, 
>
>   $$
>   \mathbb{I}(X; Y)\triangleq\mathbb{KL}(p(X, Y)\lVert p(X)p(Y))=\sum_x\sum_yp(x, y)\log{\frac{p(x, y)}{p(x)p(y)}}
>   $$
>
>   显然 $\mathbb{I}(X; Y)\geq 0$, 当且仅当 $p(X, Y)=p(X)p(Y)$ 时取等号. 

这意味着 $MI=0$ 当且仅当 $X$ 和 $Y$ 独立. 进一步我们有

$$
\mathbb{I}(X; Y)=\mathbb{H}(X) - \mathbb{H}(X\lvert Y) = \mathbb{H}(Y) - \mathbb{H}(Y\lvert X)
$$

其中 $\mathbb{H}(Y\lvert X)=\sum_xp(x)\mathbb{H}(Y\lvert X=x)$ 称为**条件熵**, 利用贝叶斯公式上式容易证明.  有了条件熵, 我们就能对互信息做出直观的解释: <font color="red">观测到随机变量 $Y$ 后随机变量 $X$ 的熵减</font>, 反之亦然. 与互信息相关的另一概念是**点互信息(pointwise mutual information, PMI)** 

>   **定义:** 对随机事件 $x$ 和 $y$, 
>
>   $$
>   \text{PMI}(x, y)\triangleq\log{\frac{p(x, y)}{p(x)p(y)}}=\log{\frac{p(x\lvert y)}{p(x)}}=\log{\frac{p(y|x)}{p(y)}}
>   $$
>
>   衡量了两个事件同时发生的概率. 

显然 $X$ 和 $Y$ 的 MI 是 PMI 的期望(从定义式中可以看出). 

### 连续随机变量的互信息

计算连续随机变量的互信息通常先对其进行离散, 然后得到区间的统计值后再采用离散 MI 的计算公式. 然而离散的步长对结果有显著的影响. 另一种方法是**最大化信息系数(maximal information coefficient, MIC)** , 即尝试多种区间大小, 然后取最大值

>   **定义:**
>
>   $$
>   \text{MIC}\triangleq\max_{x, y:xy<B}\frac{\max_{G\in\mathcal{G}(x, y)}\mathbb{I}(X(G);Y(G))}{\log{\min(x, y)}}
>   $$
>
>   其中 $\mathcal{G}(x, y)$ 是一族大小为 $x\times y$ 的网格点, $X(G), Y(G)$ 表示网格上离散了的随机变量, $B$ 是采样的区间数, 一个典型的值为 $B=N^{0.6}$. 

可以证明 MIC 的范围是 $[0, 1]$ . 下面图 A 给出了 63566 个随机变量的相关系数 CC 和 MIC 的关系图, 图 B 给出了 CC 和 MI 的关系图.

<div class="polaroid">
    <img class="cool-img" src="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3325791/bin/nihms358982f4.jpg" MI-MIC-CC/>
    <div class="container">
        <p>MI-MIC-CC</p>
    </div>
</div>

*   点 C 表示一组低 CC, 低 MIC 的随机变量, 可以看出他们是不相关的.
*   点 D 和 H 表示两组高 CC(取绝对值), 高 MIC 的随机变量, 可以看出他们几乎存在线性相关性.
*   点 E, F 和 G 表示三组低 CC, 高 MIC 的随机变量, 显然他们存在非线性的相关性, 但是此时 CC 无法反映出这种相关性, 而 MIC 仍然能较好的体现出来.
*   图 I 中左侧的两幅图的噪声比右侧的两幅图更小



## 参考

[1] Machine Learning: A Probabilistic Perspective, Kevin P. Murphy, Chapter 2, Probability

[2] https://en.wikipedia.org/wiki/File:Correlation_examples.png 

[3] Reshef D N, Reshef Y A, Finucane H K, et al. Detecting novel associations in large data sets[J]. science, 2011, 334(6062): 1518-1524. 
