layout: post
title: "NVIDIA 相关命令"
date: 2021-05-19 11:01:00 +0800
author: Jarvis
meta: Wiki_CUDA
hidden: true

* content
{:toc}

### 查看驱动版本

```bash
cat /proc/driver/nvidia/version

# NVRM version: NVIDIA UNIX x86_64 Kernel Module  435.21  Sun Aug 25 08:17:57 CDT 2019
# GCC version:  gcc version 7.4.0 (Ubuntu 7.4.0-1ubuntu1~18.04.1)
```

### 查看显卡占用情况

```bash
nvidia-smi
```

### 查看显卡文件占用情况

```bash
fuser -v /dev/nvidia*
```

### 查看nvidia-container-cli 信息

```bash
sudo nvidia-container-cli -k -d /dev/tty info
```

### 查看本机GPU拓扑

```bash
nvidia-smi topo --matrix
```

### cudnn 归档 

来源: [https://developer.nvidia.com/rdp/cudnn-archive](https://developer.nvidia.com/rdp/cudnn-archive)

### 驱动版本与CUDA版本对应关系. 

来源: [NVIDIA官网](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#cuda-major-component-versions)

| CUDA Toolkit                                      | Linux x86_64 Driver Version | Windows x86_64 Driver Version |
| ------------------------------------------------- | --------------------------- | ----------------------------- |
| CUDA 11.2.1 Update 1                              | >=460.32.03                 | >=461.09                      |
| CUDA 11.2.0 GA                                    | >=460.27.03                 | >=460.82                      |
| CUDA 11.1.1 Update 1                              | >=455.32                    | >=456.81                      |
| CUDA 11.1 GA                                      | >=455.23                    | >=456.38                      |
| CUDA 11.0.3 Update 1                              | >= 450.51.06                | >= 451.82                     |
| CUDA 11.0.2 GA                                    | >= 450.51.05                | >= 451.48                     |
| CUDA 11.0.1 RC                                    | >= 450.36.06                | >= 451.22                     |
| CUDA 10.2.89                                      | >= 440.33                   | >= 441.22                     |
| CUDA 10.1 (10.1.105 general release, and updates) | >= 418.39                   | >= 418.96                     |
| CUDA 10.0.130                                     | >= 410.48                   | >= 411.31                     |
| CUDA 9.2 (9.2.148 Update 1)                       | >= 396.37                   | >= 398.26                     |
| CUDA 9.2 (9.2.88)                                 | >= 396.26                   | >= 397.44                     |
| CUDA 9.1 (9.1.85)                                 | >= 390.46                   | >= 391.29                     |
| CUDA 9.0 (9.0.76)                                 | >= 384.81                   | >= 385.54                     |
| CUDA 8.0 (8.0.61 GA2)                             | >= 375.26                   | >= 376.51                     |
| CUDA 8.0 (8.0.44)                                 | >= 367.48                   | >= 369.30                     |
| CUDA 7.5 (7.5.16)                                 | >= 352.31                   | >= 353.66                     |
| CUDA 7.0 (7.0.28)                                 | >= 346.46                   | >= 347.62                     |

