"""Small, dependency-free tools for autonomous planar dynamical systems."""
import cmath
import math


def _point(values):
    values = tuple(float(v) for v in values)
    if len(values) != 2 or not all(math.isfinite(v) for v in values):
        raise ValueError('Expected two finite coordinates')
    return values


def _positive(value, name):
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f'{name} must be positive and finite')


def rk4(field, point, dt):
    """Advance one step for an autonomous vector field f((x,y))."""
    _positive(dt, 'dt')
    p = _point(point)
    def stage(k, scale):
        return _point(field(tuple(p[i] + scale * k[i] for i in range(2))))
    a = _point(field(p))
    b = stage(a, dt / 2)
    c = stage(b, dt / 2)
    d = stage(c, dt)
    return _point(p[i] + dt * (a[i] + 2*b[i] + 2*c[i] + d[i])/6 for i in range(2))


def simulate(field, initial, duration=20.0, dt=0.01):
    """Return (time, x, y) rows, including initial and exact final time."""
    _positive(duration, 'duration')
    _positive(dt, 'dt')
    steps = math.ceil(duration / dt)
    if steps > 1_000_000:
        raise ValueError('Simulation exceeds one million steps')
    p = _point(initial)
    rows = [(0.0, *p)]
    for i in range(1, steps + 1):
        t = min(i * dt, duration)
        p = rk4(field, p, t - rows[-1][0])
        rows.append((t, *p))
    return rows


def jacobian(field, point, epsilon=1e-5):
    _positive(epsilon, 'epsilon')
    p = _point(point)
    columns = []
    for i in range(2):
        a, b = list(p), list(p)
        a[i] += epsilon
        b[i] -= epsilon
        fa, fb = _point(field(a)), _point(field(b))
        columns.append([(fa[j]-fb[j])/(2*epsilon) for j in range(2)])
    return [[columns[j][i] for j in range(2)] for i in range(2)]


def stability(field, equilibrium, tolerance=1e-7):
    """Classify a supplied equilibrium by its linearization; no root search."""
    _positive(tolerance, 'tolerance')
    p = _point(equilibrium)
    if math.hypot(*_point(field(p))) > tolerance:
        raise ValueError('Point is not an equilibrium within tolerance')
    (a, b), (c, d) = jacobian(field, p)
    trace, determinant = a+d, a*d-b*c
    root = cmath.sqrt(trace*trace - 4*determinant)
    eigenvalues = ((trace+root)/2, (trace-root)/2)
    real = [v.real for v in eigenvalues]
    if any(abs(v) <= tolerance for v in real):
        classification = 'nonhyperbolic: linearization inconclusive'
    elif real[0] * real[1] < 0:
        classification = 'saddle'
    elif max(real) < 0:
        classification = 'asymptotically stable'
    else:
        classification = 'unstable'
    return {'classification': classification, 'trace': trace, 'determinant': determinant,
            'eigenvalues': [[v.real, v.imag] for v in eigenvalues]}


def winding_index(field, center=(0, 0), radius=1.0, samples=512):
    """Estimate vector-field index along a counterclockwise circular contour.

    Sampling cannot certify that a zero or rapid rotation was not missed.
    """
    center = _point(center)
    _positive(radius, 'radius')
    if not isinstance(samples, int) or samples < 8:
        raise ValueError('samples must be an integer >= 8')
    angles = []
    for i in range(samples):
        theta = 2*math.pi*i/samples
        v = _point(field((center[0]+radius*math.cos(theta), center[1]+radius*math.sin(theta))))
        if math.hypot(*v) < 1e-12:
            raise ValueError('Vector field vanishes on sampled contour')
        angles.append(math.atan2(v[1], v[0]))
    turns = sum(math.atan2(math.sin(angles[(i+1)%samples]-a),
                           math.cos(angles[(i+1)%samples]-a)) for i,a in enumerate(angles))/(2*math.pi)
    return turns


def lyapunov(field, initial, duration=50.0, dt=0.01, separation=1e-7, burn_in=10.0):
    """Finite-time largest exponent estimate using a renormalized nearby orbit."""
    _positive(separation, 'separation')
    if not math.isfinite(burn_in) or burn_in < 0:
        raise ValueError('burn_in must be finite and nonnegative')
    p = _point(initial)
    if burn_in:
        p = simulate(field, p, burn_in, dt)[-1][1:]
    # Reuse simulation validation before allocating the paired orbit.
    _positive(duration, 'duration')
    _positive(dt, 'dt')
    steps = math.ceil(duration/dt)
    if steps > 1_000_000:
        raise ValueError('Simulation exceeds one million steps')
    q = (p[0]+separation, p[1])
    total, elapsed = 0.0, 0.0
    for i in range(steps):
        h = min(dt, duration-elapsed)
        p, q = rk4(field,p,h), rk4(field,q,h)
        delta = (q[0]-p[0],q[1]-p[1])
        distance = math.hypot(*delta)
        if distance == 0:
            raise ValueError('Nearby trajectories collapsed numerically; increase separation')
        total += math.log(distance/separation)
        q = _point(p[j]+separation*delta[j]/distance for j in range(2))
        elapsed = min((i+1)*dt, duration)
    return total/duration


def system(name, mu=1.0):
    """Built-in planar examples. Hopf has radial dynamics r'=mu*r-r**3."""
    if not math.isfinite(mu):
        raise ValueError('mu must be finite')
    if name == 'hopf':
        return lambda p: (mu*p[0]-p[1]-(p[0]**2+p[1]**2)*p[0], p[0]+mu*p[1]-(p[0]**2+p[1]**2)*p[1])
    if name == 'vanderpol':
        return lambda p: (p[1], mu*(1-p[0]**2)*p[1]-p[0])
    if name == 'saddle':
        return lambda p: (p[0], -p[1])
    raise ValueError(f'Unknown system: {name}')
