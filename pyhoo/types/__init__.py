from typing import Any, Dict, List, Literal, Optional, TypedDict


class ErrorDescription(TypedDict):
    code: str
    description: str


class ApiResponse(TypedDict):
    result: Optional[List[Dict[str, List[Any]]]]
    error: Optional[ErrorDescription]


Endpoint = Literal["chart", "fundamentals", "options"]
