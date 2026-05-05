# KSP.setOperators

Python:
ksp.setOperators(A)

Calls C function:
KSPSetOperators

Source:
https://gitlab.com/petsc/petsc/-/blob/main/src/ksp/ksp/interface/itfunc.c

Description:
Assigns matrix A to the solver.

Mathematical Meaning:
Defines the operator in Ax = b.