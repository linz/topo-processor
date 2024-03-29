from typing import Any, Dict, List, Optional


class Validity:
    def __init__(self) -> None:
        self.log: List[Dict[str, Any]] = []
        self._valid = True

    def add_error(self, msg: str, cause: str, e: Optional[Exception] = None) -> None:
        self.log.append({"msg": msg, "level": "error", "cause": cause, "error": e})
        self._valid = False

    def add_warning(self, msg: str, cause: str, e: Optional[Exception] = None) -> None:
        self.log.append({"msg": msg, "level": "warning", "cause": cause, "error": e})

    def is_valid(self) -> bool:
        return self._valid
