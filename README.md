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

## Files in This Project

## Main Usage

Example usage of the Python module:

```python
from tutorial_module import Poisson2DKSPSolver

solver = Poisson2DKSPSolver(m=20, n=20)
result = solver.solve()

print(result.error_norm)
```

tutorial_module.py  
Contains the full PETSc solver implementation.

tutorial_presentation.ipynb  
A notebook that runs the solver, prints results, and visualizes the solution.

docs/  
Contains documentation for three mapped PETSc functions:

- mat_set_values.md  
- ksp_set_operators.md  
- ksp_solve.md  

Each documentation file includes:

- Python method  
- Underlying C function  
- C source link (GitLab)  
- Mathematical explanation  
- Parameters and return values  
- Example usage  

---

## Source-Mapped Functions

### 1. Mat.setValues

Python:
A.setValues(row, cols, values)

Calls C function:
MatSetValues

Purpose:
Adds entries into the sparse matrix A.

---

### 2. KSP.setOperators

Python:
ksp.setOperators(A)

Calls C function:
KSPSetOperators

Purpose:
Attaches the matrix A to the solver so PETSc knows which system to solve.

---

### 3. KSP.solve

Python:
ksp.solve(b, x)

Calls C function:
KSPSolve

Purpose:
Solves the linear system:

A x = b

---

## How to Run

Install dependencies:

pip install petsc petsc4py numpy matplotlib

Run the Python script:

python tutorial_module.py

Run the notebook:

jupyter notebook tutorial_presentation.ipynb

---

## Expected Output

A typical run should print something like:

Grid size: 20 x 20  
Number of unknowns: 400  
KSP converged reason: 2  
KSP iterations: 5  
2-norm error ||x-u||_2: 1.23e-12  

The exact iteration count may vary depending on solver settings.

---

## References

PETSc Tutorial:  
https://petsc.org/main/src/ksp/ksp/tutorials/ex2.c.html  

PETSc GitLab Repository:  
https://gitlab.com/petsc/petsc  

petsc4py Documentation:  
https://petsc.org/release/petsc4py/  

MatSetValues:  
https://petsc.org/main/manualpages/Mat/MatSetValues/  

KSPSetOperators:  
https://petsc.org/main/manualpages/KSP/KSPSetOperators/  

KSPSolve:  
https://petsc.org/main/manualpages/KSP/KSPSolve/  
