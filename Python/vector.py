from copy import copy
from collections.abc import Iterable
from types import UnionType
from typing import Self
import numpy as np

from utils import INF


class Field:
    def __init__(self, field: type | UnionType, zero=0, unit=1):
        """
        @param field: any Field
        @param zero:
        @param unit:
        """
        self._field = field
        self._0 = zero
        self._1 = unit

    @property
    def zero(self):
        return self._0

    @property
    def unit(self):
        return self._1

    def is_in(self, n):
        return isinstance(n, self._field)

    def __eq__(self, other):
        return self._field == other._field


class VectorSpace:
    def __init__(self, field: Field, n):
        self._dimension = n
        self._field = field
        self._vector = self.Vector3 if n == 3 else self.Vector

    @property
    def field(self):
        return self._field

    @property
    def dimension(self):
        return self._dimension

    def __eq__(self, other):
        return self.field == other.field and self.dimension == other.dimension

    class Vector:
        """
        This class is a Vector as defined in linear algebra, however in this class we assume the first position of the
        Vector to be 0.
        """

        def __init__(self, vector_space, v: Iterable):
            """
            Creates a new Vector from the origin to v.
            @param v: A point.
            """
            self._v = list(v)
            self._vs = vector_space

        def __copy__(self):
            """
            @return: A shallow copy of the vector.
            """
            return self._vs.create_vector(*copy(self._v))

        def __getitem__(self, key: int | slice):
            """
            @param key: The position in the Vector, starting from 0 and ending on len - 1.
            @return: The element at the key.
            """
            if isinstance(key, int):
                return self._v[key]
            else:
                v = self._v[key]
                vs = VectorSpace(self._vs.field, len(v))
                return vs.create_vector(*self._v[key])

        def __setitem__(self, key: int, value) -> None:
            """
            The Vector will be redimensioned if the dimention is out of range, so if you want to use it many times in
            heigher dimensions you should redimension the vector first.<br>
            @param key: The position in the Vector, starting from 0 and ending on len - 1.
            @param value: The value to insert at the position.
            """
            self._v[key] = value

        def __iadd__(self, w):
            """
            Add this Vector with w.<br>
            @param w: A Vector.
            @return: The adition of this Vector with w.
            """
            self._verify_vector_space(w)
            return self._op(self, w, op=lambda x, y, i: x._v[i] + y._v[i])

        def __add__(self, w):
            """
            Add this Vector with w.<br>
            This Vector and w are not changed in this method.<br>
            @param w: A Vector.
            @return: The addition of this Vector with w.
            """
            self._verify_vector_space(w)
            return self._op(copy(self), w, op=lambda x, y, i: x._v[i] + y._v[i])

        def __isub__(self, w):
            """
            Subtract this Vector with w.<br>
            @param w: A Vector.
            @return: The subtraction of this Vector with w.
            """
            self._verify_vector_space(w)
            return self._op(self, w, op=lambda x, y, i: x._v[i] - y._v[i])

        def __sub__(self, w):
            """
            Subtract this Vector with w.<br>
            This Vector and w are not changed in this method.<br>
            @param w: A Vector.
            @return: The subtraction of this Vector with w.
            """
            self._verify_vector_space(w)
            return self._op(copy(self), w, op=lambda x, y, i: x._v[i] - y._v[i])

        def __neg__(self):
            """
            This Vector remains unchanged.<br>
            @return: The additive inverse of this Vector.
            """
            return (-self._vs.field.unit) * self

        def __imul__(self, scalar):
            """
            @param scalar: A scalar.
            @return: The product of this Vector by the scalar.
            """
            return self._op(self, scalar, op=lambda x, y, i: x._v[i] * y)

        def __mul__(self, scalar):
            """
            This Vector remains unchanged.<br>
            @param scalar: A scalar.
            @return: The product of this Vector by the scalar.
            """
            if not self._vs.field.is_in(scalar):
                raise Exception("The scalar must be in the field where the vector space was declared.")
            return self._op(copy(self), scalar, op=lambda x, y, i: x._v[i] * y)

        def __rmul__(self, scalar):
            """
            This Vector remains unchanged.<br>
            @param scalar: A scalar.
            @return: The product of the scalar by this Vector.
            """
            return self * scalar

        def __matmul__(self, w) -> int:
            """
            This Vector remains unchanged.<br>
            @param w: A vector.
            @return: The internal product of this Vector by w.
            """
            self._verify_vector_space(w)
            return self._op_sum(self, w, op=lambda x, y, i: x._v[i] * y._v[i])

        def __len__(self) -> int:
            """
            @return: The length of this Vector.
            """
            return self._vs.dimension

        def dim(self) -> tuple[int]:
            """
            @return: A tuple with the dimension of this Vector.
            """
            return len(self),

        def __abs__(self):
            """
            @return: The distance of this Vector to the origin.
            """
            return self.norm()

        def __eq__(self, b):
            """
            Two Vectors are equal if their elements at the same dimension are equal.<br>
            @param b: A Vector.
            @return: Whether this Vector is equal to b.
            """
            if len(self) != len(b):
                return False

            for i in range(len(self)):
                if self._v[i] != b._v[i]:
                    return False
            return True

        def __gt__(self, b):
            """
            A Vector is greater than another Vector if its norm is greater than the other.<br>
            @param b: A Vector.
            @return: Whether this Vector is greater than b.
            """
            return abs(self) > abs(b)

        def __lt__(self, b):
            """
            A Vector is lesser than another Vector if its norm is lesser than the other.<br>
            @param b: A Vector.
            @return: Whether this Vector is lesser than b.
            """
            return abs(self) < abs(b)

        def __ge__(self, b):
            """
            @param b: A Vector.
            @return: Whether this Vector is greater or equal to b.
            """
            return abs(self) > abs(b) or self == b

        def __le__(self, b):
            """
            @param b: A Vector.
            @return: Whether this Vector is lesser or equal to b.
            """
            return abs(self) < abs(b) or self == b

        def __bool__(self):
            """
            @return: False if the vector is null, otherwise, True.
            """
            return bool(len(self))

        def __str__(self):
            return str(tuple(self))

        def __repr__(self):
            return str(self)

        def __iter__(self):
            return iter(self._v)

        def sin(self, w=None):
            """
            If w is None it is assumed to be the sum of all the canonical vectors of dimension n, but the last dimension.
            @param w: A Vector.
            @return: The sine of the angle between this Vector and w.
            """
            if w is None:
                w = self._vs.create_vector_equal_components(self._vs.field.unit)
                w[-1] = self._vs.field.zero
            return 1 - np.power(self.cos(w), 2)

        def cos(self, w=None):
            """
            If w is None it is assumed to be the sum of all the canonical vectors of dimension n, but the last dimension.
            @param w: A Vector.
            @return: The cosine of the angle between this Vector and w.
            """
            if w is None:
                w = self._vs.create_vector_equal_components(self._vs.field.unit)
                w[-1] = self._vs.field.zero
            return (self @ w) / (abs(self) * abs(w))

        def ang(self, w=None):
            """
            If w is None it is assumed to be the sum of all the canonical vectors of dimension n, but the last dimension.
            @param w: A Vector.
            @return: The angle between this Vector and w.
            """
            if w is None:
                w = self._vs.create_vector_equal_components(self._vs.field.unit)
                w[-1] = self._vs.field.zero
            return np.arccos(self.cos(w))

        def unit(self):
            """
            @return: The unit Vector of this Vector. Or, if this Vector is null, a copy of this Vector.
            """
            return self * (1 / abs(self))

        def proj(self, w: Self = None) -> Self:
            """
            If w is None it is assumed to be the sum of all the canonical vectors of dimension n, but the last dimension.
            @param w: The Vector where to project to.
            @return: The projection of this Vector in w.
            """
            if w is None:
                w = self._vs.create_vector_equal_components(self._vs.field.unit)
                w[-1] = self._vs.field.zero
            return w * ((self @ w) / np.power(abs(w), 2))

        def redimension(self, vector_space):
            """
            Let n be the dimension of the vector_space.
            If n is greater than the length of the Vector this method fills the Vector to the nth dimension,
            completing the new dimensions with zero.<br>

            Otherwise, the result is the projection of the Vector to the nth dimension.
            @param vector_space: The vector space of the new Vector.
            @return: The redimensioned Vector.
            """
            dif = vector_space.dimension - len(self)
            if dif < 0:
                return self.__init__(self._vs, self[:vector_space.dimension])
            return vector_space.create_vector(*(list(self) + [vector_space.field.zero] * dif))

        def norm(self, p=2):
            """
            If you want the INFINITY-norm of the vector let p = INF.<br>
            @param p: The value of p.
            @return: The p-norm of the Vector.
            """
            if p is INF:
                return max(self._v)
            return np.power(self._op_sum(self, p, op=lambda x, y, i: np.power(x._v[i], y)), 1 / p)

        @classmethod
        def _op(cls, v, w, *, op):
            for i in range(len(v)):
                v._v[i] = op(v, w, i)
            return v

        @classmethod
        def _op_sum(cls, v, w, *, op) -> int:
            s = 0
            for i in range(len(v)):
                s += op(v, w, i)
            return s

        def _verify_vector_space(self, w):
            if self._vs != w._vs:
                raise Exception('The vectors must be of the same vector space to be operated')

    class Vector3(Vector):
        def __init__(self, vector_space, v):
            super().__init__(vector_space, v)

        def __xor__(self, w: Self) -> Self:
            self._verify_vector_space(w)
            x, y, z = (self._det_2([[self[1], self[2]], [w[1], w[2]]]),
                       -self._det_2([[self[0], self[2]], [w[0], w[2]]]),
                       self._det_2([[self[0], self[1]], [w[0], w[1]]]))
            return self._vs.create_vector(x, y, z)

        @classmethod
        def _det_2(cls, m: list[list]):
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    def create_vector(self, *v, w: Iterable = None) -> Vector | Vector3:
        """
        Creates a new Vector from the point V to W.
        @param v: A point.
        @param w: Another point.
        """
        if len(v) != self.dimension:
            raise Exception("The vector must be of the same dimension as its space.")
        v = self._vector(self, v)
        if w is not None:
            v -= self.create_vector(*w)
        return v

    def create_vector_angles(self, size, *angles):
        """
        Create a Vector with the angles.
        @param size:
        @param angles: The angles in relation to each canonical Vector of this Vector's dimension, you can miss the last
        angle.
        @return: The Vector.
        """
        if len(angles) < self.dimension - 1:
            raise Exception(f"There should be at least {self.dimension - 1} angles. Recieved {len(angles)}.")

        a = [(size * np.cos(angle)) for angle in angles]
        if len(angles) == self.dimension:
            return self.create_vector(*a)

        v = self.create_vector(*a, 0)
        a.insert(len(v) - 1, np.sqrt(np.power(size, 2) - np.power(v.norm(), 2)))
        return self.create_vector(*a)

    def create_vector_equal_components(self, component):
        """
        Creates a Vector in the nth dimension with the same component.
        @param component: The component of the vector.
        @return: A Vector with the same component in the nth dimension.
        """
        return self._vector(self, [component] * self._dimension)

    def create_vector_null(self):
        """
        @return: The null vector of this vector space.
        """
        return self.create_vector_equal_components(self.field.zero)

    def create_vector_canonical_base(self, key: int):
        """
        Get a canonical base with unit at key and with dimension n.
        @param key: The position to insert the unit, starting from 0 and ending on n - 1.
        @return: The canonical base.
        """

        v = self.create_vector_null()
        v[key] = self.field.unit
        return v
