# FormalGeo20K数据集标注指南
随着现代科学的深入发展，学科分支变得越来越多，科学理论变得艰深难懂，同行审阅周期越来越长，阻碍了科学的进一步发展。自计算机出现以来，人们就尝试利用计算机强大的运算和推理能力来辅助科学研究，但受限于计算机的特点，需要先将科学知识转化为结构化的形式。在几何形式化、几何机械化领域，长期受制于三大难题：知识形式难统一、证明过程不可读、几何证明无定法。设计一套有严密语法结构但同时符合人类阅读习惯的、统一几何问题文字描述和图像描述的、统一计算和推理过程的形式化语言，是解决上述三大难题的一条可行路径。

## 1.形式化语言简介
FormalGeo形式化语言包括两大组成部分，分别是**几何定义语言（GDL）**和**条件声明语言（CDL）**。GDL用于配置推理器，使其具有可扩展性；CDL用于几何问题的形式化输入。FormalGeo形式化语言采用类似谓词逻辑的语法结构，非常容易上手,在标注工作中，我们只需关注如何将几何问题转化为CDL即可。

### 1.1几何本体论与几何表示论
**几何本体论**研究几何学领域的根本性本体，以及本体之间的关系，是问题**我们需要形式化那些东西？**的回答，其理论成果如下图所示。
<div align=center>
    <img src="cowork-pic/four-quadrant.png" width="60%">
    <br>
    Figure 1. 几何本体域-二维四象限
</div>

**几何表示论**是研究如何使用文字或符号来表示几何图形的理论，是问题**我们如何形式化？**的回答，其理论成果包括对应一致性原则和构造性作图法。对应一致性原则是指原始系统和形式化系统的静态描述和动态过程要一一对应。在几何领域，静态描述指的是几何问题的条件，动态过程是指定理。构造性作图法采用最少数量的形式化语句来描述几何图形，并按照机械化的方法自动构建出所有的几何元素。

### 1.2语法
**CDL**采用点的有序对来描述几何图形，根据其作用，可以分为三类。第一类是**构图语句**，包括基本构图语句和基本实体，推理器利用少量构图语句来构建所有的几何元素；第二类是**条件语句**，用于描述几何问题的前提条件，包括数量关系和实体关系；第三类是**目标语句**，用于声明几何问题的求解目标。  
CDL语法与谓词逻辑类似，非常简单易学，我们举两个例子：  

    Triangle(ABC)
    Equal(LengthOfLine(AB),LengthOfLine(CD))

很显然，第一句话声明了一个三角形，ABC是三角形的三个顶点；第二句话声明了一个数量关系，即直线AB的长度与直线CD的长度相等。  
现在我们介绍几个基本的概念。  
在上述两条CDL语句中，*Triangle*和*Equal*称作**谓词**，用于描述一种几何元素或几何元素之间的关系；*括号中的内容*称为**个体词**，在实体关系中，个体词为点的有序对，在数量关系中，个体词为由实数、运算符和符号构成的表达式；*LengthOfLine*称为**函数**，是个体词到个体词的映射，准确来说是实体关系个体词到代数关系个体词的映射，我们通过这样的映射，就可以用点的有序对来表示数量关系，实现了实体关系和数量关系表示形式的统一。  
介绍完毕，就是这么简单！  

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

### 2.2 Graphviz安装
登陆[官网](https://graphviz.org/download/)下载安装包，一步步安装即可：  
<div align=center>
    <img src="cowork-pic/26.png" width="80%">
</div>

将Graphviz安装路径中的bin目录添加到环境变量path中，选择 我的电脑->属性->高级系统设置->环境变量->Path->新建：  
<div align=center>
    <img src="cowork-pic/27.png" width="100%">
</div>

打开命令窗口，输入指令查看是否安装配置成功。  

    > dot -v
    dot - graphviz version 6.0.1 (20220911.1526)

### 2.3 Git安装
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

### 2.4项目初始化配置
1.新建项目文件夹，并右键，选择 Git Bash Here：
<div align=center>
    <img src="cowork-pic/9.png" width="40%">
</div>

2.初始化git并从远程仓库下载项目

	# 初始化git
	$ git init

	# 添加远程协作仓库
	$ git remote add origin https://github.com/BitSecret/FormalGeo-SAT.git

	# 拉取远程主分支到本地新分支，<your_name>换成你自己的名字，如 xiaokaizhang
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
添加.gitignore文件到你的项目目录，其作用是忽略你的IDE产生的、与项目无关的缓存or配置文件，内容为：  

    .idea
	__pycache__
	.gitignore
	data/solved

<div align=center>
    <img src="cowork-pic/13.png">
</div>

文件的内容如图所示。如果你用的是其他IDE，请将对应的缓存/配置文件或文件夹添加到.gitignore文件中。  
4.pycharm项目配置  
在你的项目文件夹右键，选择作为pycharm项目打开。  
<div align=center>
    <img src="cowork-pic/14.png">
</div>

将data和doc两个文件夹标记为Excluded，这样就不会为文件编制索引，加快打开速度。选择 文件->设置->项目->项目结构：  
<div align=center>
    <img src="cowork-pic/25.png" width="70%">
</div>


加载完成后，选择 文件->设置->项目->python解释器->全部显示：  
<div align=center>
    <img src="cowork-pic/15.png">
</div>

点击+号，选择Conda环境，将你的Conda安装地址配置到pycharm中，同时选择我们在2.1节新建的python3.10环境：  
<div align=center>
    <img src="cowork-pic/16.png" width="70%">
</div>

选定我们的python环境，然后点击应用：  
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
在项目文件夹右键，选择Git Bash Here：
<div align=center>
    <img src="cowork-pic/9.png" width="40%">
</div>

输入以下指令，将远程主分支的更新内容拉取到你的本地分支：  

	$ git pull origin main

阅读README.md，获取每周的任务分配：
<div align=center>
    <img src="cowork-pic/22.png">
</div>

上图中黄色箭头是每周的**标注识别号**，绿色箭头是每个人分配的题号，原始题目在 data/raw-problems 文件夹，共6个数据集，已经化为了统一的格式。
### 3.2标注(1个)问题
1.从 data/raw_problems 复制题目到 data/formalized-problems  
2.标注并保存问题   
<div align=center>
    <img src="cowork-pic/24.png" width="70%">
</div>

3.运行推理器，查看问题是否成功求解  

### 3.3提交已标注的问题
在每周的标注任务**全部完成后**，将所有的标注文件统一提交。  
1.在项目文件夹右键，选择Git Bash Here：
<div align=center>
    <img src="cowork-pic/9.png" width="40%">
</div>

2.提交已标注的问题

	# 添加已标注的问题
	$ git add data/formalized-problems

    # 提交文件，annotation_code即标注识别号，每周一在REAMDE.md发布
	$ git commit -m "<your_name> <annotation_code>"

    # 推送到远程仓库
    $ git push

## 4.注意事项和常见报错
### 4.1时间安排
A、每周的任务需在周日晚24点之前提交。  
B、每周一上午12点之前更新主分支内容。  
C、每个人第N周提交的内容将会在第N+1周周日日24点之前合并到主分支。  
### 4.2沟通交流
标注过程遇到任何问题及时沟通，直接在群里提出(最高效的)，或填写[在线协作文档](https://docs.qq.com/sheet/DRk55TFZVb0hiWEJn)。
### 4.3常见问题


## 附录1 标注口诀
**1.先构图后标注**  
首先标注**基本构图CDL**，有3个，分别是Polygon、Collinear和Cocircular。在推理器构图阶段，会根据识别到的基本构图CDL自动构建基本实体CDL，参见下图。标注完基本构图CDL后，还需要补充标注无法由基本构图CDL扩展得到的**基本实体CDL**（这就要求对于构图过程比较熟悉，其实也很简单）。然后标注**问题文本CDL**，即问题的自然描述转化来的CDL。其次标注**问题图形CDL**，即问题的图像转化来的CDL。再次标注**解题目标CDL**，共有三类，分别是Value、Equal、Relation。最后标注**定理序列CDL**，根据推理器执行结果不断调整定理，直至解题完成。   
<div align=center>
    <img src="cowork-pic/auto-expand.png" width="50%">
</div>

**2.逆时针法则**  
很多图形的文字表示都是按照逆时针的方向，将图形的点按顺序列出，如多边形、角、三角形等。逆时针法则主要是为了区分镜像图形。  
<div>
    <img src="cowork-pic/40.png" width="40%">
</div>

    Triangle(ABC)
    Angle(AOB)
    Polygon(ABCDE)

**3.旋转不变性**  
图形旋转后还是原图形，各种性质不变，但点的位置变化了，因此一个图形可能有多个文字表示。再标注时，我们仅需标注一个表示即可，其他表示会由推理器自动构建。  
<div>
    <img src="cowork-pic/41.png" width="40%">
</div>

    Triangle(ABC),Triangle(ABC),Triangle(ABC)

**4.从左到右，从上到下**  
有些不封闭的图形，如平行、相交关系等，用逆时针法则不符合人的思维习惯，这时候就使用第三条口诀。  
<div>
    <img src="cowork-pic/42.png" width="40%">
</div>

    Parallel(AB,CD)
    Intersect(O,AB,CD)
    Perpendicular(AO,BO)

## 附录2 谓词标注对照手册
### A、基本构图谓词
| 名称 | 格式 | 多种表示 | 实体存在性约束 | 扩展 |
|:---:|:---:|:---:|:---:|:---:|
| 基本形状 | Polygon(*) | * | / | Angle,Triangle,Quadrilateral |
| 共线点 | Collinear(*) | * | / | Angle |
| 共圆点 | Cocircular(O,*) | * | / | Arc,Circle |
#### Polygon
<div>
    <img src="cowork-pic/Polygon.png" width="40%">
</div>

    Polygon(ABCDE),Polygon(BCDEA),Polygon(CDEAB),Polygon(DEABC),Polygon(EABCD)
    例1: Polygon(ADE),Polygon(DBCE)
    例2: Polygon(ABC),Polygon(ACD),Polygon(ADE),Polygon(AEF)

备注：  
#### Collinear
<div>
    <img src="cowork-pic/Collinear.png" width="40%">
</div>

    Collinear(AMB),Collinear(BMA)
    例1: Collinear(AOB),Collinear(COD)
    例2: Collinear(BCDEF)

备注：  
#### Cocircular
<div>
    <img src="cowork-pic/Cocircular.png" width="27%">
</div>

    Cocircular(O,AC),Cocircular(O,CA)
    例1: Cocircular(O,ABCD)

备注：  
### B、基本实体
| 名称 | 格式 | 多种表示 | 实体存在性约束 | 扩展 |
|:---:|:---:|:---:|:---:|:---:|
| 点 | Point(A) | / | / | / |
| 线 | Line(AB) | BA | / | Point(A),Point(B) |
| 角 | Angle(ABC) | / | / | Line(AB),Line(BC) |
| 三角形 | Triangle(ABC) | BCA,CAB | / | / |
| 四边形 | Quadrilateral(ABCD) | BCDA,CDAB,DABC | / | / |
| 弧 | Arc(AB) | / | / | Point(A),Point(B) |
| 圆 | Circle(O) | / | / | Point(O) |
#### Point
<div>
    <img src="cowork-pic/Point.png" width="40%">
</div>

    Point(A)
    例1: Point(A),Point(B),Point(C)
    例2: Point(O),Point(A),Point(C)

备注：  
#### Line
<div>
    <img src="cowork-pic/Line.png" width="40%">
</div>

    Line(AB),Line(BA)
    例1: Line(AB),Line(CD)
    例2: Line(AO),Line(BO)

备注：  
#### Angle
<div>
    <img src="cowork-pic/Angle.png" width="40%">
</div>

    Angle(AOB)
    例1: Angle(ABC),Angle(BCA),Angle(CAB)
    例2: Angle(AOC),Angle(COB),Angle(BOD),Angle(DOA)

备注：  
#### Triangle
<div>
    <img src="cowork-pic/Triangle.png" width="40%">
</div>

    Triangle(ABC),Triangle(BCA),Triangle(CAB)
    例1: Triangle(ADE),Triangle(ABC)
    例2: Triangle(ABD),Triangle(ADC),Triangle(ABC)

备注：  
#### Quadrilateral
<div>
    <img src="cowork-pic/Quadrilateral.png" width="40%">
</div>

    Quadrilateral(ABCD),Quadrilateral(BCDA),Quadrilateral(CDAB),Quadrilateral(DABC)
    例1: Quadrilateral(DBCE)
    例2: Quadrilateral(ABCD)

备注：  
#### Arc
<div>
    <img src="cowork-pic/Arc.png" width="40%">
</div>

    Arc(AB)
    例1: Arc(AC),Arc(CA)
    例2: Arc(AB),Arc(BC),Arc(CD),...

备注：  
#### Circle
<div>
    <img src="cowork-pic/Circle.png" width="40%">
</div>

    Circle(O)
    例1: Circle(A),Circle(B)
    例2: Circle(O)

备注：  
### C、实体
| 名称 | 格式 | 多种表示 | 实体存在性约束 | 扩展 |
|:---:|:---:|:---:|:---:|:---:|
| 直角三角形 | RightTriangle(ABC) | / | Triangle(ABC) | Perpendicular(AB,CB) |
| 等腰三角形 | IsoscelesTriangle(ABC) | / | Triangle(ABC) | Equal(LengthOfLine(AB),LengthOfLine(AC)) |
| 等边三角形 | EquilateralTriangle(ABC) | BCA,<br>CAB | Triangle(ABC) | Equal(LengthOfLine(AB),LengthOfLine(AC))<br>Equal(LengthOfLine(AB),LengthOfLine(BC)) |
#### RightTriangle
<div>
    <img src="cowork-pic/RightTriangle.png"  width="14%">
</div>

    RightTriangle(ABC)

备注：  
#### IsoscelesTriangle
<div>
    <img src="cowork-pic/IsoscelesTriangle.png"  width="14%">
</div>

    IsoscelesTriangle(ABC)

备注：  
#### EquilateralTriangle
<div>
    <img src="cowork-pic/EquilateralTriangle.png"  width="14%">
</div>

    EquilateralTriangle(ABC),EquilateralTriangle(BCA),EquilateralTriangle(CAB)

备注：  
### D、实体关系
|名称|格式|多种表示|实体存在性约束|扩展|
|:---:|:---:|:---:|:---:|:---:|
| 中点 | Midpoint(M,AB) | MBA | Point(M),<br>Line(AB) | Equal(LengthOfLine(AM),LengthOfLine(MB)) |
| 两线相交 | Intersect(O,AB,CD) | OCDBA,<br>OBADC,<br>ODCAB | Point(O),<br>Line(AB),<br>Line(CD) | / |
| 两线平行 | Parallel(AB,CD) | DCBA | Line(AB),<br>Line(CD) | / |
| 两线垂直 | Perpendicular(AO,OC) | / | Line(AO),<br>Line(OC) | Equal(MeasureOfAngle(AOC),90) |
| 垂直平分线 | PerpendicularBisector(AB,CO) | / | Line(AB),<br>Line(CO) | Perpendicular(AO,CO)<br>Perpendicular(CO,BO)<br>Midpoint(AO,OB) |
| 角平分线 | Bisector(BD,ABC) | / | Line(BD),<br>Angle(ABC) | Equal(MeasureOfAngle(ABD),MeasureOfAngle(DBC)) |
| 三角形的中线 | Median(AD,ABC) | / | Line(AD),<br>Triangle(ABC),<br>Collinear(BDC) | Midpoint(D,BC) |
| 三角形的高 | IsAltitude(AD,ABC) | / | Line(AD),<br>Triangle(ABC),<br>Collinear(BDC) | Perpendicular(BD,AD)<br>Perpendicular(AD,CD)<br>Equal(LengthOfLine(AD),AltitudeOfTriangle(ABC)) |
| 三角形的中位线 | Neutrality(DE,ABC) | / | Line(DE),<br>Triangle(ABC) | Parallel(DE,BC) |
| 三角形的外心 | Circumcenter(O,ABC) | OBCA,<br>OCAB | Point(O),<br>Triangle(ABC) | / |
| 三角形的内心 | Incenter(O,ABC) | OBCA,<br>OCAB | Point(O),<br>Triangle(ABC) | / |
| 三角形的重心 | Centroid(O,ABC) | OBCA,<br>OCAB | Point(O),<br>Triangle(ABC) | / |
| 三角形的垂心 | Orthocenter(O,ABC) | OBCA,<br>OCAB | Point(O),<br>Triangle(ABC) | / |
| 三角形全等 | Congruent(ABC,DEF) | DEFABC,<br>BCAEFD,<br>EFDBCA,<br>CABFDE,<br>FDECAB | Triangle(ABC),<br>Triangle(DEF) | / |
| 三角形相似 | Similar(ABC,DEF) | DEFABC,<br>BCAEFD,<br>EFDBCA,<br>CABFDE,<br>FDECAB | Triangle(ABC),<br>Triangle(DEF) | / |
| 三角形镜像全等 | MirrorCongruent(ABC,DEF) | DEFABC,<br>BCAFDE,<br>FDEBCA,<br>CABEFD,<br>EFDCAB | Triangle(ABC),<br>Triangle(DEF) | / |
| 三角形镜像相似 | MirrorSimilar(ABC,DEF) | DEFABC,<br>BCAFDE,<br>FDEBCA,<br>CABEFD,<br>EFDCAB | Triangle(ABC),<br>Triangle(DEF) | / |
#### Midpoint
<div>
    <img src="cowork-pic/MidPoint.png"  width="14%">
</div>

    Midpoint(M,AB),Midpoint(M,BA)

备注：  
#### Intersect
<div>
    <img src="cowork-pic/Intersect.png"  width="14%">
</div>

    Intersect(O,AB,CD),Intersect(O,CD,BA),Intersect(O,BA,DC),Intersect(O,DC,AB)

备注：  
#### Parallel
<div>
    <img src="cowork-pic/Parallel.png"  width="14%">
</div>

    Parallel(AB,CD),Parallel(DC,BA)

备注：  
#### Perpendicular
<div>
    <img src="cowork-pic/Perpendicular.png"  width="14%">
</div>

    Perpendicular(AO,BO)

备注：  
#### PerpendicularBisector
<div>
    <img src="cowork-pic/PerpendicularBisector.png"  width="14%">
</div>

    PerpendicularBisector(AB,CO)

备注：  
#### Bisector
<div>
    <img src="cowork-pic/Bisector.png"  width="14%">
</div>

    Bisector(BD,ABC)

备注：  
#### Median
<div>
    <img src="cowork-pic/Median.png"  width="14%">
</div>

    Median(AM,ABC)

备注：  
#### IsAltitude
<div>
    <img src="cowork-pic/IsAltitude.png"  width="14%">
</div>

    IsAltitude(AD,ABC)

备注：  
#### Neutrality
<div>
    <img src="cowork-pic/Neutrality.png"  width="14%">
</div>

    Neutrality(DE,ABC)

备注：  
#### Circumcenter
<div>
    <img src="cowork-pic/Circumcenter.png"  width="14%">
</div>

    Circumcenter(O,ABC),Circumcenter(O,BCA),Circumcenter(O,CAB)

备注：  
#### Incenter
<div>
    <img src="cowork-pic/Incenter.png"  width="14%">
</div>

    Incenter(O,ABC),Incenter(O,BCA),Incenter(O,CAB)

备注：  
#### Centroid
<div>
    <img src="cowork-pic/Centroid.png"  width="14%">
</div>

    Centroid(O,ABC),Centroid(O,BCA),Centroid(O,CAB)

备注：  
#### Orthocenter
<div>
    <img src="cowork-pic/Orthocenter.png"  width="14%">
</div>

    Orthocenter(O,ABC),Orthocenter(O,BCA),Orthocenter(O,CAB)

备注：  
#### Congruent
<div>
    <img src="cowork-pic/Congruent.png"  width="14%">
</div>

    Congruent(ABC,DEF),Congruent(DEF,ABC),Congruent(BCA,EFD),
    Congruent(EFD,BCA),Congruent(CAB,FDE),Congruent(FDE,CAB)

备注：  
#### Similar
<div>
    <img src="cowork-pic/Similar.png"  width="14%">
</div>

    Similar(ABC,DEF),Similar(DEF,ABC),Similar(BCA,EFD),
    Similar(EFD,BCA),Similar(CAB,FDE),Similar(FDE,CAB)

备注：  
#### MirrorCongruent
<div>
    <img src="cowork-pic/MirrorCongruent.png"  width="14%">
</div>

    MirrorCongruent(ABC,DEF),MirrorCongruent(DEF,ABC),MirrorCongruent(BCA,FDE)
    MirrorCongruent(FDE,BCA),MirrorCongruent(CAB,EFD),MirrorCongruent(EFD,CAB)

备注：  
#### MirrorSimilar
<div>
    <img src="cowork-pic/MirrorSimilar.png"  width="14%">
</div>

    MirrorSimilar(ABC,DEF),MirrorSimilar(DEF,ABC),MirrorSimilar(BCA,FDE)
    MirrorSimilar(FDE,BCA),MirrorSimilar(CAB,EFD),MirrorSimilar(EFD,CAB)

备注：  
### E、基本实体属性
|名称|格式|符号|多种表示|实体存在性约束|
|:--:|:--:|:--:|:--:|:--:|
|长度|LengthOfLine(AB)|ll|BA|Line(AB)|
|弧长|LengthOfArc(AB)|la|/|Arc(AB)|
|角度|MeasureOfAngle(ABC)|ma|/|Angle(ABC)|


### F、实体属性
|名称|格式|符号|多种表示|实体存在性约束|
|:--:|:--:|:--:|:--:|:--:|
|三角形面积|AreaOfTriangle(ABC)|at|BCA,CAB|Triangle(ABC)|
|三角形周长|PerimeterOfTriangle(ABC)|pt|BCA,CAB|Triangle(ABC)|
|三角形高的长度|AltitudeOfTriangle(ABC)|alt|/|Triangle(ABC)|
|点到直线的距离|DistanceOfPointToLine(O,AB)|dpl|OBA|Point(O),Line(AB)|

### G、代数关系
|名称|格式|备注|
|:--:|:--:|:--:|
|相等|Equal(expr1,expr2)|expr可以是表达式，也可以是实体属性，并且可以嵌套表示|

### H、代数运算
|名称|格式|表达式符号|
|:--:|:--:|:--:|
|加|Add(expr1,expr2,…)|+|
|减|Sub(expr1,expr2)|-|
|乘|Mul(expr1,expr2,…)|*|
|除|Div(expr1,expr2)|/|
|幂|Pow(expr1,expr2)|^|
|正弦|Sin(expr)|@|
|余弦|Cos(expr)|#|
|正切|Tan(expr)|$|
|实数|R|1,2,3,...|
|自由变量|x|a,b,c,...|
|左括号| / |{|
|右括号| / |}|
 
### I、解题目标
|名称|格式|备注|
|:--:|:--:|:--:|
|证相等|Equal(expr1,expr2)|expr可以是表达式，也可以是实体属性，并且可以嵌套表示|
|求值|Value(expr)|expr表示由运算和实体属性构成的表达式|
|求关系|Relation($)|Relation表示任意实体、实体关系|
#### Value
代数型解题目标，求某个表达式或属性的值。

    Value(LengthOfLine(AB))
    Value(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)))
    Value(x+y)

#### Equal
代数型解题目标，证明左右俩个部分相等。

    Equal(LengthOfLine(AB),x+y)
    Equal(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)),Pow(x,2))

#### Relation
逻辑型解题目标，求某个实体或属性。

    Relation(Parallel(AB,CD))
    Relation(RightTriangle(ABC))


## 附录2 定理列表
|名称|类别|描述|
|:--:|:--:|:--:|
| line_addition(AB,BC) | / | / |
| angle_addition(ABC,CBD) | / | / |
| flat_angle(ABC) | / | / |
| adjacent_complementary_angle(AOC,COB) | / | / |
| midpoint_judgment(M,AC) | / | / |
| triangle_area_formula_common(AD,ABC) | / | / |
| triangle_area_formula_heron(ABC) | / | / |
| triangle_area_formula_sine(ABC) | / | / |
| triangle_perimeter_formula(ABC) | / | / |
| triangle_property_angle_sum(ABC) | / | / |
| triangle_property_equal_line_to_equal_angle(ABC) | / | / |
| sine_theorem(ABC) | / | / |
| cosine_theorem(ABC) | / | / |
| parallel_judgment_alternate_interior_angle(AB,CD) | / | / |
| parallel_judgment_Ipsilateral_internal_angle(AB,CD) | / | / |
| parallel_judgment_par_par(AB,CD,EF) | / | / |
| parallel_judgment_per_per(AB,CD) | / | / |
| parallel_property_collinear_extend(AB,CD,M) | / | / |
| parallel_property_alternate_interior_angle(AB,CD) | / | / |
| parallel_property_Ipsilateral_internal_angle(AB,CD) | / | / |
| parallel_property_corresponding_angle(AB,CD,M) | / | / |
| parallel_property_extend_perpendicular(AB,CD) | / | / |
| intersect_property_vertical_angle(O,AB,CD) | / | / |
| bisector_judgment_angle_equal(BD,ABC) | / | / |
| bisector_property_line_ratio(BD,ABC) | / | / |
| median_judgment(AD,ABC) | / | / |
| neutrality_judgment(DE,ABC) | / | / |
| neutrality_property_angle_equal(DE,ABC) | / | / |
| neutrality_property_line_ratio(DE,ABC) | / | / |
| neutrality_property_similar(DE,ABC) | / | / |
| altitude_judgment(AD,ABC) | / | / |
| perpendicular_bisector_judgment(AB,CO) | / | / |
| perpendicular_bisector_property_distance_equal(AB,CO) | / | / |
| perpendicular_judgment_angle(AO,CO) | / | / |
| perpendicular_property_collinear_extend(AO,CO,B) | / | / |
| right_triangle_judgment_angle(ABC) | / | / |
| right_triangle_judgment_pythagorean_inverse(ABC) | / | / |
| right_triangle_property_pythagorean(ABC) | / | / |
| right_triangle_property_special_rt_30_60(ABC) | / | / |
| right_triangle_property_special_rt_45_45(ABC) | / | / |
| isosceles_triangle_judgment_angle_equal(ABC) | / | / |
| isosceles_triangle_judgment_equilateral(ABC) | / | / |
| isosceles_triangle_judgment_line_equal(ABC) | / | / |
| isosceles_triangle_property_angle_equal(ABC) | / | / |
| isosceles_triangle_property_line_coincidence(ABC) | / | / |
| equilateral_triangle_judgment_angle_equal(ABC) | / | / |
| equilateral_triangle_judgment_isos_and_angle(ABC) | / | / |
| equilateral_triangle_judgment_line_equal(ABC) | / | / |
| equilateral_triangle_property_angle(ABC) | / | / |
| equilateral_triangle_property_line_equal(ABC) | / | / |
| congruent_judgment_aas(ABC,DEF) | / | / |
| congruent_judgment_asa(ABC,DEF) | / | / |
| congruent_judgment_hl(ABC,DEF) | / | / |
| congruent_judgment_sas(ABC,DEF) | / | / |
| congruent_judgment_sss(ABC,DEF) | / | / |
| congruent_property_angle_equal(ABC,DEF) | / | / |
| congruent_property_area_equal(ABC,DEF) | / | / |
| congruent_property_line_equal(ABC,DEF) | / | / |
| congruent_property_perimeter_equal(ABC,DEF) | / | / |
| similar_judgment_aa(ABC,DEF) | / | / |
| similar_judgment_sas(ABC,DEF) | / | / |
| similar_judgment_sss(ABC,DEF) | / | / |
| similar_property_angle_equal(ABC,DEF) | / | / |
| similar_property_area_square_ratio(ABC,DEF) | / | / |
| similar_property_line_ratio(ABC,DEF) | / | / |
| similar_property_perimeter_ratio(ABC,DEF) | / | / |
| circumcenter_judgment(O,ABC) | / | / |
| circumcenter_property_intersect(O,ABC) | / | / |
| circumcenter_property_line_equal(O,ABC) | / | / |
| incenter_property_intersect(O,ABC) | / | / |
| incenter_property_judgment(O,ABC) | / | / |
| incenter_property_line_equal(O,ABC) | / | / |
| centroid_judgment(O,ABC) | / | / |
| centroid_property_intersect(O,ABC) | / | / |
| centroid_property_line_equal(O,ABC) | / | / |
| orthocenter_property_intersect(O,ABC) | / | / |
| orthocenter_property_judgment(O,ABC) | / | / |
| orthocenter_property_line_equal(O,ABC) | / | / |

### line_addition(AB,BC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Collinear(ABC),
conclusion: Equal(LengthOfLine(AC),Add(LengthOfLine(AB),LengthOfLine(BC)))
```
备注：  
### angle_addition(ABC,CBD)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Angle(ABC)&Angle(CBD),
conclusion: Equal(MeasureOfAngle(ABD),Add(MeasureOfAngle(ABC),MeasureOfAngle(CBD)))
```
备注：  
### flat_angle(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Collinear(ABC),
conclusion: Equal(MeasureOfAngle(ABC),180), Equal(MeasureOfAngle(CBA),180)
```
备注：  
### adjacent_complementary_angle(AOC,COB)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Angle(AOC)&Angle(COB)&Collinear(AOB),
conclusion: Equal(Add(MeasureOfAngle(AOC),MeasureOfAngle(COB)),180)
```
备注：  
### midpoint_judgment(M,AC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Collinear(AMC)&Equal(LengthOfLine(AM),LengthOfLine(MC)),
conclusion: Midpoint(M,AC)
```
备注：  
### triangle_area_formula_common(AD,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: IsAltitude(AD,ABC),
conclusion: Equal(AreaOfTriangle(ABC),Mul(LengthOfLine(AD),LengthOfLine(BC),0.5))
```
备注：  
### triangle_area_formula_heron(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC),
conclusion: Equal(AreaOfTriangle(ABC),Pow(Mul(Mul(Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(AC)),0.5),Sub(Mul(Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(AC)),0.5),LengthOfLine(AB)),Sub(Mul(Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(AC)),0.5),LengthOfLine(BC)),Sub(Mul(Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(AC)),0.5),LengthOfLine(CA))),0.5))
```
备注：  
### triangle_area_formula_sine(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC),
conclusion: Equal(AreaOfTriangle(ABC),Mul(LengthOfLine(AB),LengthOfLine(BC),Sin(MeasureOfAngle(ABC)),0.5))
```
备注：  
### triangle_perimeter_formula(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC),
conclusion: Equal(PerimeterOfTriangle(ABC),Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(CA)))
```
备注：  
### triangle_property_angle_sum(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC),
conclusion: Equal(Add(MeasureOfAngle(ABC),MeasureOfAngle(BCA),MeasureOfAngle(CAB)),180)
```
备注：  
### triangle_property_equal_line_to_equal_angle(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Equal(LengthOfLine(AB),LengthOfLine(AC)),
conclusion: Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA))
```
**branch_2**
```json
premise: Triangle(ABC)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA)),
conclusion: Equal(LengthOfLine(AB),LengthOfLine(AC))
```
备注：  
### sine_theorem(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC),
conclusion: Equal(Mul(LengthOfLine(BC),Sin(MeasureOfAngle(ABC))),Mul(LengthOfLine(AC),Sin(MeasureOfAngle(CAB))))
```
备注：  
### cosine_theorem(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC),
conclusion: Equal(Add(Pow(LengthOfLine(AC),2),Mul(2,LengthOfLine(BC),LengthOfLine(AB),Cos(MeasureOfAngle(ABC)))),Add(Pow(LengthOfLine(BC),2),Pow(LengthOfLine(AB),2)))
```
备注：  
### parallel_judgment_alternate_interior_angle(AB,CD)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Angle(BAD)&Angle(CDA)&Equal(MeasureOfAngle(BAD),MeasureOfAngle(CDA)),
conclusion: Parallel(AB,CD)
```
备注：  
### parallel_judgment_Ipsilateral_internal_angle(AB,CD)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Angle(BAC)&Angle(ACD)&Equal(Add(MeasureOfAngle(BAC),MeasureOfAngle(ACD)),180),
conclusion: Parallel(AB,CD)
```
备注：  
### parallel_judgment_par_par(AB,CD,EF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Parallel(AB,CD)&Parallel(CD,EF),
conclusion: Parallel(AB,EF)
```
备注：  
### parallel_judgment_per_per(AB,CD)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Perpendicular(CD,BD)&Perpendicular(DB,AB),
conclusion: Parallel(AB,CD)
```
**branch_2**
```json
premise: Perpendicular(CD,AD)&Perpendicular(BA,DA),
conclusion: Parallel(AB,CD)
```
备注：  
### parallel_property_collinear_extend(AB,CD,M)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Collinear(AMB)&Parallel(AB,CD),
conclusion: Parallel(AM,CD), Parallel(MB,CD)
```
**branch_2**
```json
premise: Collinear(AMB)&Parallel(AM,CD),
conclusion: Parallel(AB,CD), Parallel(MB,CD)
```
**branch_3**
```json
premise: Collinear(AMB)&Parallel(MB,CD),
conclusion: Parallel(AB,CD), Parallel(AM,CD)
```
备注：  
### parallel_property_alternate_interior_angle(AB,CD)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Parallel(AB,CD)&Line(AD),
conclusion: Equal(MeasureOfAngle(BAD),MeasureOfAngle(CDA))
```
**branch_2**
```json
premise: Parallel(AB,CD)&Line(BC),
conclusion: Equal(MeasureOfAngle(CBA),MeasureOfAngle(BCD))
```
备注：  
### parallel_property_Ipsilateral_internal_angle(AB,CD)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Parallel(AB,CD)&Line(AC),
conclusion: Equal(Add(MeasureOfAngle(BAC),MeasureOfAngle(ACD)),180)
```
**branch_2**
```json
premise: Parallel(AB,CD)&Line(DB),
conclusion: Equal(Add(MeasureOfAngle(CDB),MeasureOfAngle(DBA)),180)
```
备注：  
### parallel_property_corresponding_angle(AB,CD,M)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Parallel(AB,CD)&Collinear(MAC),
conclusion: Equal(MeasureOfAngle(MAB),MeasureOfAngle(ACD))
```
**branch_2**
```json
premise: Parallel(AB,CD)&Collinear(MCA),
conclusion: Equal(MeasureOfAngle(BAC),MeasureOfAngle(DCM))
```
备注：  
### parallel_property_extend_perpendicular(AB,CD)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Parallel(AB,CD)&Perpendicular(AC,DC),
conclusion: Perpendicular(BA,CA)
```
**branch_2**
```json
premise: Parallel(AB,CD)&Perpendicular(BA,CA),
conclusion: Perpendicular(AC,DC)
```
备注：  
### intersect_property_vertical_angle(O,AB,CD)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Intersect(O,AB,CD),
conclusion: Equal(MeasureOfAngle(AOC),MeasureOfAngle(BOD))
```
备注：  
### bisector_judgment_angle_equal(BD,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Angle(ABD)&Angle(DBC)&Equal(MeasureOfAngle(ABD),MeasureOfAngle(DBC)),
conclusion: Bisector(BD,ABC)
```
备注：  
### bisector_property_line_ratio(BD,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Bisector(BD,ABC)&Collinear(CDA),
conclusion: Equal(Mul(LengthOfLine(CD),LengthOfLine(BA)),Mul(LengthOfLine(DA),LengthOfLine(BC)))
```
备注：  
### median_judgment(AD,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Midpoint(D,BC)&Line(AD),
conclusion: Median(AD,ABC)
```
备注：  
### neutrality_judgment(DE,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Collinear(ADB)&Collinear(AEC)&Parallel(DE,BC),
conclusion: Neutrality(DE,ABC)
```
备注：  
### neutrality_property_angle_equal(DE,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Neutrality(DE,ABC),
conclusion: Equal(MeasureOfAngle(ADE),MeasureOfAngle(ABC)), Equal(MeasureOfAngle(DEA),MeasureOfAngle(BCA))
```
备注：  
### neutrality_property_line_ratio(DE,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Neutrality(DE,ABC),
conclusion: Equal(Mul(LengthOfLine(AD),LengthOfLine(EC)),Mul(LengthOfLine(DB),LengthOfLine(AE)))
```
备注：  
### neutrality_property_similar(DE,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Neutrality(DE,ABC),
conclusion: Similar(ABC,ADE)
```
备注：  
### altitude_judgment(AD,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Collinear(BDC)&Line(AD)&(Equal(MeasureOfAngle(BDA),90)|Equal(MeasureOfAngle(ADC),90)),
conclusion: IsAltitude(AD,ABC)
```
备注：  
### perpendicular_bisector_judgment(AB,CO)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: (Perpendicular(AO,CO)|Equal(MeasureOfAngle(AOC),90))&(Perpendicular(CO,BO)|Equal(MeasureOfAngle(COB),90))&(Midpoint(O,AB)|Equal(LengthOfLine(AO),LengthOfLine(OB))),
conclusion: PerpendicularBisector(AB,CO)
```
备注：  
### perpendicular_bisector_property_distance_equal(AB,CO)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: PerpendicularBisector(AB,CO),
conclusion: Equal(LengthOfLine(CA),LengthOfLine(CB))
```
备注：  
### perpendicular_judgment_angle(AO,CO)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Angle(AOC)&Equal(MeasureOfAngle(AOC),90),
conclusion: Perpendicular(AO,CO)
```
备注：  
### perpendicular_property_collinear_extend(AO,CO,B)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Perpendicular(AO,CO)&Collinear(AOB),
conclusion: Perpendicular(CO,BO)
```
**branch_2**
```json
premise: Perpendicular(AO,CO)&Collinear(BOC),
conclusion: Perpendicular(BO,AO)
```
**branch_3**
```json
premise: Perpendicular(AO,CO)&(Collinear(ABO)|Collinear(BAO)),
conclusion: Perpendicular(BO,CO)
```
**branch_4**
```json
premise: Perpendicular(AO,CO)&(Collinear(OBC)|Collinear(OCB)),
conclusion: Perpendicular(AO,BO)
```
备注：  
### right_triangle_judgment_angle(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&(Perpendicular(AB,CB)|Equal(MeasureOfAngle(ABC),90)),
conclusion: RightTriangle(ABC)
```
备注：  
### right_triangle_judgment_pythagorean_inverse(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Equal(Add(Pow(LengthOfLine(AB),2),Pow(LengthOfLine(BC),2)),Pow(LengthOfLine(AC),2)),
conclusion: RightTriangle(ABC)
```
备注：  
### right_triangle_property_pythagorean(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: RightTriangle(ABC),
conclusion: Equal(Add(Pow(LengthOfLine(AB),2),Pow(LengthOfLine(BC),2)),Pow(LengthOfLine(AC),2))
```
备注：  
### right_triangle_property_special_rt_30_60(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: RightTriangle(ABC)&(Equal(MeasureOfAngle(CAB),30)|Equal(MeasureOfAngle(BCA),60)),
conclusion: Equal(LengthOfLine(AB),Mul(LengthOfLine(BC),1.7321)), Equal(LengthOfLine(AC),Mul(LengthOfLine(BC),2))
```
**branch_2**
```json
premise: RightTriangle(ABC)&(Equal(MeasureOfAngle(CAB),60)|Equal(MeasureOfAngle(BCA),30)),
conclusion: Equal(LengthOfLine(BC),Mul(LengthOfLine(AB),1.7321)), Equal(LengthOfLine(AC),Mul(LengthOfLine(AB),2))
```
备注：  
### right_triangle_property_special_rt_45_45(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: RightTriangle(ABC)&(Equal(MeasureOfAngle(CAB),45)|Equal(MeasureOfAngle(BCA),45)),
conclusion: Equal(LengthOfLine(AB),LengthOfLine(BC)), Equal(LengthOfLine(AC),Mul(LengthOfLine(AB),1.4142))
```
备注：  
### isosceles_triangle_judgment_angle_equal(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA)),
conclusion: IsoscelesTriangle(ABC)
```
备注：  
### isosceles_triangle_judgment_equilateral(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: EquilateralTriangle(ABC),
conclusion: IsoscelesTriangle(ABC)
```
备注：  
### isosceles_triangle_judgment_line_equal(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Equal(LengthOfLine(AB),LengthOfLine(AC)),
conclusion: IsoscelesTriangle(ABC)
```
备注：  
### isosceles_triangle_property_angle_equal(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: IsoscelesTriangle(ABC),
conclusion: Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA))
```
备注：  
### isosceles_triangle_property_line_coincidence(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: IsoscelesTriangle(ABC)&IsAltitude(AM,ABC),
conclusion: Median(AM,ABC), Bisector(AM,CAB)
```
**branch_2**
```json
premise: IsoscelesTriangle(ABC)&Median(AM,ABC),
conclusion: IsAltitude(AM,ABC), Bisector(AM,CAB)
```
**branch_3**
```json
premise: IsoscelesTriangle(ABC)&Collinear(BMC)&Bisector(AM,CAB),
conclusion: IsAltitude(AM,ABC), Median(AM,ABC)
```
备注：  
### equilateral_triangle_judgment_angle_equal(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(CAB)),
conclusion: EquilateralTriangle(ABC)
```
备注：  
### equilateral_triangle_judgment_isos_and_angle(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: IsoscelesTriangle(ABC)&(Equal(MeasureOfAngle(ABC),60)|Equal(MeasureOfAngle(BCA),60)|Equal(MeasureOfAngle(CAB),60)),
conclusion: EquilateralTriangle(ABC)
```
备注：  
### equilateral_triangle_judgment_line_equal(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Equal(LengthOfLine(AB),LengthOfLine(BC))&Equal(LengthOfLine(BC),LengthOfLine(AC)),
conclusion: EquilateralTriangle(ABC)
```
备注：  
### equilateral_triangle_property_angle(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: EquilateralTriangle(ABC),
conclusion: Equal(MeasureOfAngle(ABC),60)
```
备注：  
### equilateral_triangle_property_line_equal(ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: EquilateralTriangle(ABC),
conclusion: Equal(LengthOfLine(AB),LengthOfLine(BC))
```
备注：  
### congruent_judgment_aas(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(EFD))&Equal(LengthOfLine(CA),LengthOfLine(FD)),
conclusion: Congruent(ABC,DEF)
```
**branch_2**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(DEF))&Equal(LengthOfLine(CA),LengthOfLine(DE)),
conclusion: MirrorCongruent(ABC,DEF)
```
备注：  
### congruent_judgment_asa(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF))&Equal(LengthOfLine(BC),LengthOfLine(EF))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(EFD)),
conclusion: Congruent(ABC,DEF)
```
**branch_2**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD))&Equal(LengthOfLine(BC),LengthOfLine(EF))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(DEF)),
conclusion: MirrorCongruent(ABC,DEF)
```
备注：  
### congruent_judgment_hl(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: RightTriangle(ABC)&RightTriangle(DEF)&Equal(LengthOfLine(AC),LengthOfLine(DF))&(Equal(LengthOfLine(AB),LengthOfLine(DE))|Equal(LengthOfLine(BC),LengthOfLine(EF))),
conclusion: Congruent(ABC,DEF)
```
**branch_2**
```json
premise: RightTriangle(BCA)&RightTriangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(DF))&(Equal(LengthOfLine(AC),LengthOfLine(DE))|Equal(LengthOfLine(BC),LengthOfLine(EF))),
conclusion: MirrorCongruent(ABC,DEF)
```
备注：  
### congruent_judgment_sas(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(DE))&Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF))&Equal(LengthOfLine(BC),LengthOfLine(EF)),
conclusion: Congruent(ABC,DEF)
```
**branch_2**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(FD))&Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD))&Equal(LengthOfLine(BC),LengthOfLine(EF)),
conclusion: MirrorCongruent(ABC,DEF)
```
备注：  
### congruent_judgment_sss(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(DE))&Equal(LengthOfLine(BC),LengthOfLine(EF))&Equal(LengthOfLine(CA),LengthOfLine(FD)),
conclusion: Congruent(ABC,DEF)
```
**branch_2**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(FD))&Equal(LengthOfLine(BC),LengthOfLine(EF))&Equal(LengthOfLine(CA),LengthOfLine(DE)),
conclusion: MirrorCongruent(ABC,DEF)
```
备注：  
### congruent_property_angle_equal(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Congruent(ABC,DEF),
conclusion: Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF))
```
**branch_2**
```json
premise: MirrorCongruent(ABC,DEF),
conclusion: Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD))
```
备注：  
### congruent_property_area_equal(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Congruent(ABC,DEF),
conclusion: Equal(AreaOfTriangle(ABC),AreaOfTriangle(DEF))
```
**branch_2**
```json
premise: MirrorCongruent(ABC,DEF),
conclusion: Equal(AreaOfTriangle(ABC),AreaOfTriangle(DEF))
```
备注：  
### congruent_property_line_equal(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Congruent(ABC,DEF),
conclusion: Equal(LengthOfLine(AB),LengthOfLine(DE))
```
**branch_2**
```json
premise: MirrorCongruent(ABC,DEF),
conclusion: Equal(LengthOfLine(AB),LengthOfLine(DF))
```
备注：  
### congruent_property_perimeter_equal(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Congruent(ABC,DEF),
conclusion: Equal(PerimeterOfTriangle(ABC),PerimeterOfTriangle(DEF))
```
**branch_2**
```json
premise: MirrorCongruent(ABC,DEF),
conclusion: Equal(PerimeterOfTriangle(ABC),PerimeterOfTriangle(DEF))
```
备注：  
### similar_judgment_aa(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))&Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF)),
conclusion: Similar(ABC,DEF)
```
**branch_2**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))&Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD)),
conclusion: MirrorSimilar(ABC,DEF)
```
备注：  
### similar_judgment_sas(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(Mul(LengthOfLine(AB),LengthOfLine(EF)),Mul(LengthOfLine(DE),LengthOfLine(BC)))&Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF)),
conclusion: Similar(ABC,DEF)
```
**branch_2**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(Mul(LengthOfLine(AB),LengthOfLine(EF)),Mul(LengthOfLine(FD),LengthOfLine(BC)))&Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD)),
conclusion: MirrorSimilar(ABC,DEF)
```
备注：  
### similar_judgment_sss(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(Mul(LengthOfLine(AB),LengthOfLine(EF)),Mul(LengthOfLine(DE),LengthOfLine(BC)))&Equal(Mul(LengthOfLine(AB),LengthOfLine(DF)),Mul(LengthOfLine(DE),LengthOfLine(CA))),
conclusion: Similar(ABC,DEF)
```
**branch_2**
```json
premise: Triangle(ABC)&Triangle(DEF)&Equal(Mul(LengthOfLine(AB),LengthOfLine(EF)),Mul(LengthOfLine(FD),LengthOfLine(BC)))&Equal(Mul(LengthOfLine(AB),LengthOfLine(DE)),Mul(LengthOfLine(FD),LengthOfLine(CA))),
conclusion: MirrorSimilar(ABC,DEF)
```
备注：  
### similar_property_angle_equal(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Similar(ABC,DEF),
conclusion: Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF))
```
**branch_2**
```json
premise: MirrorSimilar(ABC,DEF),
conclusion: Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD))
```
备注：  
### similar_property_area_square_ratio(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Similar(ABC,DEF),
conclusion: Equal(Mul(LengthOfLine(AB),LengthOfLine(AB),AreaOfTriangle(DEF)),Mul(LengthOfLine(DE),LengthOfLine(DE),AreaOfTriangle(ABC)))
```
**branch_2**
```json
premise: MirrorSimilar(ABC,DEF),
conclusion: Equal(Mul(LengthOfLine(AB),LengthOfLine(AB),AreaOfTriangle(DEF)),Mul(LengthOfLine(FD),LengthOfLine(FD),AreaOfTriangle(ABC)))
```
备注：  
### similar_property_line_ratio(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Similar(ABC,DEF),
conclusion: Equal(Mul(LengthOfLine(AB),LengthOfLine(EF)),Mul(LengthOfLine(DE),LengthOfLine(BC)))
```
**branch_2**
```json
premise: MirrorSimilar(ABC,DEF),
conclusion: Equal(Mul(LengthOfLine(AB),LengthOfLine(EF)),Mul(LengthOfLine(FD),LengthOfLine(BC)))
```
备注：  
### similar_property_perimeter_ratio(ABC,DEF)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Similar(ABC,DEF),
conclusion: Equal(Mul(LengthOfLine(AB),PerimeterOfTriangle(DEF)),Mul(LengthOfLine(DE),PerimeterOfTriangle(ABC)))
```
**branch_2**
```json
premise: MirrorSimilar(ABC,DEF),
conclusion: Equal(Mul(LengthOfLine(AB),PerimeterOfTriangle(DEF)),Mul(LengthOfLine(FD),PerimeterOfTriangle(ABC)))
```
备注：  
### circumcenter_judgment(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Collinear(BDC)&Collinear(CEA)&PerpendicularBisector(BC,OD)&PerpendicularBisector(CA,OE),
conclusion: Circumcenter(O,ABC)
```
备注：  
### circumcenter_property_intersect(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Circumcenter(O,ABC)&Collinear(BEC)&(Perpendicular(BE,OE)|Perpendicular(OE,CE)),
conclusion: PerpendicularBisector(BC,OE)
```
**branch_2**
```json
premise: Circumcenter(O,ABC)&Midpoint(M,BC),
conclusion: PerpendicularBisector(BC,OM)
```
备注：  
### circumcenter_property_line_equal(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Circumcenter(O,ABC),
conclusion: Equal(LengthOfLine(OA),LengthOfLine(OB))
```
备注：  
### incenter_property_intersect(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Incenter(O,ABC),
conclusion: Bisector(AO,CAB)
```
备注：  
### incenter_property_judgment(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Bisector(AO,CAB)&Bisector(CO,BCA),
conclusion: Incenter(O,ABC)
```
备注：  
### incenter_property_line_equal(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Incenter(O,ABC)&Collinear(ADB)&Collinear(BEC)&(Perpendicular(AD,OD)|Perpendicular(OD,BD))&(Perpendicular(BE,OE)|Perpendicular(OE,CE)),
conclusion: Equal(LengthOfLine(OD),LengthOfLine(OE))
```
备注：  
### centroid_judgment(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&Median(AM,ABC)&Median(BN,BCA)&Collinear(AOM)&Collinear(BON),
conclusion: Centroid(O,ABC)
```
备注：  
### centroid_property_intersect(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Centroid(O,ABC)&Collinear(AOM)&Collinear(BMC),
conclusion: Median(AM,ABC)
```
备注：  
### centroid_property_line_equal(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Centroid(O,ABC)&Collinear(AOM)&Collinear(BMC),
conclusion: Equal(LengthOfLine(OA),Mul(LengthOfLine(OM),2))
```
备注：  
### orthocenter_property_intersect(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Orthocenter(O,ABC)&Collinear(AOD)&Collinear(BDC),
conclusion: IsAltitude(AD,ABC)
```
备注：  
### orthocenter_property_judgment(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Triangle(ABC)&IsAltitude(AM,ABC)&IsAltitude(BN,BCA)&Intersect(O,MA,BN),
conclusion: Orthocenter(O,ABC)
```
备注：  
### orthocenter_property_line_equal(O,ABC)
parameter:  
<div>
    <img src="cowork-pic/?.png"  width="60%">
</div>

**branch_1**
```json
premise: Orthocenter(O,ABC)&Angle(COB),
conclusion: Equal(MeasureOfAngle(COB),Add(MeasureOfAngle(ABC),MeasureOfAngle(BCA)))
```
备注：  
