"""Derive curvature directly from the metric, independently of ADM formula."""
from functools import lru_cache
import json
from pathlib import Path
import sympy as s

b = s.Symbol('b', real=True)
g1 = s.symbols('b_x b_y b_z', real=True)
xx, xy, xz, yy, yz, zz = s.symbols('b_xx b_xy b_xz b_yy b_yz b_zz', real=True)
g2 = s.Matrix([[xx, xy, xz], [xy, yy, yz], [xz, yz, zz]])
metric = s.eye(4)
metric[0,0] = b*b-1
metric[0,3] = metric[3,0] = b
inverse = metric.inv()
def D(expr, k):
    if k == 0:
        return s.S.Zero
    return s.diff(expr,b)*g1[k-1] + sum(s.diff(expr,g1[j])*g2[j,k-1] for j in range(3))
@lru_cache(None)
def Gamma(a,c,d):
    return s.expand(sum(inverse[a,k]*(D(metric[k,d],c)+D(metric[k,c],d)-D(metric[c,d],k)) for k in range(4))/2)
@lru_cache(None)
def R(a,c,m,n):
    return s.expand(D(Gamma(a,n,c),m)-D(Gamma(a,m,c),n) +
                    sum(Gamma(a,m,k)*Gamma(k,n,c)-Gamma(a,n,k)*Gamma(k,m,c) for k in range(4)))
normal = s.Matrix([1,0,0,-b])
assert (normal.T*metric*normal)[0].expand() == -1
acceleration = s.Matrix([s.expand(sum(normal[k]*D(normal[mu],k) for k in range(4)) + sum(Gamma(mu,a,c)*normal[a]*normal[c] for a in range(4) for c in range(4))) for mu in range(4)])
assert acceleration == s.zeros(4,1)
E = s.zeros(3)
for i in range(3):
    for j in range(3):
        E[i,j] = s.expand(sum(metric[i+1,a]*R(a,c,j+1,d)*normal[c]*normal[d]
                             for a in (0,3,i+1) for c in (0,3) for d in (0,3))) if i != 2 else s.expand(sum(metric[3,a]*R(a,c,j+1,d)*normal[c]*normal[d]
                             for a in (0,3) for c in (0,3) for d in (0,3)))
# For i=x,y the distinct index set above has no duplicate; z uses its two nonzero metric terms.
z = s.Matrix([0,0,1]); grad=s.Matrix(g1); hz=g2*z
expected = -b*(hz*z.T+z*hz.T)/2 - s.Rational(3,4)*grad*grad.T -g1[2]*(grad*z.T+z*grad.T)/4 +(grad.dot(grad))*z*z.T/4
assert all(s.expand(x)==0 for x in E-expected), (E,expected)
ricci = s.Matrix(4,4,lambda c,d: s.expand(sum(R(a,c,a,d) for a in range(4))))
scalar = s.expand(sum(inverse[c,d]*ricci[c,d] for c in range(4) for d in range(4)))
Gnn = s.expand((normal.T*(ricci-metric*scalar/2)*normal)[0])
assert s.expand(Gnn+(g1[0]**2+g1[1]**2)/4)==0
# Independently compute the ADM Hamiltonian expression and the electric expression.
K = (grad*z.T+z*grad.T)/2
LieK = b*K.applyfunc(lambda e: D(e,3)) + grad*(z.T*K)+(K*z)*grad.T
Eadm = -LieK+K*K
assert all(s.expand(e)==0 for e in E-Eadm)
assert s.expand((s.trace(K)**2-s.trace(K*K))/2-Gnn)==0
v,h,p,dp,r,u = s.symbols('v h p dp r u', real=True)
t = s.Symbol('s', real=True)
q = s.Matrix([t,0,u])
replacement={b:v*h, **{g1[i]:v*p*q[i] for i in range(3)}}
replacement.update({g2[i,j]:v*(dp*q[i]*q[j]+p/r*(int(i==j)-q[i]*q[j])) for i in range(3) for j in range(i,3)})
radial = E.subs(replacement, simultaneous=True).applyfunc(lambda e:s.expand(e/v**2).subs(t**2,1-u**2).expand())
radial_expected=s.Matrix([[-s.Rational(3,4)*p*p*(1-u*u),0,-h*(dp-p/r)*t*u/2-p*p*t*u],
 [0,0,0],[-h*(dp-p/r)*t*u/2-p*p*t*u,0,-h*dp*u*u-h*p/r*(1-u*u)+(1-5*u*u)*p*p/4]])
assert all(s.expand(e)==0 for e in radial-radial_expected)
assert not any(e.has(v) for e in radial)
axis=radial.subs({u:1,t:0})
assert axis == s.diag(0,0,-h*dp-p*p)
assert E.subs({**{x:0 for x in g1},**{x:0 for x in g2}})==s.zeros(3)
theta=s.Symbol('theta',real=True)
assert s.integrate(s.sin(theta)**3,(theta,0,s.pi))==s.Rational(4,3)
T=s.Symbol('T', real=True)
kernel=s.Rational(15,16)*(1-T*T)**2
assert s.integrate(kernel,(T,-1,1))==1
assert 2*s.integrate(T*kernel,(T,0,1))==s.Rational(5,16)
RR=s.Symbol('R',positive=True)
C=RR/(RR-1); a=1/(RR*(RR-1))
assert s.simplify(RR**2*a**3/3-1/(3*RR*(RR-1)**3))==0
result={"sympy_version":s.__version__,"checks":"all passed", "E_general":str(E),
        "normal_acceleration":str(acceleration),"normalized_tensor_independent_of_nonzero_v":True,
        "G_nn":str(Gnn),"rho":"-(b_x**2+b_y**2)/(32*pi)",
        "E_radial_div_v2":str(radial_expected),"axis_div_v2":str(axis),
        "integrated_energy":"-v**2*J/12 = -J/1200 at v=1/10",
        "kernel_integral":"1","kernel_abs_first_moment":"5/16",
        "K":"1/(3*R*(R-1)**3)"}
Path('symbolic-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
