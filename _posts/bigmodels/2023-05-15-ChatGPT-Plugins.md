---
layout: post
title: "ChatGPT 70 款插件测评 惊艳的开发过程与宏大的商业化愿景"
date: 2023-05-15 10:57:00 +0800
categories: 大模型
author: Jarvis
meta: Post
---

* content
{:toc}

我们对ChatGPT的插件商店中总共70款插件进行了评测。区别于Chrome，AppStore等平台的代码开发范式，开发者仅使用自然语言就可以开发ChatGPT插件，并由GPT模型自行决定在使用过程中是否调用插件。约八成插件集中于购物、餐饮、旅行、住房和求职场景，其余分布在教育、财经咨讯、内容社区和编程技术场景。商业分析、游戏、身体/心理健康、社交以及家庭和育儿场景是蓝海。约七成插件用于已有平台的商业导流，同质化严重；联网、实时信息获取和阅读网页/PDF功能是刚需。Wolfram（数学计算）、WebPilot（网页阅读）、Speak（专业翻译）、Prompt Perfect（提示词润色）、Diagram It（流程图绘制）、AskYourPDF（PDF阅读）、CreatiCode Scratch（少儿编程）、Chess（国际象棋游戏教练）、edX（公开课学习）、FiscalNote（政策咨询）等插件值得一试。



{% include image.html class="polaroid" url="2023/05/plugins/plugins.png" title="plugins" %}

## 前言
很幸运接到OpenAI的早期插件开发者的邀请，我们探索了整个插件开发的流程，并全面评测了现有的70款ChatGPT插件，为每个插件提供了一句话简介和使用样例分析。

在插件开发流程方面，不同于Chrome，AppStore等平台基于代码的开发范式，开发者在构建好本地API后，仅需使用自然语言描述在什么场景下如何使用对应的API，即可将插件部署到ChatGPT平台。猜测OpenAI的GPT系列模型具有连接不同结构化文本的能力，可能是新的零代码开发范式。在插件的使用过程中，每个会话中最多可以选择三个插件进行联合使用，并由GPT模型自行决定在使用过程中是否调用插件，以及调用哪些插件。

在现有插件测评方面，我们将插件分为了以下几个维度：场景、功能、商业化、使用体验、推荐程度。其中，场景和功能是插件的基本属性，商业化和使用体验是插件的商业属性，推荐程度是插件的综合属性。我们发现，约八成插件集中于购物、餐饮、旅行、住房和求职这些成熟的商业化场景，其余分布在教育、财经咨讯、内容社区和编程技术场景。此外，专业领域，例如商业分析、游戏、身体/心理健康，以及社交，家庭和育儿场景是蓝海。约七成插件用于已有平台的商业导流，同质化严重，或许意味着OpenAI成为新的流量分发平台的雄心。

此外，我们也发现，联网、实时信息获取和阅读网页/PDF功能是刚需。Wolfram（数学计算）、WebPilot（网页阅读）、Speak（专业翻译）、Prompt Perfect（提示词润色）、Diagram It（流程图绘制）、AskYourPDF（PDF阅读）、CreatiCode Scratch（少儿编程）、Chess（国际象棋游戏教练）、edX（公开课学习）、FiscalNote（政策咨询与分析）等插件商业化属性弱，功能强大，值得一试。

我们不仅对单个插件功能进行了评测，还对使用插件前后的对话进行了对比，发现插件的使用可以增加特定场景的效果，但是我们用对应的Prompt也可以达到类似的效果，说明插件多是基于提示词工程开发。我们还给出了联合使用多个插件进行最新的学术论文阅读的例子。

## 基于自然语言的插件开发
在ChatGPT上开发插件主要分为两步：首先构造与插件功能相关的若干API，然后按一定逻辑将API部署到ChatGPT平台。[@九号](https://www.zhihu.com/people/li-yu-cheng-15)博主已经分享了一个高质量的[ChatGPT插件开发手册](https://zhuanlan.zhihu.com/p/629207240)。我们在此不再赘述，仅扩展介绍一下使用自然语言将多个API部署到ChatGPT平台的过程。

在ChatGPT平台部署插件需要填写`manifest`文件，其中有一个参数为`description_for_model`。开发者只需要在该参数下，用自然语言描述每个API的功能，以及使用指南，即可令GPT模型自主调用API完成任务。

以Wolfram插件为例。Wolfram对应的`description_for_model`参数为


```
Access dynamic computation and curated data from WolframAlpha and Wolfram Cloud.\nGeneral guidelines:\n- Use only getWolframAlphaResults or getWolframCloudResults endpoints.\n- Prefer getWolframAlphaResults unless Wolfram Language code should be evaluated.\n- Use getWolframAlphaResults for natural-language queries in English; translate non-English queries before sending, then respond in the original language.\n- Use getWolframCloudResults for problems solvable with Wolfram Language code.\n- Suggest only Wolfram Language for external computation.\n- Inform users if information is not from Wolfram endpoints.\n- Display image URLs with Markdown syntax: ![URL]\n- ALWAYS use this exponent notation: `6*10^14`, NEVER `6e14`."
...

```
使用GPT-4模型以及提示词"Help me explain the following prompt,response in Chinese"，可以对该参数进行翻译，得到如下结果：


```
从WolframAlpha和Wolfram Cloud获取动态计算和精选数据。

通用指南：
- 只使用getWolframAlphaResults或getWolframCloudResults端点。
- 除非需要评估Wolfram语言代码，否则优先使用getWolframAlphaResults。
- 将非英语查询翻译成英语后发送至getWolframAlphaResults进行自然语言查询；然后用原始语言回复。
- 使用getWolframCloudResults解决可用Wolfram语言代码解决的问题。
- 只建议使用Wolfram语言进行外部计算。
- 如果信息不是来自Wolfram端点，请告知用户。
- 使用Markdown语法显示图片URL：！[URL]
- 始终使用此指数表示法：`6*10^14`，永远不要使用`6e14`。
...

```
可以看到，该变量描述了如何使用`WolframAlpha`以及`Wolfram Cloud`两个API完成数学计算任务，并在任务过程中对API之间的调度关系，输入格式，边际情况用自然语言进行了说明。此外，在GPT模型的运行过程中，GPT会结合上述对插件的描述，以及当前用户的输入，自主调用API完成任务。用户也可以用提示词强制调用插件，例如`请帮我用Wolfram插件计算1+1。`

## 推荐插件一览
我们发现，联网、逻辑计算，实时信息获取和阅读网页/PDF功能是刚需，代表性插件有Wolfram（数学计算）、WebPilot（网页阅读）、edX（公开课学习）、FiscalNote（政策咨询与分析）插件。此外，我们推荐一批商业属性弱，专业化功能强的插件：Speak（专业翻译）、Prompt Perfect（提示词润色）、Diagram It（流程图绘制）、AskYourPDF（PDF阅读）、CreatiCode Scratch（少儿编程）、Chess（国际象棋游戏教练）。对上述插件进行如下评测。

### Wolframe

> Access computation, math, curated knowledge & real-time data through Wolfram|Alpha and Wolfram Language.

**TL;DR**: Wolfram插件是一个强大的计算和数据查询工具，提供精确的计算和最新的数据查询服务。这个插件可以解决各种问题，包括但不限于数学计算，物理公式求解，化学元素查询，历史事件查询，地理信息查询等。Wolfram插件的存在，解决了GPT模型在处理实时数据和复杂计算方面的限制，因为GPT模型的知识库是在训练时固定的，无法获取训练后的新数据，也无法进行复杂的数学计算。通过Wolfram插件，用户可以获取最新的数据信息，进行复杂的计算，大大提高了用户体验。

**使用示例**

```
Q: 计算 sin(x)cos(x)^2 的积分

A: [Used Wolframe]

```
{% include image.html class="polaroid" url="2023/05/plugins/wolframe_results.png" title="" %}

更多详细信息，你可以访问 [Wolfram|Alpha的结果页面](https://www.wolframalpha.com/input?i=integrate+sin%28x%29cos%28x%29%5E2+dx)。

### WebPilot

>Browse & QA webpage / generate articles, from one or more URLs


**TL;DR:** WebPilot 插件使 ChatGPT 能够访问和互动网页，以获取最新信息和帮助用户理解网页内容。

**使用案例**

```jsx
Q：请使用WebPilot插件访问 techcrunch.com，并提取最新的新闻标题和摘要。

A：[Used WebPilot]

以下是TechCrunch网站上的一些最新新闻标题和摘要：

1. "This Week in Apps: Google I/O 2023 recap; Android, apps and AI; Twitter’s new CEO" - Sarah Perez

2. "All hail the Unicorn Kingdom?" - Anna Heim

3. "Netflix reportedly plans to cut spending by $300 million this year" - Aisha Malik

4. "Elon Musk appoints new Twitter CEO, NBCU’s Linda Yaccarino" - Amanda Silberling

5. "Google makes its text-to-music AI public" - Kyle Wiggers

请注意，这些只是一些最新的新闻标题，具体的新闻摘要可能需要点击标题进入文章内部查看。

```
### edX
>Find courses and content from leading universities to expand your knowledge at any level.

**TL;DR**: edX插件是一个用于在ChatGPT对话中整合学术主题信息、建议和指导的工具，它使用edX课程库和课程内容。edX是一个在线学习平台，提供来自世界各地顶级大学和机构的课程。可以帮助用户查找一流大学任意学科的课程内容，获取更深入的学习资源和信息。

**使用示例**

```
Q：帮忙查找python爬虫课程

A:

- [Python for Data Engineering Project - IBM](https://www.edx.org/course/python-for-data-engineering-project?utm_medium=plugin&utm_source=chatgpt)
    - 这门课程的目标是让你对数据工程有深入的理解。在这门课程中，你将应用Python技能进行网页抓取和数据提取，使用API将数据转换为特定的数据类型，记录操作并准备数据加载，使用Jupyter notebooks和IBM Watson Studio进行工作。

- [Marketing Analytics for Consumer Insights - The London School of Economics and Political Science](https://www.edx.org/course/lse-marketing-analytics-for-consumer-insights-online-certificate-course?utm_medium=plugin&utm_source=chatgpt)
    - 这门课程将教你如何利用网页抓取和数据可视化来理解客户情绪，利润丰厚的细分市场和行为，以便制定有针对性的营销策略。

- [Try It: Intro to Python - edX](https://www.edx.org/course/intro-python?utm_medium=plugin&utm_source=chatgpt)

    - 这是一门免费的Python入门课程，将演示如何通过Python编程提升你的职业生涯。课程中提到了Python在网页抓取等多个项目中的应用。

```

### FiscalNote
>FiscalNote enables access to select market-leading, real-time data sets for legal, political, and regulatory information.

**TL;DR:** FiscalNote是一个提供政府事务管理，政策跟踪和立法分析的平台。它可以提供来自与美国政治和政府相关的各种来源的信息, 如法律、政治和监管信息等；帮助用户了解和跟踪政府的决策和政策，以及这些决策和政策如何影响他们的业务。它可以让ChatGPT访问FiscalNote的API，以获取有关美国政府的信息。例如，它可以获取有关美国总统的公开言论，白宫的日程安排，以及与国会相关的新闻文章。

**使用示例**

```
Q：最近有没有关于基础设施法案的新闻报道？

A:
- [Photos of the week ending May 12, 2023](https://rollcall.com/2023/05/12/photos-of-the-week-ending-may-12-2023/): D.C. Del. Eleanor Holmes Norton发表了关于最近在自行车安全方面的投资，包括"基础设施投资和就业法案"下资助的"零视力项目"的评论。

- [Length of spending caps, debt limit hike mulled as talks begin](https://rollcall.com/2023/05/10/length-of-spending-caps-debt-limit-hike-mulled-as-talks-begin/): 参议院能源和自然资源委员会主席Joe Manchin III表示，能源基础设施许可协议将在某个时候达成，但他并不坚持在本月作为债务上限法案的一部分进行。

- [No debt deal, but Biden, Hill leaders agree to meet again](https://rollcall.com/2023/05/09/no-debt-deal-but-biden-hill-leaders-agree-to-meet-again/): 众议院通过的法案包括基础设施项目许可变更和其他来自之前通过的单独能源包的条款，以及废除超过5000亿美元的清洁能源税收抵免，要求国会批准任何重大行政规则制定等。

```
### Speak
>Learn how to say anything in another language with Speak, your AI-powered language tutor.

**TL;DR**：Speak插件是一个专门用于处理与语言学习相关问题的插件。它可以帮助用户翻译和解释特定的词语或短语，解释特定的外语短语的含义和用法，或者解释在特定情境或上下文中如何用外语说或做某事，并提供例句。

**使用示例**

```
Q：如何用英语表达"落霞与孤鹜齐飞，秋水共长天一色"这句话？

A: 在英语中，"落霞与孤鹜齐飞，秋水共长天一色"可以被翻译为："The radiance of the setting sun and the lonely flight of the wild duck are set off against each other; their beauty would be enough to last forever. The vastness of the autumn sky is shared equally with the calm waters of the horizon."

这是一个诗意的翻译，强调了自然之美。以下是一些其他的翻译选项：

- "The setting sun and a lone duck flying complement each other; a sight that can last forever. The serenity of autumn's sky is reflected in the tranquil horizon."（正式 - 诗意的解释，强调自然之美）

- "Sunset and ducks; a beautiful contrast of nature. The blue of the sky blends with the blue of the water horizon."（中性 - 简单且更简洁的解释）

- "When the sun sets and ducks fly, everything becomes a beautiful painting. The sky and the water merge into one."（非正式 - 更个性化的解释，使用了画作的视觉隐喻）

```
但是，笔者发现，采用Prompt工程，也可以得到与上述相似的结果：

```
Q：如何将"落霞与孤鹜齐飞，秋水共长天一色"翻译为英语，同时保留诗句原有的意象，隐喻和美感。

A: "Sunset hues and lone egret soar as one, autumn waters blend with the endless sky."

```

### Prompt Perfect

>Type 'perfect' to craft the perfect prompt, every time.

**TL;DR:** Prompt Perfect 插件是一个用于优化 ChatGPT 对话的工具，它通过重新构造用户输入的方式，使得 ChatGPT 能更准确地理解和回应，从而提高对话的质量和效率。

**使用案例**

```jsx
Q：我想知道经济学的知识。

A：[Used Prompt Perfect]

当然，我可以为您提供一些经济学的基础知识。

经济学是一门研究人们、企业、政府如何在资源有限的情况下做出决策的社会科学。它主要分为两大领域：微观经济学和宏观经济学。

微观经济学：研究个体经济单位（如家庭、企业）的行为和决策，以及这些决策如何影响市场和价格。例如，微观经济学会研究消费者购买行为、企业如何决定价格和产量等问题。

宏观经济学：研究整个经济体的行为和决策，包括研究通货膨胀、失业、经济增长、财政政策和货币政策等问题。

经济学的目标是理解和解释我们在经济活动中观察到的现象，以及预测可能发生的变化。为了达到这个目标，经济学家会使用一系列的理论模型和数据分析方法。

这只是经济学的一些基础知识，如果您有关于特定主题的问题，我会很乐意为您解答。

```

```jsx
Q：我想知道那个东西。

A：[Used Prompt Perfect]

当然，我很乐意帮助您，但是我需要您提供更多的信息。您能详细描述一下您想了解的那个东西吗？例如，它是什么类型的物品？它的用途是什么？或者，它在哪里被使用或发现？这些信息将帮助我更准确地回答您的问题。

```

### Diagram It
> Create and edit diagrams directly in chat.

**TL;DR:** Diagram It通过创建和呈现可视化图表来帮助解释和理解复杂的概念、流程或系统。例如，当用户询问如何制造汽车，或者如何理解复杂的分布式系统时，仅仅通过文字描述可能难以清晰、准确地传达信息。Diagram It插件通过生成直观的图表，使得这些复杂的概念或流程变得易于理解。

**使用示例**
{% include image.html class="polaroid" url="2023/05/plugins/diagramitcase.png" title="diagramitcase" %}

### AskYourPDF

> Unlock the power of your PDFs!, dive into your documents, find answers, and bring information to your fingertips.

**TL;DR**: AskYourPDF可以下载并搜索用户的PDF文档，以找到问题的答案和检索相关信息，能够直接对PDF信息进行总结。

**使用示例**

```
Q: 总结一下这份财报 https://static.www.tencent.com/uploads/2022/09/01/a51f96bb0a89310955a8c19e753e2a51.PDF

A: [Used AskYourPDF]

根据这份财报的摘要（在第8页），以下是一些关键信息：

1. 国际市场游戏：Riot Games开发的《VALORANT》月活跃账户数和季度流水创新高。同时，Miniclip收购了跑酷游戏《地铁跑酷》的开发商SYBO，使Miniclip的日活跃账户数增加了3000万至7000万。
2. 网络广告：微信朋友圈推出了出框式广告，受到品牌广告商的青睐。在2022年7月，开始推出视频号信息流广告，预计这将是拓展市场份额及提升盈利能力的重要机会。
3. 金融科技：2022年第二季，新一轮新冠疫情短暂抑制了商业支付活动。商业支付金额在2022年4月放缓至低个位数同比增长，但同比增速在2022年6月恢复至百分之十几。
4. 云及其他企业服务：优化收入结构并降低成本，企业服务毛利率环比提升。TDSQL数据库收入同比增长超过30%，占2022年第二季云服务收入超过5%。

这份财报的总体概述显示，腾讯在游戏、广告、金融科技和云服务等领域都取得了一定的进展。

```
### CreatiCode Scratch

> Display Scratch programs as images and write 2D/3D programs using CreatiCode Scratch extensions

**TL;DR:** CreatiCode Scratch插件让ChatGPT能将Scratch编程伪代码转为图像，使得用户能够更直观地理解和学习编程。它解决了GPT模型在处理基于块的可视化编程语言时的挑战，提高用户在学习和理解编程时的体验。

**使用案例**

```
Q: 我想创建一个3D场景，其中包含一个旋转的立方体。
A: 这是你需要的3D场景，其中包含一个旋转的立方体的Scratch程序。

```
![Sprite](https://ccdn.creaticode.com/plugin/20230514072238995-f13c-1-253.svg)

```
Q: 请解析这个scratch程序：https://ccdn.creaticode.com/plugin/20230514072238995-f13c-1-253.svg

A: 这个Scratch程序创建了一个3D场景，并在其中添加了一个立方体。当你点击绿旗后，这个立方体会开始旋转。

具体来说，这个程序的步骤如下：

1. 当绿旗被点击时，程序开始运行。
2. 初始化一个空的3D场景。这是创建3D对象所必需的。
3. 在场景中添加一个立方体。立方体的颜色是紫色（#6F1C5CFF），大小在x、y、z三个方向上都是100，边缘半径是0（意味着边缘不是圆角），并且给这个立方体命名为"cube"。
4. 程序进入一个循环，循环次数是360次。在每次循环中，立方体都会绕z轴旋转1度，然后等待0.01秒。这样，立方体就会在3D场景中持续旋转。

这个程序是一个很好的3D动画示例，展示了如何在Scratch中创建和控制3D对象。

```

### Chess

> Unleash your inner chess master with this interactive chess experience! You can play against a novice or a grandmaster!

**TL;DR**: Chess插件是ChatGPT的一个功能扩展，它允许用户与ChatGPT进行国际象棋对局，提供了多种棋力等级供用户选择，并能够实时展示棋盘状态、记录棋局历史，甚至提供FEN（Forsyth-Edwards Notation）棋盘表示法。这个插件的目的是为了增强ChatGPT的互动性，提供更丰富的用户体验。在过去，GPT模型在处理复杂的、持久的交互任务，如棋类游戏时，可能会遇到困难，因为它们通常需要长期的记忆和复杂的规则处理能力。Chess插件解决了这个问题，使得ChatGPT能够在一个持久的、规则明确的环境中与用户进行互动。这不仅提高了用户体验，也扩展了ChatGPT的应用范围。

**使用示例**

```
Q: Chess.getLevels

A: [Used Chess]  

Chess插件提供了以下几个棋力等级供您选择：
1. Beginner（初级）: Elo等级为1000，适合棋力初级的玩家。
2. Intermediate（中级）: Elo等级为1500，适合棋力中级的玩家。
3. Advanced（高级）: Elo等级为2000，适合棋力高级的玩家。
4. Expert（专家）: Elo等级为2500，适合棋力非常强的玩家。
5. Grandmaster（大师）: Elo等级为3000，适合国际象棋大师级别的玩家。  

您可以根据自己的棋力选择相应的等级。

Q: 我选择初级, 白色棋子

A: [Used Chess]

很好，我们已经开始了一局新的棋局，您执白棋，我执黑棋。现在是您的回合，请进行您的第一步。以下是棋盘的当前状态：

```
![](https://gpt-chess.atomic14.com/board.svg?cid=a6741f1d0bc68dc85981e6d009ead1b7&m=0)

```
请使用标准代数记号（SAN）格式进行移动，例如 "e4", "Nf3" 等。

Q: a4

A: [Used Chess]

我选择了 d5。现在是您的回合。这是当前的棋盘布局：

```
![](https://gpt-chess.atomic14.com/board.svg?cid=a6741f1d0bc68dc85981e6d009ead1b7&m=2)

```
请告诉我您的下一步。

Q: 接下来你有什么建议吗?

A: 根据当前的棋局，以下是一些可能的着法建议：

1. **Nf3**：这是一种常见的开局着法，控制中心并开发您的马。
2. **c4**：英式开局的典型着法，以控制中心并为白方的其他棋子提供发展空间。
3. **e3**：这是一种保守的着法，为白方的另一马提供开发空间并加固中心。
4. **d3**：这是一种相对保守的着法，为白方的皇后提供开发空间并巩固中心。

请记住，这只是一些建议，最终决策取决于您的棋局理解和个人喜好。请告诉我您想采取的着法。

```

## 联合使用多个插件完成任务
在本节中，我们联合使用多个插件，用`WebPilot`对[VAE观点下的扩散模型](https://www.jarvis73.com/2022/08/09/Diffusion-Model-2/)这篇文章进行总结，用`Diagram It`绘制草图，并用`Wolfram`可视化扩散过程。

首先，在chatgpt的页面中，选择`new chat`，右侧选择`GPT-4`，点击下方的`plugin`按钮，在`plugin store`中下载上述三个插件，并依次勾选，如下图所示：

{% include image.html class="polaroid" url="2023/05/plugins/3plugins.png" title="" %}

然后开始对话。

```
Q: 使用WebPilot插件总结下这篇文章：

https://www.jarvis73.com/2022/08/09/Diffusion-Model-2/

A: [Used WebPilot]

这篇文章是关于扩散模型的，主要讨论了扩散模型的基本概念和应用。以下是文章的主要内容：

- 扩散模型的基本概念：扩散模型是一种描述物质在空间中扩散过程的数学模型。这种模型通常用偏微分方程来描述，其中最重要的是扩散方程。

- 扩散模型的应用：扩散模型在许多领域都有应用，包括物理学、化学、生物学和社会科学。例如，在物理学中，扩散模型可以用来描述热量的传播；在化学中，扩散模型可以用来描述化学物质的扩散过程；在生物学中，扩散模型可以用来描述生物种群的扩散过程；在社会科学中，扩散模型可以用来描述信息、创新或疾病的传播过程。

- 扩散模型的数学形式：扩散模型的基本形式是一个偏微分方程，描述了物质浓度随时间和空间的变化。这个方程的解可以用来预测物质在未来的分布情况。

- 扩散模型的解：扩散模型的解通常需要用数值方法来求解，例如有限差分法或有限元法。这些方法可以用计算机来实现，得到物质在空间中的分布情况。

- 扩散模型的局限性：虽然扩散模型在许多领域都有应用，但它也有一些局限性。例如，扩散模型假设物质的扩散是均匀的，但在实际情况中，物质的扩散可能受到许多因素的影响，如温度、压力、物质的性质等。因此，扩散模型只能作为一种理想化的模型，用来描述物质扩散的基本过程。

总的来说，这篇文章提供了一个关于扩散模型的全面介绍，包括其基本概念、应用、数学形式、解法和局限性。

Q: 使用Diagram 插件给出一个思维导图

```
{% include image.html class="polaroid" url="2023/05/plugins/union-1.png" title="" %}

```
Q: 使用Wolfram插件来可视化扩散过程

```
{% include image.html class="polaroid" url="2023/05/plugins/union-2.png" title="" %}

## 全面插件评测

### Cloudflare Radar

> Get real-time insights into Internet traffic patterns and threats as seen by Cloudflare.

**TL;DR**: CloudFlare Radar插件提供实时的互联网流量、设备使用、网络安全等相关数据，帮助用户获取到最新的网络攻击、设备使用、网络协议等数据，从而在网络安全、市场研究、产品开发等方面做出更准确的决策，解决GPT的实时性问题。

**使用示例**

```
Q: 请给出 2023 年 5 月网络攻击的趋势

A: [Used Cloudflare Radar]
在2023年5月的网络攻击趋势中，我们可以看到以下的分布：

Layer 3攻击（网络层攻击）：

* TCP攻击占比53.72%
* UDP攻击占比46.23%
* GRE攻击占比0.03%
* ICMP攻击占比0.01%

Layer 7攻击（应用层攻击）：

* WAF（Web应用防火墙）攻击占比57.15%
* DDoS（分布式拒绝服务）攻击占比33.82%
* IP Reputation（IP声誉）攻击占比6.23%
* Access Rules（访问规则）攻击占比2.61%
* Bot Management（机器人管理）攻击占比0.18%
* API Shield（API防护）攻击占比0.0016%
* Data Loss Prevention（数据丢失预防）攻击占比0%

```

### Kalendar AI

> KalendarAI sales agents generate revenue with potential customers from 200+ million companies globally.

**TL;DR**: Kalendar AI插件是一个自动化的销售助手，其目的是帮助用户自动化销售流程，通过实时聊天会话从全球200+百万公司中接触潜在客户并预约会议。这个插件解决了GPT模型在销售自动化和时间管理方面的痛点，因为传统的GPT模型并不能有效地处理这些任务。通过使用Kalendar AI插件，用户可以更有效地管理他们的销售流程，节省时间，提高效率，从而极大地提高了用户体验。

**使用示例**

```
Q: Sales help

A: [Used KalendarAI]

以下是在ChatGPT中使用销售代理的命令列表。您也可以使用以下命令获取有关命令的更多信息。

* `Sales help` — 列出所有可用的命令
* `Sales new` — 通过简单地输入您的推销，定义目标受众，我们就可以创建一个新的销售代理，用于销售服务，筹款，自由职业，招聘甚至投资，并建立定制的邮箱基础设施。
* `Sales demo` — 显示一个带有销售代理聊天会话演示链接的样本电子邮件提案。
* `Sales agents` — 列出所有销售代理并提供链接到您的仪表板
* `Sales dashboard` — 以表格格式显示您的仪表板
* `Sales stats` — 提供您的销售代理的统计数据
* `Sales settings` — 更新您的帐户设置。
* `Sales upgrade` — 升级您的帐户以获取更多代理。
* `Sales support` — 通过hello@kriya.ai联系支持或安排演示：https://calendly.com/kalendar-ai/introduction

```

### Vivian Health

> Take the first step to finding your next healthcare job.

**TL;DR**: Vivian Health插件为医疗保健专业人士提供个性化的职业推荐，帮助这些专业人士找到符合他们需求的工作，包括工作周期性、工作地点、专业领域和薪酬等方面。通过Vivian Health插件，用户可以在一个对话环境中完成复杂的工作搜索，而不需要自己在多个网站或平台上进行繁琐的搜索。插件能提供最新、最相关的工作信息，解决了GPT模型无法获取实时数据的问题。

**使用示例**

```
Q: 我想找一份旧金山的护理工作，我的专业是内科，希望每周薪资超过3000美元

A: [Used Vivian Health]

1. [FlexCare Medical Staffing](https://www.vivian.com/job/444-JOB-01142213) 提供的 Allied Health Professional - Cath Lab Technologist 职位，地点在加利福尼亚州旧金山，合同期为13周，每周工作40小时，白天工作，薪资为每周4848美元。

2. [Aureus Medical Group](https://www.vivian.com/job/867-23-2327685) 提供的 Allied Health Professional - CT Technologist 职位，地点在加利福尼亚州旧金山，合同期为16周，每周工作40小时，白天工作，薪资为每周3726美元。

```

### Wishbucket

> Unified product search across all Korean platforms and brands.

**TL;DR**: Wishbucket插件是一个集成在ChatGPT上的购物搜索工具，其目的是为用户提供一个统一的，全面的，从所有韩国购物平台获取商品信息的搜索服务。

**使用示例**

```
Q: 我想买一件红色连衣裙, 价格 30 万韩元以内

A: [Used Wishbucket]

以下是我找到的一些红色连衣裙，价格在30万韩元以内：

1. [Beetlejuice Lydia's Iconic Ruffled Red Dress](https://www.wishbucket.io/items/66616) - 品牌: 사이다 CIDER, 商店: CIDER, 价格: 50,100 KRW
2. [LINEN SHIRT DRESS / RED](https://www.wishbucket.io/items/294840) - 品牌: 피에이, 商店: 29CM, 价格: 151,200 KRW
3. [Rose Wappen Stripe Dress - Red](https://www.wishbucket.io/items/318840) - 品牌: 논로컬, 商店: 더블유컨셉, 价格: 102,000 KRW

```

### Kraftful

> Your product development coach. Ask about best practices. Get top gurus’ product thinking.

**TL;DR**: Kraftful插件用于编写清晰的产品文档，旨在提升产品开发的专业知识，通过提供来自权威来源的最佳实践，帮助用户探索行业标准的最佳实践。

**使用示例**

```
Q: 开发一个基于 ChatGPT 的应用的最佳实践是什么?

A: [Used Kraftful]

在开发基于ChatGPT的应用时，以下是一些最佳实践：

1. **理解和解决消费者面临的真实问题**：这可以是改进现有的流程，例如，edjing Mix通过将音乐混音工具放入用户的口袋中，使DJ变得更加易于接触。
2. **使用ChatGPT进行日常任务**：ChatGPT可以成为处理一些枯燥和耗时任务的助手，让你专注于更有影响力的任务。例如，你可以将你的普通验收标准给到语言模型，并要求它转换为Gherkin格式。
3. **利用ChatGPT进行用户访谈**：ChatGPT理解这些最佳实践，并能生成一个可用于你的访谈的合适的问卷。记住，ChatGPT理解上下文！所以，你可以告诉它你正在访谈的用户和你想要实现的目标，模型将创建一个与你的特定情况相关的问题列表。
4. **持续学习和理解AI产品管理**：虽然ChatGPT可以显著改进你的产品，但它不能保证产品的成功。为了实现成功，你还需要具备如何成为一个AI产品经理的知识，以及对AI和机器学习的深入理解。

以上信息来源于多篇文章，包括 [6 Genius ChatGPT Hacks for Product Managers](https://theproductmanager.com/topics/product-manager-ai/) 和 [The Impact of ChatGPT on Product Managers](https://www.productmanagementexercises.com/blog/the-impact-of-chatgpt-on-product-managers/) 等。

```
### Rentable Apartments

> Get apartment options in a city of your choice, scoped to your needs and budget.

**TL;DR**: Rentable Apartments是一个租房插件，帮助用户通过直接输入自然语言需求，搜索和查找理想的公寓。

**使用示例**

```
Q: 租一个公寓, 纽约市, 两居室, 租金不超过 3000 美元, 允许养宠物

A: [Used Rentable Apartments]

```
1. [Riverview Towers](https://www.rentable.co/fort-lee-nj/riverview-towers) - 位于 Fort Lee, NJ 的2175 Hudson Terrace。有一套两卧室、两卫生间的公寓，租金为2650美元，可于2022年10月31日起租。
![](https://images.rentable.co/112324/53333996/large.jpg)
2. [106 South Harrison Street](https://www.rentable.co/east-orange-nj/106-south-harrison-street) - 位于 East Orange, NJ 的106 S Harrison St。有一套两卧室、一卫生间的公寓，租金为2100美元，可于2022年8月15日起租。
![](https://images.rentable.co/122944/69158147/large.jpeg)


### Redfin 
>Have questions about the housing market? Find the answers to help you win in today's market.

**TL;DR:** Redfin为用户提供关于美国和加拿大的房地产市场的最新和准确信息，包括房产列表，市场趋势，房屋参观，抵押贷款利率等相关查询，主要解决GPT模型的**实时性**。此外，该插件还可以根据用户通过自然语言输入的具体需求（如价格范围，卧室数量，是否有空调等）来筛选房源，使得房源搜索更加个性化和精确。

**使用示例**

{% include image.html class="polaroid" url="2023/05/plugins/redfincase.png" title="redfincase" %}





### SEO.app 
>Your personal SEO assistant for content marketing.

**TL;DR:** SEO.app插件可以帮助用户创建和优化搜索引擎优化（SEO）的内容。这个插件解决了GPT模型在创建针对特定关键词优化的内容时可能存在的问题，提供了关键词优化，情感分析，文章长度建议等功能，帮助用户在搜索引擎排名中获得更好的位置。例如，假设你想写一篇关于“可持续时尚”的博客文章，SEO.app能够令你的内容更加被搜索引擎喜欢，以便能够吸引更多的读者。

**使用示例**


```
Q：我想写一篇关于“可持续时尚”的博客文章，请给我一些优化建议。
A：[Used SEO.app]

当你写关于“可持续时尚”的博客文章时，以下是一些优化建议：

* 关键词使用：在文章的第一段和至少一个副标题中使用主要关键词“可持续时尚”。

* 情感引导：在文章中引入一些与好奇心、贪婪和信任相关的词汇，以引发读者的情感共鸣。例如，你可以讨论可持续时尚的创新性（好奇心），强调其对环境和经济的积极影响（贪婪），并提供一些关于可持续时尚品牌的认证和质量保证（信任）。

* LSI实体：在文章中包含一些与主题相关的LSI实体，如“品牌”、“产业”、“可持续性”、“快速”、“衣物”、“生产”、“商业”等。

* 参考竞争对手的文章：查看一些与你的主题相关的竞争对手的文章，了解他们是如何处理这个主题的，以便你可以创作出更好的内容。

* 回答常见问题：在文章中回答一些常见的问题，如“什么是可持续时尚？”、“可持续时尚的5个R是什么？”、“可持续时尚真的可持续吗？”和“有哪些可持续时尚的实践？”。这可以帮助你更好地满足读者的需求。

* 目标可读性和字数：尽量保持文章的可读性等级在12级，并且字数在2202字左右。

希望这些建议能帮助你写出一篇优秀的、针对搜索引擎优化的博客文章！

```

### One Word Domains 
>Check the availability of a domain and compare prices across different registrars.


**TL;DR:** One Word Domains插件可以帮助用户检查域名的可用性，并在不同的注册商之间比较价格，使用godaddy.com提供的查询服务。

**使用示例**


```
Q: 我想注册一个chat.jarvis.cn的域名，请使用One World Domains 插件给我一些建议。

A: [Used One Word Domains]
很抱歉，"chat.jarvis.cn"这个域名已经被注册了。你可以尝试其他的域名。如果你需要更多的建议或帮助，请告诉我。

Q: 给我找一个相似的域名。

A: 以下是一些可用的相似域名：
chatjarvis.cn
chat-jarvis.cn

```

### Ambition 
>Search millions of jobs near you.

**TL;DR:** Ambition的主要目标是帮助用户找到他们附近的相关工作，解决GPT模型的实时性，以及在处理特定领域信息，如就业和招聘信息时的痛点。结合GPT，可以了解用户正在寻找什么样的工作，然后进行更匹配的搜索。

**使用示例**

{% include image.html class="polaroid" url="2023/05/plugins/ambitioncase.png" title="ambitioncase" %}


### Zillow 
>Your real estate assistant is here! Search listings, view property details, and get home with Zillow.

**TL;DR:** 与Redfin相似，提供额外的租房数据。

**使用示例**

{% include image.html class="polaroid" url="2023/05/plugins/zillowcase.png" title="zillowcase" %}

### Lexi Shopper 
>Get product recommendations from your local Amazon store.

**TL;DR:** Lexi Shopper插件可以根据用户的需求和输入，从本地的Amazon商店中推荐相应的产品，并提供为何推荐该产品的解释，并根据用户反馈修改推荐。通过联合使用GPT和Amazon API，可以解决GPT模型的实时性问题，同时可以提供交互的购物推荐。

**使用示例**

```
Q: 我想买一些GPU，地区洛杉矶，请给我一些建议。

A： [Used Lexi Shopper]

我为你找到了一款在洛杉矶地区的Amazon上评价很好的显卡：PowerColor Red Devil AMD Radeon RX 6950 XT，它拥有16GB GDDR6内存，平均评分为4.4，共有330条评论。这款显卡在游戏和图形处理方面表现出色，适合需要高性能显卡的用户。

你可以点击[这里]查看更多详情或购买。

Q: 我希望显存更大些，能运行Stable Diffusion。

A: [Used Lexi Shopper]

对不起，我找到的产品似乎与你的需求不符。让我再次尝试为你找到一款显存更大，能运行Stable Diffusion的显卡。

我为你找到了一款PowerColor Red Dragon AMD Radeon™ RX 6800 XT游戏显卡，它拥有16GB GDDR6显存，支持AMD RDNA™ 2技术和PCI Express 4.0接口，能够提供更快的图形处理速度和更高的带宽，能够运行Stable Diffusion。你可以点击[这里]查看更多详情或购买。

Q: 为什么推荐AMD不推荐NVIDIA？

A：Lexi Shopper插件的推荐是基于用户的输入和需求，以及Amazon上的商品信息和评价。在这个特定的情况下，推荐AMD Radeon RX 6800 XT显卡可能是因为它在当前的搜索结果中，基于价格、性能、用户评价等因素，综合表现最好。这并不意味着Nvidia的显卡不好，只是在这个特定的搜索和需求中，AMD的这款显卡更符合你的需求。

Q: Stable Diffusion不是深度学习吗？

A: 对不起，我可能误解了你的需求。Stable Diffusion确实是深度学习的一种方法。在这种情况下，你可能需要一款具有大量显存和强大计算能力的显卡，以便处理深度学习任务。Nvidia的显卡通常在这方面表现得更好，因为它们支持CUDA技术，这是一种广泛用于深度学习的并行计算平台和API。

让我再次尝试为你找到一款适合深度学习的显卡。

[Used Lexi Shopper]

我为你找到了一款NVIDIA Tesla V100 Volta GPU加速器，它拥有32GB显存和强大的性能，可以运行Stable Diffusion等需要大量显存和计算资源的应用程序。你可以点击这里查看更多详情或购买。请注意，这款显卡的价格较高，如果你有预算限制，可能需要考虑其他的选择。

```

### Bohita 
>Create apparel with any image you can describe! Get it delivered right to your door.

**TL;DR:** Bohita插件用于创建定制服装设计的工具，可以将用户的描述转化为实际的图形设计，从而让用户能够更方便地创建和购买个性化的服装设计。它解决了当前GPT模型无法直接生成可视化图形设计的问题。

**使用示例**

{% include image.html class="polaroid" url="2023/05/plugins/bohitacase.png" title="bohitacase" %}

评价：答非所问。

### Manorlead 
>Get a list of listings for rent or sale in cities across Canada and the US based on your search criteria.

**TL;DR:** 房地产销售插件，与Redfin，Zillow类似。果然房地产是第一生产力。

### Shimmer: Nutrition Coach 
>Track meals & gain insights for a healthier lifestyle from 1m+ restaurants & grocery stores.

**TL;DR:** 
一个营养计算工具，帮助用户跟踪和计算他们的日常饮食摄入，包括卡路里、碳水化合物、脂肪和蛋白质等营养素，解决用户在健康管理和饮食控制方面的需求。针对GPT模型在提供个性化营养建议方面的痛点，因为GPT模型本身并不具备处理和分析具体营养数据的能力。

**使用示例**

{% include image.html class="polaroid" url="2023/05/plugins/shimmercase.png" title="shimmercase" %}


对比原始GPT-4的回答可以看出差异：


```
Q: 我今天早餐吃了两片全麦面包，一杯橙汁和一个煎鸡蛋。中午在椭圆机上进行了30分钟运动，帮我计算营养摄入和卡路里。

A: 根据您提供的餐食和运动信息，我们可以大致估计您的营养摄入和卡路里消耗。

早餐：

两片全麦面包：约160卡路里，6克蛋白质，28克碳水化合物，4克脂肪
一杯橙汁（约240毫升）：约110卡路里，2克蛋白质，26克碳水化合物，0克脂肪
一个煎鸡蛋：约90卡路里，6克蛋白质，0克碳水化合物，7克脂肪
早餐总计：约360卡路里，14克蛋白质，54克碳水化合物，11克脂肪。

中午运动： 椭圆机上进行30分钟运动，可根据您的体重和运动强度估算卡路里消耗。一般来说，每30分钟消耗的卡路里在180-380之间。为了准确计算，需要知道您的体重和运动强度。

请注意，这些估算可能会因个人差异而有所不同。为了获得更准确的数据，建议使用专业的营养和健身跟踪工具。

```

可以看到，Shimmer插件和GPT-4本身的回答没有很大差异，但是Shimmer的回答更好看，更适合发社交媒体，例如小红书。

### Polarr
>Search Polarr's massive pool of user generated filters to make your photos and videos perfect.

**TL;DR**:Polarr插件是一个用于查找可以用于编辑照片或视频的滤镜的工具。这个大型滤镜库包括用于基本调整、美学色彩分级、面部修饰等的滤镜。对于任何关于照片/视频编辑的用户问题或请求，你可以将请求改写为一个简短的滤镜描述，然后使用这个插件来找到合适的滤镜。返回的结果将包括匹配滤镜的文本描述和预览链接。

**使用示例**

```
Q：我需要一个可以增强照片中蓝色的滤镜

A: 这里有几个可以增强照片中蓝色的滤镜：

- [滤镜链接](https://s.polarr.co/instructions/?v6id=7DWCWU6D) - 这是一个可以增强海洋的蓝色色调，使其更加突出的滤镜。

- [滤镜链接](https://s.polarr.co/instructions/?v6id=11ED6109FC010A80B13D9D29DD6D3343) - 这是一个可以增强天空、海洋和整体饱和度的蓝色色调的滤镜。

- [滤镜链接](https://s.polarr.co/instructions/?v6id=11EDA22CB6C79FB0ACB20D64631796D2) - 这是一个可以使图片中的蓝色更加鲜艳的滤镜。

你可以点击链接预览滤镜效果，看看哪一个最符合你的需求。

```
### Glowing
>Schedule and send daily SMS messages - reminders, inspiration, helpers and more.

**TL;DR**：Glowing插件是一个可以帮助用户安排和发送每日短信的工具。用户可以将短信发送到任何有效的手机号码，包括国家代码。短信的内容由ChatGPT根据用户提供的主题生成。


### BlockAtlas
>Search the US Census! Find data sets, ask questions, and visualize.

**TL;DR**:BlockAtlas 是一个插件，它可以让你查询和获取美国人口普查局的数据。这些数据包括各种社会经济指标，如收入、教育水平、种族构成等，这些数据可以按州、县等地理单位进行查询。

**使用示例**

```
Q：查找美国的种族构成及其占比

A:
以下是美国各州的种族构成及其占比：

- 白人人口比例：

    - 最高的州：缅因州（94.6%）
    - 最低的州：夏威夷（22.8%）
    - [查看地图](https://blockatlas.com/?variable=B02001_002E~B02001_001E&scope=0&map_title=White%20Population%20in%20the%20United%20States)
    - [查看原始数据](https://api.census.gov/data/2021/acs/acs5?get=NAME,B02001_002E,B02001_001E&for=state:*)
- 非洲裔美国人人口比例：

    - 最高的州：密西西比州（37.8%）
    - 最低的州：蒙大拿州（0.4%）
    - [查看地图](https://blockatlas.com/?variable=B02001_003E~B02001_001E&scope=0&map_title=Black%20or%20African%20American%20Population%20in%20the%20United%20States)
    - [查看原始数据](https://api.census.gov/data/2021/acs/acs5?get=NAME,B02001_003E,B02001_001E&for=state:*)
- 亚洲人口比例：

    - 最高的州：夏威夷（37.3%）
    - 最低的州：西弗吉尼亚州（0.8%）
    - [查看地图](https://blockatlas.com/?variable=B02001_005E~B02001_001E&scope=0&map_title=Asian%20Population%20in%20the%20United%20States)
    - [查看原始数据](https://api.census.gov/data/2021/acs/acs5?get=NAME,B02001_005E,B02001_001E&for=state:*)
- 美洲原住民和阿拉斯加原住民人口比例：

    - 最高的州：阿拉斯加州（14.6%）
    - 最低的州：西弗吉尼亚州（0.1%）
    - [查看地图](https://blockatlas.com/?variable=B02001_004E~B02001_001E&scope=0&map_title=American%20Indian%20and%20Alaska%20Native%20Population%20in%20the%20United%20States)
    - [查看原始数据](https://api.census.gov/data/2021/acs/acs5?get=NAME,B02001_004E,B02001_001E&for=state:*)
- 夏威夷原住民和其他太平洋岛民人口比例：

    - 最高的州：夏威夷州（10.6%）
    - 最低的州：波多黎各（0.007%）
    - [查看地图](https://blockatlas.com/?variable=B02001_006E~B02001_001E&scope=0&map_title=Native%20Hawaiian%20and%20Other%20Pacific%20Islander%20Population%20in%20the%20United%20States)
    - [查看原始数据](https://api.census.gov/data/2021/acs/acs5?get=NAME,B02001_006E,B02001_001E&for=state:*)
- 两种或两种以上种族的人口比例：
    - 最高的州：夏威夷州（24.4%）
    - 最低的州：密西西比州（2.4%）
    - [查看地图](https://blockatlas.com/?variable=B02001_008E~B02001_001E&scope=0&map_title=Population%20of%20Two%20or%20More%20Races%20in%20the%20United%20States)
    - [查看原始数据](https://api.census.gov/data/2021/acs/acs5?get=NAME,B02001_008E,B02001_001E&for=state:*)

    
请注意，这些数据是根据美国人口普查局的数据进行的估计，可能存在一定的误差。

```
### Klarna Shopping
>Search and compare prices from thousands of online shops.

**TL;DR**：Klarna Shopping插件是一个工具，可以帮助用户在购物或寻找产品时获取相关的产品建议，并根据用户反馈对推荐结果进行调整。

**使用示例**

```
Q：我想要寻找一款新的运动鞋

A:

以下是我为您找到的一些运动鞋：

- [On Running On Cloud 5 Running Shoes](https://www.klarna.com/us/shopping/pl/cl337/3202375686/Shoes/On-Running-On-Cloud-5-Running-Shoes/?utm_source=openai&ref-site=openai_plugin) - $137.96
    - Fastening: Laced
    - Insole: Textile
    - Target Group: Man, Woman, Unisex
    - Color: White
    - Upper Material: Mesh
    - Sustainability Attributes: Recycled Material

- [Hoka Women's Rincon Running Shoes]((https://www.klarna.com/us/shopping/pl/cl337/3205189895/Shoes/Hoka-Women-s-Rincon-Running-Shoes/?utm_source=openai&ref-site=openai_plugin) ) - $124.95
    - Fastening: Laced
    - Target Group: Woman
    - Color: White, Black
    - Upper Material: Mesh
    - Size (US): 11, 9.5, 12, 10.5, 5, 6, 7, 8, 9, 5.5, 6.5, 7.5, 8.5, 10

- [Women's HOKA Bondi Running Shoes](https://www.klarna.com/us/shopping/pl/cl337/3205057316/Shoes/Women-s-HOKA-Bondi-Running-Shoes/?utm_source=openai&ref-site=openai_plugin) - $164.95

    - Fastening: Laced
    - Target Group: Woman
    - Color: Purple
    - Upper Material: Mesh
    - Size (US): 11, 9.5, 10.5, 6, 7, 8, 9, 6.5, 7.5, 8.5, 10
- [Women's HOKA Clifton Running Shoes](https://www.klarna.com/us/shopping/pl/cl337/3205124672/Shoes/Women-s-HOKA-Clifton-Running-Shoes/?utm_source=openai&ref-site=openai_plugin) - $144.95

    - Fastening: Laced
    - Target Group: Woman
    - Color: Blue
    - Upper Material: Mesh
    - Size (US): 11, 9.5, 10.5, 5, 6, 7, 8, 9, 5.5, 6.5, 7.5, 8.5, 10
- [On Womens Cloudultra Trail Running Shoes](https://www.klarna.com/us/shopping/pl/cl337/3202364568/Shoes/On-Womens-Cloudultra-Trail-Running-Shoes/?utm_source=openai&ref-site=openai_plugin) - $140.00

    - Properties: Reflectors
    - Fastening: Laced
    - Target Group: Woman
    - Color: Gray, White
    - Upper Material: Synthetic, Polyester
    - Lining Material: Synthetic

总的来说，这些鞋子都有不同的特点。例如，On Running On Cloud 5 Running Shoes使用了可回收材料，而Hoka Women's Rincon Running Shoes提供了多种尺寸选择。HOKA的Bondi和Clifton系列鞋子则提供了不同的颜色选择，而On Women的Cloudultra Trail Running Shoes则具有反光属性，适合在低光照条件下运动。您对哪款鞋子更感兴趣？或者，您有没有特别的需求，比如特定的颜色、尺寸或者价格范围？

```

### Savvy Trader AI

> Realtime stock, crypto and other investment data

**TL;DR**: Savvy Trader AI是一个金融数据工具，提供实时和历史的股票、加密货币信息。它解决了GPT模型无法获取最新金融数据的问题，使用户能在聊天中直接查询金融信息，提高了使用效率。

**使用案例**

```
Q: 请告诉我微软过去一个月的股价走势。

A: 在过去的一个月里，微软（MSFT）的股价走势如下:

- 2023年4月14日，开盘价为287美元，收盘价为286.14美元。
- 2023年4月17日，开盘价为289.93美元，收盘价为288.8美元。 
- 2023年4月24日，开盘价为282.09美元，收盘价为281.77美元。 
- 2023年4月26日，开盘价为296.7美元，收盘价为295.37美元。 
- 2023年4月28日，开盘价为304.01美元，收盘价为307.26美元。 
- 2023年5月1日，开盘价为306.97美元，收盘价为305.56美元。 
- 2023年5月5日，开盘价为305.72美元，收盘价为310.65美元。 
- 2023年5月10日，开盘价为308.62美元，收盘价为312.31美元。 
- 2023年5月12日，开盘价为310.55美元，收盘价为308.97美元。 

以上数据显示，微软的股价在过去的一个月里波动较大，但总体上呈现上升趋势。如果你想了解更多关于微软股价的信息，你可以访问Savvy Trader。

```
### Likewise

> Your media and entertainment companion. Get TV, Movies, Books & Podcast Recommendations

**TL;DR:** Likewise插件是一个娱乐和媒体推荐工具，为用户提供精确和及时的媒体娱乐信息，包括电影、电视剧、书籍和播客的推荐、评分、评论、上映或播出平台等信息。它解决了当前GPT模型在获取实时和特定的媒体娱乐信息方面的痛点，并能根据用户的喜好提供个性化的推荐。

**使用案例**

```
Q: 我喜欢恐怖片，请给我推荐几部Netflix上最新的恐怖电影

A: 以下是Netflix上最新的一些恐怖电影推荐：

1. [《Phenomena》](https://likewisetv.com/movies/1073413)：这部2023年的恐怖片目前在Netflix上有播放。
2. [《Viking Wolf》](https://likewisetv.com/movies/788752)：这部2022年的恐怖惊悚片在Netflix上也可以看到。
3. [《The Pale Blue Eye》](https://likewisetv.com/movies/800815)：这部2022年的犯罪、恐怖、惊悚和神秘片也在Netflix上有播放。
4. [《Psycho》](https://likewisetv.com/movies/539)：这部1960年的经典恐怖片也在Netflix上可以观看。
5. [《Morbius》](https://likewisetv.com/movies/526896)：这部2022年的动作、恐怖、科幻片也在Netflix上有播放。
6. [《Fear Street: 1978》](https://likewisetv.com/movies/591274)：这部2021年的恐怖片在Netflix上也可以看到。
7. [《Fear Street: 1666》](https://likewisetv.com/movies/591275)：这部2021年的恐怖片也在Netflix上有播放。
8. [《Fear Street: 1994》](https://likewisetv.com/movies/591273)：这部2021年的恐怖、神秘片也在Netflix上有播放。

以上就是一些在Netflix上的恐怖电影推荐，希望你会喜欢。你还想了解其他类型的电影或电视剧吗？

```

### ChatWithPDF

> Plugin for asking questions, analyzing, and parsing through PDF documents by simply providing a PDF URL

**TL;DR:** ChatWithPDF插件使ChatGPT能够加载、解析并从PDF文档中提取信息，以回答用户基于这些文档的问题。它解决了GPT模型无法直接处理PDF文件的问题，提高了用户在处理PDF文件时的体验。

**使用案例**

```
Q: https://arxiv.org/pdf/2305.00050.pdf，请阅读这篇论文并总结其内容。
A: 这篇论文主要探讨了大型语言模型（LLMs）在因果推理任务中的表现。研究者们发现，LLMs在一些因果推理任务中表现出强大的能力，例如在因果发现和实际因果推理任务中。在因果发现任务中，LLMs能够通过阅读数据集的元数据来生成因果图。在实际因果推理任务中，LLMs能够回答自然语言的反事实查询，并识别出事件的必要和充分原因。然而，需要理解人类因素以确定事件原因的任务，例如评估特定行为的正常性，对LLMs来说仍然具有挑战性。尽管LLMs可能并未真正进行因果推理，但它们在某些因果任务中的表现强大到足以提供有用的辅助，例如在因果推理中我们通常只依赖人类的部分。

Q: 这篇论文的作者有哪些？
A: （错误）
这篇论文的作者有：John Doe, Jane Doe, Richard Roe, Jane Roe

Q: 这篇论文给出了哪些定量结果和结论？
A: 这篇论文主要研究了大型语言模型（LLMs）在因果推理任务中的表现。以下是一些定量结果和结论：

- 在因果发现任务中，LLMs在Tübingen基准测试中达到了97%的准确率，超过了之前最好的83%。这个基准测试包括了来自各种领域的一百多个因果关系，包括物理学、生物学、动物学、认知科学、流行病学和土壤科学。
- 在实际因果推理任务中，GPT-4在一个包含基础物理学、逻辑和常识的反事实查询基准测试中获得了92%的准确率，比之前报告的准确率高出20个百分点。
- 在确定任何事件的必要和充分原因的任务中，GPT-4在一个常用的15个小插图的基准测试中获得了超过86%的准确率，以及一个新的基准测试，避免了任何记忆问题。
- 然而，那些在决定事件原因时重度依赖理解人类因素的任务，例如评估特定行为的正常性，对LLMs来说仍然具有挑战性：GPT-4在我们的评估正常性的基准任务中获得了70%的准确率。

这些结果表明，尽管LLMs可能并未真正进行因果推理，但它们在某些因果任务中的表现强大到足以提供有用的辅助，例如在因果推理中我们通常只依赖人类的部分。

```

### GetYourGuide

> Find tours, excursions and other travel activities you can book on GetYourGuide

**TL;DR:** GetYourGuide插件让ChatGPT用户可以直接搜索和查看旅游活动，提供了一种便捷的旅行规划方式。它解决了GPT模型在提供具体、实时和个性化旅游建议方面的痛点，提升了使用效率和体验。

**使用案例**

```
Q: 请使用GetYourGuide插件，为我规划一趟7天冰岛旅行，需要包含自然和人文景观，并提供住宿和吃饭选项。

A: 这是一个可能的7天冰岛旅行计划，包含了自然和人文景观：

第一天：雷克雅未克

- 到达雷克雅未克，休息适应。
- 可以参观城市的主要景点，如哈尔格林姆斯教堂、雷克雅未克艺术博物馆等。

第二天：黄金圈

- 参加[黄金圈全日游](https://getyourguide.com/reykjavik-l30/grand-golden-circle-tour-t67012/)，体验壮丽的自然风光，看到壮观的Geysir地区、Gullfoss瀑布和Þingvellir国家公园。

第三天：伊萨菲厄泽

- 参加[伊萨菲厄泽：Dynjandi瀑布之旅和冰岛农场访问](https://getyourguide.com/isafjordur-l32303/isafjordur-dynjandi-waterfall-tour-icelandic-farm-visit-t454748/)，探索冰岛西部峡湾的风景和山脉，参观冰岛最美丽的瀑布之一Dynjandi，参观传统农场并享用咖啡、茶和蛋糕。

第四天：阿库雷里

- 参加[阿库雷里：3小时经典观鲸之旅](https://getyourguide.com/akureyri-l2028/3-hours-akureyri-classic-whale-watching-t69424/)，在冰岛最长的冰川峡湾中寻找座头鲸，欣赏阿库雷里和Eyjafjord的自然美景和当地野生动物。

第五天：胡萨维克

- 参加[胡萨维克：观鲸之旅](https://getyourguide.com/husavik-l87259/husavik-original-whale-watching-t85302/)，在Skjálfandi湾的船上探索壮观的风景，观察鲸鱼、海豚和海鸟在其自然栖息地中的情况，了解为什么胡萨维克是冰岛的观鲸之都。

第六天：斯卡夫塔费特

- 参加[斯卡夫塔费特：冰川奇观冰川徒步旅行](https://getyourguide.com/vatnajokull-national-park-l2246/glacier-wonders-trip-t30308/)，在未受破坏的冰岛荒野中徒步旅行，前往Falljökull冰川。穿上冰川装备，向上走到冰川斜坡，欣赏美景，看到冰川块落入宁静的海洋水域。

第七天：雷克雅未克

- 参加[雷克雅未克：观鲸和海洋生物游船之旅](https://getyourguide.com/reykjavik-l30/reykjavik-scenic-whale-watching-tour-t248622/)，在Faxaflói湾的船上寻找鲸鱼，欣赏令人惊叹的风景，寻找各种当地野生动物，包括鲸鱼、海豚、鼠海豚等。

关于住宿和餐饮，我建议您查看在线旅行网站，如Booking.com或Airbnb，以找到适合您的住宿。冰岛的餐饮选择丰富，包括当地的海鲜、羊肉和冰岛酸奶等特色美食。在雷克雅未克，您可以找到各种餐厅，从高级餐厅到快餐店，都有。

请注意，这些活动的价格和可用性可能会有所变动，建议提前预订。

```
### Open Trivia

> Get trivia questions from various categories and difficulty levels

**TL;DR:** Open Trivia插件让ChatGPT可以提供和管理各种知识问答题目，增加了对话的趣味性和教育性。它解决了GPT模型在生成特定格式和主题的知识问答题目上的挑战，并通过避免问题重复，提高了用户体验。

**使用案例**

```
Q: 请给我一个中等难度的关于计算机操作系统的问题。

A: 当然，这是一个关于计算机科学的中等难度问题 不可能格式化一个写保护的DVD-R硬盘。这个说法是真的吗？ 

Q: 是的。 

A: 你的回答是正确的！一个写保护的DVD-R硬盘确实不能被格式化。写保护是一种安全功能，可以防止数据被意外删除或修改。

```

### Weather Report Data

>Current weather data for cities and airports using METAR aviation feeds.

**TL;DR:** Weather Report Data 插件为 ChatGPT 提供实时气象数据，解决了 GPT 无法获取实时信息的限制，提升了用户获取气象信息的便利性和效率。

**使用案例**

```jsx
Q：请告诉我纽约肯尼迪机场的实时气象情况。

A：[Used Weather Report Data]

纽约肯尼迪机场（ICAO代码：KJFK）的实时气象情况如下：

风向：360度
风速：10节
能见度：10海里
天空状况：晴朗
气温：21摄氏度
露点温度：3摄氏度
气压：30.06英寸汞柱
这些信息都是根据最新的METAR气象报告提供的。

```

### Turo

>Search for the perfect Turo vehicle for your next trip.

**TL;DR:** Turo 插件在 ChatGPT 中提供了车辆租赁服务，用户可以直接输入需求，系统会自动搜索并推荐车辆。这解决了用户在多平台间切换和手动搜索的问题，提高了使用效率和体验。

**使用案例**

```jsx
Q：我需要在洛杉矶从5月20日到5月25日租一辆车。

A：[Used Turo]

以下是我为您找到的在洛杉矶从2023年5月20日到2023年5月25日的租车选项：

2017 Ford Mustang - 每日价格$45（不包括税费和费用），距离您4.97英里，车主评分5星。

2020 Chevrolet Equinox - 每日价格$45（不包括税费和费用），距离您1.30英里，车主评分5星。

2021 Infiniti QX50 - 每日价格$56（不包括税费和费用），距离您11.21英里，车主评分5星。

您可以点击车型链接查看更多详情并进行预订。如果您想查看更多选项，可以点击这里查看所有在洛杉矶的可用车辆。

```

### DEV Community

> Plugin for recommending articles or users from DEV Community.


**TL;DR:** DEV Community 插件可以帮助用户在 DEV Community 网站上搜索和推荐相关的编程和技术文章。这个插件的目的是为了方便用户获取到最新的编程知识和技术趋势，解决了用户需要在大量信息中寻找相关文章的问题。。

**使用案例**
注意，搜索文章准确度不高。例如文章 1 中的 Symgony 其实是一个 PHP 的框架，而非大模型的文章。
```jsx

Q：请推荐关于大模型的5篇文章。

A：[Used DEV Community]

以下是关于大模型的一些文章推荐：

Symfony internals and security by jmau111⭐⭐⭐

AI Everything. A Peak Into the Google Keynote at Google I/O 2023 by LemonBoy

AISTA versus AINIRO by Thomas Hansen

Python OOPS by atchukolanaresh

Smart Cities? Smart Villages? Can we have them both? Is there a quick way to this? by Stephen Gitahi

这些文章涵盖了大模型在不同领域的应用，包括AI、Python编程、智能城市等，希望对你有所帮助。

```

### ndricks Sports

> Get information about pro teams (NHL, NBA, NFL, MLB) teams by calling the ndricks Software Sports API.


**TL;DR:** ndricks Sports 插件为 ChatGPT 提供了获取最新美国专业体育队伍信息的功能，包括 ESPN 和 CBS Sports 的新闻。这个插件解决了 ChatGPT 知识库截止日期限制的问题，使其能提供最新的体育新闻，从而提高了用户体验，满足了用户对实时体育新闻的需求。

**使用案例**

注意，结果其实不太对

```jsx
Q：请告诉我关于洛杉矶湖人队的最新新闻。

A：[Used ndricks Sports]

以下是关于洛杉矶湖人队的最新新闻：

1. ESPN报道，湖人队在昨晚的比赛中以112比108击败了波士顿凯尔特人队。这场胜利主要归功于球队的主力球员，他们在比赛中发挥出色，特别是安东尼·戴维斯，他在比赛中得到了30分和10个篮板。

2. CBS Sports报道，湖人队的球员勒布朗·詹姆斯在比赛中受伤，可能需要休息一段时间。湖人队的教练表示，他们将密切关注詹姆斯的恢复情况，并希望他能尽快回到球场。

3. 此外，湖人队正在积极寻找新的球员来增强球队的实力。他们正在与多位自由球员进行谈判，希望能在季后赛开始前找到合适的人选。

以上就是关于洛杉矶湖人队的最新新闻，如果你有其他问题，欢迎随时向我提问。

```

### Speechki

> The easiest way to convert texts to ready-to-use audio — download link, audio player page, or embed!

**TL;DR:** Speechki 插件是 ChatGPT 的语音转文字工具，它可以将语音信息转化为文字，目的是为了提供更方便的交互方式，解决在需要手动输入信息的场景中的效率问题。。


### Crafty Clues

> Guess the words that the AI craftily clues for you. Add restrictions to make the game more interesting!

**TL;DR:** Crafty Clues 是一个词汇猜测游戏插件，旨在提高用户与 ChatGPT 的互动性和娱乐性。它通过提供有趣的词汇挑战，增强了学习新词汇和语言技能的乐趣。

**使用案例**

```jsx
Q：请开始一轮 Crafty Clues 游戏。

A：[Used Crafty Clues]

好的，让我们开始一轮 Crafty Clues 游戏。

我将给出一个线索，你需要猜测我在描述什么词汇。请注意，我不能使用与目标词汇直接相关的词汇。你只有一次猜测的机会。

线索：这是一种结构，通常用于在空中移动或稳定身体，可以在自然界和人造物品中找到。

现在，你可以尝试猜测我在描述什么词汇。

Q：翅膀。

A：恭喜你，你猜对了！我描述的词汇确实是 "Wings"（翅膀）。这是一种结构，通常用于在空中移动或稳定身体，可以在自然界和人造物品中找到。我不能使用与这个词汇直接相关的词，如 "Fly"（飞）、"Feathers"（羽毛）、"Airplane"（飞机）、"Bird"（鸟）和 "Angel"（天使）。

这就是 Crafty Clues 游戏的一部分，它可以帮助你在猜测和理解词汇的过程中提高你的语言学习能力。希望你喜欢这个游戏！

```

### Yabble

> Your ultimate AI research assistant; create surveys, specify audiences, collect data & analyze.

**TL;DR:** Yabble 插件在 ChatGPT 上提供自动化市场调查服务，简化了创建、运行和分析调查的过程，节省了研究者的时间和金钱。它解决了手动处理大量数据和生成有价值洞察的问题，提高了用户在进行市场研究时的体验。

**使用案例**

```jsx
Q：请生成一个关于 ChatGPT 竞品分析的调研报告。

A：[Used Yabble]

我们已经为您的ChatGPT竞品分析调查生成了以下问题：

1. 你过去使用过哪些聊天机器人平台，你的体验如何？
2. 在选择聊天机器人平台时，你认为哪些功能最重要？
3. 对于现有的聊天机器人平台，你希望看到哪些改进？
4. 你有多可能向他人推荐特定的聊天机器人平台，为什么？

接下来，我们需要设定调查的目标人群。请提供一些关于目标人群的信息，例如性别、年龄、地点、婚姻状况、就业状况、薪资、是否有孩子等。请注意保存您的调查代码（TKL2-E6UI），以便在后续步骤中使用。

```

### Algorithma

> Shape your virtual life with in this immersive life simulator game to begin Type /start to begin.

**TL;DR:** Algorithma 插件是一款生活模拟游戏，它允许用户通过输入命令来模拟和控制虚拟角色的生活。其目的是为用户提供一种新颖、有趣的娱乐方式，同时也可以帮助用户在模拟环境中探索和理解现实生活中可能遇到的各种情况和问题。

**使用案例**

注意：游戏到后面陷入了循环

{% include image.html class="polaroid" url="2023/05/plugins/Algorithma1.png" title="" %}

{% include image.html class="polaroid" url="2023/05/plugins/Algorithma2.png" title="" %}

{% include image.html class="polaroid" url="2023/05/plugins/Algorithma3.png" title="" %}

### KeyMate.AI Search

> Search the web by using a Custom Search Engine with KeyMate.AI, your AI-powered web search engine..

**TL;DR:** KeyMate.AI Search 插件使 ChatGPT 能够搜索互联网以获取最新信息，解决了知识过时或不足的问题。

**使用案例**

```jsx
Q：Which country is the world cup champion in 2022

A：[Used KeyMate.AI Search]

The 2022 World Cup champion is Argentina. They won the tournament held in Qatar. source

```



### Yay! Forms

> Allows you to create AI-Powered Forms, Surveys, Quizzes, or Questionnaires on Yay! Forms.

**TL;DR:** Yay! Forms 插件能帮助用户在 Yay! Forms 平台上自动创建和导入表单，简化了表单创建过程，节省了用户的时间和精力。

### AITickerChat

**TL;DR**: AITickerChat 插件是一个专门用于搜索和检索美国证券交易委员会（SEC）文件和财报电话会议记录的工具。它的目的是为用户提供最新、最准确的股票市场信息，尤其是那些可能隐藏在 SEC 文件或财报电话会议记录中的信息。这个插件解决了 GPT 模型在处理大量、复杂的金融文档时可能遇到的困难，提高了用户在获取股票市场信息时的效率和准确性。

**使用案例**

1. 用户想要了解某公司最近的财务状况，可以通过 AITickerChat 插件搜索该公司的最新 10-K 或 10-Q 报告。
2. 用户对某公司的未来发展方向感兴趣，可以通过搜索财报电话会议记录，获取公司高层对未来的看法和计划。
3. 用户想要比较两家公司的财务状况，可以通过 AITickerChat 插件同时搜索两家公司的 SEC 文件，进行对比分析


```
Q: 
查一下亚马逊的的财务状况

A:
根据亚马逊最近的 10-Q 报告，以下是一些关于其财务状况的关键信息：

亚马逊的净产品销售从 2022 年的 56,455 百万美元增长到 2023 年的 56,981 百万美元。净服务销售从 2022 年的 59,989 百万美元增长到 2023 年的 70,377 百万美元。总净销售从 2022 年的 116,444 百万美元增长到 2023 年的 127,358 百万美元。

操作费用包括销售成本、履行、技术和内容、销售和营销、一般和行政以及其他运营费用（收入），总计从 2022 年的 112,775 百万美元增长到 2023 年的 122,584 百万美元。

操作收入从 2022 年的 3,669 百万美元增长到 2023 年的 4,774 百万美元。

亚马逊的 AWS 销售在 2023 年第一季度相比上一年同期增长了 16%，这主要反映了客户使用量的增加，部分抵消了由长期客户合同驱动的价格变动。

亚马逊在 2023 年第一季度的股东权益为 154,526 百万美元，高于 2022 年的 146,043 百万美元。

以上信息显示，亚马逊在 2023 年的销售和操作收入都有所增长，但同时其操作费用也有所增加。总的来说，亚马逊的财务状况在 2023 年相比 2022 年有所改善。

更多详细信息，您可以查看完整的 10-Q 报告。

请注意，投资决策应基于全面的研究和理解，而不仅仅是基于一份财务报告。如果您需要进一步的投资建议，建议咨询专业的财务顾问。

```

### BizToc

**TL;DR:** BizToc插件是一个专门用于查询和获取商业新闻的工具，它的目的是为用户提供最新、最相关的商业信息。

**使用案例**：

1. 用户想了解最新的苹果公司新闻，可以使用BizToc插件查询"Apple"，插件会返回所有包含"Apple"的最新商业新闻。
2. 用户想了解特定行业的最新动态，如金融行业，可以使用BizToc插件查询"Finance"，插件会返回所有与金融相关的最新商业新闻。


```
Q: 
查看苹果公司的商业新闻

A:
以下是有关苹果公司的最新商业新闻：

Apple发布新款iPad Pro - Apple在其春季产品发布会上推出了新款iPad Pro，该设备配备了更强大的M1芯片，以及更先进的显示技术。这款新iPad Pro的价格从799美元起，预计将在5月下旬开始发货。

Apple的隐私政策引发广告商的抗议 - Apple最近的隐私政策更新引发了广告商的抗议。这项政策要求应用开发者在收集用户数据之前获取用户的明确同意，这对许多依赖广告收入的应用开发者构成了挑战。

Apple与Epic Games的法律纠纷继续 - Apple与Epic Games之间的法律纠纷仍在继续。Epic Games指控Apple的App Store政策构成反竞争行为，而Apple则反驳说其政策是为了保护用户的安全和隐私。

Apple的Q2财报超出预期 - Apple的第二季度财报超出了分析师的预期。公司的营收和利润均有所增长，尤其是其服务业务的表现尤为出色。

请问你对哪篇新闻感兴趣，想要了解更多的信息呢？


```
### Change

**TL;DR**: Change为用户提供有影响力的非营利组织信息，帮助他们在自己的社区和更广泛的范围内找到值得支持的非营利组织，使用户能够更好地了解和参与公益活动。

**使用案例**

1. 用户可以询问特定类别的非营利组织，例如：“我想找一些环保类的非营利组织。”
2. 用户可以询问特定地区的非营利组织，例如：“我想找一些在加利福尼亚州的非营利组织。”
3. 用户可以询问特定非营利组织的详细信息，例如：“我想了解更多关于 'One Tree Planted' 这个非营利组织的信息。”


```
Q: 
我想找一些环保类的非营利组织。

A:
以下是一些环保类的非营利组织：

charity: water

使命：charity: water 是一个非营利组织，致力于为全球的人们提供干净和安全的水。
EIN：22-3936753
KABOOM!

使命：永久结束游乐设施的不公平。
EIN：52-1970904
Bye Bye Plastic

使命：我们是一个富有颠覆性的非营利组织，致力于消除音乐和活动行业的一次性塑料。我们创建了各种项目，激活行业的每一个利益相关者，包括艺术家、观众和活动组织者，使他们意识到我们的一次性行为，并积极地为他们提供教育和替代方案，以做出可持续的决策。
EIN：87-1256019
你可以调整这些参数以获得更准确的推荐，也可以询问有关任何非营利组织的更多详细信息。


```

### Coupert

**TL;DR**: Coupert为用户提供实时的优惠券信息和商家的现金返还信息，帮助用户在购物时节省金钱。

**使用案例**

1. 用户正在寻找某个特定商店的优惠券。例如，用户可以问：“我可以在哪里找到Amazon的优惠券？”ChatGPT可以使用Coupert插件，输入Amazon的域名，然后返回包含Amazon优惠券信息的回复。
2. 用户正在寻找某个特定产品的优惠券。例如，用户可以问：“我在购买Nike运动鞋时有什么优惠？”ChatGPT可以使用Coupert插件，输入Nike的域名，然后返回包含Nike优惠券信息的回复。
3. 用户想知道某个商店是否有现金返还活动。例如，用户可以问：“我在购物时可以在哪里获得现金返还？”ChatGPT可以使用Coupert插件，输入商店的域名，然后返回包含现金返还信息的回复。


```
Q:
我在购买Uniqlo时有什么优惠？

A:
Uniqlo US在其官方网站上提供了现金返还活动，返还比例在6.72%到6.82%之间。但是，我没有找到任何可用的优惠券。这可能会随着时间的推移而改变，所以建议您定期查看Uniqlo的官方网站或者其他优惠券网站以获取最新的优惠信息。您可以点击这里访问Uniqlo US的官方网站。

```
### Giftwrap

**TL;DR**: Giftwrap插件为用户提供个性化的礼物推荐服务。这个插件解决了GPT模型在提供具体、个性化的礼物建议方面的痛点。在过去，GPT模型可能会提供一些通用的礼物建议，但是缺乏针对特定场合、关系或价格范围的个性化推荐。Giftwrap插件通过考虑这些因素，可以提供更加精准和个性化的礼物建议，从而极大地提高了用户体验。

**使用案例**

1. 用户寻找特定场合的礼物：例如，用户可以询问“我需要一些母亲节礼物的建议”，然后Giftwrap插件会提供一些适合母亲节的礼物建议。
2. 用户寻找特定关系的礼物：例如，用户可以询问“我需要一些送给我男朋友的生日礼物的建议”，然后Giftwrap插件会提供一些适合男朋友的生日礼物建议。
3. 用户寻找特定价格范围的礼物：例如，用户可以询问“我需要一些价格在50到100美元之间的礼物建议”，然后Giftwrap插件会提供一些在这个价格范围内的礼物建议。
4. 用户寻找特定标签的礼物：例如，用户可以询问“我需要一些带有‘环保’标签的礼物建议”，然后Giftwrap插件会提供一些带有“环保”标签的礼物建议。


```
Q:
我需要一些送给我女朋友的生日礼物的建议

A:
这里有一些我为你的女朋友的生日挑选的礼物建议：

过去现在未来耳环：这款耳环由三个环组成，分别代表过去、现在和未来，是一个优雅的饰品，也是一个时刻提醒我们活在当下的象征。价格为46美元。

DIY雨滴蛋糕 - 分子美食套装：这是一个可以在家制作雨滴蛋糕的套装，雨滴蛋糕是一种美观又美味的甜点，可以让你的女朋友享受制作和品尝的乐趣。价格为38美元。

婚礼纪念品库：这是一个可以整理和保存婚礼纪念品的系统，包括照片、邀请函和其他小物件，可以让你们的美好回忆得到妥善保存。价格为107美元。

开花棒棒糖：这是一种特别的棒棒糖，棒棒糖的棒子里嵌入了种子，吃完棒棒糖后，可以将棒子种入土中，种出香草或花朵。价格为20美元。

善良的小枝碗：这是一个手工制作的陶瓷碗，碗的表面印有真实的玫瑰、百里香和满天星的印记，是一个永恒的春天的象征。价格为100美元。

手工雕刻的心形服务勺：这是一个由肯尼亚的手工艺人制作的木质勺子，既美观又实用，可以用来舀茶叶、咖啡或调拌酱汁。价格为20美元。

```

### Hauling Buddies

**TL;DR**: Hauling Buddies 插件是一个专门为用户提供动物运输服务信息的工具，它可以帮助用户找到附近的可靠动物运输商，阅读他们的评价，获取联系方式，以及查询他们是否符合必要的法规，如 USDA 认证和 FMCSA 数据库。这个插件的存在是为了解决 GPT 模型在特定领域信息检索方面的限制，提供了更专业、更准确的动物运输服务信息。

**使用案例**

1. 用户需要为他的宠物找到一个可靠的运输服务，他可以使用 Hauling Buddies 插件搜索附近的动物运输商，并阅读他们的评价。
2. 用户想要确认一个动物运输商是否拥有 USDA 认证，他可以通过这个插件搜索 USDA 认证数据库。
3. 用户想要查看一个动物运输商是否在 FMCSA 数据库中，他可以通过这个插件搜索 FMCSA 数据库。


```
Q:
查找洛杉矶附近的动物运输商

A:
这是我找到的一些洛杉矶附近的动物运输商：

Paws Door 2 Door Express

地址：Inglewood, California
电话：+1 310-764-1703
服务：家禽，小动物
描述：这是一个家族经营的业务，他们以爱心和关怀运输宠物，就像与他们的家庭成员一起旅行。他们有超过6年的宠物运输和照顾的经验，服务全国范围。
Pets4jets USA LLC

地址：Fullerton, California
电话：+1 657-346-6135
服务：小动物
描述：Pets 4 Jets 提供宠物运输服务，包括国内和国际运输，他们承诺以最大的安全和关怀处理您的毛茸茸的家庭成员。他们拥有 USDA 认证。

```

### PortfolioPilot

**TL;DR**: PortfolioPilot插件是一个个性化的AI驱动投资指导工具，为用户提供全面的投资组合评估，个性化的投资建议，以及获取关于ETFs，股票，加密货币，债券和共同基金等各种证券的最新信息。

使用案例：

1. 用户可以通过该插件获取他们投资组合的详细评估，包括预期收益，风险调整收益，多样化，风险，波动性，以及通胀风险和信用风险等下行保护因素。
2. 用户可以获取具体的，可操作的建议，描述如何改进他们的投资组合，包括在哪里投资额外的资金。
3. 用户可以获取关于任何公开公司的广泛的最新信息，包括新闻，预期收益，风险，财务信息，估值，基金曝光，相关证券等。
4. 用户可以使用ETF和股票搜索功能，根据一系列过滤器找到优秀的基金和股票。

```
Q: 给我一个投资组合的案例

A:
在这个具体的使用案例中，用户有一个投资组合，包括：

Apple (AAPL) 股票，价值 5000 美元
Google (GOOG) 股票，价值 3000 美元
比特币 (BTC-USD)，价值 2000 美元
以太坊 (ETH-USD)，价值 1000 美元
现金 (CUR:USD)，价值 1000 美元
使用 PortfolioPilot 插件，我们可以获取以下投资组合的详细信息：

Apple (AAPL) 占投资组合的 41.67%，预期收益率为 8.40%，预期风险为 30.34%，市场Beta值为 0.96。
Google (GOOG) 占投资组合的 25.00%，预期收益率为 10.09%，预期风险为 36.14%，市场Beta值为 0.86。
比特币 (BTC-USD) 占投资组合的 16.67%，预期收益率为 16.40%，预期风险为 60.07%，市场Beta值为 0.48。
以太坊 (ETH-USD) 占投资组合的 8.33%，预期收益率为 17.16%，预期风险为 74.19%，市场Beta值为 0.60。
现金 (CUR:USD) 占投资组合的 8.33%，预期收益率为 0.25%，预期风险为 0.00%，市场Beta值为 0.00。
投资组合的总价值为 11999.99 美元，预期总收益率为 10.21%。

```
### Tabelog

**TL;DR**: Tabelog插件提供更精确和实时的餐厅预订信息。

**使用案例**


```
Q:
帮我随便找一家餐厅

A:
我为您找到了一些寿司餐厅的信息：

蔵六雄山 - 位于六本木，总评分为3.77，可预订的时间有2023年5月15日的19:00和20:30。
蔵六雄山

北浜鮨やまの - 位于北浜，总评分为3.71，可预订的时间有2023年5月15日的18:00和19:00。
北浜鮨やまの

鮨 昇 - 位于東銀座，总评分为3.71，可预订的时间有2023年5月15日的18:30、19:00和19:30。

```
### Video Insights

**TL;DR**: Video Insights 插件是一个专门用于提取视频内容的工具，它可以获取各种视频提供商（如 YouTube 或 Daily Motion）的视频摘要、元数据和完整字幕，能够解决 GPT 模型无法直接处理视频内容的问题。通过 Video Insights 插件，用户可以直接在聊天中获取视频的关键信息，无需自己观看整个视频，从而大大提高了用户体验。

**使用案例**

1. 用户想要了解一个 YouTube 视频的内容，但没有时间或者不方便观看，可以使用 Video Insights 插件获取视频的完整字幕和摘要。
2. 用户在浏览网页时发现一个感兴趣的视频，但视频的提供商不是 YouTube 或 Daily Motion，可以使用 Video Insights 插件获取该视频的信息。

```
Q:
请任意帮我找到一个视频，并总结其内容

A:
我找到了一部视频，它是 Taylor Swift 的音乐视频 "Look What You Made Me Do"。这部视频于2017年8月28日发布，时长为4分16秒。这是一部非常受欢迎的音乐视频，已经获得了超过13亿的观看次数，以及超过1200万的点赞。视频的描述中包含了 Taylor Swift 的社交媒体链接和她的官方商店链接。

```
### Wahi

**TL;DR**: Wahi插件提供房地产列表搜索服务，包括出售、出租或租赁的公寓、房屋、公寓和公寓。

**使用案例**

```
Q:
找一个在多伦多找到一套售价在50万到100万加元的房子

A:
我为您找到了一套位于多伦多的公寓，售价为999,000加元。以下是一些详细信息：

地址：485 Rosewell Ave, Unit 301, Toronto, Ontario, M4R 2J2
房源类型：公寓
卧室数量：2
浴室数量：2
停车位数量：1
年度税额：3279.73加元
房源面积：900-999平方英尺
最近的高评分学校评分：9.4
房源上市日期：2023-05-08
更多详情和图片，您可以访问以下链接：https://wahi.com/ca/en/real-estate/on/gta/toronto/lytton-park/485-rosewell-ave-301-toronto-m4r2j2-ontario

```

## 作者列表


[@捡到一束光](https://www.zhihu.com/people/feng-hao-zhe-66)[@Serendipity](https://www.zhihu.com/people/zhu-wang-xiao-miao-o)[@Jarvis73](https://www.zhihu.com/people/lin-xi-1-1)[@ZeroWang](https://www.zhihu.com/people/zerowangzy)[@周杰辉](https://www.zhihu.com/people/zhou-jie-hui-11)[@春风十里](https://www.zhihu.com/people/weng-luo-xuan)

**注：本文由上述作者联合创作，排名不分先后。**
