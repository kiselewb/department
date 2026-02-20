class AppException(Exception):
    detail = "Main App Error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFound(AppException):
    detail = "Object Not Found"


class PlanNotFound(AppException):
    detail = "Plan Not Found"
