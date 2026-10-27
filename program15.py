from abc import ABC, abstractmethod
import math

class GeometricEntity(ABC):
    """
    An abstract geometric framework (ABC) that enforces mandatory 
    blueprints for mathematical and spatial operations.
    """
    
    @abstractmethod
    def __add__(self, other):
        """Mandatory blueprint for overloading the addition operator."""
        pass

    @abstractmethod
    def __eq__(self, other):
        """Mandatory blueprint for overloading the equality operator."""
        pass

    @abstractmethod
    def __str__(self):
        """Mandatory blueprint for string representation."""
        pass


class Vector(GeometricEntity):
    """
    A concrete subclass representing a 2D vector.
    Implements abstract contracts and overloads magic dunder methods.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Overloads the '+' operator to perform intuitive vector addition."""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise TypeError("Can only add Vector to another Vector.")

    def __eq__(self, other):
        """Overloads the '==' operator to check if two vectors are identical."""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        """Overloads the string representation for intuitive display."""
        return f"Vector({self.x}, {self.y})"


class Circle(GeometricEntity):
    """
    A concrete subclass representing a circle.
    Implements abstract contracts for spatial calculations.
    """
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        """Calculates the spatial area of the circle."""
        return math.pi * (self.radius ** 2)

    def __add__(self, other):
        """
        Overloads the '+' operator to combine circles.
        Creates a new circle whose area is the sum of both circles' areas.
        """
        if isinstance(other, Circle):
            # Calculate new radius based on combined area
            combined_area = self.area() + other.area()
            new_radius = math.sqrt(combined_area / math.pi)
            return Circle(new_radius)
        raise TypeError("Can only add Circle to another Circle.")

    def __eq__(self, other):
        """Overloads the '==' operator to check if two circles have the same radius."""
        if isinstance(other, Circle):
            return math.isclose(self.radius, other.radius, rel_tol=1e-9)
        return False

    def __str__(self):
        """Overloads the string representation for the circle."""
        return f"Circle(radius={self.radius:.2f})"


def main():
    """Main execution function demonstrating operator overloading and ABCs."""
    # Initialize Vector instances
    v1 = Vector(2, 3)
    v2 = Vector(4, 1)
    
    # Demonstrate vector addition and equality
    v3 = v1 + v2
    print(f"{v1} + {v2} = {v3}")
    print(f"v1 == Vector(2, 3): {v1 == Vector(2, 3)}")
    print(f"v1 == v2: {v1 == v2}")
    
    print("-" * 30)
    
    # Initialize Circle instances
    c1 = Circle(3)
    c2 = Circle(4)
    
    # Demonstrate circle addition (combining areas)
    c3 = c1 + c2
    print(f"{c1} + {c2} = {c3}")
    print(f"c1 Area: {c1.area():.2f} | c2 Area: {c2.area():.2f}")
    print(f"Combined Area (c3): {c3.area():.2f}")
    print(f"c3 == Circle(5.0): {c3 == Circle(5.0)}")

if __name__ == "__main__":
    main()