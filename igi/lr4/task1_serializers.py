"""
Purpose: Serialization modules (CSV and Pickle) using polymorphism.
Lab Work: 4
Version: 1.0
Developer: Ivan Safonau
Date: 2026-04-07
"""

import csv
import pickle
from task1_models import Student

class BaseSerializer:
    """Base class for serializers."""
    def save(self, filepath: str, students: list):
        raise NotImplementedError("Must be overridden in child class.")

    def load(self, filepath: str) -> list:
        raise NotImplementedError("Must be overridden in child class.")


class CSVSerializer(BaseSerializer):
    """Polymorphic class for CSV serialization."""
    def save(self, filepath: str, students: list):
        """Saves a list of Student objects to a CSV file."""
        with open(filepath, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["surname_initials", "day", "month", "year"])
            writer.writeheader()
            for student in students:
                writer.writerow(student.to_dict())

    def load(self, filepath: str) -> list:
        """Loads a list of Student objects from a CSV file."""
        students = []
        try:
            with open(filepath, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    student = Student(
                        surname_initials=row["surname_initials"],
                        day=int(row["day"]),
                        month=int(row["month"]),
                        year=int(row["year"])
                    )
                    students.append(student)
        except FileNotFoundError:
            pass 
        return students


class PickleSerializer(BaseSerializer):
    """Polymorphic class for Pickle serialization."""
    def save(self, filepath: str, students: list):
        """Saves a list of Student objects to a binary file using pickle."""
        data_to_save = [student.to_dict() for student in students]
        with open(filepath, 'wb') as f:
            pickle.dump(data_to_save, f)

    def load(self, filepath: str) -> list:
        """Loads a list of Student objects from a binary pickle file."""
        students = []
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                for row in data:
                    student = Student(**row)
                    students.append(student)
        except FileNotFoundError:
            pass
        return students