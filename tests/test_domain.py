import cmath,itertools,tempfile,unittest
from fractions import Fraction
from pathlib import Path
from dynamics_topology import analyze
from dynamics_topology.io import create,verify

def model(matrix):return {'schema_version':1,'matrix':[[str(x) for x in row] for row in matrix],'initial':['1','2'],'steps':8}

class DomainTests(unittest.TestCase):
    def test_stable_diagonal(self):
        r=analyze(model([['1/2',0],[0,'1/3']]))
        self.assertEqual(r['classification'],'SCHUR_STABLE')
        self.assertEqual(r['lyapunov_certificate']['equation_residual'],['0','0','0'])
        self.assertTrue(all(Fraction(b)<Fraction(a) for a,b in zip(r['potential'],r['potential'][1:])))
    def test_identity_critical(self):self.assertEqual(analyze(model([[1,0],[0,1]]))['classification'],'CRITICAL_OR_NONDECAYING')
    def test_jordan_boundary_not_bounded_claim(self):
        r=analyze(model([[1,1],[0,1]]));self.assertEqual(r['classification'],'CRITICAL_OR_NONDECAYING');self.assertEqual(r['status'],'FAIL')
    def test_unstable(self):self.assertEqual(analyze(model([[2,0],[0,0]]))['classification'],'UNSTABLE')
    def test_rotation_unit_circle(self):self.assertEqual(analyze(model([[0,-1],[1,0]]))['classification'],'CRITICAL_OR_NONDECAYING')
    def test_stable_nonnormal(self):self.assertTrue(analyze(model([['1/2',10],[0,'1/2']]))['lyapunov_certificate']['positive_definite'])
    def test_nilpotent(self):self.assertEqual(analyze(model([[0,1],[0,0]]))['trajectory'][-1],['0','0'])
    def test_625_spectral_oracle(self):
        for a,b,c,d in itertools.product([Fraction(x,2) for x in [-2,-1,0,1,2]],repeat=4):
            tr=float(a+d);det=float(a*d-b*c);disc=cmath.sqrt(tr*tr-4*det)
            rho=max(abs((tr+disc)/2),abs((tr-disc)/2))
            expected='SCHUR_STABLE' if rho<1-1e-9 else ('UNSTABLE' if rho>1+1e-9 else 'CRITICAL_OR_NONDECAYING')
            self.assertEqual(analyze(model([[a,b],[c,d]]))['classification'],expected)
    def test_exact_residual_not_only_trajectory(self):
        for a in ['1/2','-1/3','0']:
            r=analyze(model([[a,'3/5'],[0,'1/4']]))
            self.assertEqual(r['lyapunov_certificate']['equation_residual'],['0','0','0'])
    def test_strict_rationals(self):
        for v in ['1e999999999','NaN','1/0','1000001',True,0.5]:
            with self.assertRaises(ValueError):analyze(model([[v,0],[0,0]]) if isinstance(v,str) else {'schema_version':1,'matrix':[[v,'0'],['0','0']],'initial':['1','0'],'steps':1})
    def test_step_limit(self):
        d=model([[0,0],[0,0]]);d['steps']=33
        with self.assertRaises(ValueError):analyze(d)
    def test_failure_replay_consistent(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';self.assertEqual(create(p,model([[2,0],[0,0]]))['status'],'FAIL');self.assertEqual(verify(p)['status'],'FAIL')
