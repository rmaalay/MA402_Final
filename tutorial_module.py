from __future__ import annotations

import sys
from dataclasses import dataclass

import numpy as np
import petsc4py

petsc4py.init(sys.argv)
from petsc4py import PETSc


@dataclass
class SolverResult:
    x: PETSc.Vec
    u_exact: PETSc.Vec
    b: PETSc.Vec
    A: PETSc.Mat
    error_norm: float
    iterations: int
    converged_reason: int


class Poisson2DKSPSolver:
    def __init__(self, m: int = 20, n: int = 20):
        self.m = m
        self.n = n
        self.N = m * n

    def _idx(self, i, j):
        return i * self.n + j

    def assemble_matrix(self):
        A = PETSc.Mat().createAIJ([self.N, self.N], nnz=5)
        A.setUp()

        rstart, rend = A.getOwnershipRange()

        for row in range(rstart, rend):
            i = row // self.n
            j = row % self.n

            cols = [row]
            vals = [4.0]

            if i > 0:
                cols.append(self._idx(i - 1, j))
                vals.append(-1.0)
            if i < self.m - 1:
                cols.append(self._idx(i + 1, j))
                vals.append(-1.0)
            if j > 0:
                cols.append(self._idx(i, j - 1))
                vals.append(-1.0)
            if j < self.n - 1:
                cols.append(self._idx(i, j + 1))
                vals.append(-1.0)

            A.setValues(row, cols, vals)

        A.assemblyBegin()
        A.assemblyEnd()

        return A

    def create_vectors(self, A):
        b, x = A.createVecs()
        u = x.duplicate()

        u.set(1.0)
        x.set(0.0)

        A.mult(u, b)

        return u, b, x

    def setup_ksp(self, A):
        ksp = PETSc.KSP().create()
        ksp.setOperators(A)
        ksp.setType("cg")
        ksp.getPC().setType("jacobi")
        return ksp

    def solve(self):
        A = self.assemble_matrix()
        u, b, x = self.create_vectors(A)
        ksp = self.setup_ksp(A)

        ksp.solve(b, x)

        err = x.copy()
        err.axpy(-1.0, u)
        error_norm = err.norm()

        return SolverResult(
            x=x,
            u_exact=u,
            b=b,
            A=A,
            error_norm=float(error_norm),
            iterations=ksp.getIterationNumber(),
            converged_reason=ksp.getConvergedReason(),
        )

    def solution_as_grid(self, x):
        arr = x.getArray()
        return np.array(arr).reshape((self.m, self.n))


if __name__ == "__main__":
    solver = Poisson2DKSPSolver(20, 20)
    result = solver.solve()

    if PETSc.COMM_WORLD.getRank() == 0:
        print("Grid size:", solver.m, "x", solver.n)
        print("Unknowns:", solver.N)
        print("Iterations:", result.iterations)
        print("Error:", result.error_norm)