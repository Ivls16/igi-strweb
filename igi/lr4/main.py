"""
Purpose: Unified entry point for all Lab 4 tasks.
Lab Work: 4
Version: 1.0
Developer: Ivan Safonau
Date: 2026-04-07
"""

import sys, math, os
from exceptions_validators import get_valid_int, get_valid_string
from task1_models import SchoolClass, Student
from task1_serializers import CSVSerializer, PickleSerializer
from task2_analyzer import TextAnalyzer
from task3_math import ArccosTaylor
from task4_shapes import IsoscelesTrapezoid
from task5_numpy import NumpyAnalyzer
from task6_pandas import StrokeAnalyzer

def run_task_1():
    """Logic for Student Management (Serialization)."""
    school_class = SchoolClass()
    print("\n--- Task 1: School Class Manager ---")
    print("1 - CSV Mode | 2 - Pickle Mode")
    fmt = get_valid_int("Choice: ", 1, 2)
    
    serializer = CSVSerializer() if fmt == 1 else PickleSerializer()
    fname = "students.csv" if fmt == 1 else "students.pkl"

    while True:
        print("\n1. Add Dummy Data | 2. Show Sorted | 3. Search | 4. Avg Birthday | 5. Back to Main")
        c = get_valid_int(">> ", 1, 5)
        
        if c == 1:
            data = [{"surname_initials": "Safonau I.", "day": 7, "month": 4, "year": 2005}]
            for d in data: school_class.add_student(Student(**d))
            serializer.save(fname, list(school_class))
            print("Data saved.")
        elif c == 2:
            school_class._students = serializer.load(fname)
            school_class.sort_students()
            for s in school_class: print(s)
        elif c == 3:
            q = get_valid_string("Surname to find: ")
            res = school_class.search_student(q)
            print(res if res else "Not found.")
        elif c == 4:
            print(f"Avg Birthday: {school_class.get_average_birthday()}")
        else: break

def run_task_2():
    """Logic for Text Analysis (Regex & Archives)."""
    print("\n--- Task 2: Regex Text Analyzer ---")
    analyzer = TextAnalyzer()
    
    # Create a dummy file for testing if it doesn't exist
    test_file = "source_text.txt"
    if not os.path.exists(test_file):
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Hello! This is a test. Today is 07/04/2026.")

    try:
        analyzer.read_from_file(test_file)
        print(f"File '{test_file}' loaded.")
        
        # Perform analysis
        analyzer.perform_general_analysis()
        modified_text = analyzer.perform_variant_analysis()
        
        # Save and Archive
        res_file = "analysis_results.txt"
        analyzer.save_results(res_file)
        
        print("\nAnalysis Results:")
        for line in analyzer.results: print(line)
        
        print("\nArchiving results...")
        analyzer.create_zip(res_file, "results.zip")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def run_task_3():
    """Logic for Taylor Series, Stats and Plotting."""
    print("\n--- Task 3: Arccos Taylor Series & Statistics ---")
    eps = 0.0001 # Can be asked from user via get_valid_float if you have one
    calc = ArccosTaylor(eps)
    
    while True:
        print("\n1. Calculate for specific X | 2. Show Table & Plot | 3. Back")
        c = get_valid_int(">> ", 1, 3)
        
        if c == 1:
            try:
                # Use a custom validator or simple input
                x = float(input("Enter x (-1 to 1): "))
                res, n = calc(x)
                math_res = math.acos(x)
                
                print(f"\nResults for x={x}:")
                print(f"Taylor F(x): {res:.6f} (n={n})")
                print(f"Math F(x):   {math_res:.6f}")
                print(f"Difference:  {abs(res - math_res):.6e}")
                
                # Stats (Requirement a)
                stats = calc.calculate_stats(calc.last_sequence)
                print("\nSequence Statistics (Terms of series):")
                for k, v in stats.items():
                    print(f" - {k}: {v:.6f}")
            except Exception as e:
                print(f"Error: {e}")

        elif c == 2:
            # Requirement: Table and Plot
            print(f"{'x':>6} | {'n':>4} | {'F(x)':>10} | {'Math F(x)':>10} | {'eps':>8}")
            print("-" * 50)
            for xv in [-0.8, -0.4, 0, 0.4, 0.8]:
                f_x, n = calc(xv)
                m_x = math.acos(xv)
                print(f"{xv:6.1f} | {n:4d} | {f_x:10.5f} | {m_x:10.5f} | {calc.precision:8.4f}")
            
            calc.plot_comparison(-0.95, 0.95, "arccos_plot.png")
        
        else: break

def run_task_4():
    """Logic for Geometry Shapes (Task 4)."""
    print("\n--- Task 4: Isosceles Trapezoid Builder ---")
    
    try:
        # 1) Input values (Requirement 1)
        h = float(input("Enter height (h): "))
        a = float(input("Enter top base (a): "))
        b = float(input("Enter middle line (b): "))
        color = get_valid_string("Enter color (e.g., 'blue', 'green', 'orange'): ")
        label = get_valid_string("Enter text to put inside the figure: ")

        # 2) Data validation happens inside constructor (Requirement 2)
        trap = IsoscelesTrapezoid(h, a, b, color)

        # 4) Output info to screen (Requirement 4)
        print("\n" + "="*20)
        print(trap.get_info())
        print("="*20)

        # 3) Build, color, label and show/save (Requirement 3 & 4)
        trap.draw(label)

    except ValueError:
        print("Error: Please enter numeric values for dimensions.")
    except Exception as e:
        print(f"Error: {e}")

def run_task_5():
    """Logic for NumPy Research (Task 5)."""
    print("\n--- Task 5: NumPy Operations & Statistics ---")
    
    try:
        n = get_valid_int("Enter number of rows (n): ", 1, 100)
        m = get_valid_int("Enter number of columns (m): ", 1, 100)
        
        analyzer = NumpyAnalyzer(n, m)
        print(f"\nGenerated Matrix:\n{analyzer.matrix}")
        
        # Demonstrate requirements
        analyzer.demonstrate_basics()
        analyzer.demonstrate_operations()
        
        # General stats
        print("\n--- General Statistics ---")
        for key, val in analyzer.calculate_statistics().items():
            print(f"{key}: {val:.4f}")
            
        # Variant Task
        evens, odds, corr = analyzer.perform_variant_task()
        print("\n--- Variant Analysis ---")
        print(f"Even numbers count: {evens}")
        print(f"Odd numbers count:  {odds}")
        print(f"Correlation coefficient (between evens and odds): {corr:.4f}")
        print("(Note: Correlation calculated using equal-sized slices of even/odd sets)")

    except Exception as e:
        print(f"Error: {e}")

def run_task_6():
    """Logic for Pandas Data Analysis (Task 6)."""
    print("\n--- Task 6: Stroke Prediction Data Analysis ---")
    dataset_path = "healthcare-dataset-stroke-data.csv"
    
    try:
        analyzer = StrokeAnalyzer(dataset_path)
        print(analyzer)

        while True:
            print("\n1. Demonstrate Series (Task A)")
            print("2. Perform Statistical Analysis (Task B)")
            print("3. Back to Main Menu")
            c = get_valid_int(">> ", 1, 3)

            if c == 1:
                analyzer.demonstrate_series_logic()
            elif c == 2:
                res = analyzer.perform_statistical_analysis()
                print(f"\n[RESULT] Average glucose level is {res} times higher in stroke patients.")
            else:
                break
                
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please download 'healthcare-dataset-stroke-data.csv' from Kaggle.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    while True:
        print("\n" + "X"*40)
        print("UNIVERSITY LAB 4: MAIN MENU")
        print("X"*40)
        print("1. Task 1: Student Serialization")
        print("2. Task 2: Text Analysis & Regex")
        print("3. Task 3: Taylor Series & Stats")
        print("4. Task 4: Geometry (Trapezoid)")
        print("5. Task 5: NumPy Matrix Research")
        print("6. Task 6: Pandas Data Analysis") 
        print("7. Exit System")
        
        choice = get_valid_int("Select Task: ", 1, 7)
        
        if choice == 1: run_task_1()
        elif choice == 2: run_task_2()
        elif choice == 3: run_task_3()
        elif choice == 4: run_task_4()
        elif choice == 5: run_task_5()
        elif choice == 6: run_task_6()
        else: sys.exit()

if __name__ == "__main__":
    main()