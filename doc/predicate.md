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