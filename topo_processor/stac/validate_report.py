from typing import Dict, List


class ValidateReport:
    total: int
    report_per_error_type: Dict[str, Dict[str, int]]

    def __init__(self):
        self.total = 0
        self.report_per_error_type = {}

    def add_errors(self, errors_per_schema: Dict[str, List[str]]) -> None:
        if errors_per_schema:
            for schema_uri in errors_per_schema:
                if schema_uri not in self.report_per_error_type:
                    self.report_per_error_type[schema_uri] = {}
                for error in errors_per_schema[schema_uri]:
                    if error in self.report_per_error_type[schema_uri]:
                        self.report_per_error_type[schema_uri][error] = self.report_per_error_type[schema_uri][error] + 1
                    else:
                        self.report_per_error_type[schema_uri][error] = 1

        self.total = self.total + 1
