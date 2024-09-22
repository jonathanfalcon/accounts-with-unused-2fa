from typing import Dict, List, Optional, TypedDict

class TotpJsonValues(TypedDict):
    methods: List[str]
    documentation: str
    recovery: Optional[str]

Type_TotpJson = Dict[str, TotpJsonValues]
