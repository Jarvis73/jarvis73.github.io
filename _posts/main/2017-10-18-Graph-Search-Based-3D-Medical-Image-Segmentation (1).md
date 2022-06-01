---
layout: post
title: 基于图搜索的三维医学图像分割方法 (一)
date: 2017-10-18 20:49:00 +0800
categories: Algorithm
mathjax: true
author: Jarvis
meta: Post
---

* content
{:toc}

文章标题: Optimal Surface Segmentation in Volumetric Images --- A graph-Theoretic Approach

作者: Kang Li, Xiaodong Wu, Danny Z. Chen, Milan Sonka

## **介绍**
目前已经有很多基于图搜索的方法应用在了2D自然图像的分割上. 而很多医学图像(比如CT)是3D的, 在使用2D分割方法的时候就会丢失第三个维度的纹理信息, 而直接把之前的2D方法拓展到3D则又会遇到计算量剧增的困扰. 本文提出了一种将三维表面的分割问题转化为赋权有向图上最小割计算的方法. 在医学图像中许多表面是有很强的关联性的, 这种表面我们称之为*成对的*, 比如气管的内壁和外壁. 在分割过程中充分利用这种关联性可以有效的提高分割的准确性. 本文的主要工作是把图搜索技术拓展到了3维及以上的维度并应用到了 $ k $ 个关联表面的划分上, 同时该方法向下兼容二维的图搜索. 

本文提出的方法有一定的局限性, 要求划分的表面必须是类似于地形图的3D图像或柱面图(可以沿着长边展开成类地形图). 

+-+-+-+-


## **相关工作**
* 基于图的图像分割

* 使用图割的能量最小化方法

* 成对表面的分割

## **图构造**
有向图中的*闭集*是顶点集的一个子集, 其中所有的顶点的后代都在该集合内. 这里顶点的后代指的是从该顶点出发沿图的边所能到达的所有点. 
一个闭集的*损失*指的是集合中每个顶点损失的总和. *最小闭集问题*是指在图中寻找一个损失最小的闭集, 该问题的解决可以通过把最小闭集问题转化为一个计算赋权有向图的 $ s-t $ 割的问题. 而*图像分割问题*的解决方案即是把分割问题转化为最小闭集问题.
### 单表面
这一小节我们首先介绍一系列的概念, 有些概念容易混淆, 应当注意区分.

<div class="polaroid">
    <img class="cool-img" src="/images/2017-10-18/single-surface.png" single-surface/>
    <div class="container">
        <p>图1: 单表面问题, 虚线表示可选择的边(按文章中的意思是都包含在了边集中)</p>
    </div>
</div>

记三维图像为三维矩阵 $ \mathcal{A}(x, y, z) $ . 类地形图的曲面如图所示, 即是指对于每个 $ (x, y) $ , 都有唯一的 $ z $ 与之对应. 令 $ X, Y, Z $ 表示图像在 $ \mathbf{x, y, z} $ 方向的尺寸. 

定义函数

$$ 
\mathcal{N}: (x, y) \rightarrow \mathcal{N}(x, y),
$$ 

表示前述的曲面, 那么函数应当满足

$$ 
	x\in\mathbf{x}=\{0,1,\dots, X-1\}, \\
	y\in\mathbf{y}=\{0,1,\dots, Y-1\}, \\
	\mathcal{N}(x, y)\in\mathbf{z}=\{0,1,\dots, Z-1\}. \\
$$ 

一个曲面称为*可行的*, 如果满足由 $ \Delta_x, \Delta_y $ 定义的*光滑性约束*: 如果 $ \mathcal{A}(x,y,z) $ 和 $ \mathcal{A}(x+1,y,z') $ 是可行曲面上的两个体素, 则 $ \lvert z-z'\rvert \leq\Delta_x $ . 如果 $ \mathcal{A}(x,y,z) $ 和 $ \mathcal{A}(x,y+1,z') $ 是可行曲面上的两个体素, 则 $ \lvert z-z'\rvert \leq\Delta_y $ . 容易看出该约束保证了曲面的光滑性, 即不会产生突变. 

 $ c(x,y,z) $ 定义为体素 $ \mathcal{A}(x,y,z) $ 的损失函数, 与其落在曲面上的可能性成负相关. *最优曲面*就是总的损失函数最小的曲面. 

定义一个加权有向图 $ G=(V, E) $ , 每个顶点 $ V(x,y,z) $ 代表唯一的体素 $ \mathcal{A}(x,y,z)\in\mathcal{A} $ , 顶点的权重(损失)为

![eq01](/images/2017-10-18/eq1.png)

**注意:** 这里有几个点需要区分, 我们把原始的3D图像称为**图像**, 而把由顶点和边组成的称为**图**; 图像中的点称为**体素**, 每个体素对应的值称为**损失**; 图中的点称为**顶点**, 每个顶点对应的值称为**权重**, 图中的边就称为**边**, 要注意区分.

<br />

如果 $ z>z' $ , 则称 $ V(x,y,z) $ 在顶点 $ V(x',y',z') $ *上面*或者称顶点 $ V(x,y,z) $ *高于*顶点 $ V(x',y',z') $ ; 类似地我们可以定义*下面*和*低于*这两种叫法.
 $ Col(x,y):=\{V(x,y,z)|z\in\mathbf{z}\} $ 称为图 $ G $ 的$ (x,y) $*列*, 其中 $ x\in\mathbf{x}, y\in\mathbf{y} $ . 
两个 $ (x,y)-\text{列} $ 相邻当且仅当两个 $ (x,y) $ 相邻. 本文假设 $ Col(x,y) $ 只与 $ Col(x+1,y),Col(x-1,y),Col(x,y+1),Col(x,y-1) $ 四个列相邻. 

图 $ G $ 的边有两种类型: *列内边*(intracolumn)  $ \;E^a $ 和*列间边* (intercolumn) $ \;E^r $ , 定义如下:

(2)

$$ 
	E^a=\{V(x,y,z)\rightarrow V(x,y,z-1)|z>0\}
$$ 

(3)

$$ 
E^r=\{V(x,y,z)\rightarrow V(x\pm 1,y,\max(0,z-\Delta_x)),\; V(x,y,z)\rightarrow V(x,y\pm 1,\max(0,z-\Delta_y))|z>0\}	
$$ 

从图1(b)可以看到列内边和列间边的区别. 直观上, 如果体素 $ \mathcal{A}(x,y,z) $ 在可行面 $ \mathcal{N} $ 上, 那么它的4个相邻体素不会低于 $ \mathcal{A}(x,y,\max(0,z-\Delta_x)) $ . 根据 $ E^r $ 的构造规则, 顶点集 $ V(\mathbf{x,y}, 0) $ 是强连通的(这里是因为保留了虚线边), 同时也是定义于 $ G $ 上的最低的可行面, 我们称之为*基础集*, 记作 $ V^B $ .

<div class="polaroid">
    <img class="cool-img" src="/images/2017-10-18/image-unfolding.png" image-unfolding/>
    <div class="container">
        <p>图2: 图像展开</p>
    </div>
</div>

有时候目标曲面是沿着某个方向环绕的(即柱形曲面), 此时需要先展开, 再应用本文的算法. 所以沿着展开面的两条边界要满足光滑性条件. 比如沿 $ x $ 方向环绕, 则
$$ 
V(0,y,z)\rightarrow V(X-1,y,\max(0,z-\Delta_x)),\quad V(X-1,y,z)\rightarrow V(0,y,\max(0,z-\Delta_x)).
$$  

### 多重表面
不考虑曲面的相交或重叠, 4D有向图 $ G(V, E) $ 可以划分为 $ k(k\geq 2) $ 个3D有向图, 满足 $ V=\bigcup_{i=1}^kV_i $ 和 $ E=\bigcup_{i=1}^kE_i\cup E^s $ .  $ E^s $ 中的边称为*面间边*(intersurface). 考虑不相交的二重曲面(比如人体组织的内壁和外壁), 记两个曲面之间的最大和最小距离分别为 $ \delta^u, \;\delta^l $ , 我们把下面由这两个参数形成的约束称为*分离约束*. 记两个的3D图为 $ G_1 $ 和 $ G_2 $ , 3D图中的列分别为 $ Col_1(x,y),\;Col_2(x,y) $ , 3D图对应的图像中的曲面记为 $ \mathcal{N}_1 $ 和 $ \mathcal{N}_2 $ . 我们假设曲面 $ \mathcal{N}_1 $ 在 $ \mathcal{N}_2 $ 的上面:

*  $ \forall V_1(x,y,z) \in Col_1(x,y), \; z\geq\delta^u, \; V_1(x,y,z)\rightarrow V_2(x,y,z-\delta^u) $ 

*  $ \forall V_2(x,y,z) \in Col_2(x,y), \; z<Z-\delta^l, \; V_2(x,y,z)\rightarrow V_1(x,y,z+\delta^l) $ 

* 由分离约束( $\mathcal{N}_2$ 至少比 $\mathcal{N}_1$ 低 $\delta_l$ 个体素单元), 所以 $V_1(x,y,z), z<\delta^l$ 不可能在面 $ \mathcal{N}_1 $ 上; $ V_2(x,yz), z\geq Z-\delta^l $ 不可能在面 $ \mathcal{N}_2 $ 上. 所以这些点直接丢掉. 

* 4D图 $ G_1 $ 的基础集变为 $ V_1(\mathbf{x,y},\delta_l) $ , 顶点 $ V(x, y, \delta^l) $ 的权重变为 $ w_1(x,y,\delta^l)=c_1(x,y,\delta_l) $. $ c_1(x, y, \delta^l)$ 就是曲面 $\mathcal{N}1$ 中体素 $\mathcal{A}(x,y,\delta^l)$ 的损失. $G_1$ 的列间边要修正使得 $V_1(x,y,\delta^l)$ 强连通.  $ G $ 的基础集为 $ V^B=V_(\mathbf{x,y},\delta^l)\cup V_2(\mathbf{x,y},0) $.

* 加入 $ V_1(0,0,\delta_l)\rightarrow V_2(0,0,0) $ 使得 $ V^B $ 强连通(图 $ V_1 $ 和 $ V_2 $ 单独均为强连通图,  $ \delta^l $ 保证了存在从 $ V_2 $ 到 $ V_1 $ 的边, 为了保强连通性需要至少一条从 $ V_1 $ 到 $ V_2 $ 的边). 

<div class="polaroid">
    <img class="cool-img" src="/images/2017-10-18/multi-surface.png" multi-surface/>
    <div class="container">
        <p>图3: (a)不相交; (b)相交</p>
    </div>
</div>


面间边表示如下:  

![eq04](/images/2017-10-18/eq04.png)

另外, 两个曲面可能相交,(比如追踪运动的表面时), 此时 $ \delta^l $ 和 $ \delta^u $ 代表一个曲面可以到达另一个曲面下面或者上面的最大距离. 这种情况下的面间边包括 $ V_1(x,y,z) \rightarrow V_2(x,y,\max(0,z-\delta^l)) $ 和 $ V_2(x,y,z) \rightarrow V_1(x,y,\max(0,z-\delta^u)) $ . 

## **曲面划分算法**
多重耦合表面的划分可以标准化为计算4D几何图上的最小闭集问题. 我们的算法时间复杂度与光滑化参数( $ \Delta_{xi},\; \Delta_{yi}, i=1,...,k $ )和曲面分离参数( $ \delta^l_{i,i+1},\; \delta^u_{i,i+1},i=1,...,k $ )无关. 我们统称光滑化约束和曲面分离约束为*几何约束*.

### 最小闭集
单表面的情况下,  $ \forall\;\mathcal{N}\in\mathcal{A}, C=\{V(\mathbf{x,y},z)|z\leq\mathcal
N(x,y)\} $ 形成了 $ G $ 中的一个闭集, 其中 $ \mathcal{N}(x,y) $ 表示一个曲面. 由式(1)可知 $ C $ 和 $ \mathcal{N} $ 的损失相同. 

**引理1.** 任意的 $ k $ 个 $ \mathcal{A} $ 中的可行面与 $ G $ 中的一个有相同损失的非空闭集关联.

**引理2.**  $ G $ 中的任一个非空闭集定义了 $ \mathcal{A} $ 上有相同损失的 $ k $ 个可行面. 

**引理3.**  $ G $ 中的最小非空闭集 $ C^* $ 决定了 $ \mathcal{A} $ 中的 $ k $ 个最优表面. 

如果最小闭集是空集, 那么任意非空闭集的损失都是非负的. 因为基础集 $ V^B $ 是强连通的, 并且是最低的 $ k $ 个面, 所以它总是包含在任意的非空闭集中. 因此, 为了保证最小闭集有负的损失, 我们把基础集中点的损失都初始化为 $ -1 $ , 这相当于把任意非空闭集的损失平移了一个负常数. 平移后, 我们可以很容易找到一个最小闭集 $ C^\* $ , 并且 $ C^\* $ 是平移前的最小非空闭集. 

在图1和图3中, 把从 $ V^B $ 外指向 $ V^B $ 内的边画成虚线, 表示这些边是可选的. 这就意味着如果几何约束越宽松(即 $ \Delta $ 或 $ \delta $ 越大), 图的边就越少, 图就越小.

### 计算最优的 $ k $ 个面
由引理3, 我们需要计算最小损失的非空闭集 $ C^\* $ , 而可以通过计算相关图上 $ G_{st} $ 上的最小割来计算 $ C^\* $ .

令 $ V^+ $ 和 $ V^- $ 表示图 $ G $ 上损失为正和负的点集. 定义一个新的有向图 $ G_{st}=(V\cup\{s,t\}, E\cup E_{st}) $ , 其中 $ G=(V, E) $ ,  $ s $ 是*源*,  $ t $ 是*汇*. 令 $ E $ 中所有边权为无穷大.  $ E_{st} $ 包含了:

*  $ s\rightarrow v\in V^- $ , 边权为 $ -w(v) $ 

*  $ V^+\ni v\rightarrow t $ , 边权为 $ w(v) $ 

令 $ (S, T) $ 为 $ G_{st} $ 的一个有限损失的割,  $ c(S,T) $ 为割的总损失. 可以证明

$$ 
c(S,T)=-w(V^-)+\sum_{v\in S-\{s\}}w(v), 
$$ 

其中 $ w(V^-) $ 是固定的. 因为 $ S-\{s\} $ 是闭集, 所以 $ (S, T) $ 的损失和 $ G $ 中关联的闭集的损失差一个常数. 因此 $ G_{st} $ 中最小割的源集为 $ S^\*-\{s\} $ 与 $ G $ 中的最小闭集 $ C^\* $ 关联. 

图 $ G_{st} $ 有 $ O(kn) $ 个顶点和 $ O(kn) $ 条边, 所以计算最小闭集 $ C^* $ 的时间复杂度为 $ T(kn, kn) $ . 计算出最小闭集后, 取每一列中 $ z $ 值最大的点得到的集合即是最优的 $ k $ 个表面.

**定理1.**  $ n $ 个体素的三维图像 $ \mathcal{A}(\mathbf{x,y,z}) $ 的最优 $ k $ 个表面可以在 $ T(kn,kn) $ 的时间内算出.

#### **Algorithm1 算法描述**
**Require:**  $ k,\Delta_x,\Delta_y,\delta^l,\delta^u $  和损失函数
1. 构建图 $ G_{st}=(V\cup\{s,t\}, E\cup E_{st}]) $ ;
2. 计算 $ G_{st} $ 的最小s-t割 $ (S^\*, T^\*) $ ;
3. 从 $ S^\*-\{s\} $ 中还原 $ k $ 个最优表面;

## **损失函数**
### 基于边的损失函数

(5)

$$
	c(x,y,z)=-e(e,y,z)\cdot p(\phi(x,y,z))+q(x,y,z)
$$

其中 $e(x,y,z)$ 是图像一阶导和二阶导的raw edge response, 

(6)

$$
	e(x,y,z)=(1-\lvert \omega\rvert )\cdot(\mathscr{I}*\mathscr{M}_{first\;derivative})(x,y,z)\dotplus\omega\cdot(\mathscr{I}*\mathscr{M}_{second\;derivative})(x,y,z).
$$

其中 $\dotplus$ 表示pixel-wise的求和, $*$ 是卷积算子, 权重系数 $-1<\omega<1$ 控制了一二阶导数的相对影响. $\phi(x,y,z)$ 定义了边界取向, 在损失函数中用一个取向惩罚项来表示, 当 $\phi(x,y,z)$ 落在给定范围之外, 则取 $0<p<1$; 否则 $p=1$. $q(x,y,z)>0$ 是位置惩罚项. 

### 不基于边的损失函数

(7)

$$
	\epsilon(S,a_1;a_2)=\int_{inside(S)}(\mathscr{I}(x,y,z)-a_1)^2\;dxdydz + \int_{outside(S)}(\mathscr{I}(x,y,z)-a_2)^2\;dxdydz
$$

其中常数 $a_1,\; a_2$ 是表面 $S$ 内侧和外侧的平均强度.

定义由列 $Col(x',y')$ 的得到的 $\mathcal{A}(x',y',z')$ 的损失为

(8)

$$
	c(x',y',z')=\sum_{z\leq z'}(\mathscr{I}(z',y',z)-a_1)^2 + \sum_{z> z'}(\mathscr{I}(z',y',z)-a_2)^2
$$

那么 $\mathcal{N}$ 的总损失就等于 $\epsilon(\mathcal{N},a_1;a_2)$ (离散在网格上的损失). 但是由于最优表面不知道, 所以 $a_1,\; a_2$ 是未知的, 所以哪些点属于表面内侧和外侧的无从知晓的. 但是我们的图的构造保证了: 如果 $V(x',y',z')$ 在 $\mathcal{N}$ 上, 那么满足 $\mathbf{z_1}\equiv${$z\lvert z\leq\max(0,z'-\lvert x-x'\rvert \Delta_x-\lvert y-y'\rvert \Delta_y)$} 的点 $V(\mathbf{x,y,z_1})$ 在与 $\mathcal{N}$ 相关的闭集 $C$ 中. 相应的, 满足 $\mathbf{z_2}\equiv${$z\lvert z'+\lvert x-x'\rvert \Delta_x-\lvert y-y'\rvert \Delta_y<z<Z$} 的点 $V(\mathbf{x,y,z_2})$ 一定不在 $C$ 中. 这就意味着如果点 $V(x',y',z')$ 在可行面 $\mathcal{N}$ 上, 那么点 $V(\mathbf{x,y,z_1})$ 在 $\mathcal{N}$ 内部, 而点 $V(\mathbf{x,y,z_2})$ 在 $\mathcal{N}$ 外部.

从而$\hat{a_1}(x',y',z')$ 和 $\hat{a_2}(x',y',z')$可以作为 $a_1$ 和 $a_2$ 的近似:

(9)

$$
	\hat{a_1}(x',y',z')=\text{mean}(\mathscr{I}(\mathbf{x,y,z_1})) 
$$

(10)

$$
	\hat{a_2}(x',y',z')=\text{mean}(\mathscr{I}(\mathbf{x,y,z_2}))
$$
