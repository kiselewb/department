class AppException(Exception):
    detail = "Main App Error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class DataIsRequiredException(AppException):
    detail = "Укажите обязательные данные"


class RequestBodyRequiredException(DataIsRequiredException):
    detail = "Тело запроса не может быть пустым"


class ObjectNotFoundException(AppException):
    detail = "Объект не найден"


class DepartmentNotFoundException(ObjectNotFoundException):
    detail = "Подразделение не найдено"


class TargetDepartmentNotFoundException(ObjectNotFoundException):
    detail = "Целевое подразделение не найдено"


class ParentDepartmentNotFoundException(ObjectNotFoundException):
    detail = "Родительское подразделение не найдено"


class DepartmentNotSelfParentException(AppException):
    detail = "Подразделение не может быть родителем самому себе"


class DepartmentNameExistsException(AppException):
    detail = "Наименование подразделения должно быть отличным от уже существующих подразделений в этом родителе"


class DepartmentCycleException(AppException):
    detail = "Подразделение не может быть родителем своего родителя (Ошибка цикла)"


class ReassignModeException(AppException):
    detail = "Поле reassign_to_department_id обязательно при режиме 'REASSIGN'"


class ReassignToSelfException(AppException):
    detail = "Удаляемое подразделение не может являться целевым"