class Validity:
    is_valid = True
    log = []

    def add_error(self, msg: str, cause: str, e):
        self.log.append({"msg": msg, "level": "error", "cause": cause, "error": e})
        self.is_valid = False

    def add_warning(self, msg: str, cause: str, e):
        self.log.append({"msg": msg, "level": "warning", "cause": cause, "error": e})
