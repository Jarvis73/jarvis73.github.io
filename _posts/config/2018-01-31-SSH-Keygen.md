---
layout: post
title: SSH 工具教程 (Tutorial of SSH tools)
date: 2022-09-17 21:33:00 +0800
categories: Tools
author: Jarvis
meta: Post
pin: True
---

* content
{:toc}

ssh 是远程连接的利器, 可以说凡是涉及到 linux 服务器, ssh 就是一个绕不开的话题. 本文作为一个教程, 尽可能详细的帮助读者设置 ssh, 并给出一些常用的 ssh 配置方法 (主要用于 linux 系统的远程登录和文件传输).



## 1. 简介

ssh 分为两个部分, `sshd` 服务端和 `ssh` 客户端. `sshd` 通常在服务器上已经建好并处于可用状态, 因此本文只讨论 ssh 客户端, 即用户通过 ssh 客户端远程连接到服务器上进行操作. 

ssh 是一个多平台软件, 在 Windows/Linux/Mac 上均有相应的程序. 

* Windows 下 (以 Win11 为例), 右键开始菜单, 打开【Windows 终端】(Win10 下是打开 【PowerShell】), 输入 `Get-Command ssh` 即可查看到 ssh 的安装路径在什么位置, 比如:

  ```
  C:\Windows\System32\OpenSSH\ssh.exe
  ```

  此时输入 `ssh` 回车, 如果有如下的返回结果, 则说明 ssh 已经正常安装了.

  ```
  $ ssh
  usage: ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface]
            [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
            [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
            [-i identity_file] [-J [user@]host[:port]] [-L address]
            [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port]
            [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
            [-w local_tun[:remote_tun]] destination [command]
  ```

  如果找不到 ssh, 则可以从 [Github](https://github.com/PowerShell/Win32-OpenSSH/releases) 下载 OpenSSH (选择 `.msi` 后缀的), 然后双击安装即可.

* Linux 下, 通常默认就有 ssh

## 2. 使用方法

### 2.1 密码登录

执行以下命令, 然后输入密码, 即可通过密码登录到远程服务器.

```bash
ssh <用户名>@<服务器地址> -p <端口>
```

{% include card.html type="info" content="如果使用默认端口 22, 则 `-p <端口>` 可以不写." %}

### 2.2 密钥登录 (免密登录)

我们可以通过 `ssh-keygen` 来生成密钥对. 密钥对包含公钥和私钥, 创建密钥如下:

```bash
# Windows
ssh-keygen -t rsa -b 2048 -f C:\Users\<用户名>\.ssh\mykey

# Linux
ssh-keygen -t rsa -b 2048 -f /home/<用户名>/.ssh/mykey
```

{% include card.html type="info" content="要求输入 `passphase` 时直接回车, 这样才可以免密登录. 再次回车, 生成结束, 输出的指纹和图可以不管." %}

* `-t rsa`: 指定密钥类型为 RSA
* `-b 2048`: 指定密钥的位数为 2048
* `-f /home/<用户名>/.ssh/mykey`: 指定密钥名称为 `mykey` (可以自定义), 放在用户的 `.ssh` 目录下.

这个命令会生成 `mykey` 和 `mykey.pub` 两个文本文件. 获取公钥 `mykey.pub` 的内容:

```bash
# Windows
cat C:\Users\<用户名>\.ssh\mykey.pub

# Linux
cat /home/<用户名>/.ssh/mykey.pub
```

复制公钥的内容, 然后通过密码先登录到服务器上, 创建 `~/.ssh` 目录, 创建 `~/.ssh/authorized_keys` 文件(注意文件名拼写, 不可写错), 把复制的内容粘贴到末尾新的一行:

```bash
# 把公钥放到服务器的 `authorized_keys` 文件的末尾. 
mkdir ~/.ssh
echo "<复制的公钥粘贴到这里>" >> ~/.ssh/authorized_keys

# 限制 `.ssh` 和 `authorized_keys` 的访问权限为只能自己访问
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

接下来退出服务器, 回到本地的终端. 如果本地是 Linux, 则还需要限制私钥的权限为只能自己访问:

```bash
chmod 600 ~/.ssh/mykey
```

注意以上权限修改是必要的, 否则可能由于安全性低的问题 ssh 拒绝使用密钥. 

最后我们可以使用 `-i` 选项指定私钥登录服务器, 不再需要输入密码:

```bash
ssh <用户名>@<服务器地址> -p <端口> -i ~\.ssh\mykey
```

{% include card.html type="info" title="登录时显示 Permission denied" content="如果确保上面的秘钥和权限配置无误, 仍然显示 `Permission denied (publickey)` 的话, 可能是管理员开启了 ssh 登录白名单, 新建的账户不在白名单里所以无法登录. 找管理员编辑 `/etc/ssh/sshd_config` 文件, 如果其中的 `AllowUsers` 设置是启用的, 则在末尾加上当前用户即可." %}



### 2.3 使用配置文件

注意到上面登录服务器需要指定一大堆参数. 我们可以使用配置文件来简化登录过程. 在**本地**创建并编辑文件 `~/.ssh/config`

```
Host <自定义别名>
    HostName <服务器地址>
    Port <端口>
    User <用户名>
    IdentityFile <私钥路径>
```

比如, 一个配置可以是这样的

```
Host lab
    HostName 192.168.1.2
    Port 22
    User jarvis
    IdentityFile ~/.ssh/mykey
```

最后, 我们可以直接这样登录服务器:

```bash
ssh lab
```

非常方便, 也好记. 此外, 如果要配置多台远程服务器, 只需要按照 2.2 再创建一个密钥对, 像 2.3 里那样增加一个块写入配置即可.

### 2.4 其他用法

* ssh 的时候如果配置了密钥, 但想强制使用密码登录:

```bash
ssh lab -o PubkeyAuthentication=no
```

* 曾经 ssh 登陆过某个服务器地址, 后来该地址的服务器重装过系统, 则需要在 `~/.ssh/known_hosts` 文件中找到该服务器地址, 并删除整行 (vim 打开的话, dd 命令删除光标所在行), 否则会登陆不上服务器. 

## 3. ssh 隧道, 端口转发

### 3.1 本地转发

用一幅图来说明 ssh 隧道是做什么的. 

{% include image.html class="polaroid" url="2022/09/ssh.png" title="ssh 隧道本地转发示意图" %}

本地转发的意思是通过 ssh 隧道, 把本地的数据转发到远程端口. 

#### 3.1.1 开启隧道

假设你的本地机器是 host2, 可以通过 ssh 访问 host3, 但是无法直接访问 host4 上开在 9000 端口的 http 服务, 而 host3 可以访问 host4, 此时就可以利用 ssh 隧道通过 host3 访问 host4 的服务, 如下:

```bash
# host2

# 本地转发模板
ssh -L [<本地地址>:]<本地端口>:<目标地址>:<目标端口> host3

# 比如上面的例子, -L 表示本地转发
# 用法 1: 使用回环地址 127.0.0.1 或者 localhost
ssh -L 127.0.0.1:10001:192.168.1.4:9000 host3
ssh -L localhost:10001:192.168.1.4:9000 host3

# 用法 2: 省略<本地地址>
ssh -L 10001:192.168.1.4:9000 host3

# 用法3: 使用本地外部地址
ssh -L 192.168.1.2:10001:192.168.1.4:9000 host3
```

{% include card.html type="primary" content="由于 host2 开启的转发端口 10001 是在本地, 因此称为【本地转发】." %}


#### 3.1.2 从 host2 访问

因为隧道是在 host2 上开的, 所以可以在 host2 本地通过 host3 访问 host4 上的 http 服务, 其中
* 用法 1 和 2 访问: `http://127.0.0.1:10001` 或 `http://localhost:10001` 
* 用法 3 访问: `http://192.168.1.2:10001`

{% include card.html type="info" content="上图中, 只有 host2 和 host3 之间的通信是 ssh 加密的." %}

#### 3.1.3 从 host1 访问

如果需要从 host1 通过 host2 访问 host4 上的服务, 则需要增加 `-g` 参数:

```bash
# host2
ssh -g -L 10001:192.168.1.4:9000 host3
```

此时在 host1 上访问 `http://192.168.1.2:10001` 即可.

#### 3.1.4 ssh 跳板

```bash
# host2
ssh -g -L 10022:192.168.1.4:22 host3
```

我们把 host2 上的 10022 映射到了 host4 上的 22 端口, 而 22 端口是 ssh 端口, 这意味着 host2 成了外界和 host4 直接的跳板机, 此时我们可以从 host1 或者 host2 上 ssh 连接到 host4:

```bash
# host2
ssh jarvis@localhost -p 10022
# host1
ssh jarvis@192.168.1.2 -p 10022
```

如果我们不希望 ssh 登录, 只是建立隧道后进入后台的话, 可以加上 `-f` 参数 (fork):

```bash
# host2
ssh -f -g -L 10022:192.168.1.4:22 host3 ifconfig
ssh -f -N -g -L 10022:192.168.1.4:22 host3
```

注意我们额外加了 `-N` 参数, 否则必须指定一个要执行的远程命令

### 3.2 远程转发

假如我们有这样的场景, host3 和 host4 都在内网, 而 host2 在外网, 我们无法通过 host2 直接访问 host3 和 host4, 但是从 host3 可以访问 host2.

{% include image.html class="polaroid" url="2022/09/ssh_remote.png" title="ssh 隧道远程转发示意图" %}

远程转发的意思是通过 ssh 隧道, 把远程端口的数据转发到本地. 

#### 3.2.1 开启隧道

远程转发需要在 host3 上开启隧道:

```bash
# host3
ssh -R [<远程地址>:]远程端口:<目标地址>:<目标端口> host1

# 举例
ssh -R 10001:192.168.1.4:9000 host2
```

这样就在 host2 上的 10001 端口建立了 ssh 隧道连接. 当有主机连接 `host2:10001` 时, 流量就会被通过 ssh 隧道转发到 host3, 然后再有 host3 转发给 host4. 由于 host3 发起的转发端口在 host2 上(对于 host3 来说是远程), 因此成为远程端口转发. 


#### 3.2.2 从 host2 访问

```bash
# host2
ssh jarvis@localhost -p 10001

# host2 (这个连不上)
ssh jarvis@10.76.1.101 -p 10001
```

{% include card.html type="warning" content="【远程端口】10001 是由 host2 上的 sshd 服务控制的, 因此即使指定了【远程地址】, host2 上的 sshd 也只会把 10001 绑定在回环地址 127.0.0.1 (localhost) 上. " %}

```bash
# host2
# 查看端口绑定
netstat -tnlp
```

#### 3.2.3 ssh 跳板 + 从 host1 访问

为了能从 host1 和 host2 上通过 10.76.1.101 访问, 需要在 host2 的 sshd 配置文件中, 把 `GatewayPorts=no` 改为 `GatewayPorts=yes`. 启用该项之后, 无论【远程地址】设置为什么都会绑定在所有地址 (0.0.0.0) 上.

```bash
# host2
ssh -g -R *:10001:192.168.1.4:9000 host2
ssh -g -R 10001:192.168.1.4:9000 host2

# 类似 3.2 中的, 也可以加 -f -N 参数, 参数可缩写
ssh -fgNR 10001:192.168.1.4:9000 host2
```

然后在 host1 上访问

```bash
# host1
ssh jarvis@10.76.1.101 -p 10001
```

### 3.3 动态端口转发

前面的两种端口转发无论是本地转发还是远程转发, 都只能进行一对一的端口转发, 这意味着同一个端口只能解析一种固定的协议. 比如我把本地的 10001 端口转发到远程的 80 端口 (web 服务, http 协议), 那么本地的 10001 端口只能用于 web 服务的访问, 不能用于 ssh 连接. 

ssh 支持动态转发, 由 ssh 判断发起请求的工具使用的是什么协议, 并动态的转发到相应的目标端口. 

{% include image.html class="polaroid" url="2022/09/ssh_dynamic.png" title="ssh 隧道动态转发示意图" %}

如上图所示, 我们希望从 host2 既能访问互联网, 又能通过 ssh 连接到 host4. 单独开两个端口映射显然是可以的, 但这并不优雅. 这时候我们就可以使用动态转发, 格式如下:

```bash
# host2
ssh -D [<绑定地址>:]端口 host3

# 比如上面的例子
ssh -fgN -D 10022 host3
```

执行了上面的命令之后, host2 就会在本地开启 SOCKS4 或 SOCKS5 服务来监听 10022 端口. 这时候只要客户端工具将自身的代理设置为 `host2:10022`, 则该程序所有的数据就会被经由 `host2:10022` 转发给 host3, 然后由 host3 自动根据协议类型决定把数据发往何处. 

比如本地使用浏览器代理, 那么浏览器使用的 http/https 流量就会被 host3 转发到互联网上. 如果使用 SecurtCRT 或 putty 等支持代理上网的客户端工具, 则连接 host4 的 ssh 流量也可以通过 host3 被发往 host4. 


## 4. 其他 ssh 相关命令

* `scp`: 文件复制命令, 通常会随着 ssh 一起安装好. 

{% include card.html type="info" content="`scp` 命令也支持 `~/.ssh/config` 文件中的配置. `scp` 复制命令必须在本地执行." %}

```bash
# 本地文件 --> 远程服务器
scp /path/to/source_file lab:~/target_dir

# 本地文件夹 --> 远程服务器
scp -r /path/to/source_dir lab:~/target_dir

# 远程文件 --> 本地当前目录
scp lab:~/source_file .

# 远程文件夹 --> 本地当前目录
scp -r lab:~/source_dir .
```

* `sftp`: 基于 SSH 加密传输的 FTP 命令行工具, 通常会随着 ssh 一起安装好. 

```bash
# 登录远程服务器
sftp lab

# 列出服务器文件, 列出本地文件(相当于 local ls)
ls
lls

# 改变服务器当前目录, 改变本地当前目录 
cd
lcd

# 本地文件 --> 远程服务器
put source_file

# 本地文件夹 --> 远程服务器
put -R source_dir

# 远程文件 --> 本地当前目录
get source_file

# 远程文件夹 --> 本地当前目录
get -R source_dir
```

* SFTP 图形化界面的软件 [FileZilla Client](https://filezilla-project.org/) 也比较好用. 

* `ssh-keygen`: 生成密钥对, 2.2 节介绍了.
