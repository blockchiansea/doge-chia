from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from dogechia.types.spend_bundle_conditions import SpendBundleConditions
from dogechia.util.ints import uint16, uint64
from dogechia.util.streamable import Streamable, streamable


@streamable
@dataclass(frozen=True)
class NPCResult(Streamable):
    error: Optional[uint16]
    conds: Optional[SpendBundleConditions]
    cost: uint64  # The total cost of the block, including CLVM cost, cost of
    # conditions and cost of bytes
