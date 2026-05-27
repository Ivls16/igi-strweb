"""
Purpose: Abstract geometry classes and isosceles trapezoid visualization.
Lab Work: 4
Version: 1.0
Developer: Ivan Safonau
Date: 2026-04-07
"""

from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from exceptions_validators import InvalidStudentDataError

class FigureColor:
    """Class to manage figure color using properties."""
    def __init__(self, color_name: str):
        self._color = color_name

    @property
    def color(self) -> str:
        """Getter for color."""
        return self._color

    @color.setter
    def color(self, value: str):
        """Setter for color."""
        if not value:
            raise InvalidStudentDataError("Color cannot be empty.")
        self._color = value


class GeometricFigure(ABC):
    """Abstract base class for all geometric figures."""
    
    @abstractmethod
    def calculate_area(self) -> float:
        """Abstract method to calculate area."""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Abstract method to get string info."""
        pass


class IsoscelesTrapezoid(GeometricFigure):
    """Class representing an isosceles trapezoid."""
    
    # Static attribute for figure name
    FIGURE_NAME = "Isosceles Trapezoid"

    def __init__(self, h: float, a: float, b: float, color: str):
        """
        Constructor.
        h - height
        a - one base
        b - middle line
        color - color name (e.g., 'blue', 'red')
        """
        if h <= 0 or a <= 0 or b <= 0:
            raise InvalidStudentDataError("Parameters must be positive.")
        
        c = 2 * b - a
        if c <= 0:
            raise InvalidStudentDataError("Invalid middle line: second base would be <= 0.")

        self.h = h
        self.a = a 
        self.c = c 
        self.b = b 
        
        self.figure_color = FigureColor(color)

    def calculate_area(self) -> float:
        """Area = middle_line * height."""
        return self.b * self.h

    def get_name(self) -> str:
        """Returns class-level figure name."""
        return self.FIGURE_NAME

    def get_info(self) -> str:
        """Returns formatted string info using .format()."""
        info_template = (
            "Figure: {name}\n"
            "Color: {color}\n"
            "Parameters: h={h:.2f}, base1(a)={a:.2f}, base2(c)={c:.2f}, middle_line(b)={b:.2f}\n"
            "Area: {area:.2f}"
        )
        return info_template.format(
            name=self.get_name(),
            color=self.figure_color.color,
            h=self.h,
            a=self.a,
            c=self.c,
            b=self.b,
            area=self.calculate_area()
        )

    def draw(self, label_text: str, save_path: str = "trapezoid.png"):
        """Visualizes the trapezoid using matplotlib."""
        fig, ax = plt.subplots()
        
        points = [
            [-self.c / 2, 0],          
            [self.c / 2, 0],           
            [self.a / 2, self.h],      
            [-self.a / 2, self.h]     
        ]
        
        polygon = patches.Polygon(
            points, 
            closed=True, 
            facecolor=self.figure_color.color, 
            edgecolor='black',
            label=self.get_name()
        )
        
        ax.add_patch(polygon)
        
        plt.text(0, self.h / 2, label_text, ha='center', va='center', fontweight='bold')
        
        max_dim = max(self.a, self.c, self.h)
        ax.set_xlim(-max_dim, max_dim)
        ax.set_ylim(-0.5, max_dim + 1)
        ax.set_aspect('equal')
        
        plt.title(f"Drawing of {self.get_name()}")
        plt.grid(True, linestyle='--')
        
        plt.savefig(save_path)
        print(f"[INFO] Figure saved to {save_path}")
        plt.show()