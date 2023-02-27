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
**CDL**采用点的有序对来描述几何图形，根据构图的先后顺序，可以分为：构图语句（包括基本构图语句和基本实体）和其他语句（实体、实体关系、代数关系等），具体可参考附录。  
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
    (FormalGeo)> pip install -v func_timeout==4.3.5
    
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

### 2.3项目初始化配置
1.新建项目文件夹，并右键，选择 Git Bash Here：
<div align=center>
    <img src="cowork-pic/9.png" width="40%">
</div>

2.初始化git并从远程仓库下载项目

	# 初始化git
	$ git init

	# 添加远程协作仓库
	$ git remote add origin https://github.com/BitSecret/FormalGeo-SAT.git

	# 拉取远程主分支到本地新分支
	$ git fetch origin main:<your_name>

	# 切换到你的本地分支
	$ git checkout <your_name>

	# 将你的本地新分支推送到远程仓库
	$ git push --set-upstream origin <your_name>

如果一切顺利，现在你的本地仓库已经有了我们的项目文件：
<div align=center>
    <img src="cowork-pic/10.png">
</div>

查看我们的[远程协作仓库](https://github.com/BitSecret/FormalGeo-SAT)，也有了你的远程分支：
<div align=center>
    <img src="cowork-pic/11.png">
    <img src="cowork-pic/12.png">
</div>

3.添加 .gitignore 文件：  
添加.gitignore文件到你的项目目录，其作用是忽略你的IDE产生的、与项目无关的缓存or配置文件。
<div align=center>
    <img src="cowork-pic/13.png">
</div>

文件的内容如图所示。如果你用的是其他IDE，请将对应的缓存/配置文件或文件夹添加到.gitignore文件中。  
4.pycharm项目配置  
在你的项目文件夹右键，选择作为pycharm项目打开。首次打开会为文件编制索引，加载较慢，耐心等待。  
<div align=center>
    <img src="cowork-pic/14.png">
</div>

加载完成后，选择 文件->设置->项目->python解释器->全部显示：  
<div align=center>
    <img src="cowork-pic/15.png">
</div>

点击+号，选择Conda环境，将你的Conda安装地址配置到pycharm中，同时选择我们在2.1节新建的python3.10环境：  
<div align=center>
    <img src="cowork-pic/16.png" width="70%">
</div>

点击确定，加载Conda环境。勾选关联项目，然后点击应用：  
<div align=center>
    <img src="cowork-pic/17.png" width="60%">
</div>

选择python解释器，点击应用：  
<div align=center>
    <img src="cowork-pic/18.png" width="60%">
</div>

配置完成后，会载入环境，编制索引，加载较慢，耐心等待。  
5.首次运行  
右键 main.py ，选择运行。若程序成功编译并输出 pid： ，则证明环境配置成功。  
<div align=center>
    <img src="cowork-pic/19.png" width="30%">
    <img src="cowork-pic/20.png">
</div>

随便输入一个 data/formalized-problems 文件夹中的序号，查看推理器输出：
<div align=center>
    <img src="cowork-pic/21.png">
</div>

## 3.标注协作
### 3.1与主分支同步
1.在项目文件夹右键，选择Git Bash Here：
<div align=center>
    <img src="cowork-pic/9.png" width="40%">
</div>

2.输入以下指令，将远程主分支的更新内容拉取到你的本地分支：  

	$ git pull origin main

3.阅读README.md，获取每周的任务分配：
<div align=center>
    <img src="cowork-pic/22.png">
</div>

上图中黄色箭头是每周的**标注识别号**，绿色箭头是每个人分配的题号，原始题目在 data/raw-problems 文件夹，共6个数据集，已经化为了统一的格式。
### 3.2标注(1个)问题
1.复制模板到 data/formalized-problems ，并改名为 <problem_id>.json ：
<div align=center>
    <img src="cowork-pic/23.png">
</div>

2.将原始问题具有的信息添加到 <problem_id>.json ，同时添加上自己的标注信息：  
<div align=center>
    <img src="cowork-pic/24.png">
</div>

3.按照附录的各种手册，标注并保存问题。

### 3.3提交已标注的问题
在每周的标注任务完成后，将所有的标注文件统一提交。  
1.在项目文件夹右键，选择Git Bash Here：
<div align=center>
    <img src="cowork-pic/9.png" width="40%">
</div>

2.提交已标注的问题

	# 添加文件
	$ git add data/formalized-problems

    # 提交文件，annotation_code即标注识别号，每周一在REAMDE.md发布
	$ git commit -m "<your_name> <annotation_code>"

    # 推送到远程仓库
    $ git push

## 4.注意事项和常见报错
### 4.1时间安排
A、每周的任务需在周日晚24点之前提交。  
B、每周一上午12点之前更新主分支内容。  
C、每个人第N周提交的内容将会在第N+1周日24点之前合并到主分支。  
### 4.2沟通交流
标注过程遇到任何问题及时沟通，直接在群里提出(最高效的)，或填写[在线协作文档](https://docs.qq.com/sheet/DRk55TFZVb0hiWEJn)。
### 4.3常见问题

## 附录1 单个问题标注流程

## 附录2 谓词列表
### A、基本构图谓词
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>格式</b></td>
        <td align="center"><b>多种表示</b></td>
        <td align="center"><b>实体存在性约束</b></td>
        <td align="center"><b>扩展</b></td>
    </tr>
    <tr>
        <td align="center">基本形状</td>
	    <td align="center">Shape($)</td>
	    <td align="center">*</td>
	    <td align="center">/</td>
	    <td align="center">Polygon</td>
    </tr>
    <tr>
        <td align="center">共线点</td>
	    <td align="center">Collinear($)</td>
	    <td align="center">*</td>
	    <td align="center">/</td>
	    <td align="center">Line</td>
    </tr>
    <tr>
        <td align="center">共圆点</td>
	    <td align="center">Cocircular(O,$)</td>
	    <td align="center">*</td>
	    <td align="center">/</td>
	    <td align="center">Point,Arc</td>
    </tr>
</table>

### B、基本实体
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>格式</b></td>
        <td align="center"><b>多种表示</b></td>
        <td align="center"><b>实体存在性约束</b></td>
        <td align="center"><b>扩展</b></td>
    </tr>
    <tr>
        <td align="center">点</td>
	    <td align="center">Point(A)</td>
        <td align="center">/</td>
	    <td align="center">/</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">线</td>
	    <td align="center">Line(AB)</td>
        <td align="center">BA</td>
	    <td align="center">/</td>
	    <td align="center">Point(A),Point(B)</td>
    </tr>
    <tr>
        <td align="center">角</td>
	    <td align="center">Angle(ABC)</td>
        <td align="center">/</td>
	    <td align="center">/</td>
	    <td align="center">Line(AB),Line(BC)</td>
    </tr>
    <tr>
        <td align="center">多边形</td>
	    <td align="center">Polygon($)</td>
        <td align="center">*</td>
	    <td align="center">/</td>
	    <td align="center">Angle</td>
    </tr>
    <tr>
        <td align="center">弧</td>
	    <td align="center">Arc(AB)</td>
        <td align="center">/</td>
	    <td align="center">/</td>
	    <td align="center">Point(A),Point(B)</td>
    </tr>
    <tr>
        <td align="center">圆</td>
	    <td align="center">Circle(O)</td>
        <td align="center">/</td>
	    <td align="center">/</td>
	    <td align="center">Point(O)</td>
    </tr>

</table>

### C、实体
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>格式</b></td>
        <td align="center"><b>多种表示</b></td>
        <td align="center"><b>实体存在性约束</b></td>
        <td align="center"><b>扩展</b></td>
    </tr>
    <tr>
        <td align="center">三角形</td>
	    <td align="center">Triangle(ABC)</td>
	    <td align="center">BCA,CAB</td>
	    <td align="center">Polygon(ABC)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">直角三角形</td>
	    <td align="center">RightTriangle(ABC)</td>
	    <td align="center">/</td>
	    <td align="center">Polygon(ABC)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">等腰三角形</td>
	    <td align="center">IsoscelesTriangle(ABC)</td>
	    <td align="center">/</td>
	    <td align="center">Polygon(ABC)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">等边三角形</td>
	    <td align="center">EquilateralTriangle(ABC)</td>
	    <td align="center">BCA,CAB</td>
	    <td align="center">Polygon(ABC)</td>
	    <td align="center">/</td>
    </tr>
</table>

### D、实体关系
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>格式</b></td>
        <td align="center"><b>多种表示</b></td>
        <td align="center"><b>实体存在性约束</b></td>
        <td align="center"><b>扩展</b></td>
    </tr>
    <tr>
        <td align="center">中点</td>
	    <td align="center">Midpoint(M,AB)</td>
	    <td align="center">MBA</td>
	    <td align="center">Point(M),Line(AB)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">两线相交</td>
	    <td align="center">Intersect(O,AB,CD)</td>
	    <td align="center">OCDBA,OBADC,ODCAB</td>
	    <td align="center">Point(O),Line(AB),Line(CD)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">两线平行</td>
	    <td align="center">Parallel(AB,CD)</td>
	    <td align="center">DCBA</td>
	    <td align="center">Line(AB),Line(CD)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">两线垂直</td>
	    <td align="center">Perpendicular(AO,OC)</td>
	    <td align="center">/</td>
	    <td align="center">Line(AO),Line(OC)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">垂直平分线</td>
	    <td align="center">PerpendicularBisector(AB,CO)</td>
	    <td align="center">/</td>
	    <td align="center">Line(AB),Line(CO)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">角平分线</td>
	    <td align="center">Bisector(BD,ABC)</td>
	    <td align="center">/</td>
	    <td align="center">Line(BD),Angle(ABC)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">三角形的中线</td>
	    <td align="center">Median(AD,ABC)</td>
	    <td align="center">/</td>
	    <td align="center">Line(AD),Polygon(ABC),Collinear(BDC)</td>
	    <td align="center">Triangle(ABC)</td>
    </tr>
    <tr>
        <td align="center">三角形的高</td>
	    <td align="center">IsAltitude(AD,ABC)</td>
	    <td align="center">/</td>
	    <td align="center">Line(AD),Polygon(ABC),Collinear(BDC)</td>
	    <td align="center">Triangle(ABC)</td>
    </tr>
    <tr>
        <td align="center">三角形的中位线</td>
	    <td align="center">Neutrality(DE,ABC)</td>
	    <td align="center">/</td>
	    <td align="center">Line(DE),Polygon(ABC)</td>
	    <td align="center">Triangle(ABC)</td>
    </tr>
    <tr>
        <td align="center">三角形的外心</td>
	    <td align="center">Circumcenter(O,ABC)</td>
	    <td align="center">OBCA,OCAB</td>
	    <td align="center">Point(O),Polygon(ABC)</td>
	    <td align="center">Triangle(ABC)</td>
    </tr>
    <tr>
        <td align="center">三角形的内心</td>
	    <td align="center">Incenter(O,ABC)</td>
	    <td align="center">OBCA,OCAB</td>
	    <td align="center">Point(O),Polygon(ABC)</td>
	    <td align="center">Triangle(ABC)</td>
    </tr>
    <tr>
        <td align="center">三角形的重心</td>
	    <td align="center">Centroid(O,ABC)</td>
	    <td align="center">OBCA,OCAB</td>
	    <td align="center">Point(O),Polygon(ABC)</td>
	    <td align="center">Triangle(ABC)</td>
    </tr>
    <tr>
        <td align="center">三角形的垂心</td>
	    <td align="center">Orthocenter(O,ABC)</td>
	    <td align="center">OBCA,OCAB</td>
	    <td align="center">Point(O),Polygon(ABC)</td>
	    <td align="center">Triangle(ABC)</td>
    </tr>
    <tr>
        <td align="center">三角形全等</td>
	    <td align="center">Congruent(ABC,DEF)</td>
	    <td align="center">DEFABC,BCAEFD,EFDBCA,CABFDE,FDECAB</td>
	    <td align="center">Polygon(ABC),Polygon(DEF)</td>
	    <td align="center">Triangle(ABC),Triangle(DEF)</td>
    </tr>
    <tr>
        <td align="center">三角形相似</td>
	    <td align="center">Similar(ABC,DEF)</td>
	    <td align="center">DEFABC,BCAEFD,EFDBCA,CABFDE,FDECAB</td>
	    <td align="center">Polygon(ABC),Polygon(DEF)</td>
	    <td align="center">Triangle(ABC),Triangle(DEF)</td>
    </tr>
    <tr>
        <td align="center">三角形镜像全等</td>
	    <td align="center">MirrorCongruent(ABC,DEF)</td>
	    <td align="center">DEFABC,BCAFDE,FDEBCA,CABEFD,EFDCAB</td>
	    <td align="center">Polygon(ABC),Polygon(DEF)</td>
	    <td align="center">Triangle(ABC),Triangle(DEF)</td>
    </tr>
    <tr>
        <td align="center">三角形镜像相似</td>
	    <td align="center">MirrorSimilar(ABC,DEF)</td>
	    <td align="center">DEFABC,BCAFDE,FDEBCA,CABEFD,EFDCAB</td>
	    <td align="center">Polygon(ABC),Polygon(DEF)</td>
	    <td align="center">Triangle(ABC),Triangle(DEF)</td>
    </tr>
</table>

### E、基本实体属性
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>格式</b></td>
        <td align="center"><b>多种表示</b></td>
        <td align="center"><b>实体存在性约束</b></td>
    </tr>
    <tr>
        <td align="center">长度</td>
	    <td align="center">Length(AB)</td>
	    <td align="center">BA</td>
	    <td align="center">Line(AB)</td>
    </tr>
    <tr>
        <td align="center">弧长</td>
	    <td align="center">ArcLength(AB)</td>
	    <td align="center">/</td>
	    <td align="center">Arc(AB)</td>
    </tr>
    <tr>
        <td align="center">角度</td>
	    <td align="center">Measure(ABC)</td>
	    <td align="center">/</td>
	    <td align="center">Angle(ABC)</td>
    </tr>
    <tr>
        <td align="center">面积</td>
	    <td align="center">Area($)</td>
	    <td align="center">*</td>
	    <td align="center">Polygon($)/Circle(O)</td>
    </tr>
    <tr>
        <td align="center">周长</td>
	    <td align="center">Perimeter($)</td>
	    <td align="center">*</td>
	    <td align="center">Polygon($)/Circle(O)</td>
    </tr>
</table>

### F、实体属性
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>格式</b></td>
        <td align="center"><b>多种表示</b></td>
        <td align="center"><b>实体存在性约束</b></td>
    </tr>
    <tr>
        <td align="center">三角形高的长度</td>
	    <td align="center">AltitudeOfTriangle(ABC)</td>
	    <td align="center">/</td>
	    <td align="center">Polygon(ABC)</td>
    </tr>
    <tr>
        <td align="center">点到直线的距离</td>
	    <td align="center">DistanceOfPointToLine(O,AB)</td>
	    <td align="center">OBA</td>
	    <td align="center">Point(O),Line(AB)</td>
    </tr>
</table>

### G、代数关系
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>格式</b></td>
        <td align="center"><b>备注</b></td>
    </tr>
    <tr>
        <td align="center">相等</td>
	    <td align="center">Equal($,$)</td>
	    <td align="center">$可以是表达式，也可以是实体属性，并且可以嵌套表示</td>
    </tr>
</table>

### H、代数运算
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>格式</b></td>
        <td align="center"><b>表达式符号</b></td>
    </tr>
    <tr>
        <td align="center">加</td>
	    <td align="center">Add(expr1,expr2,…)</td>
	    <td align="center">+</td>
    </tr>
    <tr>
        <td align="center">减</td>
	    <td align="center">Sub(expr1,expr2)</td>
	    <td align="center">-</td>
    </tr>
    <tr>
        <td align="center">乘</td>
	    <td align="center">Mul(expr1,expr2,…)</td>
	    <td align="center">*</td>
    </tr>
    <tr>
        <td align="center">除</td>
	    <td align="center">Div(expr1,expr2)</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">幂</td>
	    <td align="center">Pow(expr1,expr2)</td>
	    <td align="center">^</td>
    </tr>
    <tr>
        <td align="center">正弦</td>
	    <td align="center">Sin(expr)</td>
	    <td align="center">@</td>
    </tr>
    <tr>
        <td align="center">余弦</td>
	    <td align="center">Cos(expr)</td>
	    <td align="center">#</td>
    </tr>
    <tr>
        <td align="center">正切</td>
	    <td align="center">Tan(expr)</td>
	    <td align="center">$</td>
    </tr>
    <tr>
        <td align="center">实数</td>
	    <td align="center">R</td>
	    <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">自由变量</td>
	    <td align="center">x</td>
	    <td align="center">/</td>
    </tr>
</table>

### I、解题目标
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>格式</b></td>
        <td align="center"><b>备注</b></td>
    </tr>
    <tr>
        <td align="center">证相等</td>
	    <td align="center">Equal($,$)</td>
	    <td align="center">$可以是表达式，也可以是实体属性，并且可以嵌套表示</td>
    </tr>
    <tr>
        <td align="center">求值</td>
	    <td align="center">Value(Expression($))</td>
	    <td align="center">Expression表示由运算和实体属性构成的表达式</td>
    </tr>
    <tr>
        <td align="center">求关系</td>
	    <td align="center">Relation($)</td>
	    <td align="center">Relation表示任意实体、实体关系</td>
    </tr>
</table>

## 附录3 定理列表
<table width="100%">
	<tr>
	    <td align="center"><b>名称</b></td>
        <td align="center"><b>前提</b></td>
        <td align="center"><b>结论</b></td>
    </tr>
    <tr>
        <td align="center">/</td>
	    <td align="center">/</td>
	    <td align="center">/</td>
    </tr>
</table>

## 附录4 图形-文字表示对照手册

条件的自动扩展
<div align=center>
    <img src="cowork-pic/auto-expand.png" width="60%">
    <br>
    Figure 1. 几何本体域-二维四象限
</div>

### A、基本构图谓词
### B、基本实体
### C、实体
### D、实体关系
### E、基本实体属性
### F、实体属性
### G、代数关系
### H、代数运算
### H、解题目标
