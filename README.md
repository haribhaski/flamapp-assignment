
# FlamAPP Assignment

Recovered Parameters:

```text
θ = 30°
M = 0.03
X = 55
```

Desmos Form:

```text
(
t*cos(0.523599)
- exp(0.03*abs(t))*sin(0.3*t)*sin(0.523599)
+ 55,

42
+ t*sin(0.523599)
+ exp(0.03*abs(t))*sin(0.3*t)*cos(0.523599)
)
```

Desmos Link: https://www.desmos.com/calculator/j7kzb7yv3s

---

## Problem Statement

The objective of this assignment was to recover the unknown parameters `θ`, `M`, and `X` of a parametric curve using only the provided `(x,y)` samples.

The curve is defined as:

```text
x(t) = t*cos(θ) - e^(M|t|)sin(0.3t)sin(θ) + X

y(t) = 42 + t*sin(θ) + e^(M|t|)sin(0.3t)cos(θ)
```

---

## Initial Exploration

My first step was to inspect the dataset and visualize the raw points.

Files generated:

```text
results/
├── data_summary.txt
└── original_signal.png
```

The visualization immediately showed that the data followed a smooth parametric curve rather than a simple function.

---

## Key Insight

My initial assumption was that the samples were generated using evenly spaced values of `t`.

I tested this using:

```python
t = np.linspace(6, 60, len(data))
```

The overall shape looked correct, but the curve did not align accurately with the observed points.

This led to the key realization:

> The dataset provides only `(x,y)` values and never specifies which value of `t` generated each point.

Therefore, `t` must be treated as an unknown quantity.

---

## Mathematical Interpretation

The equations can be rewritten as:

```text
u(t) = t

v(t) = exp(M|t|)sin(0.3t)
```

which gives:

```text
x - X = u cos(θ) - v sin(θ)

y - 42 = u sin(θ) + v cos(θ)
```

This is the standard form of a 2D rotation matrix.

This observation shows:

* θ controls global rotation
* X controls horizontal translation
* M controls exponential growth/decay of oscillations
* t controls the position of an individual point on the curve

This naturally motivated a nested optimization strategy.

---

## Optimization Approach

### Outer Optimization

The outer optimization searched for:

```text
θ
M
X
```

I used Differential Evolution because it performs well on nonlinear search spaces and is less sensitive to local minima.

---

### Inner Optimization

For every observed point:

```text
(xi, yi)
```

I searched for the value of `t` that produced the closest point on the generated curve.

This was implemented using:

```python
scipy.optimize.minimize_scalar
```

with:

```text
6 ≤ t ≤ 60
```

The optimization structure therefore becomes:

```text
Outer:
    Find θ, M, X

Inner:
    Find best t for each point
```

---

## Refinement

After Differential Evolution identified a good solution region, Nelder-Mead was used to locally refine the parameters.

This improved the final precision of the recovered values.

---

## Results

Recovered parameters:

```text
θ ≈ 30°
M ≈ 0.03
X ≈ 55
```

Generated outputs:

```text
results/
├── final_result.txt
├── fitted_curve.png
├── verification.txt
└── verification_plot.png
```

---

## Independent Verification

To verify the solution independently, I generated a dense version of the recovered curve using 20,000 points and performed a nearest-neighbor search using a KD-tree.

Metrics:

```text
Mean Error ≈ 0.0008
RMSE       ≈ 0.0009
Max Error  ≈ 0.0023
```

The small residual is consistent with discretization of the 20,000-point verification grid rather than meaningful model mismatch.

This provides an independent confirmation of the recovered parameters.

---

## Why I Believe the Solution Is Correct

Several observations support the result:

1. The recovered curve visually overlaps the observed data.
2. The optimization loss is extremely small.
3. Global and local optimizers converge to the same region.
4. The recovered values are extremely close to simple round numbers:

```text
θ = 30°
M = 0.03
X = 55
```

Combined with the near-zero residual error, this strongly suggests that these are the true generating parameters.

---

## Lessons Learned

The biggest lesson from this assignment was that a visually reasonable model is not necessarily the correct model.

My first implementation assumed evenly spaced values of `t`, which produced the correct overall shape but an incorrect fit.

The key breakthrough was realizing that `t` was not provided and needed to be recovered separately for every observation.

Once the problem was reformulated in this way, the parameter recovery became straightforward.

---

## References

- SciPy documentation — `differential_evolution`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html
- SciPy documentation — `minimize` (Nelder-Mead method): https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
- SciPy documentation — `minimize_scalar`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html
- SciPy documentation — `cKDTree`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html
- Storn, R., & Price, K. (1997). Differential Evolution – A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces. *Journal of Global Optimization*, 11, 341–359.

---

## Limitations

* The nested optimization is computationally expensive.
* θ and X exhibit mild correlation during optimization.
* Estimation of M becomes increasingly sensitive at larger values of `t` because of the exponential term.
* Noisy or sparse datasets would increase uncertainty.

---

## Future Improvements

Possible extensions include:

* Bootstrap confidence intervals
* Faster nearest-point search strategies
* Alternative optimizers such as Least Squares
* Parallelization of the inner optimization stage

---

## Running the Project

```bash
pip install -r requirements.txt

python main.py
python solve.py
python verify.py
```

Dependencies:

```text
numpy
pandas
matplotlib
scipy
```
