"""Executable synthetic domain adapter, not independent scientific reproduction."""
from dynamics_topology import analyze
DATA={'schema_version': 1, 'matrix': [['1/2', '0'], ['0', '1/3']], 'initial': ['1', '1'], 'steps': 8}

def check():
    result=analyze(DATA)
    return {'domain':result['domain'],'statement':'The supplied synthetic exact linear discrete-time stability fixture satisfies its declared reference checks.','passed':bool(result["classification"]=="SCHUR_STABLE" and result["lyapunov_certificate"]["positive_definite"]),
            'configuration':DATA,'observed':result,'scope':'Exact rational 2x2 discrete-time linear maps x(t+1)=A x(t). Jury margins classify strict Schur stability. Solve A^T P A-P=-I with rational elimination and check P positive definite. Critical/boundary results do not assert boundedness. No continuous-time, nonlinear, uncertain-parameter or physical stability claim.'}
