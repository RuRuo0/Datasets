# GFS-Basic

GFS-Basic is a geometry formal system designed based on the
[Geometry Formalization Theory](https://arxiv.org/abs/2310.18021), suitable for the solver
[FormalGeo](https://github.com/FormalGeo/FormalGeo) version 0.0.1. FormalGeo-0.0.1 contains 25 built-in predicates.
On this basis, GFS-Basic has detailed summaries of common nouns and theorems in the field of plane geometry, and has
newly defined 63 predicates and 196 theorems.

## Preset Predicates

3 construction predicates: Shape, Collinear, Cocircular; 6 basic entity predicates: Point, Line, Arc, Angle, Polygon,
Circle; 2 algebraic relation predicates: Equal, Equation; 1 attribute predicate: Free; 10 operation predicates: Add,
Sub, Mul, Div, Pow, Mod, Sqrt, Sin, Cos, Tan; 3 problem target predicates: Value, Equal, Relation.

### Construction Predicates

#### Shape(*)

Shape is the most basic construction predicate. It uses several edges or arcs to declare a closed geometric figure,
which can be an angle or a shape formed by edges and arcs. For closed geometric figures, list the edges of the figure in
a counterclockwise direction. For non-closed geometric figures, first connect the gaps to transform them into closed
geometric figures.

<div>
    <img src="pic/Shape.png" alt="Shape" width="60%">
</div>

**1.Declare a point**  
As shown in Figure 1, P is the center of the circle O. We can declare a point like this：

    Shape(P)

**2.Declare a point**  
As shown in Figure 2, AB are the two points of the line segment. We can declare the line segment like this:

    Shape(AB)

When declaring a line segment using Shape, the segment is assumed to be undirected by default, so declaring it this way
is also valid:

    Shape(BA)

**3.Declare a angle**  
As shown in Figure 3, angle B is formed by two line segments. It is important to note that when declaring an angle, the
line segments are directed, and the order in which the two lines appear follows the counterclockwise direction,
connecting head to tail. Therefore, angle B can be represented as:

    Shape(AB,BC)

**4.Declare a shape**  
If we declare shapes one edge or one angle at a time, it can be quite cumbersome. Instead, we can directly declare a
shape composed of several line segments and arcs. In the construction stage, the reasoner will automatically expand the
angles, lines, and arcs in the shape.

For the quadrilateral in Figure 3, we can declare it like this:

    Shape(AB,BC,CD,DA)
    Shape(BC,CD,DA,AB)
    Shape(CD,DA,AB,BC)
    Shape(DA,AB,BC,CD)

A quadrilateral can be represented in the four ways mentioned above, and we can choose one of them. For more complex
shapes, like the one in Figure 4, it can be declared as:

    Shape(OAB,BE,EA)
    Shape(OBC,CE,EB)
    Shape(EC,OCD,DP,PE)
    Shape(AE,EP,PD,ODA)

It should be noted that although EP and PD are collinear, when declaring a closed figure, we cannot directly declare ED;
we need to declare all the smallest edges. Closed figures can be composed of lines and arcs. Lines have two directions,
but arcs only have one. When declaring lines, they should be arranged in a counterclockwise direction, with the points
connecting end to end; when declaring arcs, it's important to note that there is only one way to represent them. When an
arc appears on its own, there is no need to declare it using Shape, as the appearance of an arc is always accompanied by
the Cocircular predicate. All arcs will be automatically extended by the Cocircular predicate.

#### Collinear(*)

Collinear is used to declare that three or more points are collinear. Since two points are always collinear, there is no
need to declare collinearity for just two points.

<div>
    <img src="pic/Collinear.png" alt="Collinear" width="45%">
</div>

Declaring collinearity is extremely simple; just list all the points on a line in order. The collinearity in Figure 1
can be declared as:

    Collinear(AMB)

Collinearity does not have a direction, so declaring it from the other direction is also valid:

    Collinear(BMA)

The collinearity in Figure 2 can be declared as:

    Collinear(BCDEF)

The collinearity in Figure 3 can be declared as:

    Collinear(ADB)
    Collinear(AEC)

Collinearity will automatically expand in the reasoner to include all lines and flat angles. For instance,
Collinear(AMB) will expand to include Line(AM), Line(MB), Line(AM), Angle(AMB), and Angle(BMA).

#### Cocircular(O,*)

Cocircular is used to declare several points that are concyclic. Like Collinear, it involves listing several points in
order. However, it differs from Collinear in two ways: first, even if only one point is on the circle, it needs to be
declared, and second, the declaration of concyclic points should follow a counterclockwise direction, and it can start
from any point.

<div>
    <img src="pic/Cocircular.png" alt="Cocircular" width="60%">
</div>

In Figure 1, the points that are concyclic can be declared as:

    Cocircular(O,ABCD)
    Cocircular(O,BCDA)
    Cocircular(O,CDAB)
    Cocircular(O,DABC)

The concyclic declaration in Figure 1 can have the above four forms, and any one of them can be chosen. Figures 2 to 4
show several special cases of concyclic declarations. In Figure 2, where there is only one point on the circle, it also
needs to be declared:

    Cocircular(O,A)

In Figure 3, where there are no points on the circle, it also needs to be declared:

    Cocircular(O)

In Figure 4, where two circles have a common point, they need to be declared separately:

    Cocircular(O,AB)
    Cocircular(P,BA)

After declaring cocircular, all arcs and circles will be automatically expanded.

### Basic Entity Predicates

Basic entities are derived from basic constructions and do not change after the construction phase is complete. We do
not need to declare basic entities; the following information is provided to help us understand the internal logic of
the formal system. Basic construction predicates declare the structural information of a shape, which is the relative
positional information of points. Basic entities are essentially the 'unzipped' version of basic constructions, making
them more convenient to use during the reasoning process.

#### Point(A)

It's about points, straightforward and simple.

<div>
    <img src="pic/Point.png" alt="Point" width="45%">
</div>


The declaration of points in Figures 1-3:

    Point(A)
    Point(A),Point(B),Point(C)
    Point(A),Point(C),Point(O)

#### Line(AB)

Line declares an undirected line segment.

<div>
    <img src="pic/Line.png" alt="Line" width="45%">
</div>

Since it is undirected, the line segment in Figure 1 can be declared in two ways; either one can be chosen:

    Line(AB)
    Line(BA)

The declaration of line in Figures 2 and 3:

    Line(AB),Line(CD)  
    Line(AO),Line(BO) 

#### Arc(OAB)

Arc declares a segment of an arc, consisting of three points. The first point is the center of the circle to which the
arc belongs, and the remaining two points form the arc. They should be listed in counterclockwise order.

<div>
    <img src="pic/Arc.png" alt="Arc" width="45%">
</div>


The declaration of arcs in Figures 1-3:

    Arc(OAB)
    Arc(OAC),Arc(OCA)
    Arc(OAB),Arc(OBC),Arc(OCD),Arc(ODA)

#### Angle(ABC)

An angle is formed by three points. When declaring an angle, the points should be ordered according to the
counterclockwise principle.

<div>
    <img src="pic/Angle.png" alt="Angle" width="45%">
</div>


The declaration of angles in Figures 1-3:

    Angle(AOB)
    Angle(ABC),Angle(BCA),Angle(CAB)
    Angle(AOC),Angle(COB),Angle(BOD),Angle(DOA)

#### Polygon(*)

A polygon is formed by several straight lines, and all points should be listed in counterclockwise order. A polygon with
n sides has n different representations.

<div>
    <img src="pic/Polygon.png" alt="Polygon" width="45%">
</div>

    Polygon(ABC),Polygon(BCA),Polygon(CAB)
    Polygon(ABCD),Polygon(BCDA),Polygon(CDAB),Polygon(DABC)
    Polygon(ABCDE),Polygon(BCDEA),Polygon(CDEAB),Polygon(DEABC),Polygon(EABCD)

#### Circle(O)

Circle is used to declare a circle, and it's important to distinguish between the circle and its center.

<div>
    <img src="pic/Circle.png" alt="Circle" width="45%">
</div>


The declaration of circles in Figures 1-3:

    Cirlce(O)
    Cirlce(B),Cirlce(A)
    Cirlce(O)

### Algebraic Relation Predicates

Algebraic relations are expressed as algebraic expressions, denoted as "expr." An "expr" is a formula composed of
symbols, operators, and nested attributes. Any expression that conforms to the sympy syntax can be correctly parsed.

#### Equal(expr1,expr2)

Equal accepts two "expr" values, representing an algebraic equivalence relationship.

    Equal(a,5)  
    Equal(MeasureOfAngle(ABC),30)  
    Equal(Add(LengthOfLine(AB),a+5,x),y^2)

#### Equation(expr)

Equation accepts one "expr" value, representing an equation.

    Equation(a-5)  
    Equation(Sub(MeasureOfAngle(ABC),30))  
    Equation(Sub(Add(LengthOfLine(AB),a+5,x),y^2))

### Attribution Predicates

#### Free(y)

Declare a free symbol, which can represent an unknown variable or refer to a geometric property.

### Operation Predicates

|        名称         |         格式         |   表达式符号   | 优先级 |
|:-----------------:|:------------------:|:---------:|:---:|
|        Add        | Add(expr1,expr2,…) |     +     |  1  |
|        Sub        |  Sub(expr1,expr2)  |     -     |  1  |
|        Mul        | Mul(expr1,expr2,…) |     *     |  2  |
|        Div        |  Div(expr1,expr2)  |     /     |  2  |
|        Pow        |  Pow(expr1,expr2)  |    **     |  3  |
|        Mod        |  Mod(expr1,expr2)  |    mod    |  3  |
|       Sqrt        |    Sqrt(expr1)     |   sqrt    |  4  |
|        Sin        |     Sin(expr)      |    sin    |  4  |
|        Cos        |     Cos(expr)      |    cos    |  4  |
|        Tan        |     Tan(expr)      |    tan    |  4  |
|    Real Number    |         R          | 1,2,3,... |  /  |
|  Free Variables   |         f          | a,b,c,... |  /  |
| Left parenthesis  |         /          |     (     |  5  |
| Right parenthesis |         /          |     )     |  0  |  

### Problem Target Predicates

#### Value(expr)

"expr" can be an expression or a geometric entity property, and it can be nested. Algebraic problem-solving goals
involve finding the value of an expression or property.

    Value(LengthOfLine(AB))
    Value(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)))
    Value(x+y)

#### Equal(expr1,expr2)

"expr" can indeed be an expression or a geometric entity property, and it can be nested. Algebraic problem-solving goals
can involve proving the equality of two expressions or properties on the left and right sides of an equation.

    Equal(LengthOfLine(AB),x+y)
    Equal(Add(MeasureOfAngle(ABC),MeasureOfAngle(DEF)),Pow(x,2))

#### Relation(*)

In logical problem-solving goals, the aim is to find a specific entity or property. "Relation" represents any entity or
entity relationship.

    Relation(Parallel(AB,CD))
    Relation(RightTriangle(ABC))  

