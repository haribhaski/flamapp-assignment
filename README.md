# FlamAPP Assignment

## Recovering Unknown Parameters from a Parametric Curve

### 1. What is this assignment about?

In this assignment, we are given a set of `(x, y)` points stored in `xy_data.csv`.

These points were generated from a mathematical curve, but some of the curve parameters were hidden.

The goal is to recover the unknown values:

* θ (theta)
* M
* X

using only the observed points and the given curve equation. The assignment description asks us to estimate these unknown parameters from the provided data. 

---

## 2. Understanding the Curve

The curve is defined by two equations:

```text
x(t) = t*cos(θ) - e^(M|t|)*sin(0.3t)*sin(θ) + X

y(t) = 42 + t*sin(θ) + e^(M|t|)*sin(0.3t)*cos(θ)
```

At first glance this looks complicated, but it can be understood in three parts:

### θ (Theta)

Theta controls the rotation of the curve.

If theta changes, the entire curve tilts in a different direction.

---

### M

The exponential term contains M:

```text
e^(M|t|)
```

This controls whether the oscillations grow or shrink as `t` increases.

* Positive M → oscillations grow
* Negative M → oscillations decay
* M near zero → oscillations stay roughly constant

---

### X

X simply shifts the curve horizontally.

Increasing X moves everything to the right.

Decreasing X moves everything to the left.

### A Useful Observation

The equations can also be viewed from a geometric perspective.

If we define:

u(t) = t

v(t) = e^(M|t|) sin(0.3t)

then the curve becomes:

x - X = u cos(θ) - v sin(θ)

y - 42 = u sin(θ) + v cos(θ)

This is exactly the form of a 2D rotation matrix.

In other words, the curve can be interpreted as a base signal `(u,v)` that is rotated by an angle θ and then shifted horizontally by X.

Recognizing this structure was useful because it showed that θ acts globally on the entire curve, while t acts locally on individual points. This observation naturally led to the nested optimization approach used later in the project.

---

## 3. First Step: Explore the Data

Before attempting any optimization, I inspected the dataset.

The purpose of this step was:

* Verify the file loads correctly
* Check the number of points
* Look for missing values
* Visualize the overall shape of the curve

This is handled in `main.py`, which loads the dataset, prints basic statistics, and saves a scatter plot of the raw data.  

Generated outputs:

```text
results/
├── data_summary.txt
└── original_signal.png
```

---

## 4. Initial Idea

My first thought was:

> If the parameter t ranges from 6 to 60, perhaps the observed points are evenly spaced in t.

Using this assumption, I generated:

```python
t = np.linspace(6, 60, len(data))
```

and compared the generated curve with the observed points.

Although the overall shape looked reasonable, the fit was not accurate.

The curve matched the trend but did not correctly align with many of the observed points.

This suggested that the data points were not necessarily sampled at evenly spaced values of t.

---

## 5. Main Insight

The important realization was:

> The dataset gives us x and y values, but it never tells us which value of t produced each point.

This means that t is effectively unknown for every observation.

Instead of forcing:

```text
Point 1 → t1
Point 2 → t2
Point 3 → t3
```

using evenly spaced values,

I allowed the algorithm to find the best t value for every observed point.

This became the key idea behind the solution.

Instead of treating t as a known quantity, the problem was reformulated as a parameter estimation task where θ, M and X are global variables, while t is recovered separately for each observed point. This reduced the dimensionality of the outer optimization problem and allowed the optimizer to focus only on the three unknown parameters requested in the assignment.

---

## 6. Optimization Strategy

The optimization was performed in two levels.

### Outer Optimization

The outer optimizer searched for:

```text
θ
M
X
```

within the assignment limits. 

I used Differential Evolution because:

* It does not require gradients
* It performs well on non-linear problems
* It is less likely to get trapped in local minima

The implementation can be found in `solve.py`. 

---

### Inner Optimization

For every observed point:

```text
(x_i, y_i)
```

I searched for the value of t that produced the closest point on the curve.

This was done using a bounded one-dimensional optimization over:

```text
6 ≤ t ≤ 60
```

The implementation uses `minimize_scalar`. 

This creates a nested optimization structure:

```text
Outer:
    Find θ, M, X

Inner:
    Find best t for each point
```

---

## 7. Refinement Step

After Differential Evolution found a good solution, I used Nelder-Mead as a local optimization method to further improve the parameter estimates. 

The purpose of this step was to fine-tune the parameters after the global search had already identified a promising region.

---

## 8. Outputs Generated

The program generates:

```text
results/
├── data_summary.txt
├── original_signal.png
├── final_result.txt
└── fitted_curve.png
```

The fitted curve plot overlays:

* Observed data points
* Predicted curve

allowing a visual comparison of the fit. 

---

## 9. Why I Trust the Result

Several observations increase confidence that the recovered parameters are correct.

1. The predicted curve visually overlaps the observed data over the full range of points.

2. The final optimization loss is extremely small, indicating that the generated curve closely matches the provided dataset.

3. Differential Evolution and Nelder-Mead converge to nearly the same region of the parameter space. This suggests the solution is stable rather than being an artifact of a single optimization run.

4. The recovered parameters are remarkably close to simple round values:

   - θ ≈ 30°
   - M ≈ 0.03
   - X ≈ 55

   Combined with the very small residual error, this strongly suggests that these are the true generating parameters rather than arbitrary values found by chance.

Taken together, the visual fit, low residual error, and convergence behaviour provide strong evidence that the recovered parameters accurately describe the original curve.
---

## 10. Limitations

Although the fit is very accurate, there are still a few limitations worth noting.

1. The optimization is computationally expensive because every evaluation of the objective function requires multiple inner searches to recover the best t value for each observed point.

2. Some correlation exists between θ and X. Small changes in the rotation angle can sometimes be partially compensated by horizontal translation, making these parameters slightly coupled during optimization.

3. The parameter M controls the exponential envelope:

   e^(M|t|)

   Because this term grows with increasing t, the later portions of the curve have a stronger influence on estimating M than the earlier portions. As a result, noise in the high-t region could affect the estimate more strongly.

4. If the dataset were significantly noisier or contained fewer points, parameter recovery would become more difficult and uncertainty would increase.

These limitations are common in inverse parameter estimation problems and should be considered when applying the same methodology to real-world data.
---

## 11. Possible Improvements

If more time were available, I would explore:

* Confidence intervals for the parameters
* Bootstrap resampling
* Faster nearest-point search methods
* Alternative optimizers such as Least Squares
* Parallelization of the inner optimization loop

---

## 12. How to Run

```bash
pip install -r requirements.txt

python main.py
python solve.py
```

Dependencies used:

```text
numpy
pandas
matplotlib
scipy
```
