"""CadQuery - A parametric 3D CAD scripting framework.

CadQuery is an intuitive, easy-to-use Python module for building parametric
3D CAD models. It is similar to OpenSCAD, but uses Python instead of a
specialized scripting language.

CadQuery has several goals:

* Build models with scripts that are as close as possible to how you would
  describe the object to a human.
* Create parametric models that can be easily customized by end users.
* Output high quality CAD formats such as STEP and DXF in addition to STL.
* Provide a clean, easy-to-use API with good documentation.

Example usage::

    import cadquery as cq

    # Create a simple box
    result = cq.Workplane("XY").box(1, 2, 3)

    # Export to STEP
    result.val().exportStep("box.step")
"""

from .cq import CQ, Workplane  # noqa: F401
from .occ_impl.geom import Vector, Matrix, Plane, BoundBox  # noqa: F401
from .occ_impl.shapes import (
    Shape,
    Vertex,
    Edge,
    Wire,
    Face,
    Shell,
    Solid,
    Compound,
)  # noqa: F401
from .assembly import Assembly, Constraint  # noqa: F401
from .sketch import Sketch  # noqa: F401
from .selectors import (  # noqa: F401
    NearestToPointSelector,
    ParallelDirSelector,
    DirectionSelector,
    PerpendicularDirSelector,
    TypeSelector,
    DirectionMinMaxSelector,
    CenterNthSelector,
    RadiusNthSelector,
    LengthNthSelector,
    DirectionNthSelector,
    AndSelector,
    SumSelector,
    SubtractSelector,
    InverseSelector,
    StringSyntaxSelector,
)
from .cq_types import Real  # noqa: F401

__version__ = "2.4.0"
__author__ = "CadQuery Contributors"
__license__ = "Apache Public License 2.0"

__all__ = [
    # Core classes
    "CQ",
    "Workplane",
    # Geometry primitives
    "Vector",
    "Matrix",
    "Plane",
    "BoundBox",
    # Shape classes
    "Shape",
    "Vertex",
    "Edge",
    "Wire",
    "Face",
    "Shell",
    "Solid",
    "Compound",
    # Assembly
    "Assembly",
    "Constraint",
    # Sketch
    "Sketch",
    # Selectors
    "NearestToPointSelector",
    "ParallelDirSelector",
    "DirectionSelector",
    "PerpendicularDirSelector",
    "TypeSelector",
    "DirectionMinMaxSelector",
    "CenterNthSelector",
    "RadiusNthSelector",
    "LengthNthSelector",
    "DirectionNthSelector",
    "AndSelector",
    "SumSelector",
    "SubtractSelector",
    "InverseSelector",
    "StringSyntaxSelector",
    # Types
    "Real",
    # Metadata
    "__version__",
    "__author__",
    "__license__",
]
