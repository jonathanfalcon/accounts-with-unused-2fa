from typing import List, TypedDict, Union

class Uri(TypedDict):
    uri: str

class Login(TypedDict):
    uris: List[Uri]
    totp: Union[str, None]

class Item(TypedDict):
    name: str
    login: Login

class BitwardenVault(TypedDict):
    items: List[Item]

Type_BitwardenVault = BitwardenVault
