"""OpenCASCADE shape wrappers for CadQuery.

This module provides Python wrappers around OpenCASCADE topology classes,
offering a more Pythonic interface for working with 3D shapes.
"""

from typing import Optional, Tuple, List, Union, Iterator
from OCC.Core.TopoDS import (
    TopoDS_Shape,
    TopoDS_Vertex,
    TopoDS_Edge,
    TopoDS_Wire,
    TopoDS_Face,
    TopoDS_Shell,
    TopoDS_Solid,
    TopoDS_Compound,
)
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace,
)
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeSphere,
    BRepPrimAPI_MakeCylinder,
)
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import (
    TopAbs_VERTEX,
    TopAbs_EDGE,
    TopAbs_FACE,
    TopAbs_SOLID,
    TopAbs_SHELL,
)
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add

from .geom import Vector


class Shape:
    """Base class for all CadQuery shapes wrapping OCC TopoDS_Shape."""

    def __init__(self, obj: TopoDS_Shape):
        self._shape = obj

    @property
    def wrapped(self) -> TopoDS_Shape:
        """Return the underlying OCC shape object."""
        return self._shape

    def is_null(self) -> bool:
        """Return True if the shape is null/empty."""
        return self._shape.IsNull()

    def bounding_box(self) -> Tuple[Vector, Vector]:
        """Return the axis-aligned bounding box as (min_corner, max_corner)."""
        bbox = Bnd_Box()
        brepbndlib_Add(self._shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        return Vector(xmin, ymin, zmin), Vector(xmax, ymax, zmax)

    def center(self) -> Vector:
        """Return the center of the bounding box."""
        lo, hi = self.bounding_box()
        return (lo + hi) * 0.5

    def volume(self) -> float:
        """Return the volume of the shape (0 for non-solid shapes)."""
        props = GProp_GProps()
        brepgprop_VolumeProperties(self._shape, props)
        return props.Mass()

    def area(self) -> float:
        """Return the surface area of the shape."""
        props = GProp_GProps()
        brepgprop_SurfaceProperties(self._shape, props)
        return props.Mass()

    def vertices(self) -> List["Vertex"]:
        """Return all vertices of the shape."""
        explorer = TopExp_Explorer(self._shape, TopAbs_VERTEX)
        result = []
        while explorer.More():
            result.append(Vertex(explorer.Current()))
            explorer.Next()
        return result

    def edges(self) -> List["Edge"]:
        """Return all edges of the shape."""
        explorer = TopExp_Explorer(self._shape, TopAbs_EDGE)
        result = []
        while explorer.More():
            result.append(Edge(explorer.Current()))
            explorer.Next()
        return result

    def faces(self) -> List["Face"]:
        """Return all faces of the shape."""
        explorer = TopExp_Explorer(self._shape, TopAbs_FACE)
        result = []
        while explorer.More():
            result.append(Face(explorer.Current()))
            explorer.Next()
        return result

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Vertex(Shape):
    """A topological vertex (point in 3D space)."""

    @classmethod
    def make_vertex(cls, x: float, y: float, z: float) -> "Vertex":
        """Create a vertex at the given coordinates."""
        builder = BRepBuilderAPI_MakeVertex(gp_Pnt(x, y, z))
        return cls(builder.Vertex())


class Edge(Shape):
    """A topological edge (curve bounded by two vertices)."""
    pass


class Face(Shape):
    """A topological face (surface bounded by edges)."""
    pass


class Solid(Shape):
    """A topological solid (closed 3D volume)."""

    @classmethod
    def make_box(
        cls,
        length: float,
        width: float,
        height: float,
        pnt: Optional[Vector] = None,
    ) -> "Solid":
        """Create a box solid with the given dimensions.

        Args:
            length: Length along X axis.
            width: Width along Y axis.
            height: Height along Z axis.
            pnt: Optional origin point (defaults to origin).
        """
        origin = pnt or Vector(0, 0, 0)
        builder = BRepPrimAPI_MakeBox(
            gp_Pnt(origin.x, origin.y, origin.z), length, width, height
        )
        return cls(builder.Shape())

    @classmethod
    def make_sphere(cls, radius: float, pnt: Optional[Vector] = None) -> "Solid":
        """Create a sphere solid with the given radius."""
        origin = pnt or Vector(0, 0, 0)
        builder = BRepPrimAPI_MakeSphere(
            gp_Pnt(origin.x, origin.y, origin.z), radius
        )
        return cls(builder.Shape())

    @classmethod
    def make_cylinder(
        cls,
        radius: float,
        height: float,
        pnt: Optional[Vector] = None,
        axis: Optional[Vector] = None,
    ) -> "Solid":
        """Create a cylinder solid with the given radius and height."""
        origin = pnt or Vector(0, 0, 0)
        direction = axis or Vector(0, 0, 1)
        ax = gp_Ax2(
            gp_Pnt(origin.x, origin.y, origin.z),
            gp_Dir(direction.x, direction.y, direction.z),
        )
        builder = BRepPrimAPI_MakeCylinder(ax, radius, height)
        return cls(builder.Shape())
