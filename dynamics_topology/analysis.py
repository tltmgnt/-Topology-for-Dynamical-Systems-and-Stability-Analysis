"""Exact rational Schur stability and Lyapunov certificates for real 2x2 maps."""
from fractions import Fraction
import re


def rational(x):
    if not isinstance(x,str) or not re.fullmatch(r'-?[0-9]{1,7}(?:/[1-9][0-9]{0,6})?',x):raise ValueError('rational inputs must be bounded strings, e.g. 1/2')
    try:q=Fraction(x)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc
    if abs(q.numerator)>1000000 or q.denominator>1000000:raise ValueError('rational magnitude/precision limit')
    return q


def solve(matrix,values):
    rows=[list(a)+[b] for a,b in zip(matrix,values)]
    for col in range(3):
        pivot=next((r for r in range(col,3) if rows[r][col]),None)
        if pivot is None:return None
        rows[col],rows[pivot]=rows[pivot],rows[col]
        scale=rows[col][col];rows[col]=[x/scale for x in rows[col]]
        for r in range(3):
            if r!=col:
                factor=rows[r][col];rows[r]=[a-factor*b for a,b in zip(rows[r],rows[col])]
    return [row[-1] for row in rows]


def analyze(data):
    if not isinstance(data,dict) or set(data)!={'schema_version','matrix','initial','steps'} or type(data['schema_version']) is not int or data['schema_version']!=1:raise ValueError('exact schema_version 1, matrix, initial, steps required')
    m=data['matrix']
    if not isinstance(m,list) or len(m)!=2 or any(not isinstance(r,list) or len(r)!=2 for r in m):raise ValueError('matrix must be 2x2')
    if not isinstance(data['initial'],list) or len(data['initial'])!=2 or type(data['steps']) is not int or not 0<=data['steps']<=32:raise ValueError('two initial coordinates and 0..32 steps required')
    a,b,c,d=[rational(x) for row in m for x in row]
    trace=a+d;det=a*d-b*c
    margins=[1-trace+det,1+trace+det,1-det]
    stable=all(v>0 for v in margins)
    classification='SCHUR_STABLE' if stable else ('CRITICAL_OR_NONDECAYING' if all(v>=0 for v in margins) else 'UNSTABLE')
    coeff=[[a*a-1,2*a*c,c*c],[a*b,a*d+b*c-1,c*d],[b*b,2*b*d,d*d-1]]
    p=solve(coeff,[Fraction(-1),Fraction(0),Fraction(-1)])
    positive=p is not None and p[0]>0 and p[0]*p[2]-p[1]*p[1]>0
    if stable and not positive:raise ValueError('internal Lyapunov certificate inconsistency')
    initial=[rational(x) for x in data['initial']];trajectory=[initial]
    for _ in range(data['steps']):
        x,y=trajectory[-1];trajectory.append([a*x+b*y,c*x+d*y])
    def potential(state):
        x,y=state;return p[0]*x*x+2*p[1]*x*y+p[2]*y*y
    residual=[sum(row[j]*p[j] for j in range(3))-rhs for row,rhs in zip(coeff,[-1,0,-1])] if p else None
    certificate={'matrix':[[str(p[0]),str(p[1])],[str(p[1]),str(p[2])]],'positive_definite':positive,'equation_residual':[str(x) for x in residual]} if p else None
    return {'schema_version':1,'domain':'dynamics','classification':classification,'status':'PASS' if stable else 'FAIL',
            'jury_margins':[str(x) for x in margins],'lyapunov_certificate':certificate,
            'trajectory':[[str(v) for v in state] for state in trajectory],
            'potential':[str(potential(state)) for state in trajectory] if positive else None,
            'execution_authorized':False,
            'scope':'Exact real rational linear discrete-time 2x2 map only. Critical classification makes no boundedness claim (Jordan growth may occur). No nonlinear, continuous-time, uncertain-model or physical stability guarantee.'}
