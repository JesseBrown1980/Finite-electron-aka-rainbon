#!/usr/bin/env python3
"""Continuum extrapolation of the dimensionless size-gap product, integer-only.

Input: box-converged points (x_k, y_k) with x = 1/l^2 (cloud width l in
lattice units) and y = c = <r^2> m Delta / hbar^2, both as exact rationals
(x = num/den, y in micro-units). Least-squares fit y = Rinf - C x, solved
exactly over the rationals with integers (no Fraction: numerators and a
common denominator are carried explicitly), then reported in micro-units with
the residual of every point and the maximum |residual|.
usage: spacing_fit.py "JE:Lchosen:y_micro" ...   (harmonic: l^2 = sqrt(JE/3))
x_k is computed from l^2 = sqrt(JE/3) as an integer square root at scale 1e12.
json=0
"""
import math
import sys

S = 10**12


def main():
    pts = []
    for a in sys.argv[2:]:
        je, y = a.split(":")
        je, y = int(je), int(y)
        if sys.argv[1] == "harmonic":
            l2 = math.isqrt(je * S * S // 3)          # l^2 = sqrt(JE/3), scaled by S
        else:
            # linear: l^3 = JE/5 (hbar^2/m = 2JE, sigma = 10 JB, JB=1) -> l^2 = (JE/5)^(2/3)
            l2 = round_cuberoot_sq(je)
        x = S * S // l2                               # 1/l^2 scaled by S
        pts.append((je, x, y))
    n = len(pts)
    sx = sum(p[1] for p in pts); sy = sum(p[2] for p in pts)
    sxx = sum(p[1] * p[1] for p in pts); sxy = sum(p[1] * p[2] for p in pts)
    det = n * sxx - sx * sx
    # y = a + b x ;  a = (sxx sy - sx sxy)/det ;  b = (n sxy - sx sy)/det   (b in micro per unit x/S)
    a_num = sxx * sy - sx * sxy
    b_num = n * sxy - sx * sy
    rinf = a_num // det
    print("FIT|potential=%s|points=%d|Rinf=%d/1000000|C=%d/1000000|json=0" % (sys.argv[1], n, rinf, -(b_num * S) // det))
    worst = 0
    for je, x, y in pts:
        pred = (a_num + b_num * x) // det
        res = y - pred
        worst = max(worst, abs(res))
        print("FIT_POINT|JE=%d|x=%d/%d|c=%d/1000000|fit=%d/1000000|residual=%d/1000000|json=0" % (je, x, S, y, pred, res))
    print("FIT|max_abs_residual=%d/1000000|json=0" % worst)


def round_cuberoot_sq(je):
    # (JE/5)^(2/3) * S  = cuberoot((JE/5)^2) * S = cuberoot(JE^2 S^3 / 25)
    t = je * je * S * S * S // 25
    lo, hi = 0, 1
    while hi * hi * hi <= t:
        hi *= 2
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if mid * mid * mid <= t:
            lo = mid
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    main()
