#!/usr/bin/env python3
"""What a finite composite electron would look like to experimentalists.

Input: the model's dimensionless size-gap product
    c = <r^2> m Delta / hbar^2            (measured by `cloud` + `cluster`)
for a cloud of three preons of mass m whose first excitation (the excited
electron e*) lies Delta above the ground state (the electron). Non-relativistic
scaling gives the charge radius
    r = sqrt(c) * hbar c / sqrt(m c^2 * Delta).
The non-relativistic model is self-consistent only for m c^2 >~ Delta; at the
boundary m c^2 = Delta it gives r = sqrt(c) hbar c / Delta. Lighter preons
need a relativistic treatment, which this model does not provide.

Experimental bars (sources in README):
  e* mass > 5.6 TeV (CMS, 13 TeV, Lambda = m*), radius < 2.8e-19 m (LEP form
  factor), contact scale Lambda > 21.3 TeV (LEP, g^2/4pi = 1),
  a_e known to 1.3e-13 (Fan et al. 2023).
g-2 shift of a composite electron of scale M: ~ m_e/M without chiral
protection, ~ (m_e/M)^2 with it (Brodsky-Drell).
Integer-only: lengths in zeptometres (1e-21 m), energies in MeV.
usage: experiment_map.py C_MICRO [DELTA_MIN_MEV=5600000]       json=0
"""
import math
import sys

HBARC_MEV_ZM = 197326980          # hbar c = 197.326980 MeV fm = 197,326,980 MeV zm
ME_KEV = 511                      # electron mass, keV (0.511 MeV)
LEP_RADIUS_ZM = 280               # 2.8e-19 m
AE_SIGMA_E15 = 130                # 1.3e-13 = 130e-15


def main():
    c_micro = int(sys.argv[1])
    dmin = int(sys.argv[2]) if len(sys.argv) > 2 else 5_600_000      # MeV
    # r_zm = sqrt(c) * hbarc / sqrt(m * Delta); with m = k * Delta:
    #      = sqrt(c / k) * hbarc / Delta
    for k_num, k_den, label in ((1, 1, "m=Delta (NR boundary)"), (10, 1, "m=10*Delta (deeply NR)")):
        # r^2 [zm^2] = c_micro/1e6 * hbarc^2 / (k Delta^2)
        r2 = (c_micro * HBARC_MEV_ZM * HBARC_MEV_ZM * k_den) // (1_000_000 * k_num * dmin * dmin)
        r_zm = math.isqrt(r2)
        print("MAP|c=%d/1000000|Delta_min=%dMeV|preon_mass=%s|r_max=%dzm|LEP_limit=%dzm|ratio_LEP_over_model=%d|json=0"
              % (c_micro, dmin, label, r_zm, LEP_RADIUS_ZM, LEP_RADIUS_ZM // max(1, r_zm)))
    # electron mass in an NR three-preon cloud: >= 3 m c^2 >= 3 Delta
    print("MAP|electron_mass_if_NR_cloud>=%dMeV|observed=0.511MeV|tuning_needed=1_part_in_%d|json=0"
          % (3 * dmin, (3 * dmin * 1000) // ME_KEV))
    # g-2: M = Delta_min
    # unprotected: m_e/M ; protected: (m_e/M)^2   (in units of 1e-15)
    unprot_e15 = (ME_KEV * 10**15) // (dmin * 1000)
    prot_e15 = (ME_KEV * ME_KEV * 10**15) // (dmin * 1000 * dmin * 1000)
    print("MAP|g-2_shift_unprotected=%de-15|g-2_shift_protected=%de-15|measured_sigma=%de-15|unprotected_excluded_by_factor=%d|protected_allowed=%d|json=0"
          % (unprot_e15, prot_e15, AE_SIGMA_E15, unprot_e15 // AE_SIGMA_E15, int(prot_e15 < AE_SIGMA_E15)))


if __name__ == "__main__":
    main()
