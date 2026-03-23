from typing import TypedDict, Optional


class IndividualService(TypedDict):
    """a service dict"""

    name: str
    protocol: Optional[str]
    description: Optional[str]
    note: Optional[str]
    port: Optional[str]
