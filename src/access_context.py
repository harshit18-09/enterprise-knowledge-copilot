class AccessContext:
    def __init__(self, allowed_levels: list[str]):
        self.allowed_levels = allowed_levels

ADMIN = AccessContext(["public", "internal", "restricted"])
EMPLOYEE = AccessContext(["public", "internal"])
GUEST = AccessContext(["public"])