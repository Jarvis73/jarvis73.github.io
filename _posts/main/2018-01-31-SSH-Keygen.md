---
layout: post
title: Windows 下 SSH-Keygen 使用方法
date: 2018-01-31 20:07:00 +0800
categories: Tools
excerpt: 本文记录了使用 OpenSSH 登陆远程服务器的方法, 并设置免密登陆. 同时给出了使用多个密钥登陆多个服务器的方法.
author: Jarvis
meta: Post
---

* content
{:toc}

**更新:**
* **2018-11-12** 增加可能的出现的问题及解决方案




## 1. 下载 Win32-OpenSSH

windows 版的 SSH 称为 Win32-OpenSSH,  可以从 [Github](https://github.com/PowerShell/Win32-OpenSSH) 下载. 可以选择下载最新版的 Release, 这样就不需要再编译源码了, 下载后可以直接使用.

解压后目录如下:
```
    FixHostFilePermissions.ps1
    FixUserFilePermissions.ps1
    install-sshd.ps1
    libcrypto-41.dll
    OpenSSHUtils.psd1
    OpenSSHUtils.psm1
    scp.exe
    sftp-server.exe
    sftp.exe
    ssh-add.exe
    ssh-agent.exe
    ssh-keygen.exe
    ssh-keyscan.exe
    ssh-shellhost.exe
    ssh.exe
    sshd.exe
    sshd_config
    uninstall-sshd.ps1
```

然后把该目录加入`用户环境变量`.

## 2. 生成密钥对

查看 `ssh-keygen` 的使用方法:

```bash
ssh-keygen --help
```

输出

```bash
usage: ssh-keygen [-q] [-b bits] [-t dsa | ecdsa | ed25519 | rsa]
                  [-N new_passphrase] [-C comment] [-f output_keyfile]
       ssh-keygen -p [-P old_passphrase] [-N new_passphrase] [-f keyfile]
       ssh-keygen -i [-m key_format] [-f input_keyfile]
       ssh-keygen -e [-m key_format] [-f input_keyfile]
       ssh-keygen -y [-f input_keyfile]
       ssh-keygen -c [-P passphrase] [-C comment] [-f keyfile]
       ssh-keygen -l [-v] [-E fingerprint_hash] [-f input_keyfile]
       ssh-keygen -B [-f input_keyfile]
       ssh-keygen -F hostname [-f known_hosts_file] [-l]
       ssh-keygen -H [-f known_hosts_file]
       ssh-keygen -R hostname [-f known_hosts_file]
       ssh-keygen -r hostname [-f input_keyfile] [-g]
       ssh-keygen -G output_file [-v] [-b bits] [-M memory] [-S start_point]
       ssh-keygen -T output_file -f input_file [-v] [-a rounds] [-J num_lines]
                  [-j start_line] [-K checkpt] [-W generator]
       ssh-keygen -s ca_key -I certificate_identity [-h] [-U]
                  [-D pkcs11_provider] [-n principals] [-O option]
                  [-V validity_interval] [-z serial_number] file ...
       ssh-keygen -L [-f input_keyfile]
       ssh-keygen -A
       ssh-keygen -k -f krl_file [-u] [-s ca_public] [-z version_number]
                  file ...
       ssh-keygen -Q -f krl_file file ...
```

解释一下:

* `-q` 表示静默生成密钥
* `-b bits` 指定密钥位数, 一般可选 1024, 2048, 4096
* `-t rsa` 指定生成 rsa 公私密钥对
* `-C comment` 附加该密钥的注释, 会添加到公钥的末尾
* `-f output_keyfile` 指定输出的文件名

以上是可以用到的, 其他的就先不管了.

执行命令

```bash
ssh-keygen -t rsa -b 4096 -C "some comments" -f C:/Users/<yourname>/.ssh/id_rsa
```

然后要求输入 `passphase` 时直接回车, 这样之后登陆时才不需要再输入任何密码, 再次回车, 生成结束, 输出的指纹和图可以不管.

此时在刚才指定的路径下得到两个文件 `id_rsa` 和 `id_rsa.pub` . 这里的 `id_rsa` 是私钥, 需要妥善保存(其实就是放着不动), `id_rsa.pub` 是公钥, 把公钥复制到远程电脑

```bash
scp C:/Users/<yourname>/.ssh/id_rsa.pub <user>@<remote server>:/home/<user>/.ssh
```

然后使用密码用 SSH 登陆到远程服务器 `ssh <user>@<remote server>`, 并执行以下操作:

```bash
$ mkdir .ssh                        # 创建文件夹 .ssh
$ cd .ssh                           # 进入文件夹 .ssh
$ touch authorized_keys             # 创建文件 authorized_keys
$ cat id_rsa.pub > authorized_keys  # 把公钥复制到 authorized_keys 中
$ exit
```

现在使用 `ssh <user>@<remote server>` 即可免密登陆.

### 附注 1

上文提到的 `<remote server>` 填入服务器 ip 地址或者域名, `<username>` 填入自己当前账户的用户名, `<user>` 填入登陆服务器的用户名.

### 附注 2

上面的文件名必须是 `id_rsa` 才可以按照上面的操作成功登陆, 因为 ssh 在登陆时会自动寻找 `.ssh` 文件夹下的 `id_rsa` 文件. 为了能够自定义名称(如果要使用不同的公私钥对登陆不同的服务器, 那么需要生成不同的密钥), 我们使用**配置文件**来指定登陆不同服务器所使用的不同密钥. 

在 `C:/Users/<username>/.ssh/` 下创建文件 `config`, 并用文本编辑器打开后填入

```
Host <short_name>
    HostName <remote server>
    IdentityFile F:/Users/<username>/.ssh/file1
    User <user>
    Port <port>
```

上面的 `<short_name>` 自己指定一个简单的名字, `<port>` 为远程服务器的 ssh 服务端口(如果需要则指定, 使用默认端口时去掉该行即可).

最后即可直接使用 `ssh short_name` 免密登陆服务器.

## 3. 可能的问题及解决方案

* **设置好了免密登录, 在登陆时仍然要求输入密码.** 
  1. 检查`config`文件的设置是否正确
  2. 检查远程电脑上的`authorized_keys`中的公钥是否正确
  3. 检查远程电脑上的文件夹权限(尤其是下面第一条容易忽略, 即`/home`下的用户文件夹要保证`others`**无写权限**)
    * `chmod o-w ~/`
    * `chmod 700 ~/.ssh`
    * `chmod 600 ~/.ssh/authorized_keys`
