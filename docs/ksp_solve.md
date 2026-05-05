# KSP.solve

## Python Method
```python
ksp.solve(b, x)
```

## Calls C Function
KSPSolve

## Source

C implementation:  
https://gitlab.com/petsc/petsc/-/blob/main/src/ksp/ksp/interface/itfunc.c  

Header:  
https://gitlab.com/petsc/petsc/-/blob/main/include/petscksp.h  

---

## Description

Solves a linear system using an iterative Krylov method.

---

## Parameters

- `b` : PETSc.Vec  
  Right-hand side vector  

- `x` : PETSc.Vec  
  Solution vector (modified in place)  

---

## Returns

None — solution is stored in `x`

---

## Mathematical Meaning

Solves:

\[
Ax = b
\]

The solver generates approximations:

\[
x_0, x_1, x_2, \dots
\]

and minimizes the residual:

\[
r_k = b - Ax_k
\]

until convergence.

In this project:

\[
b = Au
\]

so the true solution is:

\[
x = u
\]

We verify accuracy using:

\[
\|x - u\|_2
\]

---

## Example

```python
from petsc4py import PETSc

A = PETSc.Mat().createAIJ([2,2])
A.setUp()

b, x = A.createVecs()

ksp = PETSc.KSP().create()
ksp.setOperators(A)

ksp.solve(b, x)
```
