import os
import circle, square

dimension = float(os.getenv("RADIUS", 1.0))

print(f"Контейнер запущен!")
print(f"Радиус: {dimension}")
print(f"Площадь круга: {circle.area(dimension)}")
print(f"Периметр круга: {circle.perimeter(dimension)}")
print(f"Сторона: {dimension}")
print(f"Площадь квадрата: {square.area(dimension)}")
print(f"Периметр квадрата: {square.perimeter(dimension)}")