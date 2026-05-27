"""
Purpose: Researching NumPy capabilities: arrays, indexing, and statistics.
Lab Work: 4
Version: 1.0
Developer: Ivan Safonau
Date: 2026-04-07
"""

import numpy as np
from exceptions_validators import InvalidStudentDataError

class NumpyAnalyzer:
    """Class to explore NumPy array operations and statistics."""

    def __init__(self, n: int, m: int):
        if n <= 0 or m <= 0:
            raise InvalidStudentDataError("Matrix dimensions must be positive.")
        self.n = n
        self.m = m
        # Create integer matrix A[n,m] with random numbers (0 to 100)
        self.matrix = np.random.randint(0, 101, size=(n, m))

    def demonstrate_basics(self):
        """Showcases array creation and indexing (Requirements a1-a3)."""
        print("\n--- NumPy Basics Demonstration ---")
        
        # 1. array() creation
        simple_arr = np.array([1, 2, 3])
        print(f"Created via array(): {simple_arr}")
        
        # 2. Specific types of arrays
        zeros = np.zeros((2, 2))
        ones = np.ones((2, 2))
        print(f"Zeros:\n{zeros}\nOnes:\n{ones}")

        # 3. Indexing and Slicing
        print(f"Original Matrix (first 2 rows):\n{self.matrix[:2, :]}")
        if self.n > 1 and self.m > 1:
            print(f"Element at [1,1]: {self.matrix[1, 1]}")
            print(f"Slice (middle part):\n{self.matrix[0:2, 0:2]}")

    def demonstrate_operations(self):
        """Showcases element-wise functions (Requirement a4)."""
        print("\n--- Universal Functions (ufuncs) ---")
        sq_matrix = np.square(self.matrix[:2, :2]) # Element-wise square
        print(f"Square of first 2x2 elements:\n{sq_matrix}")
        
    def calculate_statistics(self):
        """General statistical operations (Requirement b1-b5)."""
        data = self.matrix.flatten()
        stats = {
            "Mean": np.mean(data),
            "Median": np.median(data),
            "Variance": np.var(data),
            "Std Deviation": np.std(data)
        }
        return stats

    def perform_variant_task(self):
        """Individual variant: even/odd counts and correlation."""
        flat = self.matrix.flatten()
        
        evens = flat[flat % 2 == 0]
        odds = flat[flat % 2 != 0]
        
        count_even = len(evens)
        count_odd = len(odds)
        
        # Correlation requires two arrays of same length
        # We take the minimum length to find correlation between existing sequences
        min_len = min(count_even, count_odd)
        if min_len > 1:
            corr_matrix = np.corrcoef(evens[:min_len], odds[:min_len])
            correlation = corr_matrix[0, 1]
        else:
            correlation = 0.0

        return count_even, count_odd, correlation

    def __str__(self):
        return f"NumpyAnalyzer with {self.n}x{self.m} matrix."