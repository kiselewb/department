from fastapi import Request, FastAPI
from app.api.exceptions import (
    ParentDepartmentNotFoundHTTPException,
    DepartmentNotSelfParentHTTPException,
    DepartmentNameExistsHTTPException,
    DepartmentNotFoundHTTPException,
    DepartmentCycleHTTPException,
    DataIsRequiredHTTPException,
    RequestBodyRequiredHTTPException, ReassignModeHTTPException, TargetDepartmentNotFoundHTTPException,
    ReassignToSelfHTTPException,
)
from app.utils.exceptions import (
    ParentDepartmentNotFoundException,
    DepartmentNotSelfParentException,
    DepartmentNameExistsException,
    DepartmentNotFoundException,
    DepartmentCycleException,
    DataIsRequiredException,
    RequestBodyRequiredException, ReassignModeException, TargetDepartmentNotFoundException, ReassignToSelfException,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DataIsRequiredException)
    async def data_is_required(request: Request, exc: DataIsRequiredException):
        raise DataIsRequiredHTTPException()

    @app.exception_handler(RequestBodyRequiredException)
    async def request_body_is_required(
        request: Request, exc: RequestBodyRequiredException
    ):
        raise RequestBodyRequiredHTTPException()

    @app.exception_handler(DepartmentNotFoundException)
    async def department_not_found(request: Request, exc: DepartmentNotFoundException):
        raise DepartmentNotFoundHTTPException()

    @app.exception_handler(TargetDepartmentNotFoundException)
    async def target_department_not_found(request: Request, exc: TargetDepartmentNotFoundException):
        raise TargetDepartmentNotFoundHTTPException()

    @app.exception_handler(ParentDepartmentNotFoundException)
    async def parent_department_not_found(
        request: Request, exc: ParentDepartmentNotFoundException
    ):
        raise ParentDepartmentNotFoundHTTPException()

    @app.exception_handler(DepartmentNotSelfParentException)
    async def department_not_self_parent(
        request: Request, exc: DepartmentNotSelfParentException
    ):
        raise DepartmentNotSelfParentHTTPException()

    @app.exception_handler(DepartmentNameExistsException)
    async def department_name_exists(
        request: Request, exc: DepartmentNameExistsException
    ):
        raise DepartmentNameExistsHTTPException()

    @app.exception_handler(DepartmentCycleException)
    async def department_cycle(request: Request, exc: DepartmentCycleException):
        raise DepartmentCycleHTTPException()

    @app.exception_handler(ReassignModeException)
    async def reassign_mode(request: Request, exc: ReassignModeException):
        raise ReassignModeHTTPException()

    @app.exception_handler(ReassignToSelfException)
    async def reassign_mode(request: Request, exc: ReassignToSelfException):
        raise ReassignToSelfHTTPException()
