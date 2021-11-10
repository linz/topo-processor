from typing import Dict, List


class ValidateReport:
    total: int
    report_per_error_type: Dict[str, Dict[str, int]]

    def __init__(self):
        self.total = 0
        self.report_per_error_type = {}

    def add_errors(self, errors_per_schema: Dict[str, List[str]]) -> None:
        for schema_uri in errors_per_schema:
            for error in errors_per_schema[schema_uri]:
                self.increment_error(schema_uri, error)
        self.total = self.total + 1

    def increment_error(self, schema: str, error: str) -> None:
        existing = self.report_per_error_type.get(schema)
        if existing is None:
            self.report_per_error_type[schema] = existing = {}
        existing[error] = existing.get(error, 0) + 1
