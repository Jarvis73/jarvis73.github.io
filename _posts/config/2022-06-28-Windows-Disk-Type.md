---
layout: post
title: "GPT 分区设置"
date: 2022-06-28 11:35:00 +0800
categories: Config
author: Jarvis
meta: Post
---

* content
{:toc}

**TL;DR** 记录了 GPT 分区设置的常用命令, 以及 GPT 分区表类型和分区属性.



## 1. 查看硬盘和分区

* 使用 diskpart 工具

```powershell
# 使用管理员模式打开终端, 输入 diskpart 进入分区管理程序
diskpart

# 查看所有硬盘
list disk

# 选择硬盘编号
select disk 0

# 查看当前硬盘所有分区
list part

# 选择硬盘分区
select part 1

# 查看分区所有属性
detail part

# 修改分区属性, 属性值根据下面的表格自行判断
gpt attributes=0xXXXXXXXXXXXXXXXX
```

## 2. GPT 分区表类型[^1]

| Guid | 说明 |
|:----:|:----:|
| C12A7328-F81F-11D2-BA4B-00A0C93EC93B | EFI系统分区 |
| E3C9E316-0B5C-4DB8-817D-F92DF00215AE | 微软保留（MSR）分区 |
| EBD0A0A2-B9E5-4433-87C0-68B6B72699C7 | 基本数据分区 |
| 5808C8AA-7E8F-42E0-85D2-E1E90434CFB3 | 逻辑软盘管理工具元数据分区 |
| AF9B60A0-1431-4F62-BC68-3311714A69AD | 逻辑软盘管理工具数据分区 |
| DE94BBA4-06D1-4D40-A16A-BFD50179D6AC | 微软恢复分区 |
| BFBFAFE7-A34F-448A-9A5B-6213EB736C22 | Lenovo OEM分区（一键还原启动分区）[^2] |
| F4019732-066E-4E12-8273-346C5641494F | Sony OEM分区（一键还原启动分区）[^2] |

## 3. GPT 分区属性[^1]


| 属性值 | 说明 |
|:----:|:----:|
| 0x0000000000000001 | 将分区表示为必需分区 |
| 0x8000000000000000 | 当硬盘被挂载到另一台电脑时（或电脑首次检测到硬盘时）默认不分配盘符 |
| 0x4000000000000000 | 该分区无法被 Mount Manager 检测到, 也即无法被挂载 |
| 0x2000000000000000 | 该分区是另一个分区的 shadow copy |
| 0x1000000000000000 | 该分区为只读 |

* Windows下通常采用以下分区类型和分区属性组合：

| 分区 | Guid | 属性值 |
|:----:|:----:|:----:|
| 普通数据分区  | EBD0A0A2-B9E5-4433-87C0-68B6B72699C7 | 0x0000000000000000 |
| OEM分区      | 无特定GUID值，OEM决定                  | 0x8000000000000001 |
| WinRE分区    | DE94BBA4-06D1-4D40-A16A-BFD50179D6AC | 0x8000000000000001 |
| EFI系统分区  | C12A7328-F81F-11D2-BA4B-00A0C93EC93B  | 0x8000000000000001 |
| MSR保留分区  | E3C9E316-0B5C-4DB8-817D-F92DF00215AE  | 0x8000000000000000 |
| 恢复/备份分区 | DE94BBA4-06D1-4D40-A16A-BFD50179D6AC | 0x8000000000000001 |

* 用优启通制作的U盘安装系统后, 可能会启动后出现 Z 盘 (实际上是 EFI 系统分区), 默认属性值是 0x8000000000000000, 可以修改为 0x4000000000000000, 这样可以在系统启动时禁止挂载该分区. (直接移除盘符的话, 在重启系统后又会出现.)


## Reference

[^1]:
    [MDSN: ns-vds-create_partition_parameters](https://docs.microsoft.com/zh-cn/windows/win32/api/vds/ns-vds-create_partition_parameters?redirectedfrom=MSDN)

[^2]: 
    [MBR&GPT硬盘分区类型&属性详解（Win下更改/设置OEM/恢复分区方法）](https://blog.csdn.net/Blaider/article/details/48340627)
