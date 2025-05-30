#!/usr/bin/env python3
"""
connection_curvature.py

Compute Christoffel symbols, Riemann tensor, Ricci tensor, and Ricci scalar
for a warp-bubble metric ansatz, and export to LaTeX.
"""

import sympy as sp
from sympy import Function, symbols

# Define coordinates and profile function
t, r, theta, phi = symbols('t r theta phi')
f = Function('f')(r, t)

# Hardcoded metric ansatz line element
metric_line = r"ds^2 = -\,dt^2 + \bigl[1 - f(r,t)\bigr]\\,dr^2 + r^2\\,d\theta^2 + r^2\sin^2(\theta)\\,d\phi^2"

# Construct the metric tensor
g = sp.diag(
    -1,
    1 - f,
    r**2,
    r**2 * sp.sin(theta)**2
)

coords = (t, r, theta, phi)
g_inv = g.inv()

# Compute Christoffel symbols Γ^k_{ij}
Gamma = [[[sp.simplify(
    sp.Rational(1, 2) * sum(
        g_inv[k, m] * (
            sp.diff(g[m, j], coords[i])
            + sp.diff(g[m, i], coords[j])
            - sp.diff(g[i, j], coords[m])
        )
        for m in range(4)
    )
) for j in range(4)] for i in range(4)] for k in range(4)]

# Compute Riemann tensor R^i_{ j k l }
Riemann = [[[[sp.simplify(
    sp.diff(Gamma[i][j][l], coords[k])
    - sp.diff(Gamma[i][j][k], coords[l])
    + sum(
        Gamma[s][j][l] * Gamma[i][s][k]
        - Gamma[s][j][k] * Gamma[i][s][l]
        for s in range(4)
    )
) for l in range(4)] for k in range(4)] for j in range(4)] for i in range(4)]

# Compute Ricci tensor R_{ij} and Ricci scalar R
Ricci = [[sp.simplify(
    sum(Riemann[k][i][k][j] for k in range(4))
) for j in range(4)] for i in range(4)]
R_scalar = sp.simplify(
    sum(g_inv[i, j] * Ricci[i][j] for i in range(4) for j in range(4))
)

# Compute Ricci tensor contraction R_{μν}R^{μν}
Ricci_contraction = sp.simplify(
    sum(g_inv[i, k] * g_inv[j, l] * Ricci[i][j] * Ricci[k][l] 
        for i in range(4) for j in range(4) for k in range(4) for l in range(4))
)

# Export results to LaTeX
with open("connection_curvature.tex", "w") as texfile:
    texfile.write(r"\documentclass{article}\usepackage{amsmath}\begin{document}")
    texfile.write(r"\n\n\section*{Metric Definition}\n")
    texfile.write(r"\[")
    texfile.write(metric_line)
    texfile.write(r"\]\n\n")

    texfile.write(r"\section*{Christoffel Symbols}\n")
    texfile.write(r"\[")
    texfile.write(sp.latex(sp.Matrix(Gamma)))
    texfile.write(r"\]\n\n")

    texfile.write(r"\section*{Riemann Tensor}\n")
    texfile.write(r"\[")
    texfile.write(sp.latex(sp.Matrix(Riemann)))
    texfile.write(r"\]\n\n")

    texfile.write(r"\section*{Ricci Tensor}\n")
    texfile.write(r"\[")
    texfile.write(sp.latex(Ricci))
    texfile.write(r"\]\n\n")

    texfile.write(r"\section*{Ricci Scalar}\n")
    texfile.write(r"\[")
    texfile.write(sp.latex(R_scalar))
    texfile.write(r"\]\n\n")

    texfile.write(r"\section*{Ricci Tensor Contraction}\n")
    texfile.write(r"\[")
    texfile.write("R_{\\mu\\nu}R^{\\mu\\nu} = " + sp.latex(Ricci_contraction))
    texfile.write(r"\]\n\n")

    texfile.write(r"\end{document}")
