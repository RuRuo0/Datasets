# FormalGeo20K数据集标注指南
随着现代科学的深入发展，学科分支变得越来越多，科学理论变得艰深难懂，同行审阅周期越来越长，阻碍了科学的进一步发展。自计算机出现以来，人们就尝试利用计算机强大的运算和推理能力来辅助科学研究，但受限于计算机的特点，需要先将科学知识转化为结构化的形式。在几何形式化、几何机械化领域，长期受制于三大难题：知识形式难统一、证明过程不可读、几何证明无定法。设计一套有严密语法结构但同时符合人类阅读习惯的、统一几何问题文字描述和图像描述的、统一计算和推理过程的形式化语言，是解决上述三大难题的一条可行路径。

## 1.形式化语言简介
FormalGeo形式化语言包括两大组成部分，分别是**几何定义语言（GDL）**和**条件声明语言（CDL）**。GDL用于配置推理器，使其具有可扩展性；CDL用于几何问题的形式化输入。FormalGeo形式化语言采用类似谓词逻辑的语法结构，非常容易上手,在标注工作中，我们只需关注如何将几何问题转化为CDL即可。

### 1.1几何本体论与几何表示论
**几何本体论**研究几何学领域的根本性本体，以及本体之间的关系，是问题*我们需要形式化那些东西？*的回答，其理论成果如下图所示。
<div align=center>
    <img src="cowork-pic/four-quadrant.png" width="60%">
    <br>
    Figure 1. 几何本体域-二维四象限
</div>

**几何表示论**是研究如何使用文字或符号来表示几何图形的理论，是问题*我们如何形式化？*的回答，其理论成果包括对应一致性原则和构造性作图法。对应一致性原则是指原始系统和形式化系统的静态描述和动态过程要一一对应。在几何领域，静态描述指的是几何问题的条件，动态过程是指定理。构造性作图法采用最少数量的形式化语句来描述几何图形，并按照机械化的方法自动构建出所有的几何元素。

### 1.2语法
**CDL**采用点的有序对来描述几何图形，根据其作用，可以分为三类。第一类是**构图语句**，包括基本构图语句和基本实体，推理器利用少量构图语句来构建所有的几何元素；第二类是**条件语句**，用于描述几何问题的前提条件，包括数量关系和实体关系；第三类是目标语句，用于声明几何问题的求解目标。  
CDL语法与谓词逻辑类似，非常简单易学，我们举两个例子：  

    Triangle(ABC)
    Equal(LengthOfLine(AB),LengthOfLine(CD))

很显然，第一句话声明了一个三角形，ABC是三角形的三个顶点；第二句话声明了一个数量关系，即直线AB的长度与直线CD的长度相等。  
现在我们介绍几个基本的概念。  
在上述两条CDL语句中，*Triangle*和*Equal*称作谓词，用于描述一种几何元素或几何元素之间的关系；*括号中的内容*称为个体词，在实体关系中，个体词为点的有序对，在数量关系中，个体词为由实数、运算符和符号构成的表达式；*LengthOfLine*称为函数，是个体词到个体词的映射，准确来说是实体关系个体词到代数关系个体词的映射，我们通过这样的映射，就可以用点的有序对来表示数量关系，实现了实体关系和数量关系表示形式的统一。  
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
1.复制模板到 data/formalized-problems ，并改名为 <problem_id>.json：
<div align=center>
    <img src="cowork-pic/23.png">
</div>

2.将原始问题具有的信息添加到 <problem_id>.json ，同时添加上自己的标注信息：  
<div align=center>
    <img src="cowork-pic/24.png">
</div>

3.按照附录的各种手册，标注并保存问题。

### 3.3提交已标注的问题
在每周的标注任务**全部完成后**，将所有的标注文件统一提交。  
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
## 附录1 谓词列表
### A、基本构图
| 名称 | 格式 | 多种表示 | 实体存在性约束 | 扩展 |
|:---:|:---:|:---:|:---:|:---:|
| 基本形状 | Polygon($) | * | / | Angle,Triangle,Quadrilateral |
| 共线点 | Collinear($) | * | / | Angle |
| 共圆点 | Cocircular(O,$) | * | / | Arc,Circle |

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

### C、实体
| 名称 | 格式 | 多种表示 | 实体存在性约束 | 扩展 |
|:---:|:---:|:---:|:---:|:---:|
| 直角三角形 | RightTriangle(ABC) | / | Triangle(ABC) | Perpendicular(AB,CB) |
| 等腰三角形 | IsoscelesTriangle(ABC) | / | Triangle(ABC) | Equal(LengthOfLine(AB),LengthOfLine(AC)) |
| 等边三角形 | EquilateralTriangle(ABC) | BCA,<br>CAB | Triangle(ABC) | Equal(LengthOfLine(AB),LengthOfLine(AC))<br>Equal(LengthOfLine(AB),LengthOfLine(BC)) |

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

### I、解题目标
|名称|格式|备注|
|:--:|:--:|:--:|
|证相等|Equal(expr1,expr2)|expr可以是表达式，也可以是实体属性，并且可以嵌套表示|
|求值|Value(expr)|expr表示由运算和实体属性构成的表达式|
|求关系|Relation($)|Relation表示任意实体、实体关系|

## 附录2 定理列表
|名称|描述|
|:--:|:--:|
|line_addition|/|
|angle_addition|/|
|perpendicular_property_collinear_extend|/|
|triangle_property_angle_sum|/|
|triangle_property_equal_line_to_equal_angle|/|
|triangle_perimeter_formula|/|
|sine_theorem|/|
|cosine_theorem|/|
|right_triangle_judgment_angle|/|
|pythagorean|/|
|right_triangle_property_special_rt_30_60|/|
|isosceles_triangle_judgment_equilateral|/|
|isosceles_triangle_property_line_coincidence|/|
|neutrality_property_line_ratio|/|
|neutrality_judgment|/|
|bisector_judgment_angle_equal|/|
|bisector_property_line_ratio|/|
|incenter_property_intersect|/|
|congruent_property_angle_equal|/|
|similar_property_line_ratio|/|

## 附录3 图形-文字对照手册
标注几何问题CDL的顺序为：  
**1.标注构图CDL**  
首先标注基本构图CDL，有3个，分别是Polygon、Collinear和Cocircular。在推理器构图阶段，会根据识别到的基本构图CDL自动构建基本实体CDL，参见图<构图的自动扩展>。标注完基本构图CDL后，还需要补充标注无法由基本构图CDL扩展得到的基本实体CDL（这就要求对于构图过程比较熟悉，其实也很简单）。  
**2.标注条件CDL**  
包括图像和文字的标注。  
**3.标注目标CDL**  
共有三类，分别是Value、Equal、Relation。  
<div align=center>
    <img src="cowork-pic/auto-expand.png" width="60%">
    构图的自动扩展
</div>

### A、基本构图谓词
#### Polygon
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Collinear
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Cocircular
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
### B、基本实体
#### Point
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Line
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Angle
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Triangle
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Quadrilateral
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Arc
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Circle
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
### C、实体
#### RightTriangle
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### IsoscelesTriangle
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### EquilateralTriangle
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
### D、实体关系
#### Midpoint
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Intersect
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Parallel
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Perpendicular
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### PerpendicularBisector
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Bisector
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Median
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### IsAltitude
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Neutrality
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Circumcenter
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Incenter
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Centroid
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Orthocenter
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Congruent
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### Similar
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### MirrorCongruent
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
#### MirrorSimilar
<div align=center>
    <img src="cowork-pic/?.png" width="50%">
</div>

CDL：  
标注要点：  
例1：  
例2：  
### E、基本实体属性,实体属性,代数关系和代数运算
### F、解题目标
