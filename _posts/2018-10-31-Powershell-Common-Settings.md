---
layout: post
title: "Powershell: 定制一个优雅的终端"
data: 2018-10-31 21:49:00
categories: Tools
figure: https://docs.microsoft.com/media/hubs/powershell/powershell-features-windows.svg
author: Jarvis
meta: Post
---

* content
{:toc}

> [PowerShell](https://docs.microsoft.com/zh-cn/powershell/scripting/powershell-scripting?view=powershell-6) 是构建于 .NET 上基于任务的命令行 shell 和脚本语言。 PowerShell 可帮助系统管理员和高级用户快速自动执行用于管理操作系统（Linux、macOS 和 Windows）和流程的任务。
> 使用 PowerShell 命令可以从命令行管理计算机。 PowerShell 提供程序可让你访问数据存储（如注册表和证书存储），与你访问文件系统一样方便。 PowerShell 具有丰富的表达式分析器和完全开发的脚本语言。
> Powershell 是在 [Github](https://github.com/powershell/powershell) 开源的.




<div class="polaroid">
    <img class="cool-img" src="https://docs.microsoft.com/media/hubs/powershell/powershell-features-windows.svg" Shannon/>
    <div class="container">
        <a href="https://docs.microsoft.comzh-cn/powershell/scripting/powershell-scripting?view=powershell-6">Powershell</a>
    </div>
</div>

## Powershell

在 打开 Powershell 后会自动执行脚本 `文档\WindowsPowershell\Microsoft.PowerShell_profile.ps1`, 其中 `文档` 是指资源管理器首页的 `文档` 文件夹. 我们可以在脚本中定义预执行的命令, 和自定义函数. 下面先列举几个, 之后逐渐补充.

### 定制终端提示符样式

打开 powershell 后会自动执行 `prompt` 函数, 通过该函数可以定义如下的终端样式

```
@Jarvis F:\Users\10717
$
```

函数如下

```powershell
function prompt  
{
    $my_path = $(get-location).toString()

    # 定义了终端提示格式
    Write-Host ("@") -nonewline -foregroundcolor 'Green'  
    Write-Host ("Jarvis ") -nonewline -foregroundcolor 'Green'  
    Write-Host ($my_path) -nonewline -foregroundcolor 'DarkGreen'  
    $realLASTEXITCODE = $LASTEXITCODE
    Write-VcsStatus
    $global:LASTEXITCODE = $realLASTEXITCODE
    Write-Host ("")
    Write-Host ("$") -nonewline -foregroundcolor 'Cyan'  
    return " "  
}
```

* `Write-Host` 命令用于在终端输出字符串, 其中换行符为 `&apos;n`

### 激活 Anaconda 子环境

```powershell
Set-Alias act ActivatePythonEnv

function ActivatePythonEnv($version)
{
    & cmd /k "activate $version & powershell"
}
```

* `Set-Alias` 命令用于给函数名或命令起别名
* `act python3.6` 这类命令可以用于开启名称为 `python3.6` 的 conda 虚拟环境.

### 在终端开启代理服务器

我们假设代理服务器为 `http://127.0.0.1:1080`, 并且已经开启了系统代理(如pac模式, 仅能使用浏览器走代理, 而此时终端无法走代理), 那么以下函数可以在不需要开全局代理的情况下, 仅在当前终端开启和关闭代理:

```powershell
Set-Alias fly Set-Proxy-XXX
Set-Alias land Clear-Proxy-XXX

function Set-Proxy-XXX
{
    $proxy = 'http://localhost:1080'

    # temporary
    $env:HTTP_PROXY = $proxy
    $env:HTTPS_PROXY = $proxy

    # forever
    # [System.Environment]::SetEnvironmentVariable("HTTP_PROXY", $proxy, "User")
    # [System.Environment]::SetEnvironmentVariable("HTTPS_PROXY", $proxy, "User")
    
    Write-Host "`n   OPEN powershell proxy channel!`n"
}

function Clear-Proxy-XXX
{
    # temporary
    Remove-Item env:HTTP_PROXY
    Remove-Item env:HTTPS_PROXY

    # forever
    # [Environment]::SetEnvironmentVariable('http_proxy', $null, 'User')
    # [Environment]::SetEnvironmentVariable('https_proxy', $null, 'User')

    Write-Host "`n   CLOSE powershell proxy channel!`n"
}
```

* 通过命令 `fly` 开启终端代理
* 通过命令 `land` 关闭终端代理
