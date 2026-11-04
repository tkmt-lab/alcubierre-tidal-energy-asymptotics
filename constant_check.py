"""Exact rational arithmetic for the uniform envelopes in Section 5.3.
The analytic reduction is in the paper; these checks do not formalize it.
"""
from fractions import Fraction as F
import json
from pathlib import Path
checks={}
def check(name,left,right,strict=False):
    left,right=F(left),F(right)
    assert left<right if strict else left<=right, (name,left,right)
    checks[name]={"left":str(left),"right":str(right),"strict":strict,"passed":True}
check('beta_squared_below_0.21_squared',4*F(4,3)/128,F(21,100)**2,True)
check('inner_strip_in_wall',F(4,3)/128,F(1,2),True)
check('junction_monotonicity',F(3,64),(F(3,2)-F(1,128**3))/3,True)
check('junction_positive_at_one',F(3,64),F(1,2)-F(1,128**3),True)
check('disjoint_junction_intervals',1+F(2,128**3),F(3,2)-F(1,128**3)-F(3,64),True)
check('mass_remainder',192+F(14,64),200)
check('energy_remainder',1536+3744+3456+F(288+144+18,64),9000)
# (3-2t)/(1-t)^2 <=4 on [0,1/8]: numerator <=3 and denominator >=49/64.
check('normalization_taylor_coefficient',3*F(64,49),4)
check('normalization_remainder',2*200+4*8**2,700)
normal=3*700+F(32,9)*F(16,9)+F(32,9)*F(700,64)+9000*F(64,49)
check('normalized_energy_remainder',normal,14000,True)
check('smoothing_and_normalization',14000+F(5,4)*81*F(64,49)/64**2,15000)
check('eta_remainder',128*F(16,9)+60000,61000)
# sqrt bounds are checked by squaring positive quantities.
check('sqrt128_above_11',11**2,128,True)
check('4_over_sqrt3_below_7_over3',F(16,3),F(7,3)**2,True)
check('lower_remainder',F(16,9)*(F(16,99)+F(7,3)),5,True)
result={"status":"passed","kind":"exact rational arithmetic after analytic envelope reduction", "checks":checks,
        "constants":{"eta0":128,"Bminus":5,"Bplus":61000,"gamma_remainder":15000}}
Path('constant-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
