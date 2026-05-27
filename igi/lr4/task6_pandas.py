"""
Purpose: Data analysis using Pandas library: Series, DataFrame, and statistics.
Lab Work: 4
Version: 1.0
Developer: Ivan Safonau
Date: 2026-04-07
"""

import pandas as pd
import os
from exceptions_validators import InvalidStudentDataError

class DataProcessor:
    """Base class for data handling."""
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset {file_path} not found.")
        self._df = pd.read_csv(file_path)

    @property
    def dataframe(self):
        """Getter for the main DataFrame."""
        return self._df


class StrokeAnalyzer(DataProcessor):
    """Class to analyze stroke prediction data."""

    def demonstrate_series_logic(self):
        """Task A: Working with Series and manual element addition."""
        print("\n--- Task A: Pandas Series & DataFrame Structures ---")
        
        # 3. Creating Series from column
        avg_glucose_series = self._df['avg_glucose_level']
        
        # 4. Display functionality (using pandas display style via print)
        print("Original Series Head:")
        print(avg_glucose_series.head())

        # 5. Accessing elements using .iloc and .loc
        print(f"\nElement at index 0 (iloc): {avg_glucose_series.iloc[0]}")
        
        # Calculating median and adding it as a new element with index 'median'
        median_val = avg_glucose_series.median()
        
        # Important: Pandas Series are immutable in length during direct assignment by label if not exist
        # We create a new series or use .loc to append
        avg_glucose_series_updated = pd.concat([avg_glucose_series, pd.Series([median_val], index=['median'])])
        
        print(f"\nAdded element (loc['median']): {avg_glucose_series_updated.loc['median']}")
        return avg_glucose_series_updated

    def perform_statistical_analysis(self):
        """Task B: Statistical analysis and comparison."""
        print("\n--- Task B: Statistical Analysis ---")
        
        # Information about dataframe
        print("\nDataframe Info:")
        self._df.info()

        # Calculation: How many times higher is avg glucose for stroke vs no stroke
        # avg_glucose_level where stroke == 1
        mean_stroke = self._df[self._df['stroke'] == 1]['avg_glucose_level'].mean()
        # avg_glucose_level where stroke == 0
        mean_no_stroke = self._df[self._df['stroke'] == 0]['avg_glucose_level'].mean()

        ratio = mean_stroke / mean_no_stroke
        
        print(f"\nMean glucose (Stroke):    {mean_stroke:.2f}")
        print(f"Mean glucose (No Stroke): {mean_no_stroke:.2f}")
        print(f"Ratio: {ratio:.2f}")
        
        return round(ratio, 2)

    def __str__(self):
        """Magic method for object description."""
        return f"StrokeAnalyzer: {len(self._df)} records loaded."