---
layout: post
title: "NextCloud 教程 (Tutorial of NextCloud)"
date: 2022-09-07 00:14:00 +0800
categories: Config
author: Jarvis
meta: Post
# pin: True
---

* content
{:toc}

本文是 NextCloud 私人云盘的搭建教程, 同时记录使用过的一些配置.



## 安装教程



## 配置选项

配置文件在 `app/config/config.php`

* 添加 `'overwriteprotocol' => 'https'` 以强制启用 https 访问. 在使用手机客户端的时候如果遇到 "严格模式: 不允许 HTTP 连接" 的问题, 则需要添加该配置.
