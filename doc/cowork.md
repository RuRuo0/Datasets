# FormalGeo20K数据集标注指南
随着现代科学的深入发展，学科分支变得越来越多，科学理论变得艰深难懂，同行审阅周期越来越长，阻碍了科学的进一步发展。自计算机出现以来，人们就尝试利用计算机强大的运算和推理能力来辅助科学研究，但受限于计算机的特点，需要先将科学知识转化为结构化的形式。在几何形式化、几何机械化领域，长期受制于三大难题：知识形式难统一、证明过程不可读、几何证明无定法。设计一套有严密语法结构但同时符合人类阅读习惯的、统一几何问题文字描述和图像描述的、统一计算和推理过程的形式化语言，是解决上述三大难题的一条可行路径。

## 1.形式化语言简介
FormalGeo形式化语言包括两大组成部分，分别是**几何定义语言（GDL）**和**条件声明语言（CDL）**。GDL用于配置推理器，使其具有可扩展性；CDL用于几何问题的形式化输入。FormalGeo形式化语言采用类似谓词逻辑的语法结构，非常容易上手,在标注工作中，我们只需关注如何将几何问题转化为CDL即可。
### 1.1几何本体论
几何本体论研究几何学领域的根本性本体，以及本体之间的关系，是问题*我们需要形式化那些东西？*的回答，其理论成果如下图所示。
<div align=center>
    <img src="cowork-pic/four-quadrant.png" width="60%">
    <br>
    Figure 1. 几何本体域-二维四象限
</div>
### 1.2几何表示论
几何表示论是研究如何使用文字或符号来表示几何图形的理论，是问题*我们如何形式化？*的回答，其理论成果包括对应一致性原则、构造性作图法。对应一致性原则是指原始系统和形式化系统的静态描述和动态过程要一一对应。在几何领域，静态描述指的是几何问题的条件，包括数量关系和实体关系；动态过程是指定理。构造性作图法采用最少数量的形式化语句来描述几何图形，并按照机械化的方法自动构建出所有的几何元素。
**CDL**采用点的有序对来描述几何图形，根据构图的先后顺序，可以分为：构图语句（包括基本构图语句和基本实体）和其他语句（实体、实体关系、代数关系等），具体可参考附录3查阅手册。  
### 1.3语法

## 2.环境配置
我们需要配置以下环境，熟悉环境配置的朋友可以自行安装，不熟悉的可以参照本章安装教程。  

    # python版本和依赖库
    python==3.10
	sympy==1.10.1
	graphviz==0.20.1
	
    # 方便python项目开发的IDE(任何一种都可以)
    Pycharm
    
    # 多人协作
    Git

### 2.1 python环境配置
#### 2.1.1 Conda安装
Conda是一个开源包管理系统和环境管理系统，包括多种语言的包安装、运行、更新、删除，可以解决包依赖问题，分为Anaconda和Miniconda两个安装版本。Anaconda包括Conda、Python以及一大堆安装好的工具包，如numpy、pandas等；Miniconda是一个精简版本，只包括Conda、Python。我们只需安装Miniconda即可。  
1.登陆[官网](https://conda.io/en/latest/miniconda.html)下载安装包：
<div align=center>
    <img src="cowork-pic/1.png" width="80%">
</div>
2.无脑next到这里，勾选以下内容：
<div align=center>
    <img src="cowork-pic/2.png" width="50%">
</div>
3.继续无脑next，直到安装完成。打开命令窗口，输入命令查看安装版本，检查是否安装成功：

    # 查看安装版本
    > conda --version
	conda 23.1.0
	
	# 换国内源，为后续各种包下载做准备
	> conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
	> conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
	> conda config --set show_channel_urls yes
	> conda config --show channels
	channels:
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
	  - defaults

#### 2.1.2 利用Conda安装python

	# 创建python3.10环境并激活
    > conda create -n FormalGeo python=3.10
    > conda activate FormalGeo 
	
    # 安装python依赖库
    (FormalGeo)> pip install -v sympy==1.10.1
    (FormalGeo)> pip install -v graphviz==0.20.1
    
    # 检查是否安装成功
    (FormalGeo)> pip list
    Package      Version
	------------ ---------
	certifi      2022.12.7
	graphviz     0.20.1
	mpmath       1.2.1
	pip          22.3.1
	setuptools   65.6.3
	sympy        1.10.1
	wheel        0.38.4
	wincertstore 0.2

#### 2.1.3 安装pycharm
pycharm一款用于python项目开发的IDE。安装pycharm主要是为了：①方便运行python代码和查看程序输出②查看md格式文档和阅读json格式数据。你也可以使用你自己习惯的IDE来运行python程序和查看特定格式的文件，如VS Code、Jupyter Notebook等。  
1.登陆[官网](https://www.jetbrains.com/zh-cn/pycharm/)下载安装包(社区版)：
<div align=center>
    <img src="cowork-pic/3.png" width="70%">
</div>
2.在这一页勾选几项个性化配置，其他都无脑next：
<div align=center>
    <img src="cowork-pic/4.png" width="70%">
</div>

### 2.2 Git安装
Git是一种分布式版本控制系统，用于多人协作项目开发时的版本控制，方便版本管理，非常的好用。我们的标注工作不涉及代码修改，只涉及文件的上传，只需学习几个简单的git命令就可以。  
1.登陆[官网](https://git-scm.com/)下载安装包：  
<div align=center>
    <img src="cowork-pic/5.png" width="70%">
    <img src="cowork-pic/6.png" width="70%">
</div>
2.按照其默认的勾选，无脑next，直到安装完成：
<div align=center>
    <img src="cowork-pic/7.png" width="70%">
</div>
3.首次使用，配置用户名和邮箱，在任意目录下右键，选择 Git Bash Here：
<div align=center>
    <img src="cowork-pic/8.png" width="40%">
</div>

	# 设置用户名和邮箱
	$ git config --global user.name <your_name>
	$ git config --global user.email <your_email>

	# 查看当前配置
	$ git config --global --list
	user.email=<your_email>
	user.name=<your_name>

4.

## 3.标注流程


## 4.注意事项和常见报错

## 附录1 谓词列表

## 附录2 定理列表

## 附录3 查阅手册
### A、条件的自动扩展
<div align=center>
    <img src="cowork-pic/auto-expand.png" width="60%">
    <br>
    Figure 1. 几何本体域-二维四象限
</div>