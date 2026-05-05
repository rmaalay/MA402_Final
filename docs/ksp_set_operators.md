# KSP.setOperators

## Python Method
```python
ksp.setOperators(A)
```

## Calls C Function
KSPSetOperators

## Source

C implementation:  
https://gitlab.com/petsc/petsc/-/blob/main/src/ksp/ksp/interface/itfunc.c  

Header:  
https://gitlab.com/petsc/petsc/-/blob/main/include/petscksp.h  

---

## Description

Associates a matrix with the PETSc Krylov solver.

---

## Parameters

- `A` : PETSc.Mat  
  Sparse matrix defining the linear system  

---

## Returns

None — modifies the solver in place

---

## Mathematical Meaning

Specifies the operator in the system:

\[
Ax = b
\]

The solver uses this matrix to:
- compute residuals \(r = b - Ax\)
- perform matrix-vector products
- run iterative methods like Conjugate Gradient

---

## Example

```python
from petsc4py import PETSc

A = PETSc.Mat().createAIJ([2,2])
A.setUp()

ksp = PETSc.KSP().create()
ksp.setOperators(A)
```
