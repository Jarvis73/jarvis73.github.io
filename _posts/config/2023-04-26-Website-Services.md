---
layout: post
title: "HTTPS 配置教程 (A Tutorial for HTTPS)"
date: 2023-04-26 16:25:00 +0800
categories: Config
author: Jarvis
meta: Post
pin: True
---

* content
{:toc}

[HTTP](https://developer.mozilla.org/zh-CN/docs/Web/HTTP) 是一种用于分布式、协作式和超媒体信息系统的应用层协议, 它是一种发布和接收 HTML 页面的方法, 被用于在Web浏览器和网站服务器之间传递信息. HTTP 默认工作在 TCP 协议 80 端口, 但它<span style="color:blue">以明文方式发送内容, 不提供任何方式的数据加密</span>, 因此不适合传输敏感信息. 

为了解决 HTTP 不安全的问题, [HTTPS](https://en.wikipedia.org/wiki/HTTPS) 应运而生. HTTPS 是一种透过计算机网络进行安全通信的传输协议, 它经由 HTTP进行通信, 但<span style="color:blue">利用 SSL/TLS 来加密数据包保证数据的机密性和完整性</span>. HTTPS 默认工作在 TCP 协议 443 端口. HTTPS 比 HTTP 更加安全, 适合传输敏感信息. 



## HTTP 和 HTTPS

来源: [HTTP 与 HTTPS 的区别](https://www.runoob.com/w3cnote/http-vs-https.html)

> **HTTP (HyperText Transfer Protocol: 超文本传输协议)** 是一种用于分布式、协作式和超媒体信息系统的应用层协议.  简单来说就是一种发布和接收 HTML 页面的方法, 被用于在 Web 浏览器和网站服务器之间传递信息. 
> 
> HTTP 默认工作在 TCP 协议 80 端口, 用户访问网站 http:// 打头的都是标准 HTTP 服务. 
> 
> <span style="color:blue">HTTP 协议以明文方式发送内容, 不提供任何方式的数据加密, 如果攻击者截取了 Web 浏览器和网站服务器之间的传输报文, 就可以直接读懂其中的信息.</span> 因此, HTTP 协议不适合传输一些敏感信息, 比如：信用卡号、密码等支付信息. 
>
> **HTTPS (Hypertext Transfer Protocol Secure: 超文本传输安全协议)** 是一种透过计算机网络进行安全通信的传输协议. <span style="color:blue">HTTPS 经由 HTTP 进行通信, 但利用 SSL/TLS 来加密数据包. HTTPS 开发的主要目的, 是提供对网站服务器的身份认证, 保护交换数据的隐私与完整性. </span>
>
> HTTPS 默认工作在 TCP 协议 443 端口, 它的工作流程一般如以下方式：
> 
> 1、TCP 三次同步握手
> 2、客户端验证服务器数字证书
> 3、DH 算法协商对称加密算法的密钥、hash 算法的密钥
> 4、SSL 安全加密隧道协商完成
> 5、网页以加密的方式传输, 用协商的对称加密算法和密钥加密, 保证数据机密性；用协商的 hash 算法进行数据完整性保护, 保证数据不被篡改. 


## 配置 Nginx

HTTPS 本身可以在提供 Web 服务的框架里配置, 但由于可提供服务的框架众多, 配置方式各不相同, 因此这里主要提供一种通用的方法, 即利用 Nginx 服务器<span style="color:blue">反向代理</span> Web 服务, 然后 HTTPS 统一配置在 Nginx 里. 

{% include card.html type="info" content="需要特别注意的是, 这种配置方法**只有 Nginx 和 WWW 的通信是 HTTPS 加密的, 而 Nginx 和提供 Web 服务的程序仍然使用 HTTP**. 因此这种方法适合于个人网站或小范围使用的场景下, 即 Nginx 服务和 Web 服务直接放在同一个服务器上, 或着放在安全性较高的局域网内部. " %}

{% include card.html type="primary" title="反向代理" content="我们通常所说的**代理 (proxy)** 指的是代理客户端, 从而可以通过代理服务器访问到无法直接访问的网站, 同时也可以达到隐藏客户端的目的, 例如 Shadowsocks, Clash 等代理软件. 而**反向代理 (reverse proxy)** 指的是代理服务端, 从而所有连接到服务端的请求都通过反向代理服务器转发到服务端, 同时也可以达到隐藏服务端的目的, 例如 Nginx 等可实现反向代理." %}

首先需要安装 Nginx 工具 (本文默认都在 Ubuntu 服务器上操作). 先检查一下系统中是否已经安装 Nginx, 只需要查看是否存在存放 Nginx 配置的文件夹 `/etc/nginx` 是否存在, 如果不存在则安装一下:

```bash
sudo apt install nginx
```

安装后我们即可启动 Nginx 服务器. 这里使用 `systemctl` 工具来操作 Ubuntu 上的系统服务:

```bash
# 启动 Nginx 服务器
sudo systemctl start nginx

# 查看 Nginx 服务器的状态
sudo systemctl status nginx

# 重载 Nginx 的配置文件 (后面会用到)
sudo systemctl reload nginx
```

## 域名解析

HTTPS 通常需要和域名绑定, 因此我们需要一个域名绑定到服务器的外网 IP 地址上. 域名可以从域名服务商处购买, 比如阿里云, 华为云, 腾讯云等. 购买域名后, 域名服务商通常同时会提供域名解析服务, 把域名和 IP 地址绑定. 

这里用的华为云的域名解析服务为例: 

华为云登录后, 右上角点击**控制台**

{% include image.html class="polaroid" url="2023/04/https-1.png" title="控制台" %}

在快捷导航里点击**域名注册 Domains**. 如果没有该按钮, 也可以在搜索框里搜索该服务.

{% include image.html class="polaroid" url="2023/04/https-2.png" title="域名注册按钮" %}

如果还未注册域名, 则点击右上角的**注册域名**按钮, 搜索自己喜欢的域名进行注册并付费. 假设已经注册好了域名, 则点击**解析**按钮.

{% include image.html class="polaroid" url="2023/04/https-3.png" title="解析按钮" %}

点击右上角**添加记录集**以添加一条新的解析内容. 主要关注三个部分:
* 主机记录: 通常申请下来的是二级域名 (比如 `jarvis73.com`), 解析时通常填入一个自定义的三级域名
* 类型: A 类型, 把域名指向 IPv4 地址
* 值: 域名指向的 IPv4 地址

{% include image.html class="polaroid" url="2023/04/https-4.png" title="添加解析记录" %}

完成后点击确定, 就能在列表中看到新增的解析记录了. 通常 5 分钟或更快就能完成域名解析到 IP 地址的绑定. 可以通过 `ping hahaha.jarvis73.com` 来检查是否解析正确.

{% include image.html class="polaroid" url="2023/04/https-5.png" title="解析记录列表" %}

## 申请免费 SSL 证书

> **SSL 是指安全套接字层 (Secure Sockets Layer)**, 简而言之, 它是一项标准技术, 可确保互联网连接安全, 保护两个系统之间发送的任何敏感数据, 防止网络犯罪分子读取和修改任何传输信息, 包括个人资料. 两个系统可能是指服务器和客户端（例如, 浏览器和购物网站）, 或两个服务器之间（例如, 含个人身份信息或工资单信息的应用程序）. 
>
> 此举可确保在用户和站点之间, 或两个系统之间传输的数据无法被读取. 它使用加密算法打乱传输中的数据, 防止数据通过连接传输时被黑客读取. 这里所说的数据是指任何敏感或个人信息, 例如信用卡号和其他财务信息、个人姓名和住址等.  
> 
> **TLS 是指传输层安全 (Transport Layer Security)**, 是更为安全的升级版 SSL. 由于 SSL 这一术语更为常用, 因此我们仍然将我们的安全证书称作 SSL. 但当您从DigiCert购买 SSL 时, 您真正购买的是最新的 TLS 证书, 有 ECC、RSA 或 DSA 三种加密方式可以选择.  
> 
> 如果某个网站受 SSL 证书保护, 其相应的 URL 中会显示 HTTPS. 单击浏览器地址栏的挂锁图标, 即可查看证书详细信息, 包括颁发机构和网站所有者的公司名称. 
> 
> 来源: [什么是 SSL 证书？](https://www.websecurity.digicert.com/zh/cn/security-topics/what-is-ssl-tls-https). 略作改动.

阿里云为每个用户赠送 20 个免费 SSL 证书, 其他家云服务商也会送免费证书, 大同小异, 这里仅用阿里云为例. 

首先登录阿里云, 进入控制台. 点击左上角的三横线按钮展开阿里云的服务列表, 选择**SSL 证书 (应用安全)**. 找不到就在顶部的搜索栏里搜索一下.

{% include image.html class="polaroid" url="2023/04/https-6.png" title="SSL 证书 (应用安全)" %}

点击左侧列表中的**SSL 证书**, 然后点击**免费证书**, 再点击**创建证书**. 如果没有领过, 那么此时会提示领取免费证书 (0 元购买). 领导后**创建证书**按钮就会显示**20/20**, 第一个数字表示剩余免费证书的数量, 第二个数字表示总共拥有过的免费证书数量. 

{% include image.html class="polaroid" url="2023/04/https-7.png" title="创建免费证书" %}

点击创建证书后下面列表中就会出现一个证书记录, 点击**证书申请**, 进入申请流程.

{% include image.html class="polaroid" url="2023/04/https-8.png" title="证书" %}

SSL 证书为了安全性是和域名绑定的, 因此需要填入绑定的域名 `hahaha.jarvis73.com` (仅作示例, 填入你自己的), 选择**手工 DNS 验证** (这里是因为我的域名不在阿里云, 所以需要额外验证. 如果域名也是阿里云买的, 那可能就不需要 DNS 验证了) —> 提交审核

{% include image.html class="polaroid" url="2023/04/https-9.png" title="填写证明绑定的域名" %}

提交审核后, 如果域名不是阿里云的, 则需要进行 DNS 验证

{% include image.html class="polaroid" url="2023/04/https-10.png" title="DNS 验证方法" %}

验证的方法就是在域名解析服务商那里加入一条 TXT 类型的解析记录. 按本文的教程就是在华为云域名解析的地方新增一个记录集. 依次填入**主机记录** `_dnsauth.hahaha` (填入你自己的), 选择 TXT **记录类型**, 填入一长串**记录值**. 注意记录值在 TXT 类型下必须加双引号.

{% include image.html class="polaroid" url="2023/04/https-11.png" title="新增 DNS 验证记录" %}

然后返回阿里云点击**验证**按钮即可验证该域名的所有权是本人. 如果验证失败可能稍等一下, 可能解析记录还未更新. 或者检查一下填写的域名解析信息是否正确.

{% include image.html class="polaroid" url="2023/04/https-12.png" title="验证成功" %}

关闭侧边弹窗, 返回证书列表, 等一会儿刷新一下就能看到证书申请下来了 (1 年的), 点击下载, 下载 nginx 的.

{% include image.html class="polaroid" url="2023/04/https-13.png" title="申请的证书" %}

把证书拷贝到服务器上, 解压 zip 压缩包, 得到两个文件 (key 和 pem, 注意开头的数字是随机数, 可以不用管):

```text
123456_hahaha.jarvis73.com.key
123456_hahaha.jarvis73.com.pem
```

## 在 Nginx 中配置反向代理以及证书

创建 `/etc/nginx/cert` 文件夹, 把上面申请的 key 和 pem 两个文件放入其中.

```bash
sudo mkdir /etc/nginx/cert
sudo mv 123456_hahaha.jarvis73.com.key /etc/nginx/cert
sudo mv 123456_hahaha.jarvis73.com.pem /etc/nginx/cert
```

现在创建一个反向代理服务的配置. 在 `/etc/nginx/sites-available` 文件夹下新建一个空白文件 `chatgpt` (没有后缀要求), 写入以下配置 (**注意修改带 TODO 的部分为你自己的配置**):

```text
server {
    # 这段配置监听 80 端口 (http)
    listen 80;

    # TODO: 改为你自己的域名
    server_name hahaha.jarvis73.com;

    # 关闭服务器响应头中的“Server”信息。默认情况下，nginx 会在响应头中
    # 添加“Server”信息，包含服务器软件的名称和版本号。关闭这个选项可以
    # 增加服务器的安全性，因为攻击者可能会利用这些信息来针对特定版本的
    # 服务器软件进行攻击。
    server_tokens off;

    # 80 端口强制重定向到 https
    return 301 https://$server_name$request_uri;
}

# https 端口 443
server {
    listen 443 ssl http2;
    # TODO: 改为你自己的域名
    server_name hahaha.jarvis73.com;

    # ============================================================
    # 下面一段用于配置 SSL 证书
    # ============================================================

    # TODO: *.pem 和 *.key 修改为前面申请证书的实际文件名
    ssl_certificate /etc/nginx/cert/hahaha.jarvis73.com.pem;
    ssl_certificate_key /etc/nginx/cert/hahaha.jarvis73.com.key;

    # TODO: 自定义当前 nginx 服务日志的文件名
    access_log /var/log/nginx/chatgpt-access.log;
    error_log /var/log/nginx/chatgpt-error.log;

    server_tokens off;

    # ============================================================
    # 以下部分是反向代理的设置, 具体配置方式取决于所使用的服务.
    # 特别需要注意 location 和 proxy_pass 匹配的写法, 这里不再
    # 展开, 请自行上网搜索.
    # ============================================================

    # 关闭代理的缓存. 可以保留前端的打字机效果 (ChatGPT 前端用的. 其他服务一般不需要使用该配置, 可以注释掉.)
    proxy_buffering off;

    # 反向代理 web-server 的 /admin 和 /static 请求到 3389 端口
    location /admin {
        # TODO: 设置为本地开起来的后端服务地址
        proxy_pass http://127.0.0.1:3389;

        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location /static {
        # TODO: 设置为本地开起来的后端服务地址
        proxy_pass http://127.0.0.1:3389;

        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 反向代理 client 的请求到 8080 端口
    location / {
        # TODO: 设置为本地开起来的前端服务地址
        proxy_pass http://127.0.0.1:8080;

        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

`sites-available` 中的配置文件用于归档, 如果需要让 Nginx 启用这些配置, 还需要把该配置放入 `/etc/nginx/sites-enabled`文件夹中. 这通常使用软链接来实现:

```bash
cd /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/chatgpt .
```

然后重载 Nginx 配置

```bash
sudo systemctl reload nginx
```

此时访问 `http://hahaha.jarvis73.com` 就会自动重定向到 `https://hahaha.jarvis73.com`, 同时浏览器在打开该链接时地址栏左侧会显示加锁, 点击锁的图标会显示**连接安全**(此网站具有由受信任的机构颁发的有效证书), 表示所配置的 SSL 证书核验通过.

免费证书通常是 1 年有效期, 到期需要重新申请证书并更新到 Nginx 服务中, 到期未更新则访问网站时锁的图标会加一个斜线表示不安全.
