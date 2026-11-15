import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from topodyn import simulate, stability, winding_index, lyapunov, system


class DynamicsTests(unittest.TestCase):
    def test_linear_decay_and_final_time(self):
        rows = simulate(lambda p: (-p[0],-2*p[1]), (1,1),1,0.03)
        self.assertEqual(rows[-1][0],1)
        self.assertAlmostEqual(rows[-1][1],math.exp(-1),places=7)
        self.assertAlmostEqual(rows[-1][2],math.exp(-2),places=7)

    def test_stability(self):
        self.assertEqual(stability(system('hopf',-1),(0,0))['classification'],'asymptotically stable')
        self.assertEqual(stability(system('hopf',1),(0,0))['classification'],'unstable')
        self.assertEqual(stability(system('saddle'),(0,0))['classification'],'saddle')
        self.assertIn('inconclusive',stability(system('hopf',0),(0,0))['classification'])
        with self.assertRaises(ValueError): stability(system('saddle'),(1,1))

    def test_indices(self):
        self.assertAlmostEqual(winding_index(system('hopf')),1)
        self.assertAlmostEqual(winding_index(system('saddle')),-1)
        self.assertAlmostEqual(winding_index(lambda p:(1,0)),0)
        with self.assertRaises(ValueError): winding_index(lambda p:(0,0))

    def test_hopf_attractor(self):
        final=simulate(system('hopf',1),(0.2,0),20)[-1]
        self.assertAlmostEqual(math.hypot(*final[1:]),1,places=6)
        final=simulate(system('hopf',-1),(0.2,0),10)[-1]
        self.assertLess(math.hypot(*final[1:]),1e-5)

    def test_exponent_known_linear_system(self):
        self.assertAlmostEqual(lyapunov(lambda p:(-p[0],-2*p[1]),(0,0),5,burn_in=0),-1,places=6)
        self.assertAlmostEqual(lyapunov(system('saddle'),(0,0),5,burn_in=0),1,places=6)
        self.assertLess(abs(lyapunov(system('hopf'),(0.2,0),50)),0.05)

    def test_validation(self):
        for dt in [0,-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError): simulate(system('hopf'),(1,0),1,dt)
        with self.assertRaises(ValueError): simulate(system('hopf'),(float('nan'),0))
        with self.assertRaises(ValueError): simulate(system('hopf'),(1,0),1,1e-8)

    def test_cli_exports_and_sweep(self):
        with tempfile.TemporaryDirectory() as directory:
            result=subprocess.run([sys.executable,'-m','topodyn','--duration','2','--sweep','-1','1','3','--output',directory],capture_output=True,text=True,check=True)
            report=json.loads(result.stdout)
            self.assertEqual(len(report['sweep']),3)
            self.assertEqual(json.loads((Path(directory)/'report.json').read_text()),report)
            self.assertTrue((Path(directory)/'trajectory.csv').read_text().startswith('time,x,y'))
            import xml.etree.ElementTree as ET
            ET.parse(Path(directory)/'phase.svg')

    def test_cli_invalid_input(self):
        result=subprocess.run([sys.executable,'-m','topodyn','--dt','0'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertNotIn('Traceback',result.stderr)


if __name__ == '__main__': unittest.main()
