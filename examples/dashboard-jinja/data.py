"""The same content as examples/dashboard-next, so the two can be compared."""
from dataclasses import dataclass

STREAMS = [
    {"label": "May", "current": 412_000, "previous": 388_000},
    {"label": "Jun", "current": 468_000, "previous": 401_000},
    {"label": "Jul", "current": 445_000, "previous": 437_000},
    {"label": "Aug", "current": 521_000, "previous": 452_000},
    {"label": "Sep", "current": 604_000, "previous": 478_000},
    {"label": "Oct", "current": 662_000, "previous": 509_000},
]


@dataclass(frozen=True)
class Release:
    id: str
    title: str
    artist: str
    type: str
    status: str
    streams: int
    royalties: float
    reviewer: str | None


RELEASES = [
    Release("F055-0142", "Night Signals",      "F055",          "Single", "Live",      184_320, 1_412.88, "Eddie Lake"),
    Release("F055-0141", "Kreuzberg Tapes",    "Lúcia Andrade", "EP",     "Live",       96_204,   742.19, "Eddie Lake"),
    Release("F055-0140", "Static Garden",      "Mø Verde",      "Album",  "In review",       0,     0.00, None),
    Release("F055-0139", "Hold / Release",     "F055",          "Single", "Scheduled",       0,     0.00, "Jamik Tashpulatov"),
    Release("F055-0138", "Copper Wires",       "Teodoro Reis",  "EP",     "Live",       61_877,   488.05, "Jamik Tashpulatov"),
    Release("F055-0137", "Low Tide, Repeated", "Mø Verde",      "Single", "Live",       44_190,   331.42, "Eddie Lake"),
    Release("F055-0136", "Afterimage",         "Lúcia Andrade", "Album",  "Takedown",   12_045,    94.60, "Jamik Tashpulatov"),
    Release("F055-0135", "Pirate Radio Hymns", "F055",          "EP",     "In review",       0,     0.00, None),
]

STATS = [
    {"label": "Monthly streams", "value": "662,041", "delta": "+9.6%",  "up": True,  "note": "Trending up this month", "sub": "Six straight months of growth"},
    {"label": "Net royalties",   "value": "€5,118",  "delta": "+12.5%", "up": True,  "note": "Above projection",       "sub": "Paid out on the 15th"},
    {"label": "Active releases", "value": "142",     "delta": "+4",     "up": True,  "note": "Four added this period", "sub": "Two still in review"},
    {"label": "Skip rate",       "value": "22.4%",   "delta": "-2.1%",  "up": False, "note": "Down 2.1% this period",  "sub": "Lower is better"},
]

SELECTED = {"F055-0141"}

NAV_MAIN = [("Dashboard", "layout-dashboard", False), ("Releases", "disc-3", True),
            ("Analytics", "chart-column", False), ("Royalties", "receipt", False),
            ("Catalog", "boxes", False), ("Team", "users", False)]
NAV_LIBRARY = [("Masters", "audio-lines", False), ("Reports", "file-text", False),
               ("Splits", "split", False)]
NAV_FOOTER = [("Settings", "settings", False), ("Get Help", "circle-help", False)]
