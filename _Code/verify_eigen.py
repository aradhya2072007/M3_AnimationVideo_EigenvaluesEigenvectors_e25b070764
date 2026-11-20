#!/usr/bin/env python3
"""Verify eigenvalues & eigenvectors with NumPy before rendering."""
import numpy as np

A = np.array([[3, 1], [0, 2]])
v1 = np.array([1, 0])
v2 = np.array([-1, 1])
l1, l2 = 3, 2

print("Matrix A:")
print(A)
print()

# Check 1: A @ v1 == l1 * v1
Av1 = A @ v1
print(f"A @ v1 = {Av1}")
print(f"λ1 * v1 = {l1 * v1}")
assert np.allclose(Av1, l1 * v1), "FAIL: A @ v1 != λ1 * v1"
print("✓ A·v1 = λ1·v1 VERIFIED\n")

# Check 2: A @ v2 == l2 * v2
Av2 = A @ v2
print(f"A @ v2 = {Av2}")
print(f"λ2 * v2 = {l2 * v2}")
assert np.allclose(Av2, l2 * v2), "FAIL: A @ v2 != λ2 * v2"
print("✓ A·v2 = λ2·v2 VERIFIED\n")

# Check 3: eigenvalues via np.linalg.eig
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"NumPy eigenvalues: {eigenvalues}")
print(f"NumPy eigenvectors:\n{eigenvectors}")
assert set(np.round(eigenvalues, 6)) == {2.0, 3.0}, "FAIL: eigenvalues mismatch"
print("\n✓ ALL CHECKS PASSED")
