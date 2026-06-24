#!/usr/bin/env python3
r"""A virtual Josephson junction, built from folders.        < •        (David Wise / ROOT0)

        electrode-left   <        the-dot  •        >   electrode-right

Two superconducting electrodes are folders; each holds the macroscopic phase of its
Cooper-pair condensate (psi.json). They are joined at a WEAK LINK -- the witnessed dot
the-dot/ -- which holds the coupling (Ic) and the junction's one dynamical variable,
the phase difference phi (phase.json). The phase lives AT the dot, because the junction
IS the dot.

Running this steps the junction by the real Josephson relations (overdamped RSJ):

    I_s  = Ic * sin(phi)            # DC Josephson: supercurrent set by the phase
    dphi = (I_bias - I_s) * dt      # RSJ: the phase winds under bias

When phi winds through 2*pi, one flux quantum Phi0 = h/2e slips through the dot -> an
SFQ pulse is emitted (the neuron fires). Below Ic the phase is trapped (zero voltage,
a dissipationless supercurrent); above Ic it runs and fires.

Usage:  python evolve.py [steps]      (default 400)
"""
import json, os, math, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: json.load(open(os.path.join(HERE, p), encoding="utf-8"))
def wr(p, d): json.dump(d, open(os.path.join(HERE, p), "w", encoding="utf-8"), indent=2)

L  = rd("electrode-left/psi.json")
R  = rd("electrode-right/psi.json")
J  = rd("the-dot/coupling.json")
ph = rd("the-dot/phase.json")
B  = rd("bias.json")

steps = int(sys.argv[1]) if len(sys.argv) > 1 else 400
dt, Ic, Ib = B["dt"], J["Ic"], B["I_bias"]
phi = ph["phi"]
emitted = 0
for _ in range(steps):
    Is = Ic * math.sin(phi)
    phi += (Ib - Is) * dt           # normalized units (2e*R/hbar folded into dt)
    while phi >= 2 * math.pi:
        phi -= 2 * math.pi
        emitted += 1                # one 2-pi slip = one flux quantum = one SFQ pulse

# write the evolved phase back to the dot; keep the right electrode consistent
ph["phi"] = round(phi, 6)
R["phase"] = round((L["phase"] - phi) % (2 * math.pi), 6)
wr("the-dot/phase.json", ph)
wr("electrode-right/psi.json", R)

Is = Ic * math.sin(phi)
state = {
    "phi_at_the_dot":  round(phi, 4),
    "supercurrent_Is": round(Is, 4),
    "I_bias":          Ib,
    "Ic_critical":     Ic,
    "regime": ("VOLTAGE STATE -- phase running, firing SFQ pulses" if Ib > Ic
               else "SUPERCURRENT -- zero voltage, phase trapped (dissipationless)"),
    "flux_quanta_emitted_this_run": emitted,
    "fired": emitted > 0,
    "Phi0_Wb": 2.0678e-15,
}
wr("state.json", state)

if emitted:                          # log each SFQ pulse as a file
    pd = os.path.join(HERE, "sfq-pulses"); os.makedirs(pd, exist_ok=True)
    n0 = len(glob.glob(os.path.join(pd, "*.flux")))
    for k in range(emitted):
        with open(os.path.join(pd, "pulse_%05d.flux" % (n0 + k)), "w") as f:
            f.write("Single Flux Quantum\nPhi0 = h/2e = 2.0678e-15 Wb\none 2-pi phase slip across the dot\n")

print(json.dumps(state, indent=2))
print("  ->  %d SFQ pulse(s) emitted   (%s)" % (emitted, "FIRING" if emitted else "silent"))
