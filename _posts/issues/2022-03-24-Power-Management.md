---
layout: post
title: "Thinkpad X1C 睡眠耗电很快"
date: 2022-03-24 14:20:00 +0800
categories: Issue
author: Jarvis
meta: Post
excerpt: "TL;DR. 在 BIOS 中把电源管理从 Windows 10 修改为 Linux."
---

* content
{:toc}




## 1. 问题来源

由于常年需要使用笔记本开着大量的程序工作, 常年没有关电脑的习惯, 通常晚上直接锁定走人. 有时候把笔记本睡眠后带回家, 但是忘了插电, 过两天再打开就发现电量已经耗尽关机了. 

## 2. 原因分析

这种把电池榨干的睡眠方法可以说是毫无人性, 不知道微软为什么要和笔记本厂商联合起来搞这种完全不成熟的方案. 

网上一通搜索之后发现现代 Windows 系统 (比如 Win11, 或者 Win10 >=2004) 在强推 [Modern Standby](https://docs.microsoft.com/en-us/windows-hardware/design/device-experiences/modern-standby). 

> Windows 10 Modern Standby (Modern Standby) expands the Windows 8.1 Connected Standby power model. Connected Standby, and consequently Modern Standby, enable an **instant on / instant off** user experience, **similar to smartphone power models**. Just like the phone, the S0 low power idle model enables the system to stay connected to the network while in a low power mode.

意思就是想让电脑像手机一样, 在待机时仍然保持一种低功耗状态, 并且同时能够实现一定的功能 (比如联网接收即时消息). 但这几年下来用户实测效果相当不好, 然后就出现了上文说的待机两天电池榨干的情况. 

打开 Windows 管理员命令行, 输入 `powercfg -a` (CMD 输入 `powercfg /a`) 来获取当前的待机模式. 我的待机模式如下:

```text
此系统上有以下睡眠状态:
    待机 (S0 低电量待机)

此系统上没有以下睡眠状态:
    待机 (S1)
        系统固件不支持此待机状态。

    待机 (S2)
        系统固件不支持此待机状态。

    待机 (S3)
        系统固件不支持此待机状态。

    休眠
        尚未启用休眠。

    混合睡眠
        休眠不可用。
        虚拟机监控程序不支持此待机状态。

    快速启动
        休眠不可用。
```

可以看到有 S0-S3 这几种待机模式, 当前待机模式是 S0, 这就是前述的 "Modern Standby". 而在 S0 模式之前常用的是 S3 模式, 即 "CPU 停止工作, 内存持续通电以保持数据" 的一种状态. 

## 3. 解决方案

为了切换回 S3 模式, 我们需要从系统设置和 BIOS 设置两个层面检查:

* 如果系统是 Win10 2004, 那么无法改回 S3 模式, 可以考虑升级系统.  ([参考](https://www.reddit.com/r/Dell/comments/h0r56s/getting_back_s3_sleep_and_disabling_modern/).)

* 如果系统是 Win10 20H2 及以上. 首先尝试通过修改注册表, 在 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Power` 下面新建一个 `REG_DWORD` 类型的变量, 名称为 `PlatformAoAcOverride`, 值为 `0`. 重启系统, 查看当前待机模式. 如果为 S3 则成功, 否则删除该注册表项, 进入下一步.
  * 上面的 `PlatformAoAcOverride` 的意思是 Platform Always-on/Always-connect Override.

* 检查 BIOS 设置. 在 `Power` 相关的选项中寻找
  * 如果有 `ACPI` (Advanced Configuration and Power Management Interface) 相关的选项, 则切换为 S3 模式
  * 如果有 `Power Mode = Windows 10` 相关的选项, 则切换为 `Linux`. (我的 Thinkpad X1C 就是这种情况.) 这里的 `Linux` 模式就是 S3 模式. (不知道联想为啥要写的这么隐晦.)

  保存设置重启系统. 再次命令行里检查待机模式, 发现成功切换为 S3.

最后待机模式如下:

```text
此系统上有以下睡眠状态:
    待机 (S3)

此系统上没有以下睡眠状态:
    待机 (S1)
        系统固件不支持此待机状态。

    待机 (S2)
        系统固件不支持此待机状态。

    休眠
        尚未启用休眠。

    待机(S0 低电量待机)
        系统固件不支持此待机状态。

    混合睡眠
        休眠不可用。
        虚拟机监控程序不支持此待机状态。

    快速启动
        休眠不可用。
```

在 S3 待机模式下, 睡眠后发现显示屏关闭, 片刻后风扇停止, CPU应该停止工作了. 此时动鼠标和键盘都不能唤醒电脑, 按电源键可以唤醒, 大约两秒钟进入登陆界面. 

## 4. 其他

如果发现切换到 S3 模式之后, 还是无法成功睡眠, 则可以参考下面的链接排查原因.

[一劳永逸解决WIN10所有睡眠问题](https://zhuanlan.zhihu.com/p/93306740)

