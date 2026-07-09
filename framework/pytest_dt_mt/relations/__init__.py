from typing import Type
from .base import MetamorphicRelation
from .monotonicity import MonotonicityRelation
from .invariance import InvarianceRelation
from .conservation import ConservationRelation
from .stability import StabilityRelation
from .proportionality import ProportionalityRelation
from .substitution import SubstitutionRelation

RELATION_MAP = {
    "monotonicity": MonotonicityRelation,
    "invariance": InvarianceRelation,
    "conservation": ConservationRelation,
    "stability": StabilityRelation,
    "proportionality": ProportionalityRelation,
    "substitution": SubstitutionRelation,
}

def get_relation_class(name: str) -> Type[MetamorphicRelation]:
    cls = RELATION_MAP.get(name)
    if not cls:
        raise ValueError(f"Unknown relation type: {name}")
    return cls
