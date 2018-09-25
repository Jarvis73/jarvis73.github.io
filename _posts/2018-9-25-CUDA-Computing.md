---
layout: post
title: GPU 编程 (一) -- CUDA 的安装和环境的配置
date: 2018-09-25 20:07:00
author: Jarvis
meta: Wiki_CUDA
---

* content
{:toc}

> 今天终于配好了台式, 装好了 NVIDIA 的显卡, 然而没钱只能装个 GTX 1050Ti, 4G 显存, 对于 CUDA 入门(和打游戏)也差不多够用了. 穷人是不能有什么奢求的, 对! 虽然是前言, 但还是像多吐槽两句, 自己配台式是真心折腾, 甚至最后显示器不亮, 只能去找电脑店老板了......要了50块, 真地心痛, 然鹅最后老板还不告诉我哪里没装对, 我拆开机箱看了下只有内存条被移动到了第二个插槽(原来我装的第四个插槽). 唉, 不管了, 反正现在能用了, 穷人连个机械硬盘都买不起, 就先拿个 256G 的固态凑合几个月吧. 下面开始正文, 配置 CUDA+VS2017 环境.

## 简介

我假设我们的电脑是全新的.

1. 安装 Visual Studio 2017
2. 安装 CUDA 9.2
3. 运行示例代码

这里要解释一下, 上面四步顺序不能换, 因为安装 CUDA SDK 时它会自动检测到 VS 并且安装相应的插件, 1-2两步反过来的话 VS 中就没有 CUDA 插件了. 另外现在 CUDA 10.0 已经发布了, 然而 2.1G 的文件我下了四五次都是在最后几秒钟被远程服务器中断了, 最终放弃, 改装 9.2.


## 安装 Visual Studio 2017

从 [VS 官网](https://visualstudio.microsoft.com/zh-hans/downloads/?rr=https%3A%2F%2Fwww.google.com%2F) 下载安装包, 体积很小, 是一个在线安装包. 打开进入功能选择界面, 选择以下功能:

* 从**工作负载**标签下选择`使用C++的桌面开发`
* 从**单个组件**标签下增加`Windows 8.1 SDK`(在SDK、库和框架这一堆里面). 增加该项是为了补充类似于 `stdio.h` 这类库函数, 在 Windows 10 SDK 中以 `.h` 结尾的 `C 库函数` 均被去除了.

两项选择后总大小大约6~7G(实际上需要下载的大约2~3G), 然后选择边下边装即可, 网速好的话很快就装完了. 这里我们特地给出默认的安装路径以便将来寻找: 

|项|路径|
|:-----:|:-----:|
|Visual Studio IDE|`C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional`|
|下载缓存|`C:\ProgramData\Microsoft\VisualStudio\Packages`|
|共享组件、工具和SDK|`C:\Program Files (x86)\Microsoft Visual Studio\Shared`|


## 安装 CUDA 9.2

从 [CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive) 下载 9.2 版本的 CUDA 工具包, 大约 1.5G. 打开后一路下一步并安装完成, 其中可以留意一下针对 Visual Studio 的插件. 安装遇到错误自行 Google, 反正我没遇到(除了下载时网不好经常断).


安装完成后安装程序会自动在**系统环境变量**中加入`CUDA_PATH`和`CUDA_PATH_V9_2`这两个环境变量. 然后我们也给出默认安装路径以备寻找: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.2`


## 运行示例代码

#### 1. 下载 `CUDA by Example`

可以下载这本书和配套代码, [链接附上](https://developer.nvidia.com/cuda-example). 

<div class="polaroid">
    <img class="cool-img" src="/images/CUDA/0cuda_by_example.jpg" Shannon/>
    <div class="container">
        <p>NVIDIA 官方提供的入门书: CUDA by Example</p>
    </div>
</div>

#### 2. 创建 VS 项目

打开 VS 2017, 新建空项目. 从菜单打开视图 --> 属性管理器 --> 右击项目 --> 添加新项目属性表 --> 取名, 确定 --> 双击新建的属性表, 修改并填写以下属性:

* VC++目录 --> 可执行文件目录 --> 添加 `$(CUDA_PATH)\bin`
* VC++目录 --> 包含目录 --> 添加 `$(CUDA_PATH)\include`
* VC++目录 --> 库目录 --> 添加 `$(CUDA_PATH)\lib`
* 链接器 --> 输入 --> 附加依赖项 --> 添加 `cudart.lib`
* 连接器 --> 系统 --> 子系统 --> 设为 `控制台(/SUBSYSTEM:CONSOLE)`. 该项使得控制台程序结束时停留, 而非一闪而过.

最后确定保存. 以后新建 CUDA 项目后在相应平台(Win32/x64, Debug/Release)的属性文件夹下导入该属性表即可.

#### 3. 修改项目属性以运行 CUDA 编译器

解决方案资源管理器中, 

* 右击项目 --> 生成依赖项 --> 生成自定义 --> 勾选 `CUDA 9.2(.targets, .props)`. 注意: 这里只有按照正确的顺序正确的安装了 CUDA 9.2 之后才会有该选项.
* 添加现有的 CUDA 源代码文件 `..cuda_by_example/chapter03/hello_world.cu`
* 右击 `hello_world.cu` --> 属性 --> 常规 --> 项类型 --> 选择 `CUDA C/C++`. 注意: 只有第一步勾选了 `CUDA 9.2` 的生成自定义选项后这一步才有 `CUDA C/C++` 这个选项.
* 菜单 --> 生成 --> 生成解决方案. 注意: 这里可能会报错, 看下面的解决方案.
* 菜单 --> 调试 --> 开始执行(不调试)

报错信息:

```
unsupported Microsoft Visual Studio version! Only the versions 2012, 2013, 2015 and 2017 are supported!
```

这里是由于 VS 2017 在更新的时候修改了内部版本号, 当前的内部版本号是定义在宏 `_MSC_VER` 中的, 可以在 VS 中新建一个 VC++ 项目, 并新建 `cpp` 文件, 写个 `main` 函数, 输出即可 `std::cout << _MSC_VER << std::endl;` . 我输出的是 `1915`. 接下来我们查看 CUDA 源码(路径不重复写了)中的文件 `../CUDA/v9.2/include/crt/host_config.h`, 在第131行有一个判断 `#if _MSC_VER < 1600 || _MSC_VER > 1913`, 这里因为 `1913` 比我的 `VS 1915` 版本号低, 所以才会报错. 源码这里改为 `> 1915` 即可. 


到此环境配置完成. 如有疏漏, 后续遇到了再补充.

