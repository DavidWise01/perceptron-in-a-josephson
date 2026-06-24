# The Virtual Junction — a Josephson junction built from folders

```
        electrode-left/   <        the-dot/  •        >   electrode-right/
        (a superconductor)     (the weak link)            (a superconductor)
```

A real Josephson junction is **two superconductors joined at a weak link**. That is, structurally,
the ROOT0 **J-Junction primitive** `<•` — two arms meeting at a single witnessed dot. So this junction
is built the honest way: out of folders.

- **`electrode-left/`** and **`electrode-right/`** — the two superconducting arms. Each `psi.json`
  holds the macroscopic phase of that electrode's Cooper-pair condensate.
- **`the-dot/`** — the witnessed dot **`•`**, the weak link. It holds the coupling (`coupling.json`:
  the critical current `Ic`) and the junction's single dynamical variable, the **phase difference φ**
  (`phase.json`). The phase lives *at the dot*, because the junction *is* the dot.
- **`bias.json`** — the drive current `I_bias` (and the timestep).

## Run it

```
python evolve.py [steps]     # step the junction by the real Josephson relations
python observe.py            # read the state without evolving
```

`evolve.py` integrates the overdamped RSJ model:

```
I_s   = Ic · sin(φ)             # DC Josephson relation — supercurrent set by the phase
dφ    = (I_bias − I_s) · dt     # RSJ — the phase winds under bias
```

- If **`I_bias < Ic`** the phase is **trapped** in a washboard well: zero voltage, a perfect
  dissipationless **supercurrent**. The junction is silent.
- If **`I_bias > Ic`** the phase **runs downhill**, and every time it slips through **2π** one
  **flux quantum** `Φ₀ = h/2e = 2.0678e-15 Wb` passes through the dot — an **SFQ pulse**. Each pulse
  is written as a file in `sfq-pulses/`. *That is the neuron firing.*

Set `I_bias` in `bias.json` below `Ic` (silent) or above it (firing) and watch `sfq-pulses/` fill.

## Why folders

The filesystem makes the junction's structure literal: two condensates you can open, a dot that holds
the phase, and firing you can *count as files*. It is the smallest honest model of `<•` — and the
doorway to the quantum version, where the phase φ at the dot becomes a quantum operator and the
junction becomes a **transmon qubit**.

— governor David Lee Wise · ROOT0 · the perceptron's seventh body
