---
layout: page
title: About
permalink: /about/
icon: heart
type: page
---

* content
{:toc}

## 关于我

以后再写吧~

## 联系我

* GitHub：[Jarvis73](https://github.com/Jarvis73)
* Email：zjw.cs@zju.edu.cn
* [知乎](https://www.zhihu.com/people/lin-xi-1-1)

## Changes Log

* **2019-07-28**
  * 简化了图片容器, 通过 `{% include image.html class="polaroid" url="2020-08/tSNE-5.png" title="t-viSNE 系统概览" %}` 引入图片(注意替换 url 和 title).
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
