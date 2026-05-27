"""
Purpose: Object-Oriented models representing a student and a school class.
Lab Work: 4
Version: 1.0
Developer: Ivan Safonau
Date: 2026-04-07
"""

from exceptions_validators import InvalidStudentDataError

class DictMixin:
    """A mixin to provide conversion between object and dictionary."""
    def to_dict(self) -> dict:
        """
        Returns only public-facing property names to stay compatible with CSV fieldnames.
        """
        return {
            "surname_initials": self.surname_initials,
            "day": self.day,
            "month": self.month,
            "year": self.year
        }


class Person:
    """Base class representing a general person."""
    def __init__(self, surname_initials: str):
        self._surname_initials = None
        self.surname_initials = surname_initials

    @property
    def surname_initials(self) -> str:
        """Getter for surname and initials."""
        return self._surname_initials

    @surname_initials.setter
    def surname_initials(self, value: str):
        """Setter for surname and initials with validation."""
        if not value or len(value.strip()) < 2:
            raise InvalidStudentDataError("Surname and initials cannot be empty.")
        self._surname_initials = value.strip()


class Student(Person, DictMixin):
    """Derived class representing a student. Uses multiple inheritance (Mixin)."""
    
    def __init__(self, surname_initials: str, day: int, month: int, year: int):
        super().__init__(surname_initials)
        self.day = day
        self.month = month
        self.year = year

    @property
    def day(self) -> int:
        return self._day

    @day.setter
    def day(self, value: int):
        if not (1 <= value <= 31):
            raise InvalidStudentDataError("Day must be between 1 and 31.")
        self._day = value

    @property
    def month(self) -> int:
        return self._month

    @month.setter
    def month(self, value: int):
        if not (1 <= value <= 12):
            raise InvalidStudentDataError("Month must be between 1 and 12.")
        self._month = value

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int):
        if not (1900 <= value <= 2100):
            raise InvalidStudentDataError("Year must be realistic (1900-2100).")
        self._year = value

    def __str__(self) -> str:
        return f"Student: {self.surname_initials} | DOB: {self.day:02d}.{self.month:02d}.{self.year}"

    def __lt__(self, other) -> bool:
        """Polymorphism via magic method for sorting by surname."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.surname_initials < other.surname_initials


class SchoolClass:
    """Class representing a collection of students."""
    total_school_classes_created = 0

    def __init__(self):
        self._students = []
        SchoolClass.total_school_classes_created += 1

    def add_student(self, student: Student):
        """Adds a student object to the class."""
        self._students.append(student)

    def search_student(self, surname: str) -> Student:
        """Searches for a student by exact surname and initials."""
        for student in self._students:
            if student.surname_initials.lower() == surname.lower():
                return student
        return None

    def sort_students(self):
        """Sorts students (uses Student.__lt__ magic method)."""
        self._students.sort()

    def get_average_birthday(self) -> tuple:
        """Calculates the class average birthday (day, month, year)."""
        if not self._students:
            return 0, 0, 0
        
        avg_d = sum(s.day for s in self._students) / len(self._students)
        avg_m = sum(s.month for s in self._students) / len(self._students)
        avg_y = sum(s.year for s in self._students) / len(self._students)
        
        return round(avg_d), round(avg_m), round(avg_y)

    def __iter__(self):
        """Allows iterating over the SchoolClass object."""
        return iter(self._students)