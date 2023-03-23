## 附录2 谓词标注对照手册
### A、基本构图谓词
#### Polygon(*)
<div>
    <img src="cowork-pic/Polygon.png" width="40%">
</div>

    Polygon(ABCDE),Polygon(BCDEA),Polygon(CDEAB),Polygon(DEABC),Polygon(EABCD)
    example: 1 Polygon(ADE),Polygon(DBCE)
             2 Polygon(ABC),Polygon(ACD),Polygon(ADE),Polygon(AEF)

**Notes**:    

#### Collinear(*)
<div>
    <img src="cowork-pic/Collinear.png" width="40%">
</div>

    Collinear(AMB),Collinear(BMA)
    example: 1 Collinear(AOB),Collinear(COD)
             2 Collinear(BCDEF)

**Notes**:  

#### Cocircular(O,*)
<div>
    <img src="cowork-pic/Cocircular.png" width="27%">
</div>

    Cocircular(O,AC),Cocircular(O,CA)
    example: 1 Cocircular(O,ABCD)

**Notes**:  

### B、基本实体
#### Point(A)
<div>
    <img src="cowork-pic/Point.png" width="40%">
</div>

    Point(A)
    example: 1 Point(A),Point(B),Point(C)
             2 Point(O),Point(A),Point(C)

**Notes**:  

#### Line(AB)
<div>
    <img src="cowork-pic/Line.png" width="40%">
</div>

    Line(AB),Line(BA)
    example: 1 Line(AB),Line(CD)
             2 Line(AO),Line(BO)

**Notes**:  

#### Angle(ABC)
<div>
    <img src="cowork-pic/Angle.png" width="40%">
</div>

    Angle(AOB)
    example: 1 Angle(ABC),Angle(BCA),Angle(CAB)
             2 Angle(AOC),Angle(COB),Angle(BOD),Angle(DOA)

**Notes**:  

#### Triangle(ABC)
<div>
    <img src="cowork-pic/Triangle.png" width="40%">
</div>

    Triangle(ABC),Triangle(BCA),Triangle(CAB)
    example: 1 Triangle(ADE),Triangle(ABC)
             2 Triangle(ABD),Triangle(ADC),Triangle(ABC)


**Notes**:  

#### Quadrilateral(ABCD)
<div>
    <img src="cowork-pic/Quadrilateral.png" width="40%">
</div>

    Quadrilateral(ABCD),Quadrilateral(BCDA),Quadrilateral(CDAB),Quadrilateral(DABC)
    example: 1 Quadrilateral(DBCE)
             2 Quadrilateral(ABCD)

**Notes**:  

#### Arc(AB)
<div>
    <img src="cowork-pic/Arc.png" width="40%">
</div>

    Arc(AB)
    example: 1 Arc(AC),Arc(CA)
             2 Arc(AB),Arc(BC),Arc(CD),...

**Notes**:  

#### Circle(O)
<div>
    <img src="cowork-pic/Circle.png" width="40%">
</div>

    Circle(O)
    example: 1 Circle(A),Circle(B)
             2 Circle(O)

**Notes**:  
 
### C、实体
#### RightTriangle(ABC)
<div>
    <img src="cowork-pic/RightTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: 
    extend: Perpendicular(AB,CB)
            IsAltitude(AB,ABC)
    example: 
**Notes**:  

#### IsoscelesTriangle(ABC)
<div>
    <img src="cowork-pic/IsoscelesTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: 
    extend: Equal(LengthOfLine(AB),LengthOfLine(AC))
    example: 
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
    example: 
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
    example: 
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
    example: 
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
    example: 
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
    example: 
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
    example: 
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
    example: 
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
    example: 
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
    example: 
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
    example: 
**Notes**:  

#### Midsegment(DE,ABC)
<div>
    <img src="cowork-pic/Midsegment.png"  width="14%">
</div>

    ee_check: Line(DE)
              Triangle(ABC)
    fv_check: DE,ABC
    multi: 
    extend: Neutrality(DE,ABC)
            Midpoint(D,AB)
            Midpoint(E,AC)
    example: 
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
    example: 
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
    example: 
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
    example: 
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
    example: 
**Notes**:  

#### Congruent(ABC,DEF)
<div>
    <img src="cowork-pic/Congruent.png"  width="20%">
</div>

    ee_check: Triangle(ABC)
              Triangle(DEF)
    multi: DEF,ABC
           BCA,EFD
           EFD,BCA
           CAB,FDE
           FDE,CAB
    extend: 
    example: 
**Notes**:  

#### Similar(ABC,DEF)
<div>
    <img src="cowork-pic/Similar.png"  width="20%">
</div>

    ee_check: Triangle(ABC)
              Triangle(DEF)
    multi: DEF,ABC
           BCA,EFD
           EFD,BCA
           CAB,FDE
           FDE,CAB
    extend: 
    example: 
**Notes**:  

#### MirrorCongruent(ABC,DEF)
<div>
    <img src="cowork-pic/MirrorCongruent.png"  width="20%">
</div>

    ee_check: Triangle(ABC)
              Triangle(DEF)
    multi: DEF,ABC
           BCA,FDE
           FDE,BCA
           CAB,EFD
           EFD,CAB
    extend: 
    example: 
**Notes**:  

#### MirrorSimilar(ABC,DEF)
<div>
    <img src="cowork-pic/MirrorSimilar.png"  width="20%">
</div>

    ee_check: Triangle(ABC)
              Triangle(DEF)
    multi: DEF,ABC
           BCA,FDE
           FDE,BCA
           CAB,EFD
           EFD,CAB
    extend: 
    example: 
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
    example: 1 Equal(AreaOfTriangle(ABC),10)
**Notes**:  

#### PerimeterOfTriangle(ABC)
<div>
    <img src="cowork-pic/PerimeterOfTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: BCA
           CAB
    sym: pt
    example: 1 Equal(PerimeterOfTriangle(ABC),10)
**Notes**:  

#### AreaOfQuadrilateral(ABCD)
<div>
    <img src="cowork-pic/AreaOfQuadrilateral.png"  width="14%">
</div>

    ee_check: Quadrilateral(ABCD)
    multi: BCDA
           CDAB
           DABC
    sym: aq
    example: 1 Equal(AreaOfQuadrilateral(ABCD),20)
**Notes**:  

#### PerimeterOfQuadrilateral(ABCD)
<div>
    <img src="cowork-pic/PerimeterOfQuadrilateral.png"  width="14%">
</div>

    ee_check: Quadrilateral(ABCD)
    multi: BCDA
           CDAB
           DABC
    sym: pq
    example: 1 Equal(PerimeterOfQuadrilateral(ABCD),20)
**Notes**:  

#### AltitudeOfTriangle(ABC)
<div>
    <img src="cowork-pic/AltitudeOfTriangle.png"  width="14%">
</div>

    ee_check: Triangle(ABC)
    multi: 
    sym: alt
    example: 1 Equal(AltitudeOfTriangle(ABC),5)
**Notes**:  

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
    example: 1 Equal(DistanceOfPointToLine(O,AB),3)
**Notes**:  

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
|根号|Sqrt(expr1)|√|
|正弦|Sin(expr)|@|
|余弦|Cos(expr)|#|
|正切|Tan(expr)|$|
|实数|R|1,2,3,...|
|自由变量|x|a,b,c,...|
|左括号| / |{|
|右括号| / |}|

### I、解题目标
#### Value

    example: 1 Value(LengthOfLine(AB))
             2 Value(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)))
             3 Value(x+y)

**Notes**:  
代数型解题目标，求某个表达式或属性的值。  
expr可以是表达式，也可以是实体属性，并且可以嵌套表示。  

#### Equal

    example: 1 Equal(LengthOfLine(AB),x+y)
             2 Equal(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)),Pow(x,2))
    
**Notes**:  
代数型解题目标，证明左右俩个部分相等。  
expr可以是表达式，也可以是实体属性，并且可以嵌套表示。  

#### Relation

    example: 1 Relation(Parallel(AB,CD))
             2 Relation(RightTriangle(ABC))    

**Notes**:  
逻辑型解题目标，求某个实体或属性。  
Relation表示任意实体、实体关系。  
