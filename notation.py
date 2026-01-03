import re
from move import Move

MOVE_RE = re.compile(
    r"""
    (?P<castle>O-O(-O)?) |
    (?:
        (?P<piece>[NBRQK])?
        (?P<source>[a-h1-8])?
        (?P<capture>x)?
        (?P<target>[a-h][1-8])
        (?:=(?P<promo>[NBRQ]))?
    )
    """,
    re.VERBOSE
)

def parse_algebraic(move_str: str) -> Move:
    move_str = move_str.strip()

    m = MOVE_RE.fullmatch(move_str)
    if not m:
        raise ValueError(f"Unrecognized move: {move_str}")

    if m.group("castle"):
        return Move(
            piece="K",
            target=None,
            source_hint=None,
            capture=False,
            promotion=None,
            castle=m.group("castle")
        )

    return Move(
        piece=m.group("piece") or "P",
        target=m.group("target"),
        source_hint=m.group("source"),
        capture=bool(m.group("capture")),
        promotion=m.group("promo"),
        castle=None
    )