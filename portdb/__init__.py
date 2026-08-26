from typing import TypedDict


class IndividualService(TypedDict):
    """a service dict"""

    name: str
    protocol: str | None
    description: str | None
    note: str | None
    port: str | None
