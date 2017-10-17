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
* email：jarviszhang233@gmail.com
* [Weibo](http://weibo.com/5336691469)
* [知乎](https://www.zhihu.com/people/lin-xi-1-1)
* [Facebook](https://www.facebook.com)
* [Twitter](https://twitter.com/z2014jw)
* [豆瓣](https://www.douban.com)


### Update Log



**以下为博客主题原作者的更新日志**
---

*2017.2.28*

- `[^]` 修复目录滚动 bug [#22](https://github.com/Gaohaoyang/gaohaoyang.github.io/issues/22), [#48](https://github.com/Gaohaoyang/gaohaoyang.github.io/issues/48)

*2016.6.20*

* `[+]` 在文章页中添加上一篇和下一篇文章链接。
* `[^]` 修改 font-family 顺序，避免微软雅黑将单引号解析为全角。
* `[^]` 修复标签云算法中被除数为零的 bug。[#26](https://github.com/Gaohaoyang/gaohaoyang.github.io/issues/26), [#28](https://github.com/Gaohaoyang/gaohaoyang.github.io/issues/28), [#30](https://github.com/Gaohaoyang/gaohaoyang.github.io/issues/30)

*2016.5.11 v2.0.1*

* `[^]` 优化代码，将页面中的大段评论相关代码抽离出来，放入`comments.html`
* `[+]` 添加百度统计和Google分析代码，在`_config.yml`中配置相关参数即可
* `[+]` 更新文档，添加博客主题使用方法，便于上手
* `[+]` 添加了`favicon.ico`
* `[^]` 修复 bug，目录太长时，滚动到最底部时隐藏到footer下面。修复后长目录在滚动到底部时使用`position:absolute`
* `[^]` 修改目录区的滚动条样式（仅针对`webkit`内核浏览器）
* `[^]` 修改 demo 页中 disqus 评论区 a 标签的颜色 bug，修改 blockqoute 中 p 标签的 margin
* `[+]` 添加不蒜子计数功能，在footer上显示访问量
* `[+]` 添加回到顶部功能

*2016.4.27 v2.0.0*

* `[^]` 基于 jekyll 3.1.2 重构了所有代码
* `[+]` 主页添加了摘要，在正文中使用4个换行符来分割，可在`_config.yml`中修改
* `[+]` 主页添加了近期文章、分类列表和标签云
* `[+]` 主页导航区做了视觉优化，阴影效果
* `[+]` 增加了归档、标签和分类页面
* `[+]` 增加了收藏页面
* `[+]` 评论插件可以选择 disqus 或 多说，直接在`_config.yml`中修改
* `[+]` 适配移动端
* `[+]` 页面滚动时，文章目录固定在右侧
* `[+]` 页面内容较少时，固定 footer 在页面底部
* `[^]` 使用 GitHub 风格的代码高亮写法，即\`\`\`的写法，去除`highlight.js`代码高亮插件的使用
* `[^]` 使用 Masonry 重写了 Demo 页中的瀑布流布局，响应式交互体验更好
* `[-]` 去除了 jQuery 和 BootStrap，使得加载速度更快

* 2016.3-2016.4 进行了一次大的改版和重构，详见 [README](https://github.com/Gaohaoyang/gaohaoyang.github.io/blob/master/README.md) 和博文 [对这个 jekyll 博客主题的改版和重构](http://gaohaoyang.github.io/2016/03/12/jekyll-theme-version-2.0/)
* 2015.3-2015.4 完成了这个博客主题的第一版。

## 友情链接



## Comments

{% include comments.html %}
