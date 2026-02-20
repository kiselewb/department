from fastapi import HTTPException


class AppHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class DepartmentNotFoundHTTPException(AppHTTPException):
    status_code = 404
    detail = "Department not found"
