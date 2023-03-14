## 附录2 谓词标注对照手册
### A、基本构图谓词
#### Polygon(*)
<div>
    <img src="cowork-pic/Polygon.png" width="40%">
</div>

    Polygon(ABCDE),Polygon(BCDEA),Polygon(CDEAB),Polygon(DEABC),Polygon(EABCD)

**Notes**:  
例1 Polygon(ADE),Polygon(DBCE)    
例2 Polygon(ABC),Polygon(ACD),Polygon(ADE),Polygon(AEF)   

#### Collinear(*)
<div>
    <img src="cowork-pic/Collinear.png" width="40%">
</div>

    Collinear(AMB),Collinear(BMA)

**Notes**:  
例1 Collinear(AOB),Collinear(COD)  
例2 Collinear(BCDEF)  

#### Cocircular(O,*)
<div>
    <img src="cowork-pic/Cocircular.png" width="27%">
</div>

    Cocircular(O,AC),Cocircular(O,CA)

**Notes**:  
例1 Cocircular(O,ABCD)  

### B、基本实体
#### Point(A)
<div>
    <img src="cowork-pic/Point.png" width="40%">
</div>

    Point(A)

**Notes**:  
例1 Point(A),Point(B),Point(C)  
例2 Point(O),Point(A),Point(C)  

#### Line(AB)
<div>
    <img src="cowork-pic/Line.png" width="40%">
</div>

    Line(AB),Line(BA)

**Notes**:  
例1 Line(AB),Line(CD)  
例2 Line(AO),Line(BO)  

#### Angle(ABC)
<div>
    <img src="cowork-pic/Angle.png" width="40%">
</div>

    Angle(AOB)

**Notes**:   
例1 Angle(ABC),Angle(BCA),Angle(CAB)  
例2 Angle(AOC),Angle(COB),Angle(BOD),Angle(DOA)  

#### Triangle(ABC)
<div>
    <img src="cowork-pic/Triangle.png" width="40%">
</div>

    Triangle(ABC),Triangle(BCA),Triangle(CAB)


**Notes**:  
例1 Triangle(ADE),Triangle(ABC)  
例2 Triangle(ABD),Triangle(ADC),Triangle(ABC)  

#### Quadrilateral(ABCD)
<div>
    <img src="cowork-pic/Quadrilateral.png" width="40%">
</div>

    Quadrilateral(ABCD),Quadrilateral(BCDA),Quadrilateral(CDAB),Quadrilateral(DABC)

**Notes**:  
例1 Quadrilateral(DBCE)  
例2 Quadrilateral(ABCD)  

#### Arc(AB)
<div>
    <img src="cowork-pic/Arc.png" width="40%">
</div>

    Arc(AB)

**Notes**:  
例1: Arc(AC),Arc(CA)  
例2: Arc(AB),Arc(BC),Arc(CD),...  

#### Circle(O)
<div>
    <img src="cowork-pic/Circle.png" width="40%">
</div>

    Circle(O)

**Notes**:  
例1: Circle(A),Circle(B)  
例2: Circle(O)  

### C、实体
#### RightTriangle(ABC)
<div>
    <img src="cowork-pic/RightTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: 
    extend: Perpendicular(AB,CB)
            IsAltitude(AB,ABC)
**Notes**:  

#### IsoscelesTriangle(ABC)
<div>
    <img src="cowork-pic/IsoscelesTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: 
    extend: Equal(LengthOfLine(AB),LengthOfLine(AC))
**Notes**:  

#### EquilateralTriangle(ABC)
<div>
    <img src="cowork-pic/EquilateralTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: BCA
           CAB
    extend: Equal(LengthOfLine(AB),LengthOfLine(AC))
            Equal(LengthOfLine(AB),LengthOfLine(BC))
**Notes**:  

### D、实体关系
#### Midpoint(M,AB)
<div>
    <img src="cowork-pic/Midpoint.png"  width="14%">
</div>

    ee_check: Point(M)
              Line(AB)
    fv_check: M,AB
    multi: M,BA
    extend: Equal(LengthOfLine(AM),LengthOfLine(MB))
**Notes**:  

#### Intersect(O,AB,CD)
<div>
    <img src="cowork-pic/Intersect.png"  width="14%">
</div>

    ee_check: Point(O)
              Line(AB)
              Line(CD)
    fv_check: O,AB,CD
    multi: O,CD,BA
           O,BA,DC
           O,DC,AB
    extend: 
**Notes**:  

#### Parallel(AB,CD)
<div>
    <img src="cowork-pic/Parallel.png"  width="14%">
</div>

    ee_check: Line(AB)
              Line(CD)
    fv_check: AB,CD
    multi: DC,BA
    extend: 
**Notes**:  

#### Perpendicular(AO,CO)
<div>
    <img src="cowork-pic/Perpendicular.png"  width="14%">
</div>

    ee_check: Line(AO)
              Line(CO)
    fv_check: AO,CO
    multi: 
    extend: Equal(MeasureOfAngle(AOC),90)
**Notes**:  

#### PerpendicularBisector(AB,CO)
<div>
    <img src="cowork-pic/PerpendicularBisector.png"  width="14%">
</div>

    ee_check: Line(AB)
              Line(CO)
    fv_check: AB,CO
    multi: 
    extend: Perpendicular(AO,CO)
            Perpendicular(CO,BO)
            Midpoint(O,AB)
**Notes**:  

#### Bisector(BD,ABC)
<div>
    <img src="cowork-pic/Bisector.png"  width="14%">
</div>

    ee_check: Line(BD)
              Angle(ABC)
    fv_check: BD,ABC
    multi: 
    extend: Equal(MeasureOfAngle(ABD),MeasureOfAngle(DBC))
**Notes**:  

#### Median(AD,ABC)
<div>
    <img src="cowork-pic/Median.png"  width="14%">
</div>

    ee_check: Line(AD)
              Triangle(ABC)
    fv_check: AD,ABC
    multi: 
    extend: Midpoint(D,BC)
**Notes**:  

#### IsAltitude(AD,ABC)
<div>
    <img src="cowork-pic/IsAltitude.png"  width="14%">
</div>

    ee_check: Line(AD)
              Triangle(ABC)
    fv_check: AD,ABC
              AB,ABC
              AC,ABC
    multi: 
    extend: Perpendicular(BD,AD)
            Perpendicular(AD,CD)
            Equal(LengthOfLine(AD),AltitudeOfTriangle(ABC))
**Notes**:  

#### Neutrality(DE,ABC)
<div>
    <img src="cowork-pic/Neutrality.png"  width="14%">
</div>

    ee_check: Line(DE)
              Triangle(ABC)
    fv_check: DE,ABC
    multi: 
    extend: Parallel(DE,BC)
**Notes**:  

#### Circumcenter(O,ABC)
<div>
    <img src="cowork-pic/Circumcenter.png"  width="14%">
</div>

    ee_check: Point(O)
              Triangle(ABC)
    fv_check: O,ABC
    multi: O,BCA
           O,CAB
    extend: 
**Notes**:  

#### Incenter(O,ABC)
<div>
    <img src="cowork-pic/Incenter.png"  width="14%">
</div>

    ee_check: Point(O)
              Triangle(ABC)
    fv_check: O,ABC
    multi: O,BCA
           O,CAB
    extend: 
**Notes**:  

#### Centroid(O,ABC)
<div>
    <img src="cowork-pic/Centroid.png"  width="14%">
</div>

    ee_check: Point(O)
              Triangle(ABC)
    fv_check: O,ABC
    multi: O,BCA
           O,CAB
    extend: 
**Notes**:  

#### Orthocenter(O,ABC)
<div>
    <img src="cowork-pic/Orthocenter.png"  width="14%">
</div>

    ee_check: Point(O)
              Triangle(ABC)
    fv_check: O,ABC
              A,ABC
              B,ABC
              C,ABC
    multi: O,BCA
           O,CAB
    extend: 
**Notes**:  

#### Congruent(ABC,DEF)
<div>
    <img src="cowork-pic/Congruent.png"  width="25%">
</div>

    ee_check: Triangle(ABC)
              Triangle(DEF)
    multi: DEF,ABC
           BCA,EFD
           EFD,BCA
           CAB,FDE
           FDE,CAB
    extend: 
**Notes**:  

#### Similar(ABC,DEF)
<div>
    <img src="cowork-pic/Similar.png"  width="25%">
</div>

    ee_check: Triangle(ABC)
              Triangle(DEF)
    multi: DEF,ABC
           BCA,EFD
           EFD,BCA
           CAB,FDE
           FDE,CAB
    extend: 
**Notes**:  

#### MirrorCongruent(ABC,DEF)
<div>
    <img src="cowork-pic/MirrorCongruent.png"  width="25%">
</div>

    ee_check: Triangle(ABC)
              Triangle(DEF)
    multi: DEF,ABC
           BCA,FDE
           FDE,BCA
           CAB,EFD
           EFD,CAB
    extend: 
**Notes**:  

#### MirrorSimilar(ABC,DEF)
<div>
    <img src="cowork-pic/MirrorSimilar.png"  width="25%">
</div>

    ee_check: Triangle(ABC)
              Triangle(DEF)
    multi: DEF,ABC
           BCA,FDE
           FDE,BCA
           CAB,EFD
           EFD,CAB
    extend: 
**Notes**:  

### E、基本实体属性
#### LengthOfLine(AB)
<div>
    <img src="cowork-pic/LengthOfLine.png"  width="14%">
</div>

    ee_check: Line(AB)
    multi: BA
    sym: ll
**Notes**:  

#### LengthOfArc(AB)
<div>
    <img src="cowork-pic/LengthOfArc.png"  width="14%">
</div>

    ee_check: Arc(AB)
    multi: 
    sym: la
**Notes**:  

#### MeasureOfAngle(ABC)
<div>
    <img src="cowork-pic/MeasureOfAngle.png"  width="14%">
</div>

    ee_check: Angle(ABC)
    multi: 
    sym: ma
**Notes**:  

### F、实体属性
#### AreaOfTriangle(ABC)
<div>
    <img src="cowork-pic/AreaOfTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: BCA
           CAB
    sym: at
**Notes**:  
例 Equal(AreaOfTriangle(ABC),10)  

#### PerimeterOfTriangle(ABC)
<div>
    <img src="cowork-pic/PerimeterOfTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: BCA
           CAB
    sym: pt
**Notes**:  
例 Equal(PerimeterOfTriangle(ABC),10)  

#### AltitudeOfTriangle(ABC)
<div>
    <img src="cowork-pic/AltitudeOfTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: 
    sym: alt
**Notes**:  
例 Equal(AltitudeOfTriangle(ABC),5)  

#### DistanceOfPointToLine(O,AB)
<div>
    <img src="cowork-pic/DistanceOfPointToLine.png"  width="14%">
</div>

    ee_check: Point(O)
              Line(AB)
    fv_check: O,AB
              B,AB
              A,AB
    multi: OBA
    sym: dpl
**Notes**:  
例 Equal(DistanceOfPointToLine(O,AB),3)  

### G、代数关系

    Equal(expr1,expr2)
    
**Notes**:  
expr可以是表达式，也可以是实体属性，并且可以嵌套表示。  

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
#### Value

    Value(LengthOfLine(AB))
    Value(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)))
    Value(x+y)

**Notes**:  
代数型解题目标，求某个表达式或属性的值。  
expr可以是表达式，也可以是实体属性，并且可以嵌套表示。  

#### Equal


    Equal(LengthOfLine(AB),x+y)
    Equal(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)),Pow(x,2))
    
**Notes**:  
代数型解题目标，证明左右俩个部分相等。  
expr可以是表达式，也可以是实体属性，并且可以嵌套表示。  

#### Relation
逻辑型解题目标，求某个实体或属性。  


    Relation(Parallel(AB,CD))
    Relation(RightTriangle(ABC))    

**Notes**:  
代数型解题目标，证明左右俩个部分相等。  
Relation表示任意实体、实体关系。  

