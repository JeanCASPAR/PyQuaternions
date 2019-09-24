"""A python implementations of quaternions.
/!\ Warning : Something seems doesn't work with divisions"""

import collections
import math
import numbers


class Quaternion(numbers.Number, collections.Iterable):
    """Represent a quaternion, and implements the basics mathematics operations"""
    def __new__(cls, *arg):
        """
        Create a new quaternion
        If there's just one arg, it should provide a __quaternion__ method who return a quaternion
        """
        if len(arg) == 1:
            return arg[0].__quaternion__()
        return object.__new__(cls)
        
    def __init__(self, *coords):
        """
        Initialize a new quaternion
        Leading zeros are not taking in account
        The coords are filled with 0 if necessary
        """
        if not all(map(lambda i: isinstance(i, numbers.Real), coords)):
            raise TypeError("All coords should be real numbers")
        if not all(map(lambda i: i == 0, coords[4:])):
            raise ValueError("Coords other than the 4 first should be equal to zero")
        self._a = coords[0]
        self._b = coords[1]
        self._c = coords[2]
        self._d = coords[3]
    
    
    @property
    def a(self):
        """Return the real composant"""
        return self._a
    
    
    @property
    def b(self):
        """Return the first imaginary composant"""
        return self._b
    
    @property
    def c(self):
        """Return the second imaginary composant"""
        return self._c
    
    @property
    def d(self):
        """Return the third imaginary composant"""
        return self._d
    
    real = a
    
    @property
    def imag(self):
        """Return the imaginary composant"""
        return Quaternion(0, self.b, self.c, self.d)
    
    @property
    def conjugate(self):
        """Return the conjugate of the quaternion"""
        return type(self)(self.a, -self.b, -self.c, -self.d)
    
    @property
    def norm(self):
        """Return the euclidean norm of the quaternion"""
        return math.sqrt(sum(i**2 for i in self))
    
    @property
    def matrix(self):
        """Transpose the quaternion as a matrix"""
        row_1 = [self.a, -self.b, -self.c, -self.d]
        row_2 = [self.b, self.a, -self.d, self.c]
        row_3 = [self.c, self.a, self.d, -self.b]
        row_4 = [self.d, -self.c, self.b, self.a]
        matrix = [row_1, row_2, row_3, row_4]
        return matrix
    
    @property
    def invert(self):
        """
        Return the invert of the quaternion
        Should be equal to 1 / self
        """
        return (1 / self.norm**2) * self.conjugate
    
    def __add__(self, other):
        """
        Return the sum of two quaternions
        If the other is not a quaternion, it's transformed into a quaternion before the operation
        """
        if isinstance(other, type(self)) and not isinstance(other, numbers.Complex):
            return type(self)(*(x + y for x, y in zip(self, other)))
        elif isinstance(other, numbers.Number):
            quaternion = type(self)(other.real, other.imag, 0, 0)
            return self + quaternion
        return NotImplemented

    
    def __sub__(self, other):
        if isinstance(other, type(self)) and not isinstance(other, numbers.Complex):
            return type(self)(*((x - y for x, y in zip(self, other))))
        elif isinstance(other, numbers.Complex):
            quaternion = type(self)(other.real, other.imag, 0, 0)
            return self - quaternion
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, type(self)) and not isinstance(other, numbers.Complex):
            a = self.a*other.a - self.b*other.b - self.c*other.c - self.d*other.d
            b = self.a*other.b + self.b*other.a + self.c*other.d - self.d*other.c
            c = self.a*other.c + self.c*other.a - self.b*other.d + self.d*other.b
            d = self.d*other.a + self.a*other.d + self.b*other.c - self.c*other.b
            return type(self)(a, b, c, d)
        elif isinstance(other, numbers.Complex):
            quaternion = type(self)(other.real, other.imag, 0, 0)
            return self * quaternion
        return NotImplemented
    
    def __rmul__(self, other):
        if isinstance(other, type(self)) and not isinstance(other, numbers.Complex):
            a = other.a*self.a - other.b*self.b - other.c*self.c - other.d*self.d
            b = other.a*self.b + other.b*self.a + other.c*self.d - other.d*self.c
            c = other.a*self.c + other.c*self.a - other.b*self.d + other.d*self.b
            d = other.d*self.a + other.a*self.d + other.b*self.c - other.c*self.b
            return type(self)(a, b, c, d)
        elif isinstance(other, numbers.Complex):
            quaternion = type(self)(other.real, other.imag, 0, 0)
            return self * quaternion
        return NotImplemented
    
    def __truediv__(self, other):
        if isinstance(other, type(self)) and not isinstance(other, numbers.Complex):
            return self * other.invert
        elif isinstance(other, numbers.Complex):
            quaternion = type(self)(other.real, other.imag, 0, 0).invert
            return self * quaternion
        return NotImplemented
    
    def __rtruediv__(self, other):
        if isinstance(other, type(self)) and not isinstance(other, numbers.Complex):
            return other * self.invert
        elif isinstance(other, numbers.Complex):
            quaternion = type(self)(other.real, other.imag, 0, 0).invert
            return quaternion * self.invert
        return NotImplemented
    
    def __pos__(self):
        return self
    
    def __neg__(self):
        return type(self)(-self.a, -self.b, -self.c, -self.d)
    
    def __pow__(self, value):
        if isinstance(value, numbers.Integral):
            result = 1
            for i in range(value):
                result *= self
            return result
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, type(self)) and not isinstance(other, numbers.Complex):
            return all(map(lambda i: i[0] == i[1], zip(self, other)))
        elif isinstance(other, numbers.Complex):
            quaternion = type(self)(other.real, other.imag, 0, 0)
            return self == quaternion
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, type(self)) and not isinstance(other, numbers.Complex):
            return self.norm < other.norm
        elif isinstance(other, numbers.Complex):
            quaternion = type(self)(other.real, other.imag, 0, 0)
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, type(self)) and not isinstance(other, numbers.Complex):
            return self.norm <= other.norm
        elif isinstance(other, numbers.Complex):
            quaternion = type(self)(other.real, other.imag, 0, 0)
        return NotImplemented
    
    def __hash__(self):
        return hash(tuple(self))
    
    def __repr__(self):
        return f"Quaternion({self.a} + {self.b}i + {self.c}j + {self.d}k)"
    
    def __iter__(self):
        return iter((self.a, self.b, self.c, self.d))
    
    def __getitem__(self, key):
        if isinstance(key, numbers.Integral):
            return tuple(self)[key]
        elif isinstance(key, slice):
            return tuple(self)[key]
        return NotImplemented
    
    def __bool__(self):
        return any(map(lambda i: i != 0, self))
    
    def __int__(self):
        return int(self.real)
    
    def __float__(self):
        return float(self.real)
    
    def __complex__(self):
        return complex(self.real, self.b)
    
    def __quaternion__(self):
        return self
        

Quaternion.register(numbers.Complex)
