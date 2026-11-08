"""Command line entry point; reports JSON and optionally exports CSV and SVG."""
import argparse
import csv
import json
import math
from pathlib import Path
from .core import lyapunov, simulate, stability, system, winding_index


def svg(rows):
    xs, ys = [r[1] for r in rows], [r[2] for r in rows]
    lo_x, lo_y = min(xs), min(ys)
    span = max(max(xs)-lo_x, max(ys)-lo_y, 1e-6)
    points = ' '.join(f'{30+540*(x-lo_x)/span:.2f},{570-540*(y-lo_y)/span:.2f}' for _,x,y in rows)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"><title>Phase trajectory: x horizontal, y vertical</title><rect width="600" height="600" fill="white"/><polyline points="{points}" fill="none" stroke="#2563eb" stroke-width="1.5"/></svg>\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--system', choices=['hopf','vanderpol','saddle'], default='hopf')
    parser.add_argument('--mu', type=float, default=1)
    parser.add_argument('--initial', nargs=2, type=float, default=[0.2,0])
    parser.add_argument('--duration', type=float, default=30)
    parser.add_argument('--dt', type=float, default=0.01)
    parser.add_argument('--output', type=Path, help='Output directory for report.json, trajectory.csv, phase.svg')
    parser.add_argument('--sweep', nargs=3, type=float, metavar=('START','STOP','COUNT'), help='Hopf parameter sweep; reports final radii')
    args = parser.parse_args(argv)
    try:
        field = system(args.system,args.mu)
        rows = simulate(field,args.initial,args.duration,args.dt)
        report = {'system': args.system, 'mu': args.mu, 'final_state': rows[-1],
                  'origin_stability': stability(field,(0,0)),
                  'origin_index_estimate': winding_index(field),
                  'largest_lyapunov_estimate': lyapunov(field,args.initial,args.duration,args.dt),
                  'limitations': 'Finite-time numerical estimates; not proofs of stability or bifurcation.'}
        if args.sweep:
            start,stop,count = args.sweep
            if args.system != 'hopf' or not all(math.isfinite(v) for v in args.sweep) or count != int(count) or not 2 <= count <= 1000:
                raise ValueError('Sweep requires hopf and a finite integer count from 2 to 1000')
            report['sweep'] = []
            for i in range(int(count)):
                mu = start+(stop-start)*i/(count-1)
                final = simulate(system('hopf',mu),args.initial,args.duration,args.dt)[-1]
                report['sweep'].append({'mu':mu,'final_radius':math.hypot(*final[1:])})
        encoded = json.dumps(report, indent=2, allow_nan=False)
        if args.output:
            args.output.mkdir(parents=True,exist_ok=True)
            (args.output/'report.json').write_text(encoded+'\n',encoding='utf-8')
            with (args.output/'trajectory.csv').open('w',newline='',encoding='utf-8') as f:
                writer=csv.writer(f); writer.writerow(['time','x','y']); writer.writerows(rows)
            (args.output/'phase.svg').write_text(svg(rows),encoding='utf-8')
        print(encoded)
    except (ValueError, OverflowError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
