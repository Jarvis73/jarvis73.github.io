---
layout: post
title: LSTM 学习
date: 2018-01-24 19:03:00
categories: 深度学习
mathjax: true
figure: /images/2018-1-24/LSTM.png
author: Jarvis
meta: Post
---

* content
{:toc}

## 1. 理解 LSTM

[Understanding LSTM Networks -- Colah's blogs](https://link.jianshu.com/?t=http://colah.github.io/posts/2015-08-Understanding-LSTMs/)

[理解 LSTM 网络](https://www.jianshu.com/p/9dc9f41f0b29)




## 2. tensorflow 官方代码解析

来源: [Tensorflow 多层 LSTM 代码分析](http://blog.csdn.net/u014595019/article/details/52759104)

修改为 tensorflow r1.4 版本

### 分段讲解

总的来看，这份代码主要由三步分组成。 
第一部分，是PTBModel,也是最核心的部分，负责tf中模型的构建和各种操作(op)的定义。 
第二部分，是run_epoch函数，负责将所有文本内容分批喂给模型（PTBModel）训练。 
第三部分，就是main函数了，负责将第二部分的run_epoch运行多遍，也就是说，文本中的每个内容都会被重复多次的输入到模型中进行训练。随着训练的进行，会适当的进行一些参数的调整。 
下面就按照这几部分来分开讲一下。我在后面提供了完整的代码，所以可以将完整代码和分段讲解对照着看。

---

### 参数设置

在构建模型和训练之前，我们首先需要设置一些参数。tf中可以使用 `tf.flags` 来进行全局的参数设置

```python
flags = tf.flags
logging = tf.logging    

flags.DEFINE_string(    # 定义变量 model的值为small, 后面的是注释
    "model", "small",
    "A type of model. Possible options are: small, medium, large.")

flags.DEFINE_string("data_path",   #定义下载好的数据的存放位置
                    '/home/multiangle/download/simple-examples/data/', 
                    "data_path")
flags.DEFINE_bool("use_fp16", False,    # 是否使用 float16格式？
                  "Train using 16-bit floats instead of 32bit floats")

FLAGS = flags.FLAGS     # 可以使用FLAGS.model来调用变量 model的值。

def data_type():
    return tf.float16 if FLAGS.use_fp16 else tf.float321234567891011121314151617
```

细心的人可能会注意到上面有行代码定义了 model 的值为 small.这个是什么意思呢？其实在后面的完整代码部分可以看到，作者在其中定义了几个参数类，分别有 small,medium,large 和 test 这 4 种参数。如果 model 的值为small，则会调用 SmallConfig，其他同样。在 SmallConfig 中，有如下几个参数：

```python
init_scale = 0.1        # 相关参数的初始值为随机均匀分布，范围是[-init_scale,+init_scale]
learning_rate = 1.0     # 学习速率,在文本循环次数超过max_epoch以后会逐渐降低
max_grad_norm = 5       # 用于控制梯度膨胀，如果梯度向量的L2模超过max_grad_norm，则等比例缩小
num_layers = 2          # lstm层数
num_steps = 20          # 单个数据中，序列的长度。
hidden_size = 200       # 隐藏层中单元数目
max_epoch = 4           # epoch<max_epoch时，lr_decay值=1,epoch>max_epoch时,lr_decay逐渐减小
max_max_epoch = 13      # 指的是整个文本循环次数。
keep_prob = 1.0         # 用于dropout.每批数据输入时神经网络中的每个单元会以1-keep_prob的概率不工作，可以防止过拟合
lr_decay = 0.5          # 学习速率衰减
batch_size = 20         # 每批数据的规模，每批有20个。
vocab_size = 10000      # 词典规模，总共10K个词123456789101112
```

其他的几个参数类中，参数类型都是一样的，只是参数的值各有所不同。

---

### PTBModel

这个可以说是核心部分了。而具体来说，又可以分成几个小部分：

* 多层LSTM结构的构建
* 输入预处理
* LSTM的循环
* 损失函数计算
* 梯度计算
* 修剪

#### 1.1 LSTM结构

```python
class PTBInput(object):
  """The input data."""

  def __init__(self, config, data, name=None):
    self.batch_size = batch_size = config.batch_size
    self.num_steps = num_steps = config.num_steps
    self.epoch_size = ((len(data) // batch_size) - 1) // num_steps
    self.input_data, self.targets = reader.ptb_producer(
        data, batch_size, num_steps, name=name)		# 该类主要作用是这句, 从文件中读取数据
```

**self.input_data 和 self.targets 都是 index 的序列, 尺寸为 [batch_size, num_steps]**. 注意此时不论是input还是target都是用词典id来表示单词的。

`PTBModel.__init__()` 函数:

```python
self._input = input_	# [batch_size, num_steps]

batch_size = input_.batch_size
num_steps = input_.num_steps
size = config.hidden_size		# 隐藏层规模
vocab_size = config.vocab_size	# 词典规模
```

引进参数.

```python
def lstm_cell():
      if 'reuse' in inspect.getargspec(tf.contrib.rnn.BasicLSTMCell.__init__).args:
        return tf.contrib.rnn.BasicLSTMCell(size, 
                                            forget_bias=0.0, 
                                            state_is_tuple=True,
                                            reuse=tf.get_variable_scope().reuse)
      else:
        return tf.contrib.rnn.BasicLSTMCell(size, 
                                            forget_bias=0.0, 
                                            state_is_tuple=True)
```

首先使用 `tf.contrib.rnn.BasicLSTMCell` 定义单个基本的 LSTM 单元。这里的 size 其实就是隐藏层规模。 
从源码中可以看到，在 LSTM 单元中，有 2 个状态值，分别是 c 和 h，分别对应于下图中的 c 和 h。其中 h 在作为当前时间段的输出的同时，也是下一时间段的输入的一部分。

<div class="polaroid-small">
    <img class="cool-img" src="http://static.open-open.com/lib/uploadImg/20150829/20150829181723_640.png" />
    <div class="container">
        <p>LSTM 单元</p>
    </div>
</div>

那么当 `state_is_tuple=True` 的时候，state 是元组形式，state=(c,h)。如果是 False，那么 state 是一个由c和h拼接起来的张量，`state=tf.concat(1, [c,h])`。**在运行时，则返回2值，一个是h，还有一个state。**

#### 1.2 DropoutWrapper

```python
attn_cell = lstm_cell
if is_training and config.keep_prob < 1:	# 在外面包裹 dropout
	def attn_cell():
        return tf.contrib.rnn.DropoutWrapper(lstm_cell(), output_keep_prob=config.keep_prob)
```

我们在这里使用了 dropout 方法。**所谓 dropout, 就是指网络中每个单元在每次有数据流入时以一定的概率(keep prob)正常工作，否则输出0值**。这是是一种有效的正则化方法，可以有效防止过拟合。*在 rnn 中使用 dropout 的方法和 cnn 不同*，推荐大家去把 [recurrent neural network regularization](http://arxiv.org/pdf/1409.2329.pdf) 看一遍。 
在 rnn 中进行 dropout 时，对于 rnn 的部分不进行 dropout，也就是说从 t-1 时候的状态传递到t时刻进行计算时，这个中间不进行 memory 的 dropout；仅在同一个t时刻中，多层 cell 之间传递信息的时候进行 dropout，如下图所示

<div class="polaroid-small">
    <img class="cool-img" src="http://ww3.sinaimg.cn/large/901f9a6fjw1f5vitpqyyuj20fg0bht98.jpg" />
    <div class="container">
        <p>循环神经元展开示意图</p>
    </div>
</div>

上图中，$t-2$ 时刻的输入 $x_{t−2}$ 首先传入第一层 cell，这个过程有 dropout，但是从  $t−2$ 时刻的第一层 cell 传到 $t−1, t, t+1$ 的第一层 cell 这个中间都不进行 dropout。再从 $t+1$ 时候的第一层 cell 向同一时刻内后续的 cell 传递时，这之间又有 dropout 了。

在使用 `tf.contrib.rnn.DropoutWrapper` 时，同样有一些参数，例如 `input_keep_prob, output_keep_prob` 等，分别控制输入和输出的dropout概率，很好理解。

#### 1.3 多层LSTM结构和状态初始化

```python
cell = tf.contrib.rnn.MultiRNNCell([attn_cell() for _ in range(config.num_layers)],
                                   state_is_tuple=True)
# 参数初始化,rnn_cell.RNNCell.zero_stat
self._initial_state = cell.zero_state(batch_size, data_type())
```

在这个示例中，我们使用了 2 层的 LSTM 网络。也就是说，前一层的 LSTM 的输出作为后一层的输入。使用`tf.contrib.rnn.MultiRNNCell` 可以实现这个功能。这个基本没什么好说的，`state_is_tuple` 用法也跟之前的类似。构造完多层 LSTM 以后，使用 `zero_state` 即可对各种状态进行初始化。

#### 2. 输入预处理

```python
with tf.device("/cpu:0"):
  	# 把描述单词的指标 idx ([1, 1]) 变为 embedding ([1, hidden_size]) 描述
    # 使用 embedding 描述可以让网络从描述中学习单词之间的关联, 否则单个的指标之间是独立的, 无法学习关联 ???
    embedding = tf.get_variable("embedding", [vocab_size, size], dtype=data_type())     

    # 将输入的每个 sequence ([batch_size, num_steps]) 用 embedding 表示 
    # shape = [batch_size, num_steps, hidden_size]
    # 所以每个 x_t 都是一个 batch_size x 1 x hidden_size 的向量
    # 在程序里 1 自动省去, 所以每个 x_t 实际上是 [batch_size, hidden_size] 的向量
    inputs = tf.nn.embedding_lookup(embedding, input_.input_data)

if is_training and config.keep_prob < 1:
    inputs = tf.nn.dropout(inputs, config.keep_prob)
```

之前有提到过，输入模型的 input 和 target 都是用词典 id 表示的。例如一个句子，“我/是/学生”，这三个词在词典中的序号分别是 0,5,3，那么上面的句子就是 [0,5,3]。这样就和隐藏层需要的输入维度不匹配 (输入需要长度为 hidden_size 的向量)，我们要把词典 id 转化成向量,也就是 embedding 形式。可能有些人已经听到过这种描述了。实现的方法很简单。

第一步，构建一个矩阵，就叫 embedding 好了，尺寸为 [vocab_size, embedding_size]，分别表示词典中单词数目，以及要转化成的向量的维度。一般来说，向量维度越高，能够表现的信息也就越丰富。注意这里的 embedding 变量是使用均匀分布随机初始化的, 初始化器定义在 main 函数中. 并且 embedding 是变量矩阵, 在训练过程中是进行优化的, 期望是让有关联的词语对应的 embedding 向量形成某种关系.

第二步，使用 `tf.nn.embedding_lookup(embedding,input_ids)` 假设 input_ids 的长度为 len，那么返回的张量尺寸就为 [len,embedding_size]。

举个栗子:

```python
# 示例代码
import tensorflow as tf
import numpy as np

sess = tf.InteractiveSession()

embedding = tf.Variable(np.identity(5,dtype=np.int32))
input_ids = tf.placeholder(dtype=tf.int32,shape=[None])
input_embedding = tf.nn.embedding_lookup(embedding,input_ids)

sess.run(tf.initialize_all_variables())
print(sess.run(embedding))
#[[1 0 0 0 0]
# [0 1 0 0 0]
# [0 0 1 0 0]
# [0 0 0 1 0]
# [0 0 0 0 1]]
print(sess.run(input_embedding,feed_dict={input_ids:[1,2,3,0,3,2,1]}))
#[[0 1 0 0 0]
# [0 0 1 0 0]
# [0 0 0 1 0]
# [1 0 0 0 0]
# [0 0 0 1 0]
# [0 0 1 0 0]
# [0 1 0 0 0]]
```

第三步，如果 keep_prob<1， 那么还需要对输入进行 dropout。不过这边跟 rnn 的 dropout 又有所不同，这边使用 `tf.nn.dropout`。

#### 3. LSTM循环

现在，多层 lstm 单元已经定义完毕，输入也已经经过预处理了。那么现在要做的就是将数据输入lstm进行训练了。其实很简单，只要按照文本顺序依次向cell输入数据就好了。lstm上一时间段的状态会自动参与到当前时间段的输出和状态的计算当中。

```python
outputs = []
state = self._initial_state # state 表示 各个batch中的状态
with tf.variable_scope("RNN"):
    for time_step in range(num_steps):
        if time_step > 0: tf.get_variable_scope().reuse_variables()
        # 输入: [batch_size, hidden_size]
        # 按照顺序向cell输入文本数据, cell_out: [batch_size, hidden_size]
        (cell_output, state) = cell(inputs[:, time_step, :], state) 
        outputs.append(cell_output)  # output: [num_steps][batch_size, hidden_size]

# 把之前的list展开，成 [batch, num_steps, hidden_size]
# 然后 reshape 成 [batch*numsteps, hidden_size], 这是为了后面 softmax 层计算方便
output = tf.reshape(tf.stack(axis=1, values=outputs), [-1, size])
```

这边要注意，`tf.get_variable_scope().reuse_variables()` 这行代码不可少，因为在 num_steps 的循环中实际上是在相同的权重上更新的

#### 4. 损失函数计算

```python
# softmax_w , shape=[hidden_size, vocab_size], 用于将distributed表示的单词转化为one-hot表示
softmax_w = tf.get_variable("softmax_w", [size, vocab_size], dtype=data_type())
softmax_b = tf.get_variable("softmax_b", [vocab_size], dtype=data_type())
# [batch*numsteps, vocab_size] 从隐藏语义转化成完全表示
logits = tf.matmul(output, softmax_w) + softmax_b

# loss , shape=[batch*num_steps], 带权重的交叉熵计算
loss = tf.contrib.seq2seq.sequence_loss(
    logits,					# [batch*numsteps, vocab_size]
    input_.targets,			# [batch_size, num_steps]
    tf.ones([batch_size, num_steps], dtype=data_type()),	# weight
    average_across_timesteps=False,
    average_across_batch=True			# loss = loss / batch_size
)
self._cost = cost = tf.reduce_sum(loss)
self._final_state = state
```

上面代码的上半部分主要用来将多层lstm单元的输出转化成one-hot表示的向量。关于one-hot presentation和distributed presentation的区别，可以参考 [这里](http://blog.csdn.net/u014595019/article/details/51884529#t0)

代码的下半部分，正式开始计算损失函数。这里使用了 tf 提供的现成的交叉熵计算函数, `tf.contrib.seq2seq.sequence_loss`。不知道交叉熵是什么？见[这里](http://blog.csdn.net/u014595019/article/details/52562159#t7)各个变量的具体shape我都在注释中标明了。注意其中的 `self._targets` 是词典 id 表示的。这个函数的具体实现方式不明。我曾经想自己手写一个交叉熵，不过好像 tf 不支持对张量中单个元素的操作。

#### 5. 梯度计算

之前已经计算得到了每批数据的平均误差。那么下一步，就是根据误差来进行参数修正了。当然，首先必须要求梯度

```python
self._lr = tf.Variable(0.0, trainable=False)  # lr 指的是 learning_rate
tvars = tf.trainable_variables()
```

**通过 tf.trainable_variables 可以得到整个模型中所有 trainable = True 的 Variable**。实际得到的 tvars 是一个列表，里面存有所有可以进行训练的变量。

```python
grads, _ = tf.clip_by_global_norm(tf.gradients(cost, tvars),
                                  config.max_grad_norm)
```

这一行代码其实使用了两个函数，`tf.gradients` 和 `tf.clip_by_global_norm`。 我们一个一个来。

**tf.gradients** 
用来计算导数。该函数的定义如下所示

```python
def gradients(ys,
              xs,
              grad_ys=None,
              name="gradients",
              colocate_gradients_with_ops=False,
              gate_gradients=False,
              aggregation_method=None):
```

虽然可选参数很多，但是最常使用的还是ys和xs。根据说明得知，ys和xs都可以是一个tensor或者tensor列表。而计算完成以后，该函数会返回一个长为len(xs)的tensor列表，列表中的每个tensor是ys中每个值对xs[i]求导之和。如果用数学公式表示的话，那么 `g = tf.gradients(y,x)`可以表示成 

$$
g_i = \sum_{j=0}^{len(y)}\frac{\partial y_i}{\partial x_i} \\ g = [g_0, g_1, \cdots, g_{len(x)}
$$

#### 6. 梯度修剪

**tf.clip_by_global_norm** 
修正梯度值，用于**控制梯度爆炸的问题**。梯度爆炸和梯度弥散的原因一样，都是因为链式法则求导的关系，导致梯度的指数级衰减。为了避免梯度爆炸，需要对梯度进行修剪。 
先来看这个函数的定义：

```python
def clip_by_global_norm(t_list, clip_norm, use_norm=None, name=None):
```

**输入参数**中：t_list 为待修剪的张量, clip_norm 表示修剪比例 (clipping ratio).

函数**返回2个参数**： list_clipped，修剪后的张量，以及global_norm，一个中间计算量。当然如果你之前已经计算出了 global_norm 值，你可以在 use_norm 选项直接指定 global_norm 的值。

那么具体**如何计算**呢？根据源码中的说明，可以得到 
`list_clipped[i] = t_list[i] * clip_norm / max(global_norm, clip_norm)`,其中 
`global_norm = sqrt(sum([l2norm(t)**2 for t in t_list]))`

如果你更熟悉数学公式，则可以写作 

$$
L_c^i = \frac{L_t^i N_c}{\max(N_c, N_g)},\quad N_g = \sqrt{\sum_i(L_t^i)^2}
$$
其中, $L_t^i$ 和 $L_c^i$ 代表 `t_list[i]` 和 `list_clipped[i]`, $N_c$ 和 $N_g$ 代表 clip_norm 和 global_norm 的值。 

#### 7. 优化参数

之前的代码已经求得了合适的梯度，现在需要使用这些梯度来更新参数的值了。

```python
# 梯度下降优化，指定学习速率
optimizer = tf.train.GradientDescentOptimizer(self._lr)
# optimizer = tf.train.AdamOptimizer()
# optimizer = tf.train.GradientDescentOptimizer(0.5)
self._train_op = optimizer.apply_gradients(
    zip(grads, tvars),
    global_step=tf.contrib.framework.get_or_create_global_step())  # 将梯度应用于变量
```

这一部分就比较自由了，tf 提供了很多种优化器，例如最常用的梯度下降优化（GradientDescentOptimizer）也可以使用 AdamOptimizer。这里使用的是梯度优化。值得注意的是，这里使用了optimizer.apply_gradients来将求得的梯度用于参数修正，而不是之前简单的optimizer.minimize(cost)

还有一点，要留心一下 self._train_op，只有该操作被模型执行，才能对参数进行优化。如果没有执行该操作，则参数就不会被优化。

## 3. Main 函数

```python
initializer = tf.random_uniform_initializer(-config.init_scale, config.init_scale)

with tf.name_scope("Train"):
	train_input = PTBInput(config=config, data=train_data, name="TrainInput")
	with tf.variable_scope("Model", reuse=None, initializer=initializer):
    	m = PTBModel(is_training=True, config=config, input_=train_input)
	tf.summary.scalar("Training Loss", m.cost)
	tf.summary.scalar("Learning Rate", m.lr)
```

以均匀分布 [-init_scale, init_scale] 作为所有变量的初始化器, `train_input` 是一个类, 包含了所有的训练数据.
