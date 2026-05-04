# MA 402 Final Project: Making PETSc C Code Easy to Use in Python

## Project Overview

This project translates a PETSc C tutorial into a working `petsc4py` Python program and documents three Python PETSc methods by tracing them back to their underlying C implementations.

The selected PETSc tutorial is:

**PETSc KSP Tutorial `ex2.c`: Solves a linear system in parallel with KSP**

Original tutorial:

https://petsc.org/main/src/ksp/ksp/tutorials/ex2.c.html

GitLab source:

https://gitlab.com/petsc/petsc/-/blob/main/src/ksp/ksp/tutorials/ex2.c

This project does **not** use the forbidden Bratu/SNES example from the assignment prompt. Instead, it focuses on the PETSc KSP module, which solves sparse linear systems of the form

\[
Ax = b.
\]

The translated Python program builds a sparse 2D finite-difference matrix, creates an exact solution vector, forms the right-hand side, solves the resulting linear system with PETSc's Krylov Subspace Solver interface, and reports the numerical error.

---

## Mathematical Problem

The original PETSc tutorial builds a sparse matrix that resembles a five-point finite-difference stencil on a two-dimensional grid. In this project, the unknowns are arranged on an $m \times n$ grid. Each grid point corresponds to one unknown in the vector $x \in \mathbb{R}^{mn}$.

The linear system is

$$
Ax = b
$$

where $A \in \mathbb{R}^{mn \times mn}$ is a sparse matrix. For an interior grid point, the stencil has the form

$$
(Ax)_{i,j} = 4x_{i,j} - x_{i-1,j} - x_{i+1,j} - x_{i,j-1} - x_{i,j+1}.
$$

This is the standard five-point stencil associated with the two-dimensional discrete Laplacian.

The exact solution is chosen to be

$$
u = \mathbf{1},
$$

the vector of all ones. The right-hand side is then constructed by matrix-vector multiplication:

$$
b = Au.
$$

After PETSc solves

$$
Ax = b,
$$

we compare the computed solution $x$ against the known exact solution $u$. The error is measured using the Euclidean norm:

$$
\|x - u\|_2.
$$

A small value of $\|x - u\|_2$ means PETSc recovered the known exact solution accurately.

## AI Translation Experience

The original PETSc tutorial is written in C and uses PETSc objects such as `Mat`, `Vec`, and `KSP`. The AI-assisted translation converted these objects into their corresponding `petsc4py` interfaces:

| C PETSc concept | Python petsc4py concept |
|---|---|
| `MatCreate`, `MatSetValues`, `MatAssemblyBegin/End` | `PETSc.Mat().createAIJ`, `A.setValues`, `A.assemblyBegin/End` |
| `VecCreate`, `VecSet`, `MatMult` | `A.createVecs`, `u.set`, `A.mult` |
| `KSPCreate`, `KSPSetOperators`, `KSPSolve` | `PETSc.KSP().create`, `ksp.setOperators`, `ksp.solve` |

The AI translation required debugging because PETSc objects must be assembled before they are used, and PETSc vectors must be created with compatible layouts. The final version uses `A.createVecs()` so that the solution and right-hand-side vectors have dimensions matching the matrix.

---

## Files

### `tutorial_module.py`

Contains the working Python solver.

Main class:

```python
Poisson2DKSPSolver
