---
title:  C++线性运算库梳理
date: 2017-12-16 15:15:03
category: Computer Science
tags: c++
abstract: 由于笔者在学习工作中需要大量用到c++线性运算库进行科学计算，在配置环境的摸索过程中趟了不少坑，所以写下常用工具以及配置心得，以备日后查阅，也方便新来者快速上手。
title_banner: http://nebula.wsimg.com/44531cdeed26e277e8fb54aad1292590?AccessKeyId=C9CD95C132B0D8F5C093&disposition=0&alloworigin=1

---

<!-- toc -->

由于笔者在学习工作中需要大量用到c++线性运算库进行科学计算，在配置环境的摸索过程中趟了不少坑，所以写下常用工具以及配置心得，以备日后查阅，也方便新来者快速上手。

## C++线性运算库
c++中可用的线性运算库有很多种，笔者也见过很多做计算机的同仁不满意现有的库，自己实现线性运算库。然而笔者并不打算自己重新造轮子，毕竟计算机领域的一大优势就在于我们能通过开源的优秀代码，站在别人的肩膀上更进一步。在做过一些调查以后，笔者主要介绍两个c++线性运算库，其中 Eigen 是笔者工作生产中常用的库。

### Eigen
[Eigen](http://eigen.tuxfamily.org) 是一款十分著名的线性运算模板库， Eigen 支持稠密矩阵(Dense Matrix)和稀疏矩阵(Sparse Matrix)运算，并内置实现了对两种矩阵的求解器(Solver)。使用 Eigen 十分简单，因为是模板库，所以只需要将头文件拷入 include 目录即可，缺点是编译时比较费时。Eigen 的稠密矩阵运算在某些平台上的性能甚至接近 Intel$^®$ MKL [^1]。虽然 Eigen 的求解器从效率来讲并不算最好，但将其作为矩阵容器是一个很好的选择，在求解大型问题时再通过连向诸如 SuiteSparse 等顶级求解器即可。TensorFlow 即使用了Eigen。在 3.3 之后，Eigen 引入了对其他 BLAS 的接口，支持了包括 MKL，OpenBLAS 等高性能库，使得其性能还可能更进一步提高。

### Armadillo
[Armadillo](http://arma.sourceforge.net/) 是一款年轻的线性运算模板库，拥有友好的交互接口，十分贴近 matlab 风格，迭代速度也很快，笔者十分喜欢。并且可以使用其他 BLAS 实现如 OpenBLAS 作为计算后端，实现稠密矩阵运算的加速，在某些评测下甚至超过 Eigen。但是笔者之所以没有选择它，是因为笔者的项目对 Cholmod 分解要求很高，需要连接 SuiteSparse 进行求解，而可惜 Armadillo 的稀疏矩阵求解只能连向 SuperLU，因此笔者只能转向 Eigen。

## 稀疏矩阵求解库
Eigen 与 Armadillo 提供了较好的矩阵容器以及 C++ 调用接口，也实现了稠密矩阵和稀疏矩阵的简单求解，但是对于一些特定问题的求解并不是最优，比如高性能计算界研究了很多年的稀疏矩阵求解(Sparse Matrix Solver)。对于标准的 LU/QR/Cholesky 分解，高性能计算界已经有成熟高效的计算库如 SuiteSparse。所以在追求计算速度的科研领域，还是需要掌握这些更复杂的求解库的使用。

### SuiteSparse
[SuiteSparse](http://faculty.cse.tamu.edu/davis/suitesparse.html) 是现在科学界和工业界最强大的基于 BLAS/LAPACK 的多种稀疏矩阵求解算法合集，其中包括了LU分解算法(UMFPACK)， Cholesky分解(CHOLMOD)， QR分解算法(SPQR)等算法的实现。Matlab 的矩阵求解就是使用的 SuiteSparse 的实现，可以说是相当的强大。笔者工作中就极度依赖 SuiteSparse 提供的加速，比如使用 Eigen 的自带稀疏矩阵求解器就要比使用 SuiteSparse 慢一两个数量级。

### SuperLU
[SuperLU](http://crd-legacy.lbl.gov/~xiaoye/SuperLU/) 针对LU分解所写的库，和 UMFPACK 具有相同的使用范围，在各测试集上表现也各有优劣，笔者较为推荐 UMFPACK，因为可以在 SuiteSparse 中一并安装。

## BLAS 与 LAPACK
在涉及线性运算的领域，几个术语BLAS, LAPACK是绕不过的，笔者最开始时是各种懵逼，在安装线性运算库时各种踩坑，之后在实践中才慢慢摸索清楚它们之间的关系。笔者就将我的理解总结在下面，如有笔误也欢迎指正。

### BLAS LAPACK 的含义与历史
[BLAS](http://www.netlib.org/blas/) 全称为 Basic Linear Algebra Subprograms，是一个API标准，其设计目的是为了提供对向量和矩阵计算的基础支持，具体分为BLAS1(向量间运算)，BLAS2（矩阵与向量计算），BLAS3（矩阵与矩阵计算）。设计BLAS的原因是由于不同的计算机硬件架构（总线、各级缓存、CPU寄存器数量），逻辑上相同的运算在写为机器码过程中有很大的优化空间，所以通过这样一个标准来分离底层运算及更高级的调用，达到较好的跨平台性及运算速度。现在较为知名的BLAS实现是 Netlib 的 cBLAS， 第一个做到跨平台可伸缩的 ATLAS，boost 提供的ublas，以及 GotoBLAS2 的继承改进版 OpenBLAS，还有Intel专门为Intel处理器开发的MKL。

[LAPACK](http://www.netlib.org/lapack/) 全称 Linear Algebra Package，是一个基于 Level 3 BLAS 的线性代数数值计算库，其继承了LINPACK的线性方程求解和最小二乘求解，EISPACK的特征值求解，以及实现了多种矩阵分解算法（LU, Cholesky, QR, SVD, Schur, generalized Schur）。最新的 LAPACK 是由Fortran 90写成的。LAPACKE 是 LAPACK 的 C 语言API。


### 现有的BLAS库实现
比较全的介绍可以在 BLAS 的 [wiki](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms) 中找到，以下主要谈一谈笔者的体会。

1.	[OpenBLAS](http://www.openblas.net/) 是笔者现在使用的 BLAS 库，其继承了 GotoBLAS2 的设计，还对 LAPACK 实现进行了优化，具有较好的性能。虽然赶不上 MKL 在 Intel X86-64 计算机上的性能，但是由于其开源性，笔者可以不用担心哪天 MKL 又不免费了。而且正是因为这些开源软件不断提高的品质才使得商业公司不得不免费提供他们的产品给社区以保持市场占有。所以虽然 OpenBLAS 在性能上落于 MKL 之下，笔者仍然将其放在第一位。
2.	[MKL](https://software.intel.com/en-us/mkl) 在其主页打出了"the fastest"的标语，的确是底气很足。由于是 Intel 的亲儿子，MKL 获得了很多内部支持，能够优化到CPU的最底层。在 Intel CPU 上没有比它更快的 BLAS 实现了，而且好消息是现在 MKL 可以免费下载用于学习科研目的。
3.	[ATLAS](http://math-atlas.sourceforge.net/) 全称 Automatically Tuned Linear Algebra Software，是一个可以对任何计算机硬件生成优化过的BLAS库的软件。虽然在对指定硬件架构上性能不及专门优化过的BLAS库，其自动生成能力使得它能够对任意新系统生成第一个优化过的BLAS库，并作为后来者的对比基准。
4.	[cBLAS](http://www.netlib.org/blas/) 是Netlib提供的基于 Fortrain 实现的 BLAS 的c语言API，其存在价值在于通常默认安装于系统中。
5.	[uBLAS](http://www.boost.org/doc/libs/1_65_1/libs/numeric/ublas/doc/index.html) 是 boost 包提供的 C 语言 BLAS 实现，性能不敢恭维。

6.	[cuBLAS](https://developer.nvidia.com/cublas) 是 Nvidia 为其 GPU 提供的线性运算库，包含于 CUDA 中，也可以单独下载安装。由于稠密矩阵运算是高度并行的任务，所以 GPU 更擅长做基础向量运算。在 Nvidia 官方给的测试中，使用 cuBLAS 的 Tesla P100 比使用 MKL 的 Xeon Dual E5-2699 v4 快了5倍。
7.	[clBLAS](https://github.com/clMathLibraries/clBLAS) 是 BLAS 基于 OpenCL 的实现，主要针对并行和 AMD GPU进行了优化。clBLAS的优点是它为开源项目，其作用之于 Nvidia 类似于 OpenBLAS 之于 Intel。

## OpenBLAS 在 Visual Studio 中的使用
Linux 下安装和使用 OpenBLAS 是比较方便的，在此就不再赘述。笔者主要记录一下 Win 下安装使用的步骤。
1. 下载预编译包（通常选择x64）[binary package](https://sourceforge.net/projects/openblas/files/)
2. 解压，并将包中.h, .lib, .dll分别放在合适的位置。.lib包中只有 libopenblas.dll.a 是 Visual Studio 可以调用的，另一个是只有 mingw-gcc 才能调用的。
3. 编译时包含头文件目录，链接libopenblas.dll.a。
4. 运行时需要若干 mingw dll 文件，按照提示去下载。

## SuiteSparse 在 Visual Studio 下的编译
SuiteSparse 不提供 Windows 下编译安装的官方支持，但是 Github 上有大神做了一个出来 [suitesparse-metis-for-windows](https://github.com/jlblancoc/suitesparse-metis-for-windows)，按照说明一步一步安装再编译就不会有什么问题。在配置 CMake 时可以手动指定使用的 BLAS 库，比如 OpenBLAS。

### error
Windows Kit corcert_math rint [issue](https://github.com/jlblancoc/suitesparse-metis-for-windows/issues/6)

[^1]: [矩阵运算库blas, cblas, openblas, atlas, lapack, mkl之间有什么关系，在性能上区别大吗？  - 蝙蝠果的回答 - 知乎](https://www.zhihu.com/question/27872849/answer/75968482)

<!--stackedit_data:
eyJoaXN0b3J5IjpbMjAxNTQzNDEwMiwtMTE0MjMyMzY4NSwtMT
Q0NjQ0OTI4NV19
-->