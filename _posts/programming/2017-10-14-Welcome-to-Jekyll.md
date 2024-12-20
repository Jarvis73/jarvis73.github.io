---
layout: post
title:  "Hello Jekyll!"
date:   2017-10-14 00:00:00 +0800
categories: Tools
mathjax: true
author: Jarvis
meta: Post
---

* content
{:toc}

本文介绍了 Jekyll 的安装, 展示了一些使用 Markdown 写博客的例子.



## Ubuntu 安装 Jekyll

```bash
# 安装 Ruby 和其他依赖
sudo apt-get install ruby-full build-essential zlib1g-dev

# 在 `.bashrc` 填入环境变量
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 安装 jekyll (使用代理速度更快)
gem install jekyll bundler jekyll-paginate jekyll-sitemap
```


## 一些例子

You’ll find this post in your `_posts` directory. Go ahead and edit it and re-build the site to see your changes. You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

To add new posts, simply add a file in the `_posts` directory that follows the convention `YYYY-MM-DD-name-of-post.ext` and includes the necessary front matter. Take a look at the source for this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

```python
# Define a Fibonacci function
def foo(n):
    if n < 2:
        return 1
    else:
        return n * foo(n - 1)

# Entry
if __name__ == '__main__':
    fib_n = foo(10)
    print("Fib(10) = %d" % fib_n)
```

Check out the [Jekyll docs][jekyll] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll’s dedicated Help repository][jekyll-help].

[jekyll]:      http://jekyllrb.com
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-help]: https://github.com/jekyll/jekyll-help

Block Mathjax 

$$
f(x) = \frac{ax + b}{cx + d}
$$

Inline Mathjax $$ a \neq b $$

