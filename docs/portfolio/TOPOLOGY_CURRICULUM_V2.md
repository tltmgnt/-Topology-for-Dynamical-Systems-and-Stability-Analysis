# Topology compatibility and curriculum v2 — -Topology-for-Dynamical-Systems-and-Stability-Analysis

Version 2 adapts the explicit-molecular-graph teaching pattern to this repository's actual role. This is documentation and a learning/decision framework; it introduces no mathematical engine, runtime dependency or operational permission.

## Repository decision

| Question | Repository-specific answer |
| --- | --- |
| Architectural role | specialized dynamical tool |
| Minimum useful mathematics | Exact rational linear algebra and discrete-time stability; no new differential topology required |
| Relationships to preserve | 2x2 map coefficients, Jury margins and Lyapunov certificates |
| Concrete operation / capstone | Compare A=diag(1/2,1/2), A=diag(1,1) and A=diag(2,1/2); explain strict stability versus a boundary outcome |
| Necessity and scope boundary | A critical classification does not prove boundedness; nonlinear, continuous-time and physical stability are outside scope |

The decision is a source-based recommendation, not measured proof that a new specialty improves this repository. Start with the existing implementation and compare any proposed abstraction against a simpler alternative.

## Six-criterion compatibility scorecard

Complete one scorecard per proposed candidate and per concrete operation. Leave unmeasured entries unknown. Scores are human judgments from 0 (no fit) to 5 (strong evidenced fit); unknown is not zero. Do not sum an incomplete card. A total out of 30 is a heuristic, not adoption approval, and feasibility or necessity can veto a high total.

| Criterion | Score | Required evidence |
| --- | --- | --- |
| Structural compatibility | Not yet scored | Map the repository objects and the relationships above without losing direction, labels, units or missingness. |
| Transformation support | Not yet scored | Demonstrate the capstone operation on accepted and rejected inputs. |
| Invariant preservation | Not yet scored | State the property preserved and supply a counterexample or perturbation. |
| Computational feasibility | Not yet scored | Measure size, time and memory on bounded fixtures; record limits. |
| Integration compatibility | Not yet scored | Verify existing schemas, APIs and neighboring contracts remain compatible. |
| Mathematical necessity | Not yet scored | Compare with exact rational linear algebra and discrete-time stability and explain the additional capability, if any. |

## Curriculum

Prerequisites: basic programming, sets, functions and graph vocabulary. Work in six competency-gated sessions, approximately 60–90 minutes each; empirical evaluation is a separate research activity.

| Session | Learning objective | Exercise | Completion evidence |
| --- | --- | --- | --- |
| 1. Model | Identify 2x2 map coefficients, jury margins and lyapunov certificates. | Draw a minimal valid example and one excluded relationship. | Annotated object/relation inventory with explicit assumptions. |
| 2. Contract | Distinguish schema validity from substantive correctness. | Trace validation and propose malformed, missing and boundary inputs. | Input-to-rejection table grounded in current source. |
| 3. Operation | Explain exact rational linear algebra and discrete-time stability; no new differential topology required. | Compare A=diag(1/2,1/2), A=diag(1,1) and A=diag(2,1/2); explain strict stability versus a boundary outcome. | Hand trace compared with existing software, or a clearly labeled specification when no runtime exists. |
| 4. Preservation | State what a transformation must preserve. | Rename identifiers, reorder records, then alter one meaningful relation; predict each effect under the actual contract. | Separate invariant, expected change and unsupported transformation. |
| 5. Comparison | Justify mathematical necessity and cost. | Complete the six-criterion card for the existing approach and one proposed alternative; record unknowns honestly. | Evidence-backed recommendation with baseline and explicit veto conditions. |
| 6. Reproduction | Communicate the bounded result. | Reproduce the capstone using existing offline fixtures and record software version, inputs, outputs and limitations. | Reviewable notebook or report distinguishing computation, replay, independent evaluation and authorization. |

## Source-linked reading laboratory

The table is a guided selection of source lines, not an assertion that the whole repository is covered. Line numbers refer to the inspected source blob `849a9d67cdfd1f1b5e927b4edc315f63a766ffca` in [dynamics_topology/analysis.py](../../dynamics_topology/analysis.py). Recheck anchors after source changes.

| Line | Statement | Learning check |
| --- | --- | --- |
| [1](../../dynamics_topology/analysis.py#L1) | `"""Exact rational Schur stability and Lyapunov certificates for real 2x2 maps."""` | Explain the stated scope and identify a claim the implementation does not establish. |
| [2](../../dynamics_topology/analysis.py#L2) | `from fractions import Fraction` | Identify the dependency and explain which operation needs it. |
| [3](../../dynamics_topology/analysis.py#L3) | `import re` | Identify the dependency and explain which operation needs it. |
| [6](../../dynamics_topology/analysis.py#L6) | `def rational(x):` | State the input/output contract and trace one normal and one failing case. |
| [7](../../dynamics_topology/analysis.py#L7) | `if not isinstance(x,str) or not re.fullmatch(r'-?[0-9]{1,7}(?:/[1-9][0-9]{0,6})?',x):raise ValueError('rational inputs must be bounded strings, e.g. 1/2')` | Construct the triggering input and explain why rejection preserves the contract. |
| [8](../../dynamics_topology/analysis.py#L8) | `try:q=Fraction(x)` | Explain the statement, track its state change and predict its effect on the worked example. |
| [9](../../dynamics_topology/analysis.py#L9) | `except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc` | Construct the triggering input and explain why rejection preserves the contract. |
| [10](../../dynamics_topology/analysis.py#L10) | `if abs(q.numerator)>1000000 or q.denominator>1000000:raise ValueError('rational magnitude/precision limit')` | Construct the triggering input and explain why rejection preserves the contract. |
| [11](../../dynamics_topology/analysis.py#L11) | `return q` | Predict the returned value and distinguish a computed result from authorization. |
| [14](../../dynamics_topology/analysis.py#L14) | `def solve(matrix,values):` | State the input/output contract and trace one normal and one failing case. |
| [15](../../dynamics_topology/analysis.py#L15) | `rows=[list(a)+[b] for a,b in zip(matrix,values)]` | State the loop invariant, termination argument and one boundary case. |
| [16](../../dynamics_topology/analysis.py#L16) | `for col in range(3):` | State the loop invariant, termination argument and one boundary case. |
| [17](../../dynamics_topology/analysis.py#L17) | `pivot=next((r for r in range(col,3) if rows[r][col]),None)` | State the loop invariant, termination argument and one boundary case. |
| [18](../../dynamics_topology/analysis.py#L18) | `if pivot is None:return None` | Predict the returned value and distinguish a computed result from authorization. |
| [19](../../dynamics_topology/analysis.py#L19) | `rows[col],rows[pivot]=rows[pivot],rows[col]` | Explain the statement, track its state change and predict its effect on the worked example. |
| [20](../../dynamics_topology/analysis.py#L20) | `scale=rows[col][col];rows[col]=[x/scale for x in rows[col]]` | State the loop invariant, termination argument and one boundary case. |
| [21](../../dynamics_topology/analysis.py#L21) | `for r in range(3):` | State the loop invariant, termination argument and one boundary case. |
| [22](../../dynamics_topology/analysis.py#L22) | `if r!=col:` | Trace both branches and identify the condition that changes the result. |
| [23](../../dynamics_topology/analysis.py#L23) | `factor=rows[r][col];rows[r]=[a-factor*b for a,b in zip(rows[r],rows[col])]` | State the loop invariant, termination argument and one boundary case. |
| [24](../../dynamics_topology/analysis.py#L24) | `return [row[-1] for row in rows]` | Predict the returned value and distinguish a computed result from authorization. |
| [27](../../dynamics_topology/analysis.py#L27) | `def analyze(data):` | State the input/output contract and trace one normal and one failing case. |
| [28](../../dynamics_topology/analysis.py#L28) | `if not isinstance(data,dict) or set(data)!={'schema_version','matrix','initial','steps'} or type(data['schema_version']) is not int or data['schema_version']!=1:raise ValueError('exact schema_version 1, matrix, initial, steps required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [29](../../dynamics_topology/analysis.py#L29) | `m=data['matrix']` | Explain the statement, track its state change and predict its effect on the worked example. |
| [30](../../dynamics_topology/analysis.py#L30) | `if not isinstance(m,list) or len(m)!=2 or any(not isinstance(r,list) or len(r)!=2 for r in m):raise ValueError('matrix must be 2x2')` | Construct the triggering input and explain why rejection preserves the contract. |
| [31](../../dynamics_topology/analysis.py#L31) | `if not isinstance(data['initial'],list) or len(data['initial'])!=2 or type(data['steps']) is not int or not 0<=data['steps']<=32:raise ValueError('two initial coordinates and 0..32 steps required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [32](../../dynamics_topology/analysis.py#L32) | `a,b,c,d=[rational(x) for row in m for x in row]` | State the loop invariant, termination argument and one boundary case. |
| [33](../../dynamics_topology/analysis.py#L33) | `trace=a+d;det=a*d-b*c` | Explain the statement, track its state change and predict its effect on the worked example. |
| [34](../../dynamics_topology/analysis.py#L34) | `margins=[1-trace+det,1+trace+det,1-det]` | Explain the statement, track its state change and predict its effect on the worked example. |
| [35](../../dynamics_topology/analysis.py#L35) | `stable=all(v>0 for v in margins)` | State the loop invariant, termination argument and one boundary case. |
| [36](../../dynamics_topology/analysis.py#L36) | `classification='SCHUR_STABLE' if stable else ('CRITICAL_OR_NONDECAYING' if all(v>=0 for v in margins) else 'UNSTABLE')` | State the loop invariant, termination argument and one boundary case. |
| [37](../../dynamics_topology/analysis.py#L37) | `coeff=[[a*a-1,2*a*c,c*c],[a*b,a*d+b*c-1,c*d],[b*b,2*b*d,d*d-1]]` | Explain the statement, track its state change and predict its effect on the worked example. |
| [38](../../dynamics_topology/analysis.py#L38) | `p=solve(coeff,[Fraction(-1),Fraction(0),Fraction(-1)])` | Explain the statement, track its state change and predict its effect on the worked example. |
| [39](../../dynamics_topology/analysis.py#L39) | `positive=p is not None and p[0]>0 and p[0]*p[2]-p[1]*p[1]>0` | Explain the statement, track its state change and predict its effect on the worked example. |
| [40](../../dynamics_topology/analysis.py#L40) | `if stable and not positive:raise ValueError('internal Lyapunov certificate inconsistency')` | Construct the triggering input and explain why rejection preserves the contract. |
| [41](../../dynamics_topology/analysis.py#L41) | `initial=[rational(x) for x in data['initial']];trajectory=[initial]` | State the loop invariant, termination argument and one boundary case. |
| [42](../../dynamics_topology/analysis.py#L42) | `for _ in range(data['steps']):` | State the loop invariant, termination argument and one boundary case. |
| [43](../../dynamics_topology/analysis.py#L43) | `x,y=trajectory[-1];trajectory.append([a*x+b*y,c*x+d*y])` | Explain the statement, track its state change and predict its effect on the worked example. |
| [44](../../dynamics_topology/analysis.py#L44) | `def potential(state):` | State the input/output contract and trace one normal and one failing case. |
| [45](../../dynamics_topology/analysis.py#L45) | `x,y=state;return p[0]*x*x+2*p[1]*x*y+p[2]*y*y` | Predict the returned value and distinguish a computed result from authorization. |
| [46](../../dynamics_topology/analysis.py#L46) | `residual=[sum(row[j]*p[j] for j in range(3))-rhs for row,rhs in zip(coeff,[-1,0,-1])] if p else None` | State the loop invariant, termination argument and one boundary case. |
| [47](../../dynamics_topology/analysis.py#L47) | `certificate={'matrix':[[str(p[0]),str(p[1])],[str(p[1]),str(p[2])]],'positive_definite':positive,'equation_residual':[str(x) for x in residual]} if p else None` | State the loop invariant, termination argument and one boundary case. |
| [48](../../dynamics_topology/analysis.py#L48) | `return {'schema_version':1,'domain':'dynamics','classification':classification,'status':'PASS' if stable else 'FAIL',` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [49](../../dynamics_topology/analysis.py#L49) | `'jury_margins':[str(x) for x in margins],'lyapunov_certificate':certificate,` | State the loop invariant, termination argument and one boundary case. |
| [50](../../dynamics_topology/analysis.py#L50) | `'trajectory':[[str(v) for v in state] for state in trajectory],` | State the loop invariant, termination argument and one boundary case. |
| [51](../../dynamics_topology/analysis.py#L51) | `'potential':[str(potential(state)) for state in trajectory] if positive else None,` | State the loop invariant, termination argument and one boundary case. |
| [52](../../dynamics_topology/analysis.py#L52) | `'execution_authorized':False,` | Explain the statement, track its state change and predict its effect on the worked example. |
| [53](../../dynamics_topology/analysis.py#L53) | `'scope':'Exact real rational linear discrete-time 2x2 map only. Critical classification makes no boundedness claim (Jordan growth may occur). No nonlinear, continuous-time, uncertain-model or physical stability guarantee.'}` | Explain the statement, track its state change and predict its effect on the worked example. |
## Assessment and verification

A learner must explain the model, trace the capstone, identify a counterexample and state the scope boundary. Assess these four competencies equally; a numerical score cannot compensate for an unsupported scientific or operational claim.

Relevant existing checks:

- [tests/test_domain.py](../../tests/test_domain.py)
- [tests/test_researchos.py](../../tests/test_researchos.py)

Follow [README](../../README.md) for environment and installed-package instructions. Read scripts before execution; source-reading exercises do not authorize provider calls, model downloads, live orders, hardware actions or messages. Synthetic fixtures establish software behavior only. This documentation change does not report those exercises as already executed.

## Interoperability and adoption gate

Retain explicit domain contracts. Shared assurance records should refer to domain evidence and its assumptions rather than relabeling graph reachability, homology, statistical calibration and epistemic acceptance as interchangeable quantities. The canonical ResearchOs controller remains owned by ResearchOs; this curriculum does not create another controller fork.

Adopt additional mathematics only after a versioned experiment demonstrates a useful operation, the scorecard has evidence, the simpler baseline is inadequate and existing conformance checks remain satisfied. A critical classification does not prove boundedness; nonlinear, continuous-time and physical stability are outside scope.
