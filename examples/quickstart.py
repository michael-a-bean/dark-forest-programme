"""Minimal example: run MultiField for 100 sessions and print assemblage count.

This is the substrate underlying all five papers. A 20x20 grid of nodes
with 3 energy hotspots, Hebbian learning, and locality-biased encounters.

Usage:
    python examples/quickstart.py
"""

import sys
sys.path.insert(0, ".")

from src.substrate.multifield import MultiField

# Create the substrate with default parameters
mf = MultiField(
    grid_size=20,       # 20x20 = 400 nodes
    n_hotspots=3,       # 3 energy sources drive spatially varying noise
    hotspot_energy=0.3,
    hotspot_radius=0.2,
    base_noise=0.02,
    eta=0.05,           # Hebbian learning rate
    lam=0.002,          # Multiplicative weight decay per step
    w_max=1.0,          # Hard weight clip boundary
    encounter_rate=20,  # New edges created per step (locality-biased)
    locality=0.10,      # Spatial scale of encounter locality
    prune_threshold=1e-4,  # Remove edges below this weight
    seed=42,
)

# Run 100 sessions of 300 steps each
for session in range(1, 101):
    for _ in range(300):
        mf.step()

    if session % 20 == 0:
        asm = mf.find_assemblages()
        c = mf.census()
        print(
            f"Session {session:3d}: "
            f"{len(asm)} assemblages, "
            f"{c['n_edges']} edges, "
            f"mean_w={c['mean_weight']:.4f}"
        )

# Final assemblage details
asm = mf.find_assemblages()
print(f"\nFinal: {len(asm)} assemblages")
for i, nodes in enumerate(asm):
    print(f"  Assemblage {i}: {len(nodes)} nodes")
