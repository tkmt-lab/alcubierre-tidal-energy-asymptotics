"""Reproduce all 18 exact enclosures and the LaTeX table using only Python standard library."""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

BITS=256
def bisect_increasing(fun,lo,hi):
    assert fun(lo)<=0<=fun(hi)
    for _ in range(BITS):
        mid=(lo+hi)/2
        if fun(mid)<=0: lo=mid
        else: hi=mid
    assert fun(lo)<=0<=fun(hi)
    return lo,hi

def sqrt_upper(x):
    scale=1<<BITS
    m=isqrt(x.numerator*scale*scale//x.denominator)
    lo=F(m,scale); hi=F(m+1,scale)
    assert lo*lo<=x<hi*hi
    return hi

def decimal_out(x,upper=False,digits=12):
    with localcontext() as ctx:
        ctx.prec=100
        ctx.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        value=Decimal(x.numerator)/Decimal(x.denominator)
        return str(value.quantize(Decimal(1).scaleb(-digits)))

rows=[]; table=[]
for R in (F(3,2),F(2),F(3)):
    C=R/(R-1); a=C/(R*R); K=R*R*a**3/3
    for eta_i in (128,512,2048,8192,32768,131072):
        eta=F(eta_i); gamma=eta-64; delta=eta**-3; eps=eta**-4
        a0=1+delta; b0=R-delta
        al,ah=bisect_increasing(lambda r:(r-a0)*r*r-delta,a0,1+2*delta)
        bl,bh=bisect_increasing(lambda r:C/gamma-(b0-r)*r*r,b0-C/gamma,b0)
        assert ah<bl and bl>2*b0/3
        def inner_I(r): return C/(2*delta)*(r-a0)**2
        def middle_I(left,right): return C*(1/left-1/right)
        def outer_I(r): return gamma/2*(b0-r)**2
        def inner_J(r):
            S=r-a0
            return (C/delta)**2*(a0*a0*S**3/3+a0*S**4/2+S**5/5)
        def middle_J(left,right): return C*C*(1/left-1/right)
        def outer_J(r):
            T=b0-r
            return gamma**2*(b0*b0*T**3/3-b0*T**4/2+T**5/5)
        Ilo=inner_I(al)+middle_I(ah,bl)+outer_I(bh)
        Ihi=inner_I(ah)+middle_I(al,bh)+outer_I(bl)
        Jlo=inner_J(al)+middle_J(ah,bl)+outer_J(bh)
        Jhi=inner_J(ah)+middle_J(al,bh)+outer_J(bl)
        assert 1-8/gamma<=Ilo<=Ihi<=1
        # ||q*k-q||_1 <= TV(q)*eps*5/16 and ||q*k+q||_infinity <=2C.
        smooth_error=F(5,4)*R*R*C*C*eps
        family_lo=(Jlo-smooth_error)/(Ihi*Ihi)
        family_hi=(Jhi+smooth_error)/(Ilo*Ilo)
        scaled_family_lo=eta*(family_lo-C)
        scaled_family_hi=eta*(family_hi-C)
        sqrt_hi=sqrt_upper(a/eta)
        global_lo=(R-a/eta)**2*a**3*(1-2*sqrt_hi)/3
        global_hi=scaled_family_hi
        assert 0<global_lo<K and global_lo<=global_hi
        assert family_lo<=family_hi and scaled_family_hi-scaled_family_lo<F(1,10**4)
        # Rational checks on constants used by the analytic admissibility proof.
        assert C*C/(2*gamma)+3*C*delta<=8/gamma
        A=C/(1-8/gamma)
        assert A<4 and 3*A*A+A+F(3,2)*A*A<eta
        assert gamma/(1-8/gamma)+A+F(3,2)*A*A<eta
        exact={"R":R,"eta":eta,"C":C,"a":a,"K":K,
               "alpha_lo":al,"alpha_hi":ah,"beta_lo":bl,"beta_hi":bh,
               "I_lo":Ilo,"I_hi":Ihi,"Jq_lo":Jlo,"Jq_hi":Jhi,
               "smoothing_error":smooth_error,"family_J_lo":family_lo,"family_J_hi":family_hi,
               "scaled_family_lo":scaled_family_lo,"scaled_family_hi":scaled_family_hi,
               "scaled_infimum_lo":global_lo,"scaled_infimum_hi":global_hi}
        rows.append({k:str(val) for k,val in exact.items()})
        table.append(f"| {R} | {eta_i} | {decimal_out(global_lo)} | {decimal_out(global_hi,True)} | {decimal_out(scaled_family_lo)} | {decimal_out(scaled_family_hi,True)} |")
Path('rational-intervals.json').write_text(json.dumps({"method":"Fraction arithmetic; 256 bisection steps; directed decimal rendering","rows":rows},indent=2)+'\n')
md='# 有理区間による有限例\n\n'
md+='`scaled = eta*(J-C)`。infimum 列は全許容形状の下限値の包囲、構成列は明示的な平滑化形状のエネルギーの包囲。小数は外向き丸め。完全な有理端点は rational-intervals.json。\n\n'
md+='| R | eta | infimum 下端 | infimum 上端 | 構成 scaled 下端 | 構成 scaled 上端 |\n|---|---:|---:|---:|---:|---:|\n'+'\n'.join(table)+'\n\n'
md+='極限係数: R=3/2 は16/9、R=2 は1/6、R=3 は1/72。有限表だけから一般命題を結論しない。\n'
Path('FINITE-EXAMPLES.md').write_text(md)
print(md)

tex=[r'\begin{table}[htbp]',r'\centering',r'\small',
     r'\caption{Outward-rounded rational enclosures of $\Xi_R(\eta)=\eta[J_R^*(\eta)-C]$. The lower endpoint is $L_R$ from Theorem~\ref{thm:main}; the upper endpoint comes from the explicit admissible family in Section~\ref{sec:recovery}. The last column gives the proved limit.}',
     r'\label{tab:enclosures}',r'\begin{tabular}{rrr r c}',r'\toprule',
     r'$R$ & $\eta$ & Lower endpoint & Upper endpoint & $K_R$ \\',r'\midrule']
for index,row in enumerate(rows):
    if index in (6,12): tex.append(r'\midrule')
    R=F(row['R']); eta=F(row['eta']); K=F(row['K'])
    rr=r'$3/2$' if R==F(3,2) else '$'+str(R)+'$'
    kk={F(3,2):r'$16/9$',F(2):r'$1/6$',F(3):r'$1/72$'}[R] if index%6==0 else ''
    tex.append(' & '.join([rr,str(eta),decimal_out(F(row['scaled_infimum_lo']),digits=9),
                         decimal_out(F(row['scaled_infimum_hi']),upper=True,digits=9),kk])+r' \\')
tex += [r'\bottomrule',r'\end{tabular}',r'\end{table}']
Path('table.tex').write_text('\n'.join(tex)+'\n')
