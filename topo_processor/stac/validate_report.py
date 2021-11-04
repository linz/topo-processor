from typing import Dict, List


class ValidateReport:
    total: int
    errors_per_object: Dict[str, Dict[str, List[str]]]
    report_per_error_type: Dict[str, Dict[str, int]]

    def __init__(self):
        self.total = 0
        self.errors_per_object = {}
        self.report_per_error_type = {}

    def add_errors(self, object_id: str, errors_per_schema: Dict[str, List[str]]) -> None:
        if errors_per_schema:
            self.errors_per_object[object_id] = errors_per_schema
        self.total = self.total + 1

    def build_report(self):
        for errors_stac_object in self.errors_per_object.values():
            for schema_uri in errors_stac_object:
                if schema_uri not in self.report_per_error_type:
                    self.report_per_error_type[schema_uri] = {}
                for error in errors_stac_object[schema_uri]:
                    if error in self.report_per_error_type[schema_uri]:
                        self.report_per_error_type[schema_uri][error] = self.report_per_error_type[schema_uri][error] + 1
                    else:
                        self.report_per_error_type[schema_uri][error] = 1
