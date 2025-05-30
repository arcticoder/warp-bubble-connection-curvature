# Warp Bubble Connection & Curvature

This repository provides:

- A Python script (`connection_curvature.py`) that:
  1. Loads the warp-bubble metric ansatz from `metric_ansatz.tex` (fetched at runtime).
  2. Defines the symbols and profile function \(f(r,t)\).
  3. Constructs the metric tensor \(g_{\mu\nu}\).
  4. Computes:
     - Christoffel symbols \(\Gamma^\rho_{\mu\nu}\),
     - Riemann tensor \(R^\rho_{\ \sigma\mu\nu}\),
     - Ricci tensor \(R_{\mu\nu}\),
     - Ricci scalar \(R\).
  5. Exports each result in LaTeX form.

- A LaTeX document (`connection_curvature.tex`) that organizes:
  1. The metric definition,
  2. Christoffel symbols,
  3. Riemann tensor (or its nonzero components),
  4. Ricci tensor,
  5. Ricci scalar.

---

## Requirements

- Python 3.7+
- [Sympy](https://www.sympy.org/)  
- [Requests](https://pypi.org/project/requests/)

Install dependencies via:

```bash
pip install sympy requests
```

---

## Usage

1.  **Fetch the metric ansatz**  
    The script will download the metric definition from the upstream repo:
    
```arduino
https://raw.githubusercontent.com/arcticoder/warp-bubble-metric-ansatz/main/metric_ansatz.tex
```
    
2.  **Run the computation**
    
```bash
python connection_curvature.py
```
    
    -   Outputs:
        
        -   `connection_curvature.tex` (LaTeX document)
            
        -   Optionally, intermediate `.tex` files for each tensor (if you modify the script to do so).
            
3.  **Compile the LaTeX**
    
```bash
pdflatex connection_curvature.tex
```
    

---

## File structure

```bash
├── connection_curvature.py    # Main script
├── connection_curvature.tex   # Generated LaTeX document
├── README.md                  # This file
└── LICENSE                    # (optional) choose an open-source license
```

---

## Script outline

**connection\_curvature.py** does the following:

1.  **Imports**
    
```python
import sympy as sp
from sympy import Function, symbols
import requests
```
    
2.  **Define symbols and load metric**
    
```python
t, r, θ, φ = symbols('t r theta phi')
f = Function('f')(r, t)

url = "https://raw.githubusercontent.com/arcticoder/warp-bubble-metric-ansatz/main/metric_ansatz.tex"
tex = requests.get(url).text
# parse out ds^2 line element and build g = sp.Matrix([...])
```
    
3.  **Compute Christoffel symbols**
    
```python
coords = (t, r, θ, φ)
g_inv = g.inv()
Gamma = [[[sp.simplify(
    sp.Rational(1,2)*sum(
      g_inv[k, m] * (
        sp.diff(g[m, j], coords[i])
        + sp.diff(g[m, i], coords[j])
        - sp.diff(g[i, j], coords[m])
      )
      for m in range(4)
    )
  ) for j in range(4)] for i in range(4)] for k in range(4)]
```
    
4.  **Compute Riemann tensor**
    
```python
Riemann = [[[[ sp.simplify(
    sp.diff(Gamma[r][i][j], coords[k])
    - sp.diff(Gamma[r][i][k], coords[j])
    + sum(Gamma[s][i][j]*Gamma[r][s][k]
          - Gamma[s][i][k]*Gamma[r][s][j]
          for s in range(4))
  ) for l in range(4)] for k in range(4)] for j in range(4)] for i in range(4)]
```
    
5.  **Compute Ricci tensor & scalar**
    
```python
Ricci = sp.simplify(sum(Riemann[k][i][k][j] for k in range(4)))
R_scalar = sp.simplify(sum(g_inv[i,j] * Ricci[i,j]
                            for i in range(4) for j in range(4)))
```
    
6.  **Export to LaTeX**
    
```python
with open("connection_curvature.tex", "w") as f:
    f.write(r"\documentclass{article}\usepackage{amsmath}\begin{document}")
    # Section 1: Metric
    f.write(r"\section*{Metric}\[")
    f.write(metric_line_element)
    f.write(r"\]")
    # Section 2: Christoffel symbols
    f.write(r"\section*{Christoffel Symbols}")
    f.write(sp.latex(sp.Matrix(Gamma)))
    # Section 3–5 similarly...
    f.write(r"\end{document}")
```
  
