---
layout: post
title: "Powerline 设置"
date: 2021-03-29 14:36:00 +0800
categories: Config
author: Jarvis
meta: Wiki_Ubuntu
hidden: true
---

* content
{:toc}



## 1. 简介

Powerline 是个终端状态线的插件, 可以为 bash, vim, zsh, tmux, ipython 等终端编辑和终端命令工具提供丰富的状态线显示.

## 2. 安装 `powerline-status`

参考: [Github](https://github.com/powerline/powerline)

* 在 Ubuntu 20.04 系统下可以使用 pip3 来安装:

```bash
sudo pip3 install powerline-status
```

* 获取文件的安装位置, 与所使用的 python3 版本有关

```bash
powerline_location=$(/usr/bin/pip3 show powerline-status \
    | grep -Po "(?<=Location: ).*(?=$)") && echo $powerline_location
```

* 把相关的配置文件复制到用户目录下, 方便修改

```bash
mkdir -p ~/.config/powerline/colorthemes
mkdir -p ~/.config/powerline/themes/shell

cp $powerline_location/powerline/config_files/config.json ~/.config/powerline/
```

* 为终端启用 Powerline

自行把下面的 `<powerline_location>` 修改为上面获得的路径的值.

<ul class="nav nav-tabs">
  <li class="active"><a data-tab href="#tabContent00-1">Bash</a></li>
  <li><a data-tab href="#tabContent00-2">Vim</a></li>
  <li><a data-tab href="#tabContent00-3">Tmux</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane active" id="tabContent00-1" markdown="block">
把以下内容填入 `~/.bashrc` 的末尾:

```bash
if [ -f <powerline_location>/powerline/bindings/bash/powerline.sh ]; then
    source <powerline_location>/powerline/bindings/bash/powerline.sh
fi
```

配置结果如下图所示:

{% include image.html class="polaroid" url="2021/03/bash.png" title="Bash Powerline" %}
</div>
<div class="tab-pane" id="tabContent00-2" markdown="block">
把以下内容填入 `~/.vimrc` 的末尾:

```vim
set rtp+=<powerline_location>/powerline/bindings/vim/
" Always show statusline
set laststatus=2
" Use 256 colours (Use this setting only if your terminal supports 256 colours)
set t_Co=256
```

配置结果如下图所示:

{% include image.html class="polaroid" url="2021/03/vim.png" title="Vim Powerline" %}
</div>
<div class="tab-pane" id="tabContent00-3" markdown="block">
把以下内容填入 `~/.tmux.conf` 的末尾:

```vim
source <powerline_location>/powerline/bindings/tmux/powerline.conf
set-option -g default-terminal "screen-256color"
```
配置结果如下图所示:

{% include image.html class="polaroid" url="2021/03/tmux.png" title="Tmux Powerline" %}
</div>
</div>


## 3. 安装并配置 `powerline-gitstatus`

参考: [Github](https://github.com/jaspernbrouwer/powerline-gitstatus)

* 使用 pip3 安装:

```bash
sudo pip3 install powerline-gitstatus
```

* 创建 `~/.config/powerline/colorthemes/default.json`, 填入配置:

```json
{
  "groups": {
    "gitstatus":                 { "fg": "gray8",           "bg": "gray2", "attrs": [] },
    "gitstatus_branch":          { "fg": "gray8",           "bg": "gray2", "attrs": [] },
    "gitstatus_branch_clean":    { "fg": "green",           "bg": "gray2", "attrs": [] },
    "gitstatus_branch_dirty":    { "fg": "gray8",           "bg": "gray2", "attrs": [] },
    "gitstatus_branch_detached": { "fg": "mediumpurple",    "bg": "gray2", "attrs": [] },
    "gitstatus_tag":             { "fg": "darkcyan",        "bg": "gray2", "attrs": [] },
    "gitstatus_behind":          { "fg": "gray10",          "bg": "gray2", "attrs": [] },
    "gitstatus_ahead":           { "fg": "gray10",          "bg": "gray2", "attrs": [] },
    "gitstatus_staged":          { "fg": "green",           "bg": "gray2", "attrs": [] },
    "gitstatus_unmerged":        { "fg": "brightred",       "bg": "gray2", "attrs": [] },
    "gitstatus_changed":         { "fg": "mediumorange",    "bg": "gray2", "attrs": [] },
    "gitstatus_untracked":       { "fg": "brightestorange", "bg": "gray2", "attrs": [] },
    "gitstatus_stashed":         { "fg": "darkblue",        "bg": "gray2", "attrs": [] },
    "gitstatus:divider":         { "fg": "gray8",           "bg": "gray2", "attrs": [] }
  }
}
```

* 创建 `~/.config/powerline/themes/shell/default.json`, 填入配置:

```json
{
    "segments": {
        "left": [{
                "function": "powerline.segments.shell.mode"
            },
            {
                "function": "powerline.segments.common.net.hostname",
                "priority": 10
            },
            {
                "function": "powerline.segments.common.env.user",
                "priority": 30
            },
            {
				"function": "powerline.segments.common.env.virtualenv",
				"priority": 30
			},
            {
                "function": "powerline_gitstatus.gitstatus",
                "priority": 10
            },
            {
                "function": "powerline.segments.shell.cwd",
                "priority": 10
            }
        ],
        "right": []
    }   
}
```

* 创建 `~/.config/powerline/themes/shell/__main__.json`, 填入配置:

```json
{
    "gitstatus": {
        "args": {
            "formats": {
                "branch": "\ue0a0 {}",
                "tag": " ★ {}",
                "behind": " ↓ {}",
                "ahead": " ↑ {}",
                "staged": " ● {}",
                "unmerged": " ✖ {}",
                "changed": " ✚ {}",
                "untracked": " … {}",
                "stashed": " ⚑ {}"
            },
            "show_tag": "exact"
        }
    }   
}
```

* 重新载入配置

```bash
powerline-daemon --replace
```

## 4. 安装 Powerline 字体

* 可以安装 Powerline 官方提供的补丁字体

```bash
git clone https://github.com/powerline/fonts.git && cd fonts && sh ./install.sh
```

* 也可以安装微软提供的 [Cascadia Code](https://github.com/microsoft/cascadia-code) 字体, 其中包含适用于 Powerline 的打补丁的版本. 到 Release 页面下载最新的版本, 解压后直接安装TTF. 然后在终端的预设页面把字体修改为 Cascadia Code PL Roman 即可.

