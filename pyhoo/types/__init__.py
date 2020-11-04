from typing import Any, Dict, List, Literal, TypedDict

ApiResponse = TypedDict("ApiResponse", {"result": List[Dict[str, List[Any]]]})

Endpoint = Literal["chart", "fundamentals", "options"]
