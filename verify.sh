#!/usr/bin/env bash
# Finite Electron end-to-end checks. Integer-only; every check fails closed.
set -euo pipefail
cd "$(dirname "$0")"
has() { grep -c "$@" > /dev/null; }
cargo build --release -q
B=target/release
mkdir -p build
fld() { echo "$1" | tr '|' '\n' | grep "^$2=" | cut -d= -f2 | cut -d/ -f1; }
# 1. symmetry sectors reproduce the full lattice exactly (L=6 harmonic, JE=9, JB=1)
full=$($B/cloud 6 harmonic 9 1 600 10000000)
secA=$($B/symsec 6 harmonic A 9 1 800 10000000)
secP=$($B/symsec 6 harmonic Pz 9 1 800 10000000)
test "$(fld "$full" E0)" = "$(fld "$secA" E_lowest)" && test "$(fld "$full" E0)" = 23960538
test "$(fld "$full" r2_ground)" = "$(fld "$secA" r2)" && test "$(fld "$secA" r2)" = 2597261
echo "$secA" | has "|sector_states=309|w_self_adjoint=PASS|"
echo "$secP" | has "|sector_states=1680|w_self_adjoint=PASS|"
$B/cloudb 6 harmonic build/h6.matrix > /dev/null
iv=$($B/cluster build/h6.matrix 9 1 8 4 | grep "^CLUSTER_LEVEL|k=1|" | tr '|' '\n' | grep '^interval=' | cut -d= -f2 | tr -d '[]' | cut -d/ -f1)
lo=$(( ${iv%,*} * 9 )); hi=$(( ${iv#*,} * 9 + 9 )); e1=$(fld "$secP" E_lowest)
test "$e1" -ge "$lo" && test "$e1" -le "$hi"
# 2. harmonic calibration: first excited level 6-fold degenerate on the full L=6 lattice
lv=$($B/cluster build/h6.matrix 9 1 8 4 | grep "^CLUSTER_LEVEL" | tr '|' '\n' | grep '^theta=' | cut -d= -f2 | cut -d/ -f1)
test "$(echo "$lv" | sed -n 2,7p | sort -u | wc -l)" -le 2   # levels 1..6 coincide (to 1 micro-unit rounding)
# 3. L=8 symmetry-sector values (pinned; equal to the full-lattice values)
$B/symsec 8 harmonic A 9 1 800 10000000 | has "|sector_states=1306|.*|E_lowest=29637907/1000000|eps_up=1/1000000|r2=1962201/1000000|"
$B/symsec 8 harmonic Pz 9 1 800 10000000 | has "|sector_states=8925|.*|E_lowest=40403024/1000000|eps_up=1/1000000|"
# 4. experimental mapping (calibration value c = 1)
python3 python/experiment_map.py 1000000 | has "preon_mass=m=Delta (NR boundary)|r_max=35zm|LEP_limit=280zm|"
# 5. integer-only audit
python3 python/integer_only_audit.py python/experiment_map.py
echo "VERIFY|status=PASS|json=0"
