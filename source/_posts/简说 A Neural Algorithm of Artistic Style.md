---
title: 简说 A Neural Algorithm of Artistic Style
date: 2016-04-09
category: Computer Science
title_banner: https://prisma-ai-static.com/post/573b9cea-0585-4009-837e-1096a1a0685a/image

---

今天给大家介绍一项有趣的研究，Leon A. Gatys,团队做的让神经网络学画画的工作。(http://arxiv.org/abs/1508.06576)

![nnet的杰作](http://rack.1.mshcdn.com/media/ZgkyMDE1LzA4LzI5Lzc3L3RybnNmcm0xLjMyYmFhLmpwZwpwCXRodW1iCTEyMDB4OTYwMD4/0759661a/74b/trnsfrm1.jpg)

---
## 1. 什么是神经网络
[neural network](https://en.wikipedia.org/wiki/Artificial_neural_network)在机器学习领域中，结构模仿生物的神经网络，通过调整网络中的参数来达到近似拟合高维复杂数据。

比如最简单的线性划分，判断$Wx+b$是否大于0，就是单层的Logistic Regression。可以想象，在网络的层数不断增加，非线性成分越来越多时，对于高维空间的划分就越复xi杂qi精gu细guai。

神经网络学习的核心就是通过调整网络中的参数来达到一个目标函数的较优。目标函数cost可以是很多东西，比如预测和标注的互信息，或者简单的预测准确率、预测偏离的方差。注意这里是较优，因为神经网络太复杂了，参数空间也是很高维的，无法确定你找到的是不是一个最优，所以只能退而求其次，找到一些较优解。

之前在神经网络上的工作主要是受两方面的限制：第一，计算速度；第二，编程难度。计算速度不用说，现在业界大量使用GPU（NVIDIA的出货量都涨了20%），就充分说明了CPU的不实用。编程难度主要是体现在神经网络的训练过程中，需要用到目标优化函数关于网络参数的导数，而在有现在如Caffe,Torch,Theano等工具包之前，所有这些运算都是需要人手！写！比如前人为了方便手写，就提出了什么[back propagation](https://en.wikipedia.org/wiki/Backpropagation)，利用上一层的导数来计算下一层。

---
## 2. 神经网络工程实现的关注点
神经网络在工程上实现起来，有很多细节决定了神经网络的成败，个人觉得最重要的是三个点：目标函数（loss function），网络结构设计，初始参数设置。

 - 设定好目标函数就是找准优化目标，知道什么结果是我们想要的；
 - 设计好神经网络的结构，就使得其对于给定的问题具有结构上的先验优势（比如在图像处理中使用conv nnet而不使用full connected）；
 - 设置好初始参数，防止在学习初期就掉到坑里去了。当然，还有好好的洗数据。

比如现在讨论的art style问题，核心就是定义什么是“像”。那么就需要找到一个描述两个图片像不像的函数，或者说定义一个“距离”，使得这个函数越小，两张图片的风格就越像。Google团队的核心工作就是找到了一个比较好的描述“像不像”的这样一个函数or统计量。

---
## 3. Art Style 问题的核心算法
如何描述两张图像不像，最暴力的办法就是直接算矩阵距离。再进一步，可以有一个思路是找出两张图的feature，然后比较feature之间的距离。art style的核心问题有两个：两个图像在内容上像不像、两个图像在风格上像不像。需要注意的是，我们找到的描述风格的量一定要是scale free的，否则不同大小的图之间就无法比较了。

Google的团队利用了一个前人训练好的网络，VGG网络，来获取图像的feature。VGG模型在ImageNet数据库中训练而成，我们关注的是它结构中的5个卷积层。因为它是一个训练好的而且每层的feature都是有较好性质的网络，所以直接提取它对图像进行识别时的中间层为图像的feature即可。

在VGG图像识别的中间层，数据为一个(c, h, w)的3维张量，对应c个feature，每个feature为一张(h, w)的二维数组，由于卷积神经网络的结构特性，feature中每个元素对局部的图像都有描述作用。Google团队就利用了这一点，使得对于图像feature的表征有了现成的工具。

我们需要将图像$x$通过学习$y$的风格，得到图像$z$，则我们需要定义函数$L_{content}(z; x)$描述$z$和$x$内容的差异，函数$L_{texture}(z; y)$描述$z$和$y$风格的差异，然后优化$z$。

设$F^{(n)}_{kj}$为第n层第k个feature的第i个元素(这里将(h, w)的二维数组视为一个1维向量)，则定义两个图像内容上是否相像(content loss)就有：
$$
	L_{content}(z; x) = \sum_{l,i,j} \alpha_l (F^{(l)}_{ij} - P^{(l)}_{ij})^2
$$
$F, P$分别为需要转化的图像$x$和转化后的图像$z$经过VGG时的中间层。

接下来定义两个图像风格上是否相似，这里在content loss上再进了一小步，就是使用了Gram矩阵 $G^{(n)}_{ij} = \sum_k F^{(n)}_{ik} F^{(n)}_{jk}$,即认为相似的风格可以用不同feature间的相关度表示。于是定义了两个图像风格上是否相似(texture loss)：
$$
L_{texture}(z; y) =\sum_{l,i,j} \frac{w_l}{4M_l^2N_l^2} (G^{(l)}_{ij} - A^{(l)}_{ij})^2
$$
$G, A$ 分别为被模仿的图像$y$和转化后的图像$z$计算出的Gram矩阵

所以需要优化的cost函数为：
$$
L(z; x, y) = \alpha L_{content}(z;x) + \beta L_{texture}(z;y) 
$$
工作做完了。

什么？没有看懂？回去再读一遍。
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE5NTEwMDg4NjcsLTE4OTY1MjI0ODgsMT
Y1MzY0MzYwOV19
-->