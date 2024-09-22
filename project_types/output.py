from typing import List, TypedDict

class Output(TypedDict):
    name: str
    uri: str
    documentation: str

Type_Output = List[Output]
