"""Geometry primitives and transformations for CadQuery.

This module provides core geometric types including vectors, matrices,
planes, and transformation utilities built on top of OCC (Open CASCADE).
"""

from typing import Optional, Tuple, Union
import math

from OCC.Core.gp import (
    gp_Vec,
    gp_Pnt,
    gp_Dir,
    gp_Ax1,
    gp_Ax2,
    gp_Ax3,
    gp_Trsf,
    gp_GTrsf,
    gp_XYZ,
)
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform

VectorLike = Union["Vector", Tuple[float, float, float]]

# Tolerance used for near-zero checks (e.g. normalization, comparisons).
# Lowered from 1e-10 to 1e-12 for higher precision work.
_ZERO_TOL = 1e-12


class Vector:
    """A 3D vector with common geometric operations.

    Wraps OCC's gp_Vec for use throughout CadQuery.
    """

    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Vector):
                self._wrapped = gp_Vec(arg.x, arg.y, arg.z)
            elif isinstance(arg, (tuple, list)) and len(arg) == 3:
                self._wrapped = gp_Vec(*arg)
            elif isinstance(arg, gp_Vec):
                self._wrapped = arg
            elif isinstance(arg, gp_Pnt):
                self._wrapped = gp_Vec(arg.X(), arg.Y(), arg.Z())
            elif isinstance(arg, gp_Dir):
                self._wrapped = gp_Vec(arg.X(), arg.Y(), arg.Z())
            else:
                raise TypeError(f"Cannot create Vector from {type(arg)}")
        elif len(args) == 2:
            self._wrapped = gp_Vec(args[0], args[1], 0.0)
        elif len(args) == 3:
            self._wrapped = gp_Vec(*args)
        else:
            raise TypeError(f"Vector expects 1-3 arguments, got {len(args)}")

    @property
    def x(self) -> float:
        return self._wrapped.X()

    @property
    def y(self) -> float:
        return self._wrapped.Y()

    @property
    def z(self) -> float:
        return self._wrapped.Z()

    def length(self) -> float:
        """Return the magnitude of this vector."""
        return self._wrapped.Magnitude()

    def normalized(self) -> "Vector":
        """Return a unit vector in the same direction."""
        mag = self.length()
        if mag < _ZERO_TOL:
            raise ValueError("Cannot normalize a zero-length vector")
        return Vector(self.x / mag, self.y / mag, self.z / mag)

    def dot(self, other: "Vector") -> float:
        """Dot product with another vector."""
        return self._wrapped.Dot(other._wrapped)

    def cross(self, other: "Vector") -> "Vector":
        """Cross product with another vector."""
        return Vector(self._wrapped.Crossed(other._wrapped))

    def add(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Added(other._wrapped))

    def sub(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Subtracted(other._wrapped))

    def multiply(self, scale: float) -> "Vector":
        return Vector(self._wrapped.Multiplied(scale))

    def __repr__(self) -> str:
        """Return a readable string representation of this vector."""
        return f"Vector({self.x}, {self.y}, {self.z})"
