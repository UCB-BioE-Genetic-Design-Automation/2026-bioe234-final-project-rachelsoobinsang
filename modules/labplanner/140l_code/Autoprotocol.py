from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict

# Derived Types as String Extensions
@dataclass(frozen=True)
class Aliquot(str):
    """ 
    Represents an Autoprotocol container and a well index, formatted as 'container/well'.
    Example: 'growth_plate/A1' where 'growth_plate' is the container reference, and 'A1' is the well index.
    """

@dataclass(frozen=True)
class Container(str):
    """ 
    An Autoprotocol container referenced in the refs section of the protocol, represented as a string.
    Example: 'growth_plate' where 'growth_plate' is a unique identifier for a specific container.
    """

@dataclass(frozen=True)
class Quantity(str):
    """ 
    Represents a value with a unit, formatted as 'magnitude:unit', e.g., '5:microliters'.
    Example: '50:microliter' represents a volume of 50 microliters.
    """


# Enums
class StoreWhere(Enum):
    """
    The StoreWhere enum represents various predefined storage conditions.
    Each enum value corresponds to a specific temperature setting used for storing biological samples or chemicals.
    """
    COLD_80 = "cold_80"  # Storage at -80 degrees Celsius.
    COLD_20 = "cold_20"  # Storage at -20 degrees Celsius.
    COLD_4 = "cold_4"    # Storage at 4 degrees Celsius.
    AMBIENT = "ambient"  # Storage at room temperature.
    WARM_30 = "warm_30"  # Storage at 30 degrees Celsius.
    WARM_37 = "warm_37"  # Storage at 37 degrees Celsius (typical for incubation).

class CoverType(Enum):
    """
    The CoverType enum represents different types of covers that can be used for containers.
    This includes standard covers and specialized ones like low evaporation covers.
    """
    STANDARD = "standard"      # Standard type of container cover.
    LOW_EVIPO = "low_evipo"    # Low evaporation cover type.



# Base Classes
@dataclass(frozen=True)
class Ref:
    """
    Represents a reference to a container within a protocol. 
    It can reference an existing container or specify a new one to be created.
    It also includes details on how the container should be stored, whether it should be discarded, 
    and what type of cover it should have.
    """
    id: Optional[str]                  # Identifier for an existing container.
    new: Optional[str]                 # Type of a new container to be created.
    store: Optional[StoreWhere]        # Storage location for the container.
    discard: Optional[bool]            # Whether to discard the container after use.
    cover: Optional[CoverType]         # Type of cover for the container.

    def as_dict(self):
        return {k: (v.value if isinstance(v, Enum) else v) for k, v in self.__dict__.items() if v is not None}

@dataclass(frozen=True)
class Protocol:
    """
    Defines the structure of a complete experimental protocol.
    It includes references to containers (`refs`), a list of instructions to be executed, 
    and any constraints that apply to the execution of those instructions.
    """
    refs: Dict[str, Ref]                # Dictionary of container references.
    instructions: List['Instruction']   # List of instructions to be performed.
    constraints: Optional[List['Constraint']]  # Constraints on how instructions should be performed.

    def as_dict(self):
        return {"refs": {k: v.as_dict() for k, v in self.refs.items()},
                "instructions": [instr.as_dict() for instr in self.instructions],
                "constraints": [constr.as_dict() for constr in self.constraints] if self.constraints else None}

@dataclass(frozen=True)
class Instruction:
    """
    Represents a single instruction within a protocol.
    Each instruction has an operation type (`op`) which defines its nature.
    """
    op: str  # Name of the operation.

    def as_dict(self):
        return {"op": self.op}
