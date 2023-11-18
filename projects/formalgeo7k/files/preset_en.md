# GFS-Basic

GFS-Basic是基于[几何形式化理论](https://arxiv.org/abs/2310.18021)设计的几何形式化系统，适用求解器
[FormalGeo](https://github.com/FormalGeo/FormalGeo)的版本为0.0.1。FormalGeo-0.0.1包含25个内置的谓词，GFS-Basic在此基础之上，
详细总结了平面几何领域常见的名词和定理，新定义了63个谓词和196个定理。

## Preset Predicates

内置谓词包括:  
3个构图谓词：Shape、Collinear、Cocircular；6个基本实体谓词：Point、Line、Arc、Angle、Polygon、Circle；2个代数关系谓词：
Equal、Equation；1个属性谓词：Free；10个运算谓词：Add、Sub、Mul、Div、Pow、Mod、Sqrt、Sin、Cos、Tan；3个解题目标谓词：
Value、Equal、Relation。

### 构图谓词

#### Shape(*)

Shape是最基本的构图谓词，它使用若干个边或弧来声明一个几何图形，这个几何图形可以是一条边，可以是一个角，也可以是边和弧围成的图形。使用Shape声明
几何图形时，我们需要依据有序原则、逆时针原则和旋转不变原则，这三大原则的介绍可参考cowork.md。
<div>
    <img src="pic/Shape.png" alt="Shape" width="60%">
</div>

**1.声明一个点**  
如图1所示，P是圆O的圆心，我们可以这样声明一个点：

    Shape(P)

**2.声明一条线段**  
如图2所示，AB是线段的两点，我们可以这样声明线段：

    Shape(AB)

当使用Shape声明线段时，默认线段是无向的，所以这样声明也是合法的：

    Shape(BA)

**3.声明一个角**  
如图3所示，角B由两条线段构成。需要注意，在声明角时，线段是有向的，两条线出现的顺序按照逆时针的方向，首尾相接。因此角B可以表示为：

    Shape(AB,BC)

**4.声明一个封闭图形**  
如果一个边一个边或一个角一个角来声明图形，未免也太麻烦了。我们可以直接声明一个由若干线段和弧构成的图形，在构图阶段，推理器会自动扩展出图形中的
角、线和弧。因此我们在标注图形的构图语句时，先使用Shape声明所有的最小封闭图形，然后在把那些不封闭的最小图形如角、线段、点等声明，就可以声明整个图形。  
对于图3中的四边形，我们可以这样声明：

    Shape(AB,BC,CD,DA)
    Shape(BC,CD,DA,AB)
    Shape(CD,DA,AB,BC)
    Shape(DA,AB,BC,CD)

根据旋转不变原则，一个四边形有上述四种表示，我们选择一种就可以。  
更复杂的图形，如图4，可以声明为：

    Shape(OAB,BE,EA)
    Shape(OBC,CE,EB)
    Shape(EC,OCD,DP,PE)
    Shape(AE,EP,PD,ODA)

需注意，虽然EP和PD是共线的，但在声明封闭图形时，不能直接声明ED，需要把最小的边都声明出来。  
封闭图形可以由线和弧构成，线有两个方向，弧只有一个方向。在声明线时，需要按照逆时针的方向，各点首尾相接；声明弧时，需注意弧只有一种表示方法。  
当弧单独出现时，不需要使用Shape来声明，因为弧的出现必然伴随着Cocircular谓词，所有弧将会由Cocircular谓词自动扩展得到。

#### Collinear(*)

Collinear用来声明3个及3个以上的共线点，2点一定是共线的，所以不用声明2点。

<div>
    <img src="pic/Collinear.png" alt="Collinear" width="45%">
</div>

共线声明是及其简单的，只要按顺序列出一条线上所有的点即可，如图1中的共线可声明为：

    Collinear(AMB)

共线没有方向之分，从另一个方向声明也是合法的：

    Collinear(BMA)

图2中的共线可声明为：

    Collinear(BCDEF)

图3中的共线可声明为：

    Collinear(ADB)
    Collinear(AEC)

共线会在推理器中自动扩展出所有的线和平角，如Collinear(AMB)会扩展得到Line(AM),Line(MB),Line(AM),Angle(AMB),Angle(BMA)。

#### Cocircular(O,*)

Cocircular用来声明共圆的若干个点，与Collinear相同，按照顺序列出若干点即可；但也与Collinear不同，一是即使1个点在圆上也要声明，二是共圆的
声明按照逆时针方向，且从任何点开始都可。
<div>
    <img src="pic/Cocircular.png" alt="Cocircular" width="60%">
</div>

在图1中，共圆的几点可声明为：

    Cocircular(O,ABCD)
    Cocircular(O,BCDA)
    Cocircular(O,CDAB)
    Cocircular(O,DABC)

依据三大原则，图1的共圆声明可以有上述4种形式，任选其1即可。图2到图4是几种比较特殊的共圆声明。
图2的圆上只有1个点，也要声明：

    Cocircular(O,A)

图3圆上没有点，也要声明：

    Cocircular(O)

图4两圆有公共点，要分别声明：

    Cocircular(O,AB)
    Cocircular(P,BA)

共圆声明后，会自动扩展出所有的弧和圆。

### 基本实体谓词

基本实体是由基本构图扩展来的实体，在构图结束后不会再改变。我们无需声明基本实体，下述内容是为了让我们理解形式化系统的内在逻辑。
基本构图谓词声明一个图形的结构信息，也就是点的相对位置信息。基本实体相当于是基本构图的unzip版本，在推理过程中更方便使用。

#### Point(A)

就是点，没什么好说的。
<div>
    <img src="pic/Point.png" alt="Point" width="45%">
</div>

图1-3的点的声明：

    Point(A)
    Point(A),Point(B),Point(C)
    Point(A),Point(C),Point(O)

#### Line(AB)

Line声明一个无向线段。
<div>
    <img src="pic/Line.png" alt="Line" width="45%">
</div>

因为是无向的，所以图1的线段有两种声明方法，选其一即可：

    Line(AB)
    Line(BA)

图2和图3的线段声明：

    Line(AB),Line(CD)  
    Line(AO),Line(BO) 

#### Arc(OAB)

Arc声明一段弧，由3个点组成，第1个点是弧所在的圆，其余2点是构成弧的点，按照逆时针的方向有序列出。
<div>
    <img src="pic/Arc.png" alt="Arc" width="45%">
</div>

图1-3中弧的声明：

    Arc(OAB)
    Arc(OAC),Arc(OCA)
    Arc(OAB),Arc(OBC),Arc(OCD),Arc(ODA)

#### Angle(ABC)

角由3个点构成，在声明角时，需要按照逆时针原则。
<div>
    <img src="pic/Angle.png" alt="Angle" width="45%">
</div>

图1-3的角的声明：

    Angle(AOB)
    Angle(ABC),Angle(BCA),Angle(CAB)
    Angle(AOC),Angle(COB),Angle(BOD),Angle(DOA)

#### Polygon(*)

多边形由若干个直线构成，按照逆时针的方向列出所有的点。依据旋转不变原则，一个n边形有n种表示方式。
<div>
    <img src="pic/Polygon.png" alt="Polygon" width="45%">
</div>

    Polygon(ABC),Polygon(BCA),Polygon(CAB)
    Polygon(ABCD),Polygon(BCDA),Polygon(CDAB),Polygon(DABC)
    Polygon(ABCDE),Polygon(BCDEA),Polygon(CDEAB),Polygon(DEABC),Polygon(EABCD)

#### Circle(O)

Circle用于声明一个圆，注意区别圆和圆心。
<div>
    <img src="pic/Circle.png" alt="Circle" width="45%">
</div>

图1-3中圆的声明：

    Cirlce(O)
    Cirlce(B),Cirlce(A)
    Cirlce(O)

### 代数关系谓词

代数关系由代数式表达，记为expr。expr是由符号、运算符、属性嵌套构成的式子。凡是符合sympy语法的表达式都可以被正确的解析。

#### Equal(expr1,expr2)

Equal接受两个expr，表示代数的等价关系。

    Equal(a,5)  
    Equal(MeasureOfAngle(ABC),30)  
    Equal(Add(LengthOfLine(AB),a+5,x),y^2)

#### Equation(expr)

Equation接受一个expr，表示方程。

    Equation(a-5)  
    Equation(Sub(MeasureOfAngle(ABC),30))  
    Equation(Sub(Add(LengthOfLine(AB),a+5,x),y^2))

### 属性谓词

#### Free(y)

声明一个自由符号，可以表示未知数或代指某个几何属性。

### 运算符谓词

|  名称  |         格式         |   表达式符号   | 运算符优先级 |
|:----:|:------------------:|:---------:|:------:|
|  加   | Add(expr1,expr2,…) |     +     |   1    |
|  减   |  Sub(expr1,expr2)  |     -     |   1    |
|  乘   | Mul(expr1,expr2,…) |     *     |   2    |
|  除   |  Div(expr1,expr2)  |     /     |   2    |
|  幂   |  Pow(expr1,expr2)  |    **     |   3    |
|  幂   |  Mod(expr1,expr2)  |    mod    |   3    |
|  根号  |    Sqrt(expr1)     |   sqrt    |   4    |
|  正弦  |     Sin(expr)      |    sin    |   4    |
|  余弦  |     Cos(expr)      |    cos    |   4    |
|  正切  |     Tan(expr)      |    tan    |   4    |
|  实数  |         R          | 1,2,3,... |   /    |
| 自由变量 |         f          | a,b,c,... |   /    |
| 左括号  |         /          |     (     |   5    |
| 右括号  |         /          |     )     |   0    |  

### 解题目标谓词

#### Value(expr)

expr可以是表达式，也可以是实体属性，并且可以嵌套表示。  
代数型解题目标，求某个表达式或属性的值。

    Value(LengthOfLine(AB))
    Value(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)))
    Value(x+y)

#### Equal(expr1,expr2)

expr可以是表达式，也可以是实体属性，并且可以嵌套表示。
代数型解题目标，证明左右俩个部分相等。

    Equal(LengthOfLine(AB),x+y)
    Equal(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)),Pow(x,2))

#### Relation(*)

逻辑型解题目标，求某个实体或属性。  
Relation表示任意实体、实体关系。

    Relation(Parallel(AB,CD))
    Relation(RightTriangle(ABC))  

