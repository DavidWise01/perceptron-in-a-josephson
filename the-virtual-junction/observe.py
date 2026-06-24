#!/usr/bin/env python3
"""Read the virtual junction's state from the folders (no evolution).   < •"""
import json, os, math, glob

HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: json.load(open(os.path.join(HERE, p), encoding="utf-8"))
L, R = rd("electrode-left/psi.json"), rd("electrode-right/psi.json")
J, ph, B = rd("the-dot/coupling.json"), rd("the-dot/phase.json"), rd("bias.json")

phi = ph["phi"]
Is = J["Ic"] * math.sin(phi)
pulses = len(glob.glob(os.path.join(HERE, "sfq-pulses", "*.flux")))
firing = B["I_bias"] > J["Ic"]

print("   electrode-left   <        the-dot  *        >   electrode-right")
print("   phi_L=%.3f                 phi=%.3f                 phi_R=%.3f" % (L["phase"], phi, R["phase"]))
print("   weak link:  Ic=%s   I_bias=%s   ->  %s" % (
      J["Ic"], B["I_bias"], "FIRING (voltage state)" if firing else "supercurrent (V=0)"))
print("   supercurrent  I_s = Ic*sin(phi) = %.4f" % Is)
print("   total SFQ pulses emitted so far: %d" % pulses)
