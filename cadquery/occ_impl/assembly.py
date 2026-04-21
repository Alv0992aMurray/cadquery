"""Assembly module for combining multiple shapes into a compound structure.

Provides the Assembly class which allows hierarchical composition of shapes
with location transforms and metadata.
"""

from typing import Optional, Dict, List, Tuple, Union
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.gp import gp_Trsf

from .shapes import Shape
from .geom import Vector


class AssemblyError(Exception):
    """Raised when an assembly operation fails."""
    pass


class Assembly:
    """Hierarchical assembly of shapes with optional location transforms.

    An Assembly can contain Shapes and other Assemblies as children,
    each with an optional name and location (transform).

    Example usage::

        assy = Assembly(name="root")
        assy.add(some_shape, name="base", loc=Vector(0, 0, 10))
        assy.add(other_shape, name="top")
        compound = assy.to_compound()
    """

    def __init__(
        self,
        shape: Optional[Shape] = None,
        name: Optional[str] = None,
        loc: Optional[TopLoc_Location] = None,
    ):
        """Initialize an Assembly.

        Args:
            shape: Optional root shape for this assembly node.
            name: Optional name identifier for this assembly.
            loc: Optional location transform applied to this assembly.
        """
        self.name = name or ""
        self.loc = loc or TopLoc_Location()
        self.shape: Optional[Shape] = shape
        self.children: List[Tuple["Assembly", str]] = []
        self._metadata: Dict[str, object] = {}

    def add(
        self,
        item: Union["Assembly", Shape],
        name: Optional[str] = None,
        loc: Optional[TopLoc_Location] = None,
    ) -> "Assembly":
        """Add a child shape or sub-assembly.

        Args:
            item: A Shape or Assembly to add as a child.
            name: Optional name for the child entry.
            loc: Optional location transform for the child.

        Returns:
            self, to allow method chaining.

        Raises:
            AssemblyError: If item is not a Shape or Assembly.
        """
        if isinstance(item, Shape):
            child = Assembly(shape=item, name=name, loc=loc)
        elif isinstance(item, Assembly):
            child = item
            if name:
                child.name = name
            if loc:
                child.loc = loc
        else:
            raise AssemblyError(
                f"Expected Shape or Assembly, got {type(item).__name__}"
            )

        self.children.append((child, child.name))
        return self

    def to_compound(self) -> Shape:
        """Flatten the assembly hierarchy into a single TopoDS_Compound Shape.

        All child shapes are collected recursively and combined into one
        compound, with location transforms applied.

        Returns:
            A Shape wrapping a TopoDS_Compound containing all sub-shapes.
        """
        builder = BRep_Builder()
        compound = TopoDS_Compound()
        builder.MakeCompound(compound)

        self._add_to_compound(builder, compound, self.loc)

        result = Shape(compound)
        return result

    def _add_to_compound(
        self,
        builder: BRep_Builder,
        compound: TopoDS_Compound,
        parent_loc: TopLoc_Location,
    ) -> None:
        """Recursively add shapes to the compound with accumulated transforms."""
        # Compose parent location with this node's location
        combined_loc = parent_loc.Multiplied(self.loc)

        if self.shape is not None and not self.shape.is_null():
            located_shape = self.shape.wrapped.Located(combined_loc)
            builder.Add(compound, located_shape)

        for child, _name in self.children:
            child._add_to_compound(builder, compound, combined_loc)

    def set_metadata(self, key: str, value: object) -> "Assembly":
        """Attach arbitrary metadata to this assembly node.

        Args:
            key: Metadata key string.
            value: Metadata value (any type).

        Returns:
            self, to allow method chaining.
        """
        self._metadata[key] = value
        return self

    def get_metadata(self, key: str) -> Optional[object]:
        """Retrieve metadata by key.

        Args:
            key: Metadata key string.

        Returns:
            The stored value, or None if not found.
        """
        return self._metadata.get(key)

    def __repr__(self) -> str:
        return (
            f"Assembly(name={self.name!r}, "
            f"children={len(self.children)}, "
            f"has_shape={self.shape is not None})"
        )
