"""Repository-specific executable pilot; limited to the stated software assertion."""
import math
from topodyn import simulate, system, winding_index


def check():
    field=system('hopf',1)
    final=simulate(field,(0.2,0),20)[-1]
    radius=math.hypot(*final[1:]); index=winding_index(field)
    return {'domain':'dynamical-systems','statement':'The synthetic Hopf implementation approaches radius 1 and has sampled index +1 under this configuration.',
            'passed':abs(radius-1)<1e-5 and abs(index-1)<1e-8,
            'configuration':{'mu':1,'duration':20,'dt':0.01,'initial':[0.2,0]},
            'observed':{'radius':radius,'index':index},'scope':'Finite numerical software check, not a stability proof'}
