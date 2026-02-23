from fastapi import HTTPException


class AppHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class DataIsRequiredHTTPException(AppHTTPException):
    status_code = 404
    detail = "Укажите обязательные данные"


class RequestBodyRequiredHTTPException(DataIsRequiredHTTPException):
    status_code = 404
    detail = "Тело запроса не может быть пустым"


class DepartmentNotFoundHTTPException(AppHTTPException):
    status_code = 404
    detail = "Подразделение не найдено"


class TargetDepartmentNotFoundHTTPException(AppHTTPException):
    status_code = 404
    detail = "Целевое подразделение не найдено"


class ParentDepartmentNotFoundHTTPException(AppHTTPException):
    status_code = 404
    detail = "Родительское подразделение не найдено"


class DepartmentNotSelfParentHTTPException(AppHTTPException):
    status_code = 404
    detail = "Подразделение не может быть родителем самому себе"


class DepartmentNameExistsHTTPException(AppHTTPException):
    status_code = 404
    detail = "Наименование подразделения должно быть отличным от уже существующих подразделений в этом родителе"


class DepartmentCycleHTTPException(AppHTTPException):
    status_code = 409
    detail = "Подразделение не может быть родителем своего родителя (Ошибка цикла)"


class ReassignModeHTTPException(AppHTTPException):
    status_code = 422
    detail = "Поле reassign_to_department_id обязательно при режиме 'REASSIGN'"


class ReassignToSelfHTTPException(AppHTTPException):
    status_code = 422
    detail = "Удаляемое подразделение не может являться целевым"
