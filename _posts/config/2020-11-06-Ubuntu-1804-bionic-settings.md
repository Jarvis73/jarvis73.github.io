---
layout: post
title: "Ubuntu 18.04 (bionic) 常用命令"
date: 2020-11-06 10:11:00 +0800
update: 2021-03-02
categories: Config
figure: /images/2020-11/ubuntu.png
author: Jarvis
meta: Post
---

* content
{:toc}



## A. 查看系统信息

* 查看 cpu 型号

```bash
 cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c
 
 #　8  Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz
```


* 查看操作系统内核信息

```bash
uname -a

#Linux Jarvis-LAB 5.0.0-36-generic #39~18.04.1-Ubuntu SMP Tue Nov 12 11:09:50 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```


* 查看操作系统发行版本

```bash
cat /etc/issue

# Ubuntu 18.04.3 LTS \n \l

lsb_release -a

# No LSB modules are available.
# Distributor ID: Ubuntu
# Description:    Ubuntu 18.04.2 LTS
# Release:        18.04
# Codename:       bionic
```


* 查看hostname

```bash
hostname

# Jarvis-PC
```


* 网卡信息

```bash
ip a
```


* 安装的字体

```bash
# 所有字体
fc-list

# 中文字体
fc-list :lang=zh
```


## B. 修改系统设置

### B.1 双系统中 Ubuntu 时间与 Windows时间对齐

```bash
sudo vim /etc/default/rcS
```

找到**UTC=yes**这一行，改成**UTC=no**


### B.2 修改hostname

```bash
# 1. 临时修改为abc, 修改后打开新终端显示, 重启系统失效
hostname abc

# 2. 永久修改为abc: 修改 /etc/hostname 中的值为 abc
#    重启系统
```


### B.3 启用网卡，修改网络参数

```bash
# 启用eno1网卡
sudo ifconfig eno1 up

# 修改静态ip地址 (18.04.3 server 版本)
sudo vim /etc/netplan/50-cloud-init.yaml
```

其中 `50-cloud-init.yaml`  内容为:

```yaml
network:
    ethernets:
        eno1:
            addresses: [192.168.0.110/24]
            gateway4: 192.168.0.101
            nameservers:
                addresses: [10.10.0.21]
    version: 2
```


### B.4 添加开机启动程序

参考资料: 

* 阮一峰: [Systemd 入门教程: 命令篇](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html) 
* 阮一峰: [Systemd 入门教程: 实战篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)



1. 在 `/lib` 中添加设置: `sudo vim /lib/systemd/system/rc.local.service` , 添加最下面的一段话

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
Alias=rc-local.service
```

2. 添加软连接到 `/etc` , 开机后会去这里找

```
sudo ln -s /lib/systemd/system/rc.local.service /etc/systemd/system/rc.local.service
```

3. 添加自启动命令: `sudo vim /etc/rc.local` . 要注意这个文件里使用的命令都要写全路径(因为执行该文件的时候 .bashrc 还没执行.)

```
#!/bin/bash                                                                                                                                                                                                                        
# 
# rc.local
# 
echo "hello" > /etc/test.log
```

4. 重启电脑



### B.5 开机连接 VPN

开机连接 VPN 需要单独设置一节, 因为 VPN 在 root 状态下登录是需要输入密码的(因为VPN的密码是属于用户的, 而不属于root). 因此为了开机启动 VPN, 我们需要把 VPN 密码以明文的形式写在该 VPN 的配置文件中以便开机后 root 可以登录 VPN. 
不妨假设 VPN 的名称为 ZJU. 
编辑文件: `sudo vim /etc/NetworkManager/system-connections/ZJU` , 可以找到如下的 `[vpn]` 段落.

```
[vpn]
gateway=10.5.1.7
mru=1440
mtu=1440
no-vj-comp=yes
noaccomp=yes
nopcomp=yes
password-flags=1
user=[你的VPN用户名]
service-type=org.freedesktop.NetworkManager.l2tp
```

然后需要做两处编辑:

1. 把 `password-flags=1` 修改为 `password-flags=1`
2. 在 `[vpn]` 段扩后面增加一段:

```
[vpn-secrets]
password=[你的VPN密码]
```

这样, 我们就可以在 root 下连接 VPN 了, 测试连接:

```
# 先手动断了 VPN
# root 命令行连接
sudo nmcli connection up ZJU
```

成功连接. 然后我们增加自动连接:

* 运行 `nm-connection-editor` 打开网络连接编辑面板
* 从 Ethernet(以太网) 列表中选择所使用的有线网或者从WLAN列表中选择所使用的无线网, 双击打开编辑面板
* 在 General(常规) 选项卡中勾选 Automatically connect to VPN when using this connection(使用此连接时自动连接到VPN), 并选择要开启的 VPN 

重启系统测试效果. (亲测可行)


### B.6 修改开机默认系统

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



### B.7 增加登录启动项

需要区分以下概念:

* **开机启动项**指的是针对于**所有**用户适用的启动程序.
* **登录启动项**指的是针对于**特定**用户适用的启动程序.



登录启动项的设置:

* Launcher中搜索 `Startup Application` , 并点击打开
* 直接增加启动项即可.



### B.8 自定义锁屏/登录背景 (GDM)

1. 从[这里](https://www.opendesktop.org/s/Gnome/p/1207015/)下载皮肤, 选择适合自己的系统, 如 "18.04 with asking password"
2. 解压后, 阅读 readme, 然后按步骤先安装

安装之前, 先自己备份一下 ubuntu.css :

```bash
sudo cp /usr/share/gnome-shell/theme/ubuntu.css /usr/share/gnome-shell/theme/ubuntu.css.backup
```

接下来开始安装:

   1. 执行 `./install.sh` 
   2. 寻找一个自己的喜欢的壁纸, 右键 -> script -> SetAsWallPaper (要输入密码), 这样, 程序 `~/.local/share/nautilus/scripts/SetAsWallpaper`  就会生成一张当前壁纸模糊后的版本放到 `/usr/share/backgrounds/gdmlock.jpg` , 可以自己检查一下是否正确. 
   3. 重启电脑完成
   4. 如果登录框的文字被遮挡了, 可以按照 readme 中的说明修改.
3. 双屏的时候, 登录界面的背景图可能大小不正常, 此时使用 gnome-shell-extension 中的 `Lock screen background` 插件来修正, 开关在[这里](https://extensions.gnome.org/extension/1476/unlock-dialog-background/). 开关开启后(可能非常慢, 十几分钟), 从 Extension 中开启选项 `Open Unlock Dialog Background` 即可.



### B.9 自定义 Grub 主题

1. 从[这里](https://www.opendesktop.org/s/Gnome/p/1307852/)下载皮肤
2. 解压后运行 `./install.sh` 安装



### B.10 挂载硬盘

#### B.10.1 临时挂载

* 系统重启之后，挂载将会失效

```bash
mount /dev/sda2 /media/disk1
```

#### B.10.2 永久挂载

* 先查看各个磁盘挂载的信息, 并确认目标硬盘的位置 `/dev/sd*` 

```bash
sudo fdisk -l
```

* 查看该硬盘的UUID号 (使用UUID号可以避免硬盘更换位置后 `/dev/sd*` 发生变化, 而UUID不会变.)

```bash
sudo blkid
```

* 修改 `/etc/fstab` , 在最后增加以下内容, UUID替换为上一步查出来的, 第二个参数为挂载路径, 第三个参数为分区格式, 这个可以从第一步的命令中查看, 最后的三个参数的含义见[这里](https://blog.51cto.com/lspgyy/1297432).

```bash
UUID=0A9AD66165F33762 /media/Win10OS ntfs defaults 0 0
```

### B.11 安装中文字体

#### B.11.1 Ubuntu 单系统 (TODO)

* 直接安装 Microsoft 字体

```bash
sudo apt update
sudo apt install ttf-mscorefonts-installer
# 安装完成后更新字体缓存
sudo fc-cache -f -v
```

#### B.11.2 Win10/Ubuntu 双系统:

可以直接让 Ubuntu 系统读取 Win10 系统的字体: 

* 首先按照 [B.10.2](https://www.yuque.com/jarvis73/pukm54/avi2oa/edit#UXEv9) 的教程完成 Win10 硬盘的永久挂载(即开机自动挂载), 假设挂载的位置为 `/media/Win10OS` .
* 然后创建 Win10 字体文件夹在 Ubuntu 系统的软链接, 注意对应挂载位置.

```bash
ln -s <Win10挂载位置>/Windows/Fonts /usr/share/fonts/WindowsFonts
# 例子
ln -s /media/Win10OS/Windows/Fonts /usr/share/fonts/WindowsFonts

# 最后更新字体缓存
sudo fc-cache -f -v
```

## C. 网络设置

### C.1 安装并配置 L2TP-VPN

```bash
apt install network-manager-l2tp
apt install network-manager-l2tp-gnome
```

### C.2 双网卡设置

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

#### C.2.1 设置内网的节点可以通过主节点访问外网

* 开启ip_forward的内核转发, 重启后有效.

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

### C.3 常用命令

* 命令行开启 VPN

```bash
# 文件地址 /etc/NetworkManager/system-connections
# ZJU 是 VPN 的名称
nmcli connection up ZJU
```


## D. 常用软件和工具

### D.1 常用软件(图形界面)

* Chrome, GNOME Shell Extension 用于桌面修改
* 搜狗拼音输入法 [https://pinyin.sogou.com/linux/?r=pinyin](https://pinyin.sogou.com/linux/?r=pinyin)
* 网易云音乐 [https://music.163.com/#/download](https://music.163.com/#/download)
* deepin-wine 用于安装 windows 软件 [https://www.cnblogs.com/zyrblog/p/11024194.html](https://www.cnblogs.com/zyrblog/p/11024194.html)
* Powerline 终端美化 [https://gist.github.com/Jarvis73/9a8aed3ed5175eb5aef3a2ff12bdf8b6](https://gist.github.com/Jarvis73/9a8aed3ed5175eb5aef3a2ff12bdf8b6)
* PyCharm
* Filezilla (FTP 工具)
* VSCode
* WPS (Office 软件)
* PDF阅读器
   * **福昕阅读器** (后面几个都不能很好的支持中文, 为避免折腾, 直接装福昕)
   * Okular
   * Master PDF Editor 5 (安装正版, 百度网盘Crack)
   * PDF Studio Viewer
* Zotero (文献管理工具)
* Typora (Markdown 编辑器, 可实时渲染)
* Dropbox (官网下载"下载器", 然后命令行里通过代理下载 dropbox: `proxychains dropbox start -i` )
* Flameshot (截图/贴图工具)
* gpick (屏幕取色软件)

### D.2 有用的工具

#### D.2.1 brew

brew 是 MaxOS 上的一款包管理工具, 我们也可以在 Ubuntu 上安装它. 当我们使用没有 sudo 权限的服务器时, 用 brew 可以很方便的在用户目录下安装许多常用的 linux 工具或软件.

安装 brew, 默认的安装目录是 `~/.homebrew`:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

安装完毕后可以直接使用如下命令安装软件, 比如 `privoxy`:

```bash
brew install privoxy
```

#### D.2.2 node

node 是 javascript 在本地执行的工具, 可以使用 nvm 来管理版本和安装.

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

#### D.2.3 tldr

[tldr](https://github.com/tldr-pages/tldr) 是个命令行工具, 用于常用命令的用法速查. 安装方式

```bash
npm install -g tldr
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

#### D.2.4 bat

一种具有语法高亮和Git集成的cat命令. 参考[知乎文章](https://zhuanlan.zhihu.com/p/45853010).


## E. 安装 Ubuntu

优启通: 硬盘分区类型: DiskGenius 变为 GPT 类型
Rufus: 写入U盘GPT分区类型, 用于UEFI模式启动. 写入完成后记得重命名 `./EFI/grubx64.efi`  为 `./EFI/mmx64.efi` 
**最后记得把EFI分区所在的硬盘作为第一启动硬盘 (Hard Drive BBS Priorities)**
现在假设总共有1T的硬盘, 8G内存

* `ext4` `/`     分区: 100G

* `ext4` `/boot` 分区: 2G(实际上200M就够用了)

* 交换分区:         16G(两倍内存)

* `ext4` `/usr`  分区: 200G

* `ext4` `/home` 分区: 剩余PC上一般不需要把/var和/tmp专门分区(不分区的话它们会自动和/home分区分在一起)

**问题解决:**
原来装了win + ubuntu双系统, 由ubuntu引导. 然后在win下直接删了ubuntu的分区, 导致开机无法启动, 进入了grub命令行. **解决方案: 可以制作一个U盘启动盘(比如老毛桃, 然后进入win8 PE系统, 使用引导修复工具修复win系统的引导, 之后就能正常回到win的引导界面并能正常开机了.)

### E.1 联网

以下方式依次考虑:

* 直接有线固定ip联网

* 使用PPTP VPN 联网

* 使用带ubuntu驱动的无线网卡

* L2TP VPN联网: 手机连接到电脑, 手机网络设置中开启usb以太网, 电脑共享手机网络, 然后apt安装 `network-manager-l2tp`  和 `network-manager-l2tp-gnome` 



### E.2 安装常用工具

```bash
sudo apt update
sudo apt upgrade
sudo apt install net-tools		# 安装完可以使用ifconfig, route
sudo apt install vim, git
```

### E.3 修改默认文件夹

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


### E.4 Ubuntu 界面修改

参考文章
[https://www.cnblogs.com/feipeng8848/p/8970556.html](https://www.cnblogs.com/feipeng8848/p/8970556.html)

#### E.4.1 夜灯(护眼模式)

在 GNOME Shell Extensions 市场中, 搜索 `night light slider` . 点击开关安装(注意点了开关后可能(后台)下载超级慢, 我的大概过了十几分钟才有反应. 他下载好安装的时候会弹出一个框, 所以点完了等着就行了, 可以做别的事情.)



## F 代理设置

```bash
pip install shadowsocks
# 注意要安装最新版, 目前是2.8.2
```

填写ss配置文件 `~/ssconfig/config.json` (路径无要求)

```bash
{
    "server": "12.34.56.78",
    "server_port": 6666,
    "password": "123456",
    "local_address": "127.0.0.1",
    "local_port": 1080,
    "method": "aes-256-cfb",
    "timeout": 300
}
```

然后开启 sslocal 客户端:

```bash
sslocal -c ~/ssconfig/config.json
# 如果需要后台运行, 则需要管理员权限
sudo sslocal -c ~/ssconfig/config.json -d start
```

如果出现错误: 

```
tools/miniconda3/lib/python3.8/lib-dynload/../../libcrypto.so.1.1: undefined symbol: EVP_CIPHER_CTX_cleanup
```

这是由于在openssl 1.1.0中废弃了 `EVP_CIPHER_CTX_cleanup()`  函数而引入了 `EVE_CIPHER_CTX_reset()`  函数所导致的则需要对openssl做一些修改:

* 根据错误信息定位到文件 ...../lib/python3.6/site-packages/shadowsocks/crypto/openssl.py
* 搜索 cleanup 并将其替换为 reset
* 重新启动 shadowsocks, 该问题解决


### F.1 proxychains 代理 (命令行配置)

#### F.1.1 安装

* 使用管理员权限

```bash
apt-get install proxychains
```

* 用户目录安装

```bash
# 源码编译
git clone https://github.com/rofl0r/proxychains-ng.git
cd proxychains-ng
./configure --prefix=./ --sysconfdir=./
make
# sudo make install
# sudo make install-config
wget https://raw.githubusercontent.com/haad/proxychains/master/src/proxychains.conf
```

然后在 ~/.bashrc 中加入 

```bash
# 为 proxychains4 指定别名, 这里只能指定别名, 不能使用上面 make install 安装出来的 proxychains4 命令, 因为会找不到 libproxychains4.so (也就是说只能直接运行build目录下的那个可执行文件)
alias pc4="/path/to/proxychains4"

# 设置配置文件路径
PROXYCHAINS_CONF_FILE="/path/to/proxychains-ng/proxychains.conf"
```

这里注意替换为上面 wget 下载到的文件路径. 然后 `source ~/.bashrc` 使配置生效.

#### F.1.2 配置

修改 `proxychains.conf` 中的最后一行

```
把 
socks4  127.0.0.1 9050 
修改为 
socks5  127.0.0.1 1080
```

#### F.1.4 测试

```bash
pc4 curl www.google.com

# 输出
# [proxychains] config file found: xxxxxxx/proxychains-ng/proxychains.conf
# [proxychains] preloading xxxxxxx/proxychains-ng/libproxychains4.so
# [proxychains] DLL init: proxychains-ng 4.14-git-23-g7fe8139
# [proxychains] Strict chain  ...  127.0.0.1:1080  ...  www.google.com:80  ...  OK
# <html>
# <head><title>302 Found</title></head>
# <body bgcolor="white">
# <center><h1>302 Found</h1></center>
# <hr><center>nginx/1.14.2</center>
# </body>
# </html>
```

完工.

### F.2 privoxy 代理 (命令行配置)

proxychains 是使用代理时才调用, 而 privoxy 可以以服务的方式在后台运行, 然后通过环境变量的方式指定是否使用代理. 

#### F.2.1 安装

* 使用 root 权限

```bash
sudo apt install privoxy 
```

* 不使用 root 权限 (使用 brew)
```bash
brew install privoxy
```

#### F.2.2 配置

编辑文件 `/etc/privoxy/config` (使用 brew 安装的话打开 `~/.linuxbrew/ETC/privoxy/config`), 首先搜索到 `forward-socks5t` 和 `listen-address` 这两行配置, 然后修改为如下的参数.

```
# 把本地 HTTP 流量转发到本地 1080 SOCKS5 代理
forward-socks5t / 127.0.0.1:1080 .
# 可选，默认监听本地连接
listen-address 127.0.0.1:8118
```

其中 `127.0.0.1:1080` 为 socks5 代理的地址, 最后的 `.` 不要丢掉. 而 `127.0.0.1:8118` 是 privoxy 的代理地址, 可以自定义端口, 也可指定为 `0.0.0.0:8118` 使其在局域网内可用. 

#### F.2.3 开启

* 使用 root 权限

```bash
sudo systemctl start privoxy
```

* 不使用 root 权限

```bash
privoxy ~/.linuxbrew/etc/privoxy/config
```

#### F.2.4 测试

执行如下命令, 显示代理服务器的 ip 地址则表示配置成功.

```bash
http_proxy=http://127.0.0.1:8118 curl ip.gs
```


### F.3 默认 PAC 模式(图形界面配置)

#### F.3.1 配置 PAC 模式

由于需要持续代理, 因此接下来配置pac模式. 首先安装

```bash
sudo pip3 install genpac		# 产生用户规则文件
touch ~/ssconfig/user-rules.txt
```


手动从 [https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt](https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt) 下载 `gfwlist.txt` 文件放在 `~/ssconfig/gfwlist.txt` . 接下来产生 `autoproxy.pac` 文件

```bash
genpac --pac-proxy "SOCKS5 127.0.0.1:1080" --gfwlist-proxy="SOCKS5 127.0.0.1:1080" --gfwlist-local=/home/<username>/ssconfig/gfwlist.txt --output="autoproxy.pac" --user-rule-from="user-rules.txt"
```

注意把上面的 `<username>` 替换为对应的值. 最后点击系统设置->网络->代理设置->自动，在输入框中输入`file:///home/<username>/ssconfig/autoproxy.pac` 即可实现pac代理模式. (注意替换`<username>`)

#### F.3.2 可能的问题

以Ubuntu系统为例，我们通过`genpac`生成`autoproxy.pac`文件，然后点击系统设置->网络->代理设置->自动，在输入框中输入`file://绝对路径/autoproxy.pac`。设置好以后，Chrome应当可以自动切换网络，但是Chrome无法访问google的搜索引擎，而火狐浏览器可以正常访问。

#### F.3.3 解决方案

出现上面问题的主要原因是：Chrome移除对`file://`和`data:`协议的支持，目前只能使用`http://`协议。因此，我们打算使用`nginx`实现对本地文件的`http`映射。

* 安装 nginx

```bash
sudo apt-get install nginx
```

* 修改nginx.cnf配置文件

```bash
vim /etc/nginx/nginx.conf
```

在 `http{...}` 代码块中加入如下代码


```bash
server{
    listen 80; #注意这里不用":"隔开，listen后面没有冒号
    server_name 127.0.0.1; #注意这里不用":"隔开，server_name后面没有冒号
    location /autoproxy.pac {
        alias /home/<username>/ssconfig/autoproxy.pac;
    }
}
```

 (注意替换`<username>`)

* 重启 nginx

```bash
sudo nginx -s reload
```

* 最后把`[http://127.0.0.1/autoproxy.pac](http://127.0.0.1/autoproxy.pac)`填写到系统设置->网络->代理设置->自动代理中

#### F.3.4 后台运行客户端

```bash
sudo sslocal -c ~/ssconfig/config.json -d start
```

## G. 有用的一些命令或脚本

### G.1 Google Drive 下载

```bash
# 从Google Drive获取文件的唯一ID
# 替换FILEID 为文件ID, 有两处
# 替换FILENAME为准备保存的文件名
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt
```

### G.2 代理链无法代理 nvm (bash 函数)

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


## H. 系统快捷键

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

