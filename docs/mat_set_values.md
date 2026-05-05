# Mat.setValues

## Python Method
```python
A.setValues(row, cols, values)
```

## Calls C Function
MatSetValues

## Source

C implementation:  
https://gitlab.com/petsc/petsc/-/blob/main/src/mat/interface/matrix.c  

Header:  
https://gitlab.com/petsc/petsc/-/blob/main/include/petscmat.h  

---

## Description

Inserts or adds values into a PETSc sparse matrix.

---

## Parameters

- `row` : int  
  Row index where values are inserted  

- `cols` : list[int]  
  Column indices  

- `values` : list[float]  
  Values to insert into the matrix  

---

## Returns

None — modifies the matrix in place

---

## Mathematical Meaning

Defines entries of the matrix \(A\) in the system:

\[
Ax = b
\]

In this project, it builds the finite-difference stencil:

\[
(Ax)_{i,j} = 4x_{i,j} - x_{i-1,j} - x_{i+1,j} - x_{i,j-1} - x_{i,j+1}
\]

Each call to `setValues` inserts one row of this stencil into the matrix.

---

## Example

```python
from petsc4py import PETSc

A = PETSc.Mat().createAIJ([5,5])
A.setUp()

A.setValues(2, [1,2,3], [-1.0, 2.0, -1.0])

A.assemblyBegin()
A.assemblyEnd()
```
