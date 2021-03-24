---
layout: page
title: About
permalink: /about/
icon: heart
type: page
---

* content
{:toc}


## About Me

<div style="width:150px; height:auto; float:left; display:inline">
<img src="/images/misc/me.png" class="img-circle" >
</div>
<div style="width: auto; height:auto; float:left; display:inline; padding-left: 40px">
<div style="font-size: 25px; padding-bottom: 10px"><strong>张建伟 (Zhang Jian-Wei)</strong><br /></div>
浙江大学计算机科学与技术学院 博士生 ( 2018- )<br />
研究方向: 深度学习, 图像分割, 少样本学习, 医学影像处理<br />
</div>
<div style="clear:both"></div> 

## Contact Me

* GitHub：[Jarvis73](https://github.com/Jarvis73)
* Email：<a href = "mailto:zjw.cs@zju.edu.cn">zjw.cs@zju.edu.cn</a>
* [知乎](https://www.zhihu.com/people/lin-xi-1-1)

## Changes Log

* **2021-03-24**
  * 为目录增加可折叠按钮

* **2020-11-03**
  * 增加了卡片模板, 通过 `{% raw %}{% include card.html type="info" title="" content="" %}{% endraw %}` 来使用. 其中参数 `type` 的选择有 [lemma, primary, danger, success, warning, info]. 参数 `title` 是可选的. 此模板可以用于编辑一些特殊的信息, 忽略参数 `type` 以获得普通模板, 可作为数学定理, 引理等环境.

* **2020-10-30**
  * 引入了 zui.js 库, 增加了图像浮层, Collection 页面重新设计后改用了html.
  * 首页右边栏的 Category 和 Wiki 卡片修改了外观 (zui.js).
  * 重新设计了代码块, 加入了行号, 可以显示代码类型, 加入了复制按钮

* **2020-10-26**
  * 首页的每个 Post 设计为卡片, 更容易区分不同的 Posts. 
  * 缩短了 "Recent Posts" 中的标题(通过js正则匹配去掉了标题括号中的英文), 每个标题只占一行.
  * 代码块增加了行号显示, 换了代码高亮方式, 调整了代码块背景色.

* **2019-07-28**
  * 简化了图片容器, 通过 `{% raw %}{% include image.html class="polaroid" url="2020-08/tSNE-5.png" title="t-viSNE 系统概览" %}{% endraw %}` 引入图片(注意替换 url 和 title).
  * Wiki 的类别加入了 `_config.yml`, 从而可以自动筛选
  * 修复了首页博文数量计算错误的bug(由于wiki文章被隐藏导致的)
  * 修改为使用kramdown
  * 使用[^1]表示脚注时超链接点击时可以在页内跳转. 自定义链接仍然可以打开新页

* **2018-09-22**
  * 首页摘要修改了颜色, 增加了悬浮时改变透明度的效果
  * 增加了图片的显示容器, 包括摘要图片的容器(在 `_index.scss` 中)和文章图片的容器(在 `_post.scss` 中), 其中文章的图片容器中包含下部的标题栏样式.
  * 设置页面的透明度

* **2018-09-21** 
  * 删除 Tag 页面以及所有 Tag 标签
  * 增加 Wiki 页面和 Wiki 的首页侧边栏
  * 在 Post 中增加 meta 变量, 用于区分常规 post 和 wiki post. `meta: Post` 被设置时加入常规博客, `meta: Wiki_{Class}` 被设置时加入 Wiki, 其中 `{Class}` 为对应的类别.
  * 对 Categories 页面的类别进行排序

* **2018-01-31** 
  * 添加了基于 github issues 的评论系统, 使用了 [Shiquan Sun](https://github.com/imsun/gitment) 的 **gitment** 项目.
  * 首页摘要中增加图片显示功能, 在 post 中的开头使用 `figure: /images/xxx.png` 即可, 路径格式与 post 中插入图片的路径格式相同.

## Acknowledgement
<p class="power">
    <span>
        Site powered by <a href="https://jekyllrb.com/">Jekyll</a> & <a href="https://pages.github.com/">Github Pages</a>.
    </span>
    <span>
        Theme designed by <a href="https://github.com/Gaohaoyang">HyG</a>.
    </span>
</p>
