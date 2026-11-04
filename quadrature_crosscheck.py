"""Different implementation: piecewise quadrature, without polynomial primitives."""
import json
from fractions import Fraction
from pathlib import Path
import mpmath as mp
mp.mp.dps=120
def val(s):
    f=Fraction(s)
    return mp.mpf(f.numerator)/f.denominator
data=json.loads(Path('rational-intervals.json').read_text())['rows']
out=[]
for row in data:
    R=val(row['R']); eta=val(row['eta']); C=val(row['C'])
    delta=eta**-3; gamma=eta-64
    a0=1+delta; b0=R-delta
    alpha=mp.findroot(lambda t:(t-a0)*t*t-delta,
                      (val(row['alpha_lo']),val(row['alpha_hi'])))
    beta=mp.findroot(lambda t:(b0-t)*t*t-C/gamma,
                     (val(row['beta_lo']),val(row['beta_hi'])))
    assert val(row['alpha_lo'])<=alpha<=val(row['alpha_hi'])
    assert val(row['beta_lo'])<=beta<=val(row['beta_hi'])
    branches=[(a0,alpha,lambda r:C/delta*(r-a0)),
              (alpha,beta,lambda r:C/r**2),
              (beta,b0,lambda r:gamma*(b0-r))]
    I=sum(mp.quad(fun,[lo,hi]) for lo,hi,fun in branches)
    J=sum(mp.quad(lambda r:r*r*fun(r)**2,[lo,hi]) for lo,hi,fun in branches)
    assert val(row['I_lo'])<=I<=val(row['I_hi'])
    assert val(row['Jq_lo'])<=J<=val(row['Jq_hi'])
    out.append({'R':row['R'],'eta':row['eta'],'I':mp.nstr(I,70),
                'Jq':mp.nstr(J,70),'inside_rational_enclosures':True})
result={'method':'mpmath 120 decimal digits; root solve and segmented quadrature; corroborative only',
        'mpmath_version':mp.__version__,'cases':out,'status':'all passed'}
Path('quadrature-result.json').write_text(json.dumps(result,indent=2)+'\n')
print('All 18 independently integrated I and Jq values lie inside the exact rational enclosures.')
