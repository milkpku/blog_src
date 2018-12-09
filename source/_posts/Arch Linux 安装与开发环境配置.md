
---
title: Arch Linux 安装与开发环境配置
author: Li-Ke Ma
date: 2018-11-08
category: Computer Engineering
---
笔者由于工作学习需要，时不时就要安装新系统，为了方便工作，避免重复查找，特此将一些安装中注意事项记录在此。
<!-- toc -->

---
# 我与 Arch 的相识
笔者第一次听到Arch这个名字的时候还是在2013年的大二。过完周末后的一天华仔跟我说，前几天累死了，跟着帆神装Arch，折腾了一天，最后他放弃了。我好奇问了一下，原来Arch是一种Linux，也就没有再细想。后来大三暑假去的纽约城市大学找“教授”做暑期科研，用的也只是Ubuntu，在Google的帮助下跌跌撞撞上的路。然而大三的暑期科研彻底改变了我的轨迹，回来后我决心转行计算机。转行计算机第一件事，就是要有一个Linux系统。当时的我也考虑到社区支持的原因，选择了Ubuntu，并一直使用到研一。

促使我开始关注Arch的因素主要是来自两个方面，一个是我的大学同学Catofes，还有一个是 Megvii 技术大神 Tim. Catofes是个胖宅Geek，平时就喜欢鼓捣一些酷炫Geek的东西。Sublime是他介绍给我的，Arch也是他多次安利给我的。看到他自己调教出来的动漫风Arch，别提我心里多痒痒了，但是惧于Linux的艰深难懂，我从来都只能望洋兴叹。后来在Megvii实习时候，和我一届的高中IO大神Tim就使劲安利我Arch，声称Arch拥有比Win10更强健的稳定性。当时的我正因为Ubuntu各种毛病头疼不已，于是抱着试一试的态度，把我2008年的电脑拿出来练手，居然照着安装说明把Arch装上了。后来食髓知味，尝到了Arch甜头的我就再也看不上其他任何Linux发行版了。

---
# 为什么选择 Arch
在选择Linux发行版时候，Ubuntu通常是第一考虑。持续第一的Linux桌面市场占有率，让Ubuntu成为Linux发行版中毫无疑问的统治者。庞大的用户群意味着巨大的社区，相应的配套支持也想必很好，遇到问题也有很多人可以问。但事实却不是这样的，这也是后来我转向Arch的原因。接下来我将解释为什么抛弃Ubuntu而选择Arch。

## 社区
Ubuntu拥有Linux中最大的用户社区，这一点毋庸置疑，但Arch拥有Linux中最活跃的用户社区。这个区别的根本原因是Ubuntu和Arch的社区组成不同。由于Ubuntu的安装过程比Arch友好很多，所以很多初入Linux的朋友都选择Ubuntu入手，这也导致Ubuntu用户群多为轻度新人Linux用户。而Arch的社区多为喜欢自己鼓捣计算机系统的Geek组成，他们积极维护Arch的论坛，Wiki和包源，热情回答新人的问题。所以笔者自使用Arch以来，遇到任何问题上Arch论坛搜索都能找到解答，并不担心因为社区小而无处问答。而有关Ubuntu系统的很多问题，通常都有头无尾，只能看到问题帖子之下一系列跟帖表示遇到了同样的问题，却并没有什么有用的解答。
## 稳定
Arch在用户合理设置下能够成为比Ubuntu更稳定的系统。曾经有一个梗，自从Win10出来之后，有人在网上提问，Win10和Arch谁的稳定性好？下面一致回复说，这还用问，Arch的稳定性Win10能比吗。我想，这种问题的主角，应该永远轮不到Ubuntu吧。使用过Ubuntu的朋友一定都经历过Ubuntu莫名其妙的错误和GUI卡死，笔者之前也被这些bug弄得很烦。这些bug的原因各式各样，但笔者感觉这些bug和Ubuntu整个软件体系的设计思路有一定的关系。由于Ubuntu的目标是一个大而全的Linux发行版，所以它预设了很多软件。而这些Linux软件有时有依赖库的冲突，为了解决这些冲突，Ubuntu在每一个发行版中进行了深度而复杂的设置，使得它们在发行版内部自洽。然而当更新一些软件或者更改一些设置后，这种平衡被打破，在一个地方的改动可能会影响到另一处看上去毫无关系的软件运行。而Arch的设计思想是最小化依赖，并让用户自行选择如何解决冲突。虽然听上去吓人，但在依赖库发生冲突时，最好的办法应该时去解决它而不是绕过，这样才能保证系统的一致性，从而达到较高的稳定性。

## 可定制性
Ubuntu虽大而全，但更新依赖Canonical公司，一些系统软件有复杂的依赖关系，想增添或删除都有导致系统不稳定的风险；而Arch没有版本一说，软件组合都由用户决定，并且滚动更新最新的软件。Ubuntu的软件配置由发行方Canonical决定，每一个版本中参数和软件间的互相依赖都很复杂，经常出现遇到问题用户无法修改，只能等待Canonical出更新或发布新版本。跟Ubuntu的大而全相比，Arch只提供Linux运行的最基本组件，剩下的部分由用户自行添加，所以Arch相比于Ubuntu有更好的定制性。而且由于Arch的最小依赖设计思路，增添删减软件都十分稳定，不会因为一处的改动影响另一处的软件。

此外，Arch不那么友好的安装过程，在笔者看来反而是一个优点。主要有两方面原因：第一，我可以在安装过程中深度定制安装细节，如何硬盘分区，如何boot等。第二，我可以在安装Arch过程中学习Linux的基础知识，深入理解计算机操作系统。

---
# 安装 Arch Linux
安装Arch Linux最好的说明是官网给出的 [Installation guide](https://wiki.archlinux.org/index.php/installation_guide)，接下来主要记录一些在 installation guide 之外需要注意的事项。

- **准备安装盘** 
[USB flash install](https://wiki.archlinux.org/index.php/USB_flash_installation_media) 笔者使用Rufus，十分方便。要注意U盘的盘符得是ARCH_XXXXYY，后面XY是Arch的镜像版本号，否则boot时找不到系统。

- **BIOS 设定**
启用UEFI boot，关闭Legacy boot。一定要关闭Secure boot，否则会启动失败。

- **硬盘分区** 
一般情况下笔者喜欢分为两个区，一个分给根目录，一个分给home目录用于数据储存。在此之前，要注意需要额外分一个区用于UEFI启动 [EFI system partition](https://wiki.archlinux.org/index.php/EFI_system_partition)，并格式化文件系统为fat32

- **Arch/Windows双系统**
将Windos的系统盘挂载到Arch中，安装os-prober工具，之后在grub-mkconfig时即可探测到Windows分区。

## 系统设置
安装完Arch后，它只是一个最小版的Linux发行版，没有GUI。如果是用于个人电脑，推荐安装gnome和gnome-shell
- **gdm**
[gdm](https://wiki.archlinux.org/index.php/GDM)是gnome桌面的启动引导，用于进入系统后启动gnome桌面。由于wayland与nvidia驱动有冲突，所以推荐关闭/etc/gdm/costum.conf下的wayland。
- **网络**
安装[networkmanager](https://wiki.archlinux.org/index.php/NetworkManager)，并在systemctl中启用NetworkManager.service。这样它会自动扫描可用网络并连接，不用每次使用dhcpcd。
- **ssh**
安装openssh，用systemctl开启sshd.service，之后即可通过ssh连接主机。

## 开发环境配置
- **Vim & YouCompleteMe**
Vim的风格有多种配置方法，笔者推荐一个叫 [The Ultimate vimrc](https://github.com/amix/vimrc) 的配置。

此外youcompleteme推荐自行下载编译安装，可参见笔者另一篇文章中对ycm的配置：[Windows下开发环境配置](https://blog.csdn.net/milkpku/article/details/79808117)

- **Oh-my-Zsh**
安装[oh-my-zsh]( https://github.com/robbyrussell/oh-my-zsh)，并安装[font-powerline](https://github.com/powerline/fonts)，

- **tmux**
  ```bash
  set -g prefix C-a
  unbind-key C-b
  bind-key C-a send-prefix
  ``` 

- **搜狗输入法**
搜狗输入法支持linux，需要借助fctix。除了安装fctix外，还需要安装对图形界面qt、gtk的支持。推荐安装fctix-im，里面包含所有qt和gtk工具，省去了不必要的麻烦。

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE4MDMxNjU1MDAsOTQwNDMzNzgzLDE3Nz
IwODUzMTUsLTEwMjc0NTg3ODIsMTE4MjAxMjM4MywtMjEyNjkx
MTMxOSwtMTM3MzQ5NDg5MiwtODEyMzEwMzk1LC0xMjUzODczND
QwLC0zNjY1Nzc2NDIsMzYwNDc0NzQ4LDQzOTQ5MDQ1MCwtMTQw
MjM1MjU2MiwxNjU2MjAzNzEzLDMzMTIzOTQ5MywxMTA0NDc5OT
g1LDM3NDQxOTAxMCwtMTQ0ODE0OTAzMCwtMzM1MTAwOTQyLC0y
NTczNTk5NzBdfQ==
-->