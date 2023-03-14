## 附录3 定理标注对照手册
#### line_addition(AB,BC)
<div>
    <img src="cowork-pic/line_addition.png"  width="20%">
</div>

    # branch 1
    premise: Collinear(ABC)
    conclusion: Equal(LengthOfLine(AC),Add(LengthOfLine(AB),LengthOfLine(BC)))
**Notes**:  

#### angle_addition(ABC,CBD)
<div>
    <img src="cowork-pic/angle_addition.png"  width="20%">
</div>

    # branch 1
    premise: Angle(ABC)&Angle(CBD)
    conclusion: Equal(MeasureOfAngle(ABD),Add(MeasureOfAngle(ABC),MeasureOfAngle(CBD)))
**Notes**:  

#### flat_angle(ABC)
<div>
    <img src="cowork-pic/flat_angle.png"  width="20%">
</div>

    # branch 1
    premise: Collinear(ABC)
    conclusion: Equal(MeasureOfAngle(ABC),180)

**Notes**:  

#### adjacent_complementary_angle(AOB,BOC)
<div>
    <img src="cowork-pic/adjacent_complementary_angle.png"  width="20%">
</div>

    # branch 1
    premise: Angle(AOB)&Angle(BOC)&Collinear(AOC)
    conclusion: Equal(Add(MeasureOfAngle(AOB),MeasureOfAngle(BOC)),180)
**Notes**:  

#### midpoint_judgment(M,AB)
<div>
    <img src="cowork-pic/midpoint_judgment.png"  width="20%">
</div>

    # branch 1
    premise: Collinear(AMB)&Equal(LengthOfLine(AM),LengthOfLine(MB))
    conclusion: Midpoint(M,AB)
**Notes**:  

#### triangle_area_formula_common(AD,ABC)
<div>
    <img src="cowork-pic/triangle_area_formula_common.png"  width="20%">
</div>

    # branch 1
    premise: IsAltitude(AD,ABC)
    conclusion: Equal(AreaOfTriangle(ABC),Mul(LengthOfLine(AD),LengthOfLine(BC),0.5))
**Notes**:  

#### triangle_area_formula_heron(ABC)
<div>
    <img src="cowork-pic/triangle_area_formula_heron.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)
    conclusion: Equal(AreaOfTriangle(ABC),Pow(Mul(Mul(Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(AC)),0.5),Sub(Mul(Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(AC)),0.5),LengthOfLine(AB)),Sub(Mul(Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(AC)),0.5),LengthOfLine(BC)),Sub(Mul(Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(AC)),0.5),LengthOfLine(CA))),0.5))
**Notes**:  

#### triangle_area_formula_sine(ABC)
<div>
    <img src="cowork-pic/triangle_area_formula_sine.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)
    conclusion: Equal(AreaOfTriangle(ABC),Mul(LengthOfLine(AB),LengthOfLine(AC),Sin(MeasureOfAngle(CAB)),1/2))
**Notes**:  

#### triangle_perimeter_formula(ABC)
<div>
    <img src="cowork-pic/triangle_perimeter_formula.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)
    conclusion: Equal(PerimeterOfTriangle(ABC),Add(LengthOfLine(AB),LengthOfLine(BC),LengthOfLine(CA)))
**Notes**:  

#### triangle_property_angle_sum(ABC)
<div>
    <img src="cowork-pic/triangle_property_angle_sum.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)
    conclusion: Equal(Add(MeasureOfAngle(ABC),MeasureOfAngle(BCA),MeasureOfAngle(CAB)),180)
**Notes**:  

#### triangle_property_equal_line_to_equal_angle(ABC)
<div>
    <img src="cowork-pic/triangle_property_equal_line_to_equal_angle.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Equal(LengthOfLine(AB),LengthOfLine(AC))
    conclusion: Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA))
**Notes**:  

#### triangle_property_equal_angle_to_equal_line(ABC)
<div>
    <img src="cowork-pic/triangle_property_equal_angle_to_equal_line.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA))
    conclusion: Equal(LengthOfLine(AB),LengthOfLine(AC))
**Notes**:  

#### sine_theorem(ABC)
<div>
    <img src="cowork-pic/sine_theorem.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)
    conclusion: Equal(Mul(LengthOfLine(AB),Sin(MeasureOfAngle(ABC))),Mul(LengthOfLine(AC),Sin(MeasureOfAngle(BCA))))
**Notes**:  

#### cosine_theorem(ABC)
<div>
    <img src="cowork-pic/cosine_theorem.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)
    conclusion: Equal(Add(Pow(LengthOfLine(BC),2),Mul(2,LengthOfLine(AB),LengthOfLine(AC),Cos(MeasureOfAngle(CAB)))),Add(Pow(LengthOfLine(AB),2),Pow(LengthOfLine(AC),2)))
**Notes**:  

#### parallel_judgment_alternate_interior_angle(AB,CD)
<div>
    <img src="cowork-pic/parallel_judgment_alternate_interior_angle.png"  width="20%">
</div>

    # branch 1
    premise: Angle(BAD)&Angle(CDA)&Equal(MeasureOfAngle(BAD),MeasureOfAngle(CDA))
    conclusion: Parallel(AB,CD)
**Notes**:  

#### parallel_judgment_Ipsilateral_internal_angle(AB,CD)
<div>
    <img src="cowork-pic/parallel_judgment_Ipsilateral_internal_angle.png"  width="20%">
</div>

    # branch 1
    premise: Angle(BAC)&Angle(ACD)&Equal(Add(MeasureOfAngle(BAC),MeasureOfAngle(ACD)),180)
    conclusion: Parallel(AB,CD)
**Notes**:  

#### parallel_judgment_par_par(AB,CD,EF)
<div>
    <img src="cowork-pic/parallel_judgment_par_par.png"  width="20%">
</div>

    # branch 1
    premise: Parallel(AB,CD)&Parallel(CD,EF)
    conclusion: Parallel(AB,EF)
**Notes**:  

#### parallel_judgment_per_per(AB,CD)
<div>
    <img src="cowork-pic/parallel_judgment_per_per.png"  width="40%">
</div>

    # branch 1
    premise: Perpendicular(BA,CA)&Perpendicular(AC,DC)
    conclusion: Parallel(AB,CD)
    # branch 2
    premise: Perpendicular(CD,AD)&Perpendicular(BA,DA)
    conclusion: Parallel(AB,CD)
**Notes**:  

#### parallel_property_collinear_extend(AB,CD,M)
<div>
    <img src="cowork-pic/parallel_property_collinear_extend.png"  width="60%">
</div>

    # branch 1
    premise: Collinear(AMB)&Parallel(AB,CD)
    conclusion: Parallel(AM,CD)
                Parallel(MB,CD)
    # branch 2
    premise: Collinear(MAB)&Parallel(AB,CD)
    conclusion: Parallel(MA,CD)
                Parallel(MB,CD)
    # branch 3
    premise: Collinear(ABM)&Parallel(AB,CD)
    conclusion: Parallel(AM,CD)
                Parallel(BM,CD)
**Notes**:  

#### parallel_property_alternate_interior_angle(AB,CD)
<div>
    <img src="cowork-pic/parallel_property_alternate_interior_angle.png"  width="20%">
</div>

    # branch 1
    premise: Parallel(AB,CD)&Line(AD)
    conclusion: Equal(MeasureOfAngle(BAD),MeasureOfAngle(CDA))
**Notes**:  

#### parallel_property_Ipsilateral_internal_angle(AB,CD)
<div>
    <img src="cowork-pic/parallel_property_Ipsilateral_internal_angle.png"  width="20%">
</div>

    # branch 1
    premise: Parallel(AB,CD)&Line(AC)
    conclusion: Equal(Add(MeasureOfAngle(BAC),MeasureOfAngle(ACD)),180)
**Notes**:  

#### parallel_property_corresponding_angle(AB,CD,E)
<div>
    <img src="cowork-pic/parallel_property_corresponding_angle.png"  width="40%">
</div>

    # branch 1
    premise: Parallel(AB,CD)&Collinear(EAC)
    conclusion: Equal(MeasureOfAngle(EAB),MeasureOfAngle(ACD))
    # branch 2
    premise: Parallel(AB,CD)&Collinear(ACE)
    conclusion: Equal(MeasureOfAngle(BAC),MeasureOfAngle(DCE))
**Notes**:  

#### parallel_property_extend_perpendicular(AB,CD)
<div>
    <img src="cowork-pic/parallel_property_extend_perpendicular.png"  width="30%">
</div>

    # branch 1
    premise: Parallel(AB,CD)&Perpendicular(AC,DC)
    conclusion: Perpendicular(BA,CA)
    # branch 2
    premise: Parallel(AB,CD)&Perpendicular(BA,CA)
    conclusion: Perpendicular(AC,DC)
**Notes**:  

#### intersect_property_vertical_angle(O,AB,CD)
<div>
    <img src="cowork-pic/intersect_property_vertical_angle.png"  width="20%">
</div>

    # branch 1
    premise: Intersect(O,AB,CD)
    conclusion: Equal(MeasureOfAngle(AOC),MeasureOfAngle(BOD))
**Notes**:  

#### bisector_judgment_angle_equal(BD,ABC)
<div>
    <img src="cowork-pic/bisector_judgment_angle_equal.png"  width="20%">
</div>

    # branch 1
    premise: Angle(ABD)&Angle(DBC)&Equal(MeasureOfAngle(ABD),MeasureOfAngle(DBC))
    conclusion: Bisector(BD,ABC)
**Notes**:  

#### bisector_property_line_ratio(BD,ABC)
<div>
    <img src="cowork-pic/bisector_property_line_ratio.png"  width="20%">
</div>

    # branch 1
    premise: Bisector(BD,ABC)&Collinear(CDA)
    conclusion: Equal(Mul(LengthOfLine(CD),LengthOfLine(BA)),Mul(LengthOfLine(DA),LengthOfLine(BC)))
**Notes**:  

#### median_judgment(AD,ABC)
<div>
    <img src="cowork-pic/median_judgment.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Midpoint(D,BC)&Line(AD)
    conclusion: Median(AD,ABC)
**Notes**:  

#### neutrality_judgment_parallel(DE,ABC)
<div>
    <img src="cowork-pic/neutrality_judgment_parallel.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Collinear(ADB)&Collinear(AEC)&Parallel(DE,BC)
    conclusion: Neutrality(DE,ABC)
**Notes**:  

#### neutrality_property_angle_equal(DE,ABC)
<div>
    <img src="cowork-pic/neutrality_property_angle_equal.png"  width="20%">
</div>

    # branch 1
    premise: Neutrality(DE,ABC)
    conclusion: Equal(MeasureOfAngle(ADE),MeasureOfAngle(ABC))
                Equal(MeasureOfAngle(DEA),MeasureOfAngle(BCA))
**Notes**:  

#### neutrality_property_line_ratio(DE,ABC)
<div>
    <img src="cowork-pic/neutrality_property_line_ratio.png"  width="20%">
</div>

    # branch 1
    premise: Neutrality(DE,ABC)
    conclusion: Equal(Mul(LengthOfLine(AD),LengthOfLine(EC)),Mul(LengthOfLine(DB),LengthOfLine(AE)))
**Notes**:  

#### neutrality_property_similar(DE,ABC)
<div>
    <img src="cowork-pic/neutrality_property_similar.png"  width="20%">
</div>

    # branch 1
    premise: Neutrality(DE,ABC)
    conclusion: Similar(ABC,ADE)
**Notes**:  

#### altitude_judgment(AD,ABC)
<div>
    <img src="cowork-pic/altitude_judgment.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Collinear(BDC)&Line(AD)&(Equal(MeasureOfAngle(BDA),90)|Equal(MeasureOfAngle(ADC),90))
    conclusion: IsAltitude(AD,ABC)
**Notes**:  

#### perpendicular_bisector_judgment(AB,CO)
<div>
    <img src="cowork-pic/perpendicular_bisector_judgment.png"  width="20%">
</div>

    # branch 1
    premise: Collinear(AOB)&(Perpendicular(AO,CO)|Equal(MeasureOfAngle(AOC),90)|Perpendicular(CO,BO)|Equal(MeasureOfAngle(COB),90))&(Midpoint(O,AB)|Equal(LengthOfLine(AO),LengthOfLine(OB)))
    conclusion: PerpendicularBisector(AB,CO)
**Notes**:  

#### perpendicular_bisector_property_distance_equal(AB,CO)
<div>
    <img src="cowork-pic/perpendicular_bisector_property_distance_equal.png"  width="20%">
</div>

    # branch 1
    premise: PerpendicularBisector(AB,CO)
    conclusion: Equal(LengthOfLine(CA),LengthOfLine(CB))
**Notes**:  

#### perpendicular_bisector_property_bisector(AB,CO)
<div>
    <img src="cowork-pic/perpendicular_bisector_property_bisector.png"  width="20%">
</div>

    # branch 1
    premise: PerpendicularBisector(AB,CO)&Angle(BCO)&Angle(OCA)
    conclusion: Bisector(CO,BCA)
**Notes**:  

#### perpendicular_judgment_angle(AO,CO)
<div>
    <img src="cowork-pic/perpendicular_judgment_angle.png"  width="20%">
</div>

    # branch 1
    premise: Angle(AOC)&Equal(MeasureOfAngle(AOC),90)
    conclusion: Perpendicular(AO,CO)
**Notes**:  

#### perpendicular_property_collinear_extend(AO,CO,B)
<div>
    <img src="cowork-pic/perpendicular_property_collinear_extend.png"  width="80%">
</div>

    # branch 1
    premise: Perpendicular(AO,CO)&Collinear(AOB)
    conclusion: Perpendicular(CO,BO)
    # branch 2
    premise: Perpendicular(AO,CO)&Collinear(BOC)
    conclusion: Perpendicular(BO,AO)
    # branch 3
    premise: Perpendicular(AO,CO)&(Collinear(ABO)|Collinear(BAO))
    conclusion: Perpendicular(BO,CO)
    # branch 4
    premise: Perpendicular(AO,CO)&(Collinear(OBC)|Collinear(OCB))
    conclusion: Perpendicular(AO,BO)
**Notes**:  

#### right_triangle_judgment_angle(ABC)
<div>
    <img src="cowork-pic/right_triangle_judgment_angle.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&(Perpendicular(AB,CB)|Equal(MeasureOfAngle(ABC),90))
    conclusion: RightTriangle(ABC)
**Notes**:  

#### right_triangle_judgment_pythagorean_inverse(ABC)
<div>
    <img src="cowork-pic/right_triangle_judgment_pythagorean_inverse.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Equal(Add(Pow(LengthOfLine(AB),2),Pow(LengthOfLine(BC),2)),Pow(LengthOfLine(AC),2))
    conclusion: RightTriangle(ABC)
**Notes**:  

#### right_triangle_property_pythagorean(ABC)
<div>
    <img src="cowork-pic/right_triangle_property_pythagorean.png"  width="20%">
</div>

    # branch 1
    premise: RightTriangle(ABC)
    conclusion: Equal(Add(Pow(LengthOfLine(AB),2),Pow(LengthOfLine(BC),2)),Pow(LengthOfLine(AC),2))
**Notes**:  

#### right_triangle_property_special_rt_30_60(ABC)
<div>
    <img src="cowork-pic/right_triangle_property_special_rt_30_60.png"  width="40%">
</div>

    # branch 1
    premise: RightTriangle(ABC)&(Equal(MeasureOfAngle(CAB),30)|Equal(MeasureOfAngle(BCA),60))
    conclusion: Equal(LengthOfLine(AB),Mul(LengthOfLine(BC),1.7321))
                Equal(LengthOfLine(AC),Mul(LengthOfLine(BC),2))
    # branch 2
    premise: RightTriangle(ABC)&(Equal(MeasureOfAngle(CAB),60)|Equal(MeasureOfAngle(BCA),30))
    conclusion: Equal(LengthOfLine(BC),Mul(LengthOfLine(AB),1.7321))
                Equal(LengthOfLine(AC),Mul(LengthOfLine(AB),2))
**Notes**:  

#### right_triangle_property_special_rt_45_45(ABC)
<div>
    <img src="cowork-pic/right_triangle_property_special_rt_45_45.png"  width="20%">
</div>

    # branch 1
    premise: RightTriangle(ABC)&(Equal(MeasureOfAngle(CAB),45)|Equal(MeasureOfAngle(BCA),45))
    conclusion: Equal(LengthOfLine(AB),LengthOfLine(BC))
                Equal(LengthOfLine(AC),Mul(LengthOfLine(AB),1.4142))
**Notes**:  

#### isosceles_triangle_judgment_angle_equal(ABC)
<div>
    <img src="cowork-pic/isosceles_triangle_judgment_angle_equal.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA))
    conclusion: IsoscelesTriangle(ABC)
**Notes**:  

#### isosceles_triangle_judgment_equilateral(ABC)
<div>
    <img src="cowork-pic/isosceles_triangle_judgment_equilateral.png"  width="20%">
</div>

    # branch 1
    premise: EquilateralTriangle(ABC)
    conclusion: IsoscelesTriangle(ABC)
**Notes**:  

#### isosceles_triangle_judgment_line_equal(ABC)
<div>
    <img src="cowork-pic/isosceles_triangle_judgment_line_equal.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Equal(LengthOfLine(AB),LengthOfLine(AC))
    conclusion: IsoscelesTriangle(ABC)
**Notes**:  

#### isosceles_triangle_property_angle_equal(ABC)
<div>
    <img src="cowork-pic/isosceles_triangle_property_angle_equal.png"  width="20%">
</div>

    # branch 1
    premise: IsoscelesTriangle(ABC)
    conclusion: Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA))
**Notes**:  

#### isosceles_triangle_property_line_coincidence(ABC)
<div>
    <img src="cowork-pic/isosceles_triangle_property_line_coincidence.png"  width="20%">
</div>

    # branch 1
    premise: IsoscelesTriangle(ABC)&IsAltitude(AM,ABC)
    conclusion: Median(AM,ABC)
                Bisector(AM,CAB)
    # branch 2
    premise: IsoscelesTriangle(ABC)&Median(AM,ABC)
    conclusion: IsAltitude(AM,ABC)
                Bisector(AM,CAB)
    # branch 3
    premise: IsoscelesTriangle(ABC)&Collinear(BMC)&Bisector(AM,CAB)
    conclusion: IsAltitude(AM,ABC)
                Median(AM,ABC)
**Notes**:  

#### equilateral_triangle_judgment_angle_equal(ABC)
<div>
    <img src="cowork-pic/equilateral_triangle_judgment_angle_equal.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(BCA))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(CAB))
    conclusion: EquilateralTriangle(ABC)
**Notes**:  

#### equilateral_triangle_judgment_isos_and_angle(ABC)
<div>
    <img src="cowork-pic/equilateral_triangle_judgment_isos_and_angle.png"  width="20%">
</div>

    # branch 1
    premise: IsoscelesTriangle(ABC)&(Equal(MeasureOfAngle(ABC),60)|Equal(MeasureOfAngle(BCA),60)|Equal(MeasureOfAngle(CAB),60))
    conclusion: EquilateralTriangle(ABC)
**Notes**:  

#### equilateral_triangle_judgment_line_equal(ABC)
<div>
    <img src="cowork-pic/equilateral_triangle_judgment_line_equal.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Equal(LengthOfLine(AB),LengthOfLine(BC))&Equal(LengthOfLine(BC),LengthOfLine(AC))
    conclusion: EquilateralTriangle(ABC)
**Notes**:  

#### equilateral_triangle_property_angle(ABC)
<div>
    <img src="cowork-pic/equilateral_triangle_property_angle.png"  width="20%">
</div>

    # branch 1
    premise: EquilateralTriangle(ABC)
    conclusion: Equal(MeasureOfAngle(CAB),60)
**Notes**:  

#### equilateral_triangle_property_line_equal(ABC)
<div>
    <img src="cowork-pic/equilateral_triangle_property_line_equal.png"  width="20%">
</div>

    # branch 1
    premise: EquilateralTriangle(ABC)
    conclusion: Equal(LengthOfLine(AB),LengthOfLine(AC))
**Notes**:  

#### congruent_judgment_aas(ABC,DEF)
<div>
    <img src="cowork-pic/congruent_judgment_aas.png"  width="40%">
</div>

    # branch 1
    premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(EFD))&Equal(LengthOfLine(CA),LengthOfLine(FD))
    conclusion: Congruent(ABC,DEF)
    # branch 2
    premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(DEF))&Equal(LengthOfLine(CA),LengthOfLine(DE))
    conclusion: MirrorCongruent(ABC,DEF)
**Notes**:  

#### congruent_judgment_asa(ABC,DEF)
<div>
    <img src="cowork-pic/congruent_judgment_asa.png"  width="40%">
</div>

    # branch 1
    premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF))&Equal(LengthOfLine(BC),LengthOfLine(EF))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(EFD))
    conclusion: Congruent(ABC,DEF)
    # branch 2
    premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD))&Equal(LengthOfLine(BC),LengthOfLine(EF))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(DEF))
    conclusion: MirrorCongruent(ABC,DEF)
**Notes**:  

#### congruent_judgment_hl(ABC,DEF)
<div>
    <img src="cowork-pic/congruent_judgment_hl.png"  width="40%">
</div>

    # branch 1
    premise: RightTriangle(ABC)&RightTriangle(DEF)&Equal(LengthOfLine(AC),LengthOfLine(DF))&(Equal(LengthOfLine(AB),LengthOfLine(DE))|Equal(LengthOfLine(BC),LengthOfLine(EF)))
    conclusion: Congruent(ABC,DEF)
    # branch 2
    premise: RightTriangle(BCA)&RightTriangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(DF))&(Equal(LengthOfLine(AC),LengthOfLine(DE))|Equal(LengthOfLine(BC),LengthOfLine(EF)))
    conclusion: MirrorCongruent(ABC,DEF)
**Notes**:  

#### congruent_judgment_sas(ABC,DEF)
<div>
    <img src="cowork-pic/congruent_judgment_sas.png"  width="40%">
</div>

    # branch 1
    premise: Triangle(ABC)&Triangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(DE))&Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))&Equal(LengthOfLine(AC),LengthOfLine(DF))
    conclusion: Congruent(ABC,DEF)
    # branch 2
    premise: Triangle(ABC)&Triangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(DF))&Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))&Equal(LengthOfLine(AC),LengthOfLine(DE))
    conclusion: MirrorCongruent(ABC,DEF)
**Notes**:  

#### congruent_judgment_sss(ABC,DEF)
<div>
    <img src="cowork-pic/congruent_judgment_sss.png"  width="40%">
</div>

    # branch 1
    premise: Triangle(ABC)&Triangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(DE))&Equal(LengthOfLine(BC),LengthOfLine(EF))&Equal(LengthOfLine(CA),LengthOfLine(FD))
    conclusion: Congruent(ABC,DEF)
    # branch 2
    premise: Triangle(ABC)&Triangle(DEF)&Equal(LengthOfLine(AB),LengthOfLine(FD))&Equal(LengthOfLine(BC),LengthOfLine(EF))&Equal(LengthOfLine(CA),LengthOfLine(DE))
    conclusion: MirrorCongruent(ABC,DEF)
**Notes**:  

#### congruent_property_angle_equal(ABC,DEF)
<div>
    <img src="cowork-pic/congruent_property_angle_equal.png"  width="40%">
</div>

    # branch 1
    premise: Congruent(ABC,DEF)
    conclusion: Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))
    # branch 2
    premise: MirrorCongruent(ABC,DEF)
    conclusion: Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))
**Notes**:  

#### congruent_property_area_equal(ABC,DEF)
<div>
    <img src="cowork-pic/congruent_property_area_equal.png"  width="40%">
</div>

    # branch 1
    premise: Congruent(ABC,DEF)
    conclusion: Equal(AreaOfTriangle(ABC),AreaOfTriangle(DEF))
    # branch 2
    premise: MirrorCongruent(ABC,DEF)
    conclusion: Equal(AreaOfTriangle(ABC),AreaOfTriangle(DEF))
**Notes**:  

#### congruent_property_line_equal(ABC,DEF)
<div>
    <img src="cowork-pic/congruent_property_line_equal.png"  width="40%">
</div>

    # branch 1
    premise: Congruent(ABC,DEF)
    conclusion: Equal(LengthOfLine(AB),LengthOfLine(DE))
    # branch 2
    premise: MirrorCongruent(ABC,DEF)
    conclusion: Equal(LengthOfLine(AB),LengthOfLine(DF))
**Notes**:  

#### congruent_property_perimeter_equal(ABC,DEF)
<div>
    <img src="cowork-pic/congruent_property_perimeter_equal.png"  width="40%">
</div>

    # branch 1
    premise: Congruent(ABC,DEF)
    conclusion: Equal(PerimeterOfTriangle(ABC),PerimeterOfTriangle(DEF))
    # branch 2
    premise: MirrorCongruent(ABC,DEF)
    conclusion: Equal(PerimeterOfTriangle(ABC),PerimeterOfTriangle(DEF))
**Notes**:  

#### similar_judgment_aa(ABC,DEF)
<div>
    <img src="cowork-pic/similar_judgment_aa.png"  width="40%">
</div>

    # branch 1
    premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(DEF))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(EFD))
    conclusion: Similar(ABC,DEF)
    # branch 2
    premise: Triangle(ABC)&Triangle(DEF)&Equal(MeasureOfAngle(ABC),MeasureOfAngle(EFD))&Equal(MeasureOfAngle(BCA),MeasureOfAngle(DEF))
    conclusion: MirrorSimilar(ABC,DEF)
**Notes**:  

#### similar_judgment_sas(ABC,DEF)
<div>
    <img src="cowork-pic/similar_judgment_sas.png"  width="40%">
</div>

    # branch 1
    premise: Triangle(ABC)&Triangle(DEF)&Equal(Mul(LengthOfLine(AB),LengthOfLine(DF)),Mul(LengthOfLine(DE),LengthOfLine(AC)))&Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))
    conclusion: Similar(ABC,DEF)
    # branch 2
    premise: Triangle(ABC)&Triangle(DEF)&Equal(Mul(LengthOfLine(AB),LengthOfLine(DE)),Mul(LengthOfLine(DF),LengthOfLine(AC)))&Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))
    conclusion: MirrorSimilar(ABC,DEF)
**Notes**:  

#### similar_judgment_sss(ABC,DEF)
<div>
    <img src="cowork-pic/similar_judgment_sss.png"  width="40%">
</div>

    # branch 1
    premise: Triangle(ABC)&Triangle(DEF)&Equal(Mul(LengthOfLine(AB),LengthOfLine(EF)),Mul(LengthOfLine(DE),LengthOfLine(BC)))&Equal(Mul(LengthOfLine(AB),LengthOfLine(DF)),Mul(LengthOfLine(DE),LengthOfLine(CA)))
    conclusion: Similar(ABC,DEF)
    # branch 2
    premise: Triangle(ABC)&Triangle(DEF)&Equal(Mul(LengthOfLine(AB),LengthOfLine(EF)),Mul(LengthOfLine(FD),LengthOfLine(BC)))&Equal(Mul(LengthOfLine(AB),LengthOfLine(DE)),Mul(LengthOfLine(FD),LengthOfLine(CA)))
    conclusion: MirrorSimilar(ABC,DEF)
**Notes**:  

#### similar_property_angle_equal(ABC,DEF)
<div>
    <img src="cowork-pic/similar_property_angle_equal.png"  width="40%">
</div>

    # branch 1
    premise: Similar(ABC,DEF)
    conclusion: Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))
    # branch 2
    premise: MirrorSimilar(ABC,DEF)
    conclusion: Equal(MeasureOfAngle(CAB),MeasureOfAngle(FDE))
**Notes**:  

#### similar_property_area_square_ratio(ABC,DEF)
<div>
    <img src="cowork-pic/similar_property_area_square_ratio.png"  width="40%">
</div>

    # branch 1
    premise: Similar(ABC,DEF)
    conclusion: Equal(Mul(LengthOfLine(AB),LengthOfLine(AB),AreaOfTriangle(DEF)),Mul(LengthOfLine(DE),LengthOfLine(DE),AreaOfTriangle(ABC)))
    # branch 2
    premise: MirrorSimilar(ABC,DEF)
    conclusion: Equal(Mul(LengthOfLine(AB),LengthOfLine(AB),AreaOfTriangle(DEF)),Mul(LengthOfLine(FD),LengthOfLine(FD),AreaOfTriangle(ABC)))
**Notes**:  

#### similar_property_line_ratio(ABC,DEF)
<div>
    <img src="cowork-pic/similar_property_line_ratio.png"  width="40%">
</div>

    # branch 1
    premise: Similar(ABC,DEF)
    conclusion: Equal(Mul(LengthOfLine(AB),LengthOfLine(DF)),Mul(LengthOfLine(DE),LengthOfLine(AC)))
    # branch 2
    premise: MirrorSimilar(ABC,DEF)
    conclusion: Equal(Mul(LengthOfLine(AB),LengthOfLine(DE)),Mul(LengthOfLine(DF),LengthOfLine(AC)))
**Notes**:  

#### similar_property_perimeter_ratio(ABC,DEF)
<div>
    <img src="cowork-pic/similar_property_perimeter_ratio.png"  width="40%">
</div>

    # branch 1
    premise: Similar(ABC,DEF)
    conclusion: Equal(Mul(LengthOfLine(AB),PerimeterOfTriangle(DEF)),Mul(LengthOfLine(DE),PerimeterOfTriangle(ABC)))
    # branch 2
    premise: MirrorSimilar(ABC,DEF)
    conclusion: Equal(Mul(LengthOfLine(AB),PerimeterOfTriangle(DEF)),Mul(LengthOfLine(FD),PerimeterOfTriangle(ABC)))
**Notes**:  

#### circumcenter_judgment(O,ABC,D,E)
<div>
    <img src="cowork-pic/circumcenter_judgment.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Collinear(ADB)&Collinear(CEA)&(PerpendicularBisector(AD,OD)|PerpendicularBisector(OD,BD))&(PerpendicularBisector(CE,OE)|PerpendicularBisector(OE,AE))
    conclusion: Circumcenter(O,ABC)
**Notes**:  

#### circumcenter_property_intersect(O,ABC,D)
<div>
    <img src="cowork-pic/circumcenter_property_intersect.png"  width="20%">
</div>

    # branch 1
    premise: Circumcenter(O,ABC)&Collinear(BDC)&(Perpendicular(BD,OD)|Perpendicular(OD,CD))
    conclusion: PerpendicularBisector(BC,OD)
    # branch 2
    premise: Circumcenter(O,ABC)&Midpoint(D,BC)
    conclusion: PerpendicularBisector(BC,OD)
**Notes**:  

#### circumcenter_property_line_equal(O,ABC)
<div>
    <img src="cowork-pic/circumcenter_property_line_equal.png"  width="20%">
</div>

    # branch 1
    premise: Circumcenter(O,ABC)
    conclusion: Equal(LengthOfLine(OB),LengthOfLine(OC))
**Notes**:  

#### incenter_judgment(O,ABC)
<div>
    <img src="cowork-pic/incenter_judgment.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Bisector(BO,ABC)&Bisector(CO,BCA)
    conclusion: Incenter(O,ABC)
**Notes**:  

#### incenter_property_intersect(O,ABC)
<div>
    <img src="cowork-pic/incenter_property_intersect.png"  width="20%">
</div>

    # branch 1
    premise: Incenter(O,ABC)
    conclusion: Bisector(AO,CAB)
**Notes**:  

#### incenter_property_line_equal(O,ABC,D,E)
<div>
    <img src="cowork-pic/incenter_property_line_equal.png"  width="20%">
</div>

    # branch 1
    premise: Incenter(O,ABC)&Collinear(ADB)&Collinear(AEC)&(Perpendicular(AD,OD)|Perpendicular(OD,BD))&(Perpendicular(CE,OE)|Perpendicular(OE,AE))
    conclusion: Equal(LengthOfLine(OD),LengthOfLine(OE))
**Notes**:  

#### centroid_judgment(O,ABC,M,N)
<div>
    <img src="cowork-pic/centroid_judgment.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&Median(CM,CAB)&Median(BN,BCA)&Collinear(COM)&Collinear(BON)
    conclusion: Centroid(O,ABC)
**Notes**:  

#### centroid_property_intersect(O,ABC,M)
<div>
    <img src="cowork-pic/centroid_property_intersect.png"  width="20%">
</div>

    # branch 1
    premise: Centroid(O,ABC)&Collinear(AOM)&Collinear(BMC)
    conclusion: Median(AM,ABC)
**Notes**:  

#### centroid_property_line_equal(O,ABC,M)
<div>
    <img src="cowork-pic/centroid_property_line_equal.png"  width="20%">
</div>

    # branch 1
    premise: Centroid(O,ABC)&Collinear(AOM)&Collinear(BMC)
    conclusion: Equal(LengthOfLine(OA),Mul(LengthOfLine(OM),2))
**Notes**:  

#### orthocenter_judgment(O,ABC,D,E)
<div>
    <img src="cowork-pic/orthocenter_judgment.png"  width="20%">
</div>

    # branch 1
    premise: Triangle(ABC)&IsAltitude(CD,CAB)&IsAltitude(BE,BCA)&Collinear(COD)&Collinear(BOE)
    conclusion: Orthocenter(O,ABC)
**Notes**:  

#### orthocenter_property_intersect(O,ABC,D)
<div>
    <img src="cowork-pic/orthocenter_property_intersect.png"  width="20%">
</div>

    # branch 1
    premise: Orthocenter(O,ABC)&Collinear(AOD)&Collinear(BDC)
    conclusion: IsAltitude(AD,ABC)
**Notes**:  

#### orthocenter_property_angle(O,ABC)
<div>
    <img src="cowork-pic/orthocenter_property_angle.png"  width="20%">
</div>

    # branch 1
    premise: Orthocenter(O,ABC)&Angle(COB)
    conclusion: Equal(MeasureOfAngle(COB),Add(MeasureOfAngle(ABC),MeasureOfAngle(BCA)))
**Notes**:  

