---
layout: post
title: "Ubuntu 18.04/20.04/22.04 教程 (Ubuntu 18.04/20.04/22.04 Tutorials)"
date: 2020-11-06 10:11:00 +0800
update: 2023-03-29
categories: Config
figure: /images/2020/11/ubuntu.png
author: Jarvis
meta: Post
pin: True
---

* content
{:toc}



本文统一整理 Ubuntu 18.04, 20.04 和 22.04 的系统安装和设置方法. 其中三代系统有差别的设置会通过标签分别介绍, 如下所示, 请读者务必注意.

<ul class="nav nav-tabs">
  <li><a data-tab href="#tabContent00-1">18.04 (bionic)</a></li>
  <li><a data-tab href="#tabContent00-2">20.04 (focal)</a></li>
  <li class="active"><a data-tab href="#tabContent00-3">22.04 (jammy)</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane" id="tabContent00-1" markdown="block">
Ubuntu 18.04
</div>
<div class="tab-pane" id="tabContent00-2" markdown="block">
Ubuntu 20.04
</div>
<div class="tab-pane active" id="tabContent00-3" markdown="block">
Ubuntu 22.04
</div>
</div>

## A. 查看系统信息

* 查看 cpu 信息

```bash
# CPU型号
cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c

# 物理 CPU 个数
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l

# CPU核数 (物理CPU个数 * 每个CPU的核数)
cat /proc/cpuinfo| grep "cpu cores"| uniq

# 逻辑CPU个数 (物理CPU个数 * 每个CPU的核数 * 超线程数)
cat /proc/cpuinfo| grep "processor"| wc -l
```

* 查看操作系统信息

```bash
# 查看操作系统内核信息
uname -a

# 查看操作系统发行版本
cat /etc/issue
lsb_release -a

# 查看hostname
hostname

# 网卡信息
ip a
```

* 安装的字体

```bash
# 所有字体
fc-list

# 中文字体
fc-list :lang=zh
```


## B. 安装 Ubuntu

* 下载安装镜像, 可以选择桌面版或服务器版
* 安装方法一: Rufus: 写入 U盘 GPT 分区类型, 用于 UEFI 模式启动
* 安装方法二: 优启通: 硬盘分区类型: DiskGenius 变为 GPT 类型
* **最后记得把EFI分区所在的硬盘作为第一启动硬盘 (Hard Drive BBS Priorities)**

{% include card.html type="danger" title="启动时报错" content="Failed to open \EFI\BOOT\mmx64.efi: Not Found" tail="<strong>解决方案:</strong> 在安装介质中把 `./EFI/grubx64.efi` 重命名为 `./EFI/mmx64.efi` 即可." %}

我们创建两个挂载点 `/boot` 和 `/`. 

|分区类型|挂载点|分区大小|
|:--|:--:|:--:|
| ext4 | /boot | 2G |
| ext4 | / | 剩余所有的 |


{% include card.html type="danger" title="双系统报错" content="原来装了 win + ubuntu 双系统, 由 ubuntu 引导. 然后在 win 下直接删了 ubuntu 的分区, 导致开机无法启动, 进入了 grub 命令行." tail="<strong>解决方案:</strong> 使用优启通制作一个U盘启动盘, 进入Win PE系统, 使用引导修复工具修复 win 系统的引导, 之后就能正常回到 win 的引导界面并能正常开机了." %}

### 0 配置下载源

使用 `vim` 编辑 `/etc/apt/sources.list` 文件, 注释掉原来所有的内容, 新增以下源 (不同的源选一个即可, 但注意版本 18.04/20.04/22.04 必须选对):

* 浙大源

<ul class="nav nav-tabs">
  <li><a data-tab href="#tabContentB0-1">18.04 (bionic)</a></li>
  <li><a data-tab href="#tabContentB0-2">20.04 (focal)</a></li>
  <li class="active"><a data-tab href="#tabContentB0-3">22.04 (jammy)</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane" id="tabContentB0-1" markdown="block">
```
deb https://mirrors.zju.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
```
</div>
<div class="tab-pane" id="tabContentB0-2" markdown="block">
```
deb https://mirrors.zju.edu.cn/ubuntu/ focal main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ focal-security main restricted universe multiverse
```
</div>
<div class="tab-pane active" id="tabContentB0-3" markdown="block">
```
deb https://mirrors.zju.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.zju.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
```
</div>
</div>


* 阿里云源

<ul class="nav nav-tabs">
  <li><a data-tab href="#tabContentB1-1">18.04 (bionic)</a></li>
  <li><a data-tab href="#tabContentB1-2">20.04 (focal)</a></li>
  <li class="active"><a data-tab href="#tabContentB1-3">22.04 (jammy)</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane" id="tabContentB1-1" markdown="block">
```
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```
</div>
<div class="tab-pane" id="tabContentB1-2" markdown="block">
```
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
```
</div>
<div class="tab-pane active" id="tabContentB1-3" markdown="block">
```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
```
</div>
</div>


### 1 网络设置

#### 1.1 联网

如果使用 **Ubuntu Desktop**, 那么联网可以通过 GUI 的方式填写 IP 等信息. 此处略去不表.

如果使用 **Ubuntu Server**, 那么有两种网络管理工具, `netplan` 和 `NetworkManager`. 二者我们需要选择其一. 

* 如果通过动态 IP 联网, 则什么也不需要配置

* 如果只配置静态 IP , 则使用 `netplan` 或者 `NetworkManager` 均可, 推荐前者.

* 如果需要配置 L2TP VPN, 则必须选择 `NetworkManager`

* 还可以使用安卓手机的网络共享功能临时上网. 安卓手机通过数据线连接到 Ubuntu 服务器, 手机移动网络设置中开启 `usb 网络共享`, 电脑共享手机网络


##### 1.1.1 使用 netplan 联网

如果有固定 IP, 则使用 netplan 来配置. 编辑 `/etc/netplan/*.yaml` 文件, 写入以下内容:

```
# This is the network config written by 'subiquity'
network:
  ethernets:
    eno1:                           # 网卡名称, 需要填写自己机器的, 通过 `ip a` 命令查看, 
      addresses: [192.168.1.2/24]   # 静态 IP 地址, 斜杠后面的是子网掩码, 24 表示 24 个 1, 即 255.255.255.0
      gateway4: 192.168.1.1         # 网关地址, 在 22.04 版本中不再需要这一行, 只需要指定下面的路由网关地址即可
      nameservers:
        addresses: [8.8.8.8]        # DNS 服务器地址
      routes:
      - to: 0.0.0.0/0               # 路由目标地址
        via: 192.168.1.1            # 路由网关地址
        metric: 0
  renderer: networkd                # 网络服务, networkd 和 NetworkManager 二选一, 使用 netplan 时需要指定为 networkd
  version: 2
```

{% include card.html type="info" content="我们编辑的文件 `/etc/netplan/*.yaml`, 在不同的系统中可能有不同的文件名." %}

使用以下命令应用配置:

```bash
# 检查配置的正确性
sudo netplan try

# 应用配置
sudo netplan apply
```

##### 1.1.2 使用 NetworkManager 联网

NetworkManager (简称 NM) 是另一种网络管理工具, 它支持更复杂的配置, 特别是 L2TP VPN. 我们首先介绍配置静态 IP 的方法. 使用 NM 之前, 我们修改 `/etc/netplan/*.yaml` 文件使用 NM 管理网络:

```
# This is the network config written by 'subiquity'
network:
  renderer: NetworkManager
  version: 2
```

然后编辑 `/etc/NetworkManager/NetworkManager.conf`, 修改为 `managed=true`:

```
[main]
plugins=ifupdown,keyfile

[ifupdown]
managed=true

[device]
wifi.scan-rand-mac-address=no
```

配置修改后我们需要重启网络服务

```bash
sudo systemctl restart NetworkManager
```

{% include card.html type="info" content="`NetworkManager` 使用命令行工具 `nmcli` 来管理配置. 有关 `nmcli` 的使用方法, 可以参考 `nmcli --help` 查看. " %}

接下来通过创建配置文件:

```bash
sudo nmcli c add type ethernet con-name wired ifname eno1 ipv4.addr 192.168.1.2/24 ipv4.gateway 192.168.1.1 ipv4.method manual
```

其中 `wired` 为自定义的连接名称, `eno1` 为网卡名称 (需要填写自己的). 注意修改自己的 IP 地址, 子网掩码和网关. 然后就会有个新的文件 `/etc/NetworkManager/system-connections/wired.nmconnection` 创建出来. 接下来我们编辑该文件, 并使得最终内容如下 (注意 uuid 值使用原本的就可以):

```
[connection]
id=wired
uuid=5de8cdc3-0595-4739-bf43-24f4ec666976   # 使用原来创建的默认值即可
type=ethernet                               # 有线网
autoconnect-priority=-998
interface-name=eno1                         # 网卡名称
permissions=
timestamp=1644651104

[ethernet]
mac-address-blacklist=

[ipv4]
address1=192.168.1.2/24,192.168.1.1         # IP 地址, 子网掩码和网关
dns=8.8.8.8;                                # DNS 服务器地址
dns-search=
ignore-auto-dns=true
method=manual

[ipv6]
addr-gen-mode=stable-privacy
dns-search=
method=auto

[proxy]
```

完成后启动该配置:

```bash
sudo nmcli connection up wired

# 可以使用缩写 c 代表 connection, nmcli --help 见详细用法
sudo nmcli c up wired

# 查看当前的配置
nmcli c
```

#### 1.2 L2TP VPN 连接 (校园网连外网)

在浙大内网的话, 按 [1.1 联网](#11-联网)的方法配置好 IP, 使用浙大源就可以直接通过 `apt` 从校园网直接安装软件了. 

但此时还没有外网, 还需要配置 L2TP VPN 才能连接外网. 我们使用 `NetworkManager` 提供的 L2TP 模块. 首先安装该模块:

```bash
# ubuntu server/desktop 需要安装
sudo apt install network-manager-l2tp

# ubuntu desktop 需要安装
sudo apt install network-manager-l2tp-gnome
```

**使用 Ubuntu Desktop**:

新建 L2TP VPN

* Name: ZJUVPN
* Gateway: <VPN 网关>
* User name: <用户名>
* Password: <密码>
* PPP Settings: 
  * 勾选 Allow BSD data compression
  * 勾选 Allow Deflate data compression
  * 取消勾选 Use TCP header compression
  * 取消勾选 User protocol field compression negotiation
  * 取消勾选 Use Address/Control compression

**使用 Ubuntu Server**: 

需要在终端中配置 VPN. 使用以下命令新建一个连接

```bash
sudo nmcli c add connection.id ZJUVPN type vpn vpn-type l2tp
```

其中 `ZJUVPN` 为自定义 VPN 名称. 然后编辑文件 `/etc/NetworkManager/system-connections/ZJUVPN.nmconnection`, 

```
[connection]
id=ZJUVPN
uuid=1fe18117-cbca-4f3e-9f3d-80664859b2f2   # 使用原来创建的默认值即可
type=vpn                                    # 连接类型为 vpn
autoconnect=false
permissions=
timestamp=1593424178

[vpn]
gateway=<vpn_address>                       # VPN 地址
mru=1400
mtu=1400
no-vj-comp=yes
noaccomp=yes
nopcomp=yes
password-flags=0                            # 这里设置为 0, 这样密码可以写在配置文件里, 方便自动连接
user=<username>                             # 用户名
service-type=org.freedesktop.NetworkManager.l2tp

[vpn-secrets]
password=<password>                         # 密码

[ipv4]
dns-search=
method=auto

[ipv6]
addr-gen-mode=stable-privacy
dns-search=
method=auto

[proxy]
```

启动 VPN 服务

```bash
sudo nmcli c up ZJUVPN

# 查看
nmcli c
```

我们希望开机后可以自动连接 VPN

**使用 Ubuntu Desktop**:
* 运行 `nm-connection-editor` 打开网络连接编辑面板
* 从 Ethernet(以太网) 列表中选择所使用的有线网或者从WLAN列表中选择所使用的无线网, 双击打开编辑面板
* 在 General(常规) 选项卡中勾选 Automatically connect to VPN when using this connection(使用此连接时自动连接到VPN), 并选择要开启的 VPN 

**使用 Ubuntu Server**:

编辑 `/etc/NetworkManager/system-connections/wired.nmconnection` 文件, 在下面的段落中增加一行 ZJUVPN 的 uuid 号:

```
[connection]
id=wired
uuid=5de8cdc3-0595-4739-bf43-24f4ec666976
type=ethernet
autoconnect-priority=-998
interface-name=eno1
permissions=
secondaries=1fe18117-cbca-4f3e-9f3d-80664859b2f2    # 这里填入 ZJUVPN 的 uuid 号即可.
timestamp=1644651104
```

重启系统测试效果. (亲测可行)

#### 1.3 双网卡设置

* 主节点: 一张网卡设置为外网ip， 另一张设置为内网ip. 内网网卡不设置网关.

```bash
network:
    ethernets:
        eno1:
            addresses: [10.76.2.232/21]
            gateway4: 10.76.0.10
            nameservers:
                addresses: [10.10.0.21]
            routes:
            - to: 10.0.0.0/8
              via: 10.76.0.1
              metric: 0
        eno2:
            addresses: [192.168.0.101/24]
    version: 2
```

* 设置内网的节点可以通过主节点访问外网: 开启ip_forward的内核转发, 重启后有效.

```bash
vim /etc/sysctl.conf
```

其中找到 `net.ipv4.ip_forward` , 赋值为 1.

* 设置路由表

```bash
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         _gateway        0.0.0.0         UG    0      0        0 eno1
10.0.0.0        10.76.0.1       255.0.0.0       UG    0      0        0 eno1
10.76.0.0       0.0.0.0         255.255.248.0   U     0      0        0 eno1
192.168.0.0     0.0.0.0         255.255.255.0   U     0      0        0 eno2
```

由于内网的请求源地址是内网地址, 目标地址是外网地址, 请求返回时外网地址不知道内网地址, 因此需要做网络地址转换(network address translation, NAT), 把内网地址修改为外网知道的网关地址. 数据包返回后目标地址是网关, 需要进一步转换为内网地址. 因此需要在 iptables 中添加 NAT 转发规则.

* 添加 iptables 的NAT转发规则

```bash
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o enp1s0 -j MASQUERADE
```

该规则的意思是 来自 192.168.1.0/24 经由 enp1s0 的数据包需要做 NAT 转换


### 2 安装常用工具

* 更新系统, 安装常用工具

```bash
sudo apt update; sudo apt upgrade
sudo apt install vim, git, curl, tmux, mlocate, net-tools
```

### 3 (可选) 修改默认文件夹

**方法一：**打开 系统设置-》语言支持 将“english”拖动到最上端，重启系统。重启后，会提示更新文件名称，更新后在将语言”中文“拖动到顶部，重启系统 。

**方法二：**

编辑 `~/.config/user-dirs.dirs` 文件
```bash
XDG_DESKTOP_DIR="$HOME/Desktop"
XDG_DOWNLOAD_DIR="$HOME/Download"
XDG_TEMPLATES_DIR="$HOME/Templates"
XDG_PUBLICSHARE_DIR="$HOME/Public"
XDG_DOCUMENTS_DIR="$HOME/Documents"
XDG_MUSIC_DIR="$HOME/Music"
XDG_PICTURES_DIR="$HOME/Pictures"
XDG_VIDEOS_DIR="$HOME/Videos"
```

**方法三：**打开终端，在终端中输入命令:

```bash
export LANG=en_US
xdg-user-dirs-gtk-update
```

跳出对话框询问是否将目录转化为英文路径,同意并关闭。在终端中输入命令:

```bash
export LANG=zh_CN
```

重新启动系统，系统会提示更新文件名称，选择不再提示,并取消修改。


### 4 Ubuntu 美化

参考文章 [https://www.cnblogs.com/feipeng8848/p/8970556.html](https://www.cnblogs.com/feipeng8848/p/8970556.html). 这里摘录一些.

美化工作主要围绕两个主题展开:
* 修改 Gnome 皮肤: [https://www.pling.com/s/Gnome](https://www.pling.com/s/Gnome)
* 安装 Gnome 插件: [https://extensions.gnome.org/](https://extensions.gnome.org/)

这里的 Gnome 是一个 Linux 下的桌面环境, Ubuntu 18.04 使用的是 v3.28; Ubuntu 20.04 使用的是 v3.36.

#### 4.1 安装 gnome-tweak-tool 和插件

```bash
sudo apt-get update
sudo apt-get install gnome-tweak-tool
```

安装完成后, 按 Win 键, 输入 tweak 搜索到 Tweaks 工具 (可以右键添加到收藏, 即固定到任务栏), 打开. 

此处 Tweaks 在 18.04 和 20.04 版本中略有不同, 但基本功能类似, 主要是用于调整任务栏和系统皮肤等等的属性, 读者可以自行探索. 我们重点推荐几个拓展(Extensions)

Tweaks 的拓展是通过浏览器插件来安装的. 首先安装拓展工具:

```bash
sudo apt-get install gnome-shell-extensions
```

安装完成后打开 Tweaks 的 Extensions 菜单, 可以看到已有的插件. 

现在我们要安装新的插件, 打开 Gnome 插件网址 [https://extensions.gnome.org/](https://extensions.gnome.org/), 搜索如下几个插件:

* User Themes: 用于修改系统皮肤
* Dash to Panel: 用于修改任务栏样式
* Topicon plus: 用于 wine, 后面再说

安装插件的方法很简单, 只需要打开每个插件页面的开关, 稍等片刻, 会弹出一个对话框, 点击 Install 即可. 安装完插件后在 Tweaks 的 Extensions 菜单可以看到.

#### 4.2 安装新皮肤

Ubuntu 的皮肤包含两部分, 主题和图标. 系统已有的主题存放在 `/usr/share/themes`, 图标存放在 `/usr/share/icons` 中. 我们要做的就是下载新的主题和皮肤, 把他们放入这两个系统文件夹. 

首先打开 Gnome 皮肤网站 [https://www.pling.com/s/Gnome](https://www.pling.com/s/Gnome), 点击左侧的 GTK 3/4 Themes 分类, 点击 Rating 标签, 选择一款自己喜欢的皮肤, 比如这款 [Orchis](https://www.pling.com/s/Gnome/p/1357889/). 点击 Files 标签, 可以看到有多种样式可以选择: 普通样式, 带 dark 后缀的暗黑风, 带 light 后缀的明亮风. 任意选择一个, 点击下载按钮, 稍等片刻就会下载一个压缩包 `Orchis-light.tar.xz`. 

```bash
# 解压
tar xvf Orchis-light.tar.xz

# 移动到主题文件夹
sudo mv Orchis-light /usr/share/themes
```

再打开 Gnome 皮肤网站, 点击左侧的 Full Icon Themes 分类, 点击 Score 标签, 选择一款自己喜欢的图标, 比如这款 [McMojave-circle](https://www.pling.com/p/1305429/), 任意选择一个图标样式下载. 

```bash
# 解压
tar xvf 01-McMojave-circle.tar.xz

# 移动到图标文件夹
sudo mv McMojave-circle /usr/share/icons
```

在 Tweaks 的 Apperence 菜单, 我们可以看到 Themes 下面有一系列的皮肤选项, 其中 Applications 和 Shell 下就包括我们新增加的 Orchis-light 皮肤, 在 Icons 菜单包含新增的 McMojave-circle 图标, 可以自行选择.


#### 4.3 开启夜灯 (护眼模式)

<ul class="nav nav-tabs">
  <li class="active"><a data-tab href="#tabContent1-1">18.04 (bionic)</a></li>
  <li><a data-tab href="#tabContent1-2">20.04 (focal)</a></li>
</ul>
<div class="tab-content">
<div class="tab-pane active" id="tabContent1-1" markdown="block">
在 GNOME Shell Extensions 市场中, 搜索 `night light slider` . 点击开关安装(注意点了开关后可能(后台)下载超级慢, 我的大概过了十几分钟才有反应. 他下载好安装的时候会弹出一个框, 所以点完了等着就行了, 可以做别的事情.)
</div>
<div class="tab-pane" id="tabContent1-2" markdown="block">
在系统设置的显示器选项中, 开启夜灯即可.<br/><br/><br/>
</div>
</div>



## C 代理设置

### 1 安装代理工具

安装 `shadowsocks-libev` (支持 `chacha20-ietf-poly1305` 加密方式, Python 版的 ss 不支持这个). 这里需要 Root 权限来安装.

```bash
sudo apt install shadowsocks-libev
```

填写ss配置文件 `~/tools/ssconfig/config.json` (路径无要求). 这个配置文件的内容需要由你的代理服务提供商来提供, 下面的仅为示例.

```bash
{
    "server": "12.34.56.78",
    "server_port": 6666,
    "password": "123456",
    "local_address": "127.0.0.1",
    "local_port": 1080,
    "method": "chacha20-ietf-poly1305",
    "timeout": 300
}
```

然后开启 sslocal 客户端:

```bash
ss-local -c ~/tools/ssconfig/config.json
```

这就开启了 socks 代理, 他会停留在终端前台. 但是我们终端一般使用 http/https 代理, 接下来**新开一个终端**完成后续配置. [2 proxychains 代理](#2-proxychains-代理-命令行配置)(推荐) 和 [3 privoxy 代理](#3-privoxy-代理-命令行配置) 选一个配置即可.

### 2 proxychains 代理 (命令行配置)

* 安装, 需要 Root 权限.

```bash
sudo apt install proxychains-ng
```

把默认配置文件 /etc/proxychains.conf 复制到 ~/tools/ssconfig/proxychains4.conf, 然后打开该文件, 修改最后一行配置项:

```conf
# 把下一行的内容注释掉
# socks4 127.0.0.1 9050

# 增加如下一行内容, 使用 socks5, 同时端口 1080 和 config.json 里的 local_port 对应
socks5 127.0.0.1 1080
```

接下来可以在想要使用代理的命令前加一个前缀 `proxychains4 -q -f /home/zjw_11821014/tools/proxychains4.conf`, 即可实现代理:

```bash
# 使用 curl 命令获取 `www.google.com` 的内容
proxychains4 -q -f /home/zjw_11821014/tools/proxychains4.conf curl www.google.com

# python 程序里访问互联网的程序实现代理
proxychains4 -q -f /home/zjw_11821014/tools/proxychains4.conf python main.py
```

### 3 privoxy 代理 (命令行配置)

proxychains 是使用代理时才调用, 而 privoxy 可以以服务的方式在后台运行, 然后通过环境变量的方式指定是否使用代理. 

* 安装 `privoxy`

```bash
sudo apt install privoxy 
```

{% include card.html type="info" content="没有 root 权限时, 可以使用 [brew](#homebrew) 来安装 `brew install privoxy`." %}

* 配置

编辑文件 `/etc/privoxy/config` (使用 brew 安装的话打开 `~/.linuxbrew/ETC/privoxy/config`), 首先搜索到 `forward-socks5t` 和 `listen-address` 这两行配置, 然后修改为如下的参数.

```conf
# 把本地 HTTP 流量转发到本地 1080 SOCKS5 代理
forward-socks5t / 127.0.0.1:1080 .
# 可选，默认监听本地连接
listen-address 127.0.0.1:8118
```

其中 `127.0.0.1:1080` 为 socks5 代理的地址, 最后的 `.` 不要丢掉. 而 `127.0.0.1:8118` 是 privoxy 的代理地址, 可以自定义端口, 也可指定为 `0.0.0.0:8118` 使其在局域网内可用. 

* 使用 `systemctl` 开启 privoxy 服务

```bash
sudo systemctl start privoxy
```

没有 root 权限时:
```bash
privoxy ~/.linuxbrew/etc/privoxy/config
```

* 测试

执行如下命令, 显示代理服务器的 ip 地址则表示配置成功.

```bash
http_proxy=http://127.0.0.1:8118 curl ip.gs
```


### 4 默认 PAC 模式(图形界面配置)

由于需要持续代理, 因此接下来配置pac模式. 首先安装

```bash
sudo pip3 install genpac		# 产生用户规则文件
touch ~/ssconfig/user-rules.txt
```


手动从 [https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt](https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt) 下载 `gfwlist.txt` 文件放在 `~/tools/ssconfig/gfwlist.txt` . 接下来产生 `autoproxy.pac` 文件

```bash
genpac --pac-proxy "SOCKS5 127.0.0.1:1080" --gfwlist-proxy="SOCKS5 127.0.0.1:1080" --gfwlist-local=/home/<username>/tools/ssconfig/gfwlist.txt --output="autoproxy.pac" --user-rule-from="user-rules.txt"
```

注意把上面的 `<username>` 替换为对应的值. 最后点击系统设置->网络->代理设置->自动，在输入框中输入`file:///home/<username>/tools/ssconfig/autoproxy.pac` 即可实现pac代理模式. (注意替换`<username>`)

* 可能的问题

以Ubuntu系统为例，我们通过`genpac`生成`autoproxy.pac`文件，然后点击系统设置->网络->代理设置->自动，在输入框中输入`file://绝对路径/autoproxy.pac`。设置好以后，Chrome应当可以自动切换网络，但是Chrome无法访问google的搜索引擎，而火狐浏览器可以正常访问。

* 解决方案

出现上面问题的主要原因是：Chrome移除对`file://`和`data:`协议的支持，目前只能使用`http://`协议。因此，我们打算使用`nginx`实现对本地文件的`http`映射。

安装 nginx

```bash
sudo apt install nginx
```

修改nginx.cnf配置文件 `/etc/nginx/nginx.conf`

在 `http{...}` 代码块中加入如下代码 (注意替换`<username>`)

```bash
server{
    listen 80;
    server_name 127.0.0.1;
    location /autoproxy.pac {
        alias /home/<username>/tools/ssconfig/autoproxy.pac;
    }
}
```

重启 nginx

```bash
sudo systemctl reload nginx
```

最后把`http://127.0.0.1/autoproxy.pac`填写到系统设置->网络->代理设置->自动代理中



## D. 修改系统设置

### 1 时间设置

* 修改时区. 时区是从 `/etc/localtime` 读取的, 而默认这是个软链接, 链接到哪个时区文件就是哪个时区.

```bash
# 查看时间, 发现时区是 UTC 的
date

# 删除原有的链接
sudo rm /etc/localtime

# 新建到上海时区的软链接
sudo ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 再次查看时区, 发现是 CST 即正确
date
```


### 2 修改hostname

```bash
# 1. 临时修改为abc, 修改后打开新终端显示, 重启系统失效
hostname abc

# 2. 永久修改为abc: 修改 /etc/hostname 中的值为 abc
#    重启系统
```


### 3 开机启动程序

参考资料: 

* [阮一峰: Systemd 入门教程: 命令篇](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html) 
* [阮一峰: Systemd 入门教程: 实战篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)

#### 3.1 原理简述

开机启动的服务分为两种, 系统服务和用户服务. 系统服务使用 root 权限启动, 用户服务使用用户权限启动. 在开机后登陆之前, 系统会扫描以下目录的服务并启动:

* [systemd/system 的服务](https://wiki.archlinux.org/index.php/Systemd_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)) (略去 `/run` 的)
  * `/usr/lib/systemd/system/` 
  * `/lib/systemd/system/` (软链接, 实际指向 `/usr/lib/systemd/system/`)
  * `/usr/local/lib/systemd/system/` (默认不存在该目录)
  * `/etc/systemd/system/` 

* [systemd/user 的服务](https://wiki.archlinux.org/index.php/Systemd/User#How_it_works) (略去 `/run` 的)
  * `/usr/lib/systemd/user/` 
  * `/usr/local/lib/systemd/user/` (默认不存在该目录)
  * `/usr/share/systemd/user/` (默认不存在该目录)
  * `/usr/local/share/systemd/user/` (默认不存在该目录)
  * `~/.local/share/systemd/user/` (默认不存在该目录)
  * `/etc/systemd/user/` 
  * `~/.config/systemd/user/` (默认不存在该目录)

{% include card.html type="info" content="可以使用 <code class='language-plaintext highlighter-rouge'>systemctl show --property=UnitPath</code> 命令查看扫描顺序, 优先级从低到高" %}

操作系统服务常用的命令如下:

```bash
# 启用系统服务
sudo systemctl enable xxx.service
# 禁用系统服务
sudo systemctl disable xxx.service
# 查看系统服务状态
sudo systemctl status xxx.service
# 启动系统服务
sudo systemctl start xxx.service
# 重启系统服务
sudo systemctl restart xxx.service
# 停止系统服务
sudo systemctl stop xxx.service
# 重新加载配置
sudo systemctl reload xxx.service

# 启用用户服务
systemctl --user enable xxx.service
# 其余命令类似: disable, status, start, stop
```

{% include card.html type="info" content="在操作<strong>用户服务</strong>时, 必须加 <code class='language-plaintext highlighter-rouge'>--user</code>, 否则会找不到服务, 并且必须去掉 <code class='language-plaintext highlighter-rouge'>sudo</code>, 否则会提示错误 Failed to connect to bus: No such file or directory. " %}

#### 3.2 自动运行: rc-local 服务

* 修改服务文件 `sudo vim /lib/systemd/system/rc-local.service`, 添加最下面的一段话

```
[Unit]
Description=/etc/rc.local Compatibility
Documentation=man:systemd-rc-local-generator(8)
ConditionFileIsExecutable=/etc/rc.local
After=syslog.target network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
RemainAfterExit=no
GuessMainPID=no

#这一段原文件没有，需要自己添加
[Install]
WantedBy=multi-user.target
```

这里的 `WantedBy=multi-user.target` 是把 `rc-local.service` 加入 `multi-user.target` 这一启动目标.

* 启用服务

```
sudo systemctl enable rc-local.service
```

该命令实际上是根据我们新添加的依赖关系, 建立了 `/etc/systemd/system/multi-user.target.wants/rc-local.service` 符号链接指向 `/lib/systemd/system/rc-local.service`. 系统在启动时会扫描 `multi-user.target.wants` 目录并启动其中的服务.

添加我们需要自启动命令到 `/etc/rc.local` 文件中 (与上面的配置中 `ExecStart` 的文件名对应), 该文件不存在时自己创建一个. 要注意这个文件里使用的命令都要写全路径(因为该文件是 root 执行的)

```
#!/bin/bash
#
# rc.local
#

/usr/local/bin/sslocal -c /home/<username>/tools/ssconfig/config.json -d start
```

* 为 `rc.local` 增加执行权限

```bash
sudo chmod +x /etc/rc.local
```

* 重启以测试是否成功.



### 5 (双系统) 修改开机默认系统

* 打开 grub 文件: `sudo vim /etc/default/grub` , 内容如下

```
# If you change this file, run 'update-grub' afterwards to update                                                                                                                                                                                        
# /boot/grub/grub.cfg.
# For full documentation of the options in this file, see:
#   info -f grub -n 'Simple configuration'

GRUB_DEFAULT=0
GRUB_TIMEOUT_STYLE=hidden
GRUB_TIMEOUT=10
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX=""

......
```

修改第6行, `GRUB_DEFAULT=0` 即为默认启动项, 0通常是 Ubuntu, 而 Windows 系统通常在下面, 需要在开机启动的时候数一下(从0开始数).

* 修改完毕后, 更新 grub: `sudo update-grub`  即可.



### 6 登录启动项

需要区分以下概念:

* **开机启动项**指的是针对于**所有**用户适用的启动程序.
* **登录启动项**指的是针对于**特定**用户适用的启动程序.



登录启动项的设置:

* Launcher中搜索 `Startup Application` , 并点击打开
* 直接增加启动项即可.



### 7 自定义锁屏/登录背景 (GDM)

* 从[这里](https://www.opendesktop.org/s/Gnome/p/1207015/)下载皮肤, 选择适合自己的系统, 如 "18.04 with asking password"
* 解压后, 阅读 readme, 然后按步骤先安装

  安装之前, 先自己备份一下 ubuntu.css :

  ```bash
  sudo cp /usr/share/gnome-shell/theme/ubuntu.css /usr/share/gnome-shell/theme/ubuntu.css.backup
  ```

  接下来开始安装:

  1. 执行 `./install.sh` 
  2. 寻找一个自己的喜欢的壁纸, 右键 -> script -> SetAsWallPaper (要输入密码), 这样, 程序 `~/.local/share/nautilus/scripts/SetAsWallpaper`  就会生成一张当前壁纸模糊后的版本放到 `/usr/share/backgrounds/gdmlock.jpg` , 可以自己检查一下是否正确. 
  3. 重启电脑完成
  4. 如果登录框的文字被遮挡了, 可以按照 readme 中的说明修改.
* 双屏的时候, 登录界面的背景图可能大小不正常, 此时使用 gnome-shell-extension 中的 `Lock screen background` 插件来修正, 开关在[这里](https://extensions.gnome.org/extension/1476/unlock-dialog-background/). 开关开启后(可能非常慢, 十几分钟), 从 Extension 中开启选项 `Open Unlock Dialog Background` 即可.



### 8 自定义 Grub 主题

* 从[这里](https://www.opendesktop.org/s/Gnome/p/1307852/)下载皮肤
* 解压后运行 `./install.sh` 安装


### 9 硬盘操作

#### 9.1 硬盘分区操作

```bash
# 查看已挂载磁盘
df -h

# 查看所有磁盘 (包括未挂载的磁盘)
sudo fdisk -l

# 查看某个磁盘
sudo fdisk -l /dev/sda

# 对某个磁盘操作
sudo fdisk /dev/sda
# 此时会进入操作模式, 按 m 显示所有可用命令

# 查看磁盘和分区之间的关系
sudo lsblk

# 查看磁盘分区的 UUID 号
sudo blkid
```

#### 9.2 格式化硬盘

如果是刚分好区的硬盘, 则在需要先格式化分区, 否则既无法查看UUID, 也无法挂载到某一个目录下.

```bash
sudo mkfs.ext4 /dev/sda1
```

#### 9.3 临时挂载 {#TempMount}

* 系统重启之后，挂载将会失效

```bash
sudo mount /dev/sda2 /media/disk1
```

#### 9.4 永久挂载

* 先查看各个磁盘挂载的信息 `sudo fdisk -l`, 并确认目标硬盘的位置 `/dev/sd*` 

* 查看该硬盘的UUID号 `sudo blkid` (使用UUID号可以避免硬盘更换位置后 `/dev/sd*` 发生变化, 而UUID不会变.)

* 修改 `/etc/fstab` , 在最后增加以下内容, UUID替换为上一步查出来的, 第二个参数为挂载路径, 第三个参数为分区格式, 这个可以从第一步的命令中查看, 最后的三个参数的含义见[这里](https://blog.51cto.com/lspgyy/1297432).

```bash
UUID=xxxxxxxxxxxxxxx /media/Win10OS ntfs defaults 0 0

UUID=xxxxxxx-xxxxxx-xxxxxx-xxxxxxx /data ext4 defaults 0 0
```


### 10 安装中文字体

* Ubuntu 单系统 (TODO) 

直接安装 Microsoft 字体

```bash
sudo apt update
sudo apt install ttf-mscorefonts-installer
# 安装完成后更新字体缓存
sudo fc-cache -f -v
```

* Win10/Ubuntu 双系统:

可以直接让 Ubuntu 系统读取 Win10 系统的字体: 

* 首先按照[临时挂载](#TempMount)的教程完成 Win10 硬盘的永久挂载(即开机自动挂载), 假设挂载的位置为 `/media/Win10OS` .
* 然后创建 Win10 字体文件夹在 Ubuntu 系统的软链接, 注意对应挂载位置.

```bash
ln -s <Win10挂载位置>/Windows/Fonts /usr/share/fonts/WindowsFonts
# 例子
ln -s /media/Win10OS/Windows/Fonts /usr/share/fonts/WindowsFonts

# 最后更新字体缓存
sudo fc-cache -f -v
```


## E. 常用软件和工具

### 1 常用软件 (界面操作) {#softwares}

* [Chrome](https://www.google.com/intl/zh-CN/chrome/)
* [搜狗拼音输入法](https://pinyin.sogou.com/linux/?r=pinyin)
* [网易云音乐](https://music.163.com/#/download), [QQ音乐](https://y.qq.com/download/download.html)
* [deepin-wine](https://www.cnblogs.com/zyrblog/p/11024194.html) 用于安装 [QQ 微信](https://github.com/zq1997/deepin-wine) 等
* [百度网盘](http://pan.baidu.com/download)
* [WPS](https://linux.wps.cn/) (Office 软件),  [把语言修改为中文](https://zhuanlan.zhihu.com/p/149773169)
* PDF阅读器
   * [福昕阅读器](https://www.foxitsoftware.com/pdf-reader/) (后面几个都不能很好的支持中文, 为避免折腾, 直接装福昕)
   * Okular
   * Master PDF Editor 5 (安装正版, 百度网盘Crack)
   * PDF Studio Viewer
* [Zotero](https://www.zotero.org/) (文献管理工具)
* [Typora](https://typora.io/) (Markdown 编辑器, 可实时渲染)
* [PyCharm](https://www.jetbrains.com/pycharm/)
* Filezilla (FTP 工具) (应用商店安装)
* VSCode (通过添加微软的源来安装, 见 [H.5](#vscode) 不要从应用商店安装, Ubuntu20.04应用商店安装的无法输入中文)
* [Flameshot](https://github.com/flameshot-org/flameshot) (截图/贴图工具), 从 release 中下载
* [gpick](https://github.com/thezbyg/gpick) (屏幕取色软件), apt 安装
* [Dropbox](https://www.dropbox.com/) (官网下载"下载器", 然后命令行里通过代理下载 dropbox: `proxychains dropbox start -i` )
* [Cascadia-Code](https://github.com/microsoft/cascadia-code) (微软提供的开源字体, 包含用于 Powerline 的字体和等宽字体)
* [transmissionbt](https://www.mls-tech.info/linux/ubuntu-18-setup-transmission/), [qBittorrent](https://www.qbittorrent.org/download.php)  (BT 下载工具)
* [FSearch](https://github.com/cboxdoerfer/fsearch) (Linux 下 Everything 的替代品)
* [GitKraken](https://www.gitkraken.com/) ()

### 2 进阶软件 (终端操作)

* htop (系统资源监控), apt 安装
* [Powerline 终端美化](/2021/03/29/Powerline)
* [onedrive](https://github.com/abraunegg/onedrive) (Onedrive 的 第三方 Linux 客户端)
* [Docker](https://docs.docker.com/engine/install/ubuntu/) ([安装和使用教程](https://www.yuque.com/jarvis73/pukm54/rwfl73))
* [Jellyfin](https://jellyfin.org/) (开源流媒体工具, 支持 Linux/Win10 部署, 全平台访问)
* [NextCloud](https://nextcloud.com/) (开源云盘工具, 支持 Linux 部署, 全平台访问)

### 3 有用的工具

#### 3.1 Homebrew {#homebrew}

brew 是 MaxOS 上的一款包管理工具, 我们也可以在 Ubuntu 上安装它. 当我们使用没有 sudo 权限的服务器时, 用 brew 可以很方便的在用户目录下安装许多常用的 linux 工具或软件.

安装 brew, 默认的安装目录是 `~/.homebrew`:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

安装完毕后可以直接使用如下命令安装软件, 比如 `privoxy`:

```bash
brew install privoxy
```

#### 3.2 Node.js

Node.js 是 javascript 在本地执行的工具, 可以使用 nvm 来管理版本和安装.

```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
source　~/.bashrc
nvm install node

# 安装软件包
npm install -g xxx
# 换源安装
npm install -g xxx --registry=https://registry.npm.taobao.org
# 永久换源
npm config set registry https://registry.npm.taobao.org
```

#### 3.3 Conda

Conda 是 Python 的环境管理工具. 从[这里](https://docs.conda.io/en/latest/miniconda.html)下载软件包后, 直接安装. 安装时注意填写安装路径.

```bash
sh Miniconda3-latest-Linux-x86_64.sh
```

### 4 其他工具

* tldr

[tldr](https://github.com/tldr-pages/tldr) 是个命令行工具, 用于常用命令的用法速查. 我们通常看到的写法是 **TL;DR**, 它是 "Too Long; Don't Read" 缩写, 其含义就是字面意思, 很多工具的文档写的又臭又长, 对于新手并不实用, 因此 `tldr` 提供了这些命令最常用的用法和解释. 安装方式如下

```bash
sudo apt install tldr
```

使用方法:

```bash
tldr tar

# ✔ Page not found. Updating cache...
# ✔ Creating index...
# 
#   tar
# 
#   Archiving utility.
#   Often combined with a compression method, such as gzip or bzip2.
#   More information: https://www.gnu.org/software/tar.
# 
#   - [c]reate an archive from [f]iles:
#     tar cf target.tar file1 file2 file3
# 
#   ......
# 
#   - E[x]tract a (compressed) archive [f]ile into the current directory:
#     tar xf source.tar[.gz|.bz2|.xz]
# 
#   ......
# 
#   - E[x]tract [f]iles matching a pattern:
#     tar xf source.tar --wildcards "*.html"
```

* bat

一种具有语法高亮和Git集成的cat命令. 参考[知乎文章](https://zhuanlan.zhihu.com/p/45853010).




## F. 有用的一些命令或脚本

### 1 Google Drive 下载

```bash
# 从Google Drive获取文件的唯一ID
# 替换FILEID 为文件ID, 有两处
# 替换FILENAME为准备保存的文件名
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt
```

### 2 代理链无法代理 nvm (bash 函数)

```bash
# 解决方案
# 1. 创建一个文件 nvm2
vim nvm2

# 2. 写入一下两行内容, 第一行相当于定义 nvm 函数, 第二行执行. 这样 nvm 函数就变成了 nvm2 文件.
# . /path/to/tools/nvm/nvm.sh
# nvm $@

# 3. 代理运行 nvm install node
proxychains4 nvm install node
```

### 3. ssh 断开后自动重连

* 使用 while 循环, 使 ssh 在断开后 10 分钟尝试自动重连

```
while true; do ssh <host_name>; date; sleep 10m; done
```


## G. 系统快捷键

| **按键** | **功能** |
| --- | --- |
| Super | 打开任务视图 |
| Super, 然后输入任意字符 | 系统搜索 |
| Super + L | 锁屏 |
| Super + D | 显示桌面 |
| Super + A | 显示应用程序菜单 |
| Super + Tab (Alt + Tab) | 在多个应用程序间切换 |
| Super + 箭头 | 适配应用程序到屏幕 |
| Super + M | 打开/关闭通知栏 |
| Super + 空格 | 切换输入法 |
| Alt + F2 | 运行控制台 |
| Ctrl + Alt + T | 打开一个新的终端 |
| Ctrl + Alt + 箭头 | 切换工作区 |


## H. 常见问题及解决方案

### 1 Flameshot 设置快捷键

在系统设置中, 进入键盘快捷键菜单, 点 + 自定义快捷键:
* Name: Flameshot_Screenshot_gui
* Command: flameshot gui
* Short Cut: F1

然后在系统托盘选择 Flameshot, 设置贴图快捷键为 F3

### 2 deepin-wine 微信

* 安装 

Ubuntu 20.04 下通过我们在 [E.1](#softwares) 给出的链接安装后无法通过图标打开. 可以通过安装[旧版微信]()解决该问题.

* 中文字体 (参考[deepin-wine 讨论区](https://github.com/zq1997/deepin-wine/issues/15))

Deepin-WeChat 的中文字体默认用的是"文泉驿微米黑", 所以在系统里安装该字体即可. 首先从[Github仓库](https://github.com/anthonyfok/fonts-wqy-microhei/blob/master/wqy-microhei.ttc) 下载该字体, 然后复制到字体目录病刷新字体缓存:

```bash
sudo cp wqy-microhei.ttc /usr/share/fonts
fc-cache -fv
```

重启微信. 

* 无法直接粘贴截图

安装 `libjpeg62:i386` 可解决

```bash
sudo apt install libjpeg62:i386
```

### 3 卸载自带的火狐浏览器

```bash
# 查找相关软件包
dpkg --get-selections | grep firefox
# 卸载
sudo apt purge firefox firefox-locale-en firefox-locale-zh-hans
```

### 4. Zotero 添加启动图标

解压下载的 Zotero 压缩包, 通过下面的命令为 Zotero 添加启动图标

```bash
mv Zotero_linux-x86_64 zotero
mv zotero ~/tools
cd ~/tools/zotero

./set_launcher_icon

sudo ln -s /home/<username>/tools/zotero/zotero.desktop /usr/share/applications/zotero.desktop
```

添加图标后稍等片刻即可从 Launcher 中搜索.

### 5. VSCode {#vscode}

* 安装

Ubuntu 20.04 下应用商店里安装的 VSCode 无法输入中文. 此处我们添加微软的apt源来安装([参考](https://cyfeng.science/2020/05/20/vs-code-chinese-input/)):

```bash
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt update && sudo apt install code
```

### 6. 英文语言下中文目录的排序

* 在系统语言设置为英文时, 中文目录的排序不是按拼音排的. 这时候我们需要修改 locale 中 `LC_COLLATE` 的值. 首先显示使用 `locale` 命令查看当前的语言配置(系统语言为英文, 区域设置为中国):

```text
LANG=en_US.UTF-8
LANGUAGE=en_US:en
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC=zh_CN.UTF-8
LC_TIME=zh_CN.UTF-8
LC_COLLATE="en_US.UTF-8"
LC_MONETARY=zh_CN.UTF-8
LC_MESSAGES="en_US.UTF-8"
LC_PAPER=zh_CN.UTF-8
LC_NAME=zh_CN.UTF-8
LC_ADDRESS=zh_CN.UTF-8
LC_TELEPHONE=zh_CN.UTF-8
LC_MEASUREMENT=zh_CN.UTF-8
LC_IDENTIFICATION=zh_CN.UTF-8
LC_ALL=
```

我们需要修改其中的 `LC_COLLATE="en_US.UTF-8"`.

```bash
sudo vim /etc/environment
```

在末尾添加 `LC_COLLATE=zh_CN.UTF-8`, 重启系统即可.

