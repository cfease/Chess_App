from dataclasses import dataclass
from typing import Optional

@dataclass
class Move:
    piece: str                 # 'P', 'N', 'B', 'R', 'Q', 'K'
    target: str                # square like 'e4'
    source_hint: Optional[str] # file/rank disambiguation (ignored for now)
    capture: bool
    promotion: Optional[str]
    castle: Optional[str]      # 'O-O' or 'O-O-O'

