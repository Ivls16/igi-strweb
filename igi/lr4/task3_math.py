"""
Purpose: Taylor series expansion for arccos(x), statistics, and plotting.
Lab Work: 4
Version: 1.0
Developer: Ivan Safonau
Date: 2026-04-07
"""

import math
import statistics
import matplotlib.pyplot as plt
import numpy as np
from exceptions_validators import InvalidStudentDataError

class StatsMixin:
    """Mixin for calculating statistical parameters of a sequence."""
    def calculate_stats(self, data: list):
        if not data:
            return {}
        
        mean_val = sum(data) / len(data)
        median_val = statistics.median(data)
        try:
            mode_val = statistics.mode(data)
        except statistics.StatisticsError:
            mode_val = data[0]
            
        variance_val = statistics.variance(data) if len(data) > 1 else 0
        stdev_val = math.sqrt(variance_val)
        
        return {
            "Mean": mean_val,
            "Median": median_val,
            "Mode": mode_val,
            "Variance": variance_val,
            "StDev": stdev_val
        }

class MathFunction:
    """Base class for mathematical functions."""
    FUNCTION_TYPE = "Trigonometric Approximation"

    def __init__(self, precision: float = 0.001):
        self._precision = precision

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, value):
        if value <= 0:
            raise InvalidStudentDataError("Precision must be a positive number.")
        self._precision = value

class ArccosTaylor(MathFunction, StatsMixin):
    """Class to calculate arccos(x) using Taylor series expansion."""
    
    def __init__(self, precision: float = 0.001):
        super().__init__(precision)
        self.last_sequence = []

    def calculate(self, x: float):
        if abs(x) > 1:
            raise InvalidStudentDataError("|x| must be <= 1")

        result_sum = 0
        term = x
        n = 0
        self.last_sequence = []

        while abs(term) > self.precision:
            self.last_sequence.append(term)
            result_sum += term
            multiplier = ((2 * n + 1)**2 * x**2) / ((2 * n + 2) * (2 * n + 3))
            term *= multiplier
            n += 1
            if n > 1000: break

        final_val = (math.pi / 2) - result_sum
        return final_val, n

    def __call__(self, x: float):
        return self.calculate(x)

    def plot_comparison(self, start: float, end: float, filename: str = "plot.png"):
        x_vals = np.linspace(start, end, 50)
        taylor_y = []
        math_y = [math.acos(xv) for xv in x_vals]

        for xv in x_vals:
            val, _ = self.calculate(xv)
            taylor_y.append(val)

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, taylor_y, 'r--', label='Taylor Series', linewidth=2)
        plt.plot(x_vals, math_y, 'b-', label='math.acos()', alpha=0.5)
        
        plt.axhline(0, color='black', lw=1)
        plt.axvline(0, color='black', lw=1)
        plt.title(f"Arccos(x) Approximation (eps={self.precision})")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True, linestyle=':')
        
        mid_idx = len(x_vals) // 2
        x_annotate = x_vals[mid_idx]
        y_annotate = taylor_y[mid_idx]
        
        plt.annotate(
            f'Taylor(eps={self.precision})',
            xy=(x_annotate, y_annotate),
            xytext=(x_annotate + 0.3, y_annotate + 0.5),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='green'),
            fontsize=10,
            color='green'
        )

        plt.savefig(filename)
        print(f"[INFO] Plot saved to {filename}")
        plt.show()