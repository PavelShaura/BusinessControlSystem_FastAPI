from fastapi import APIRouter, Depends, Request, Form

from src.services import employee_services
from src.utils.unit_of_work import UnitOfWork, get_uow
from src.schemas.employee_schemas import CreateEmployeeRequest, EmployeeResponse

router = APIRouter(tags=["employees"])


@router.post("/api/v1/employees/create", response_model=EmployeeResponse)
async def create_employee(
    employee_data: CreateEmployeeRequest,
    request: Request,
    uow: UnitOfWork = Depends(get_uow),
):
    return await employee_services.CreateEmployeeService()(
        uow, employee_data=employee_data, request=request
    )


@router.post("/api/v1/employees/{employee_id}/invite")
async def generate_employee_invite(
    employee_id: int, request: Request, uow: UnitOfWork = Depends(get_uow)
):
    return await employee_services.GenerateURLEmployeeInviteService()(
        uow, employee_id=employee_id, request=request
    )


@router.get("/api/v1/employees/registration-complete")
async def show_registration_form(token: str, uow: UnitOfWork = Depends(get_uow)):
    return await employee_services.ShowRegistrationFormService()(uow, token=token)


@router.post("/api/v1/employees/registration-complete")
async def complete_employee_registration(
    token: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    uow: UnitOfWork = Depends(get_uow),
):
    return await employee_services.EmployeeRegistrationCompleteService()(
        uow, token=token, password=password, password_confirm=password_confirm
    )


@router.patch("/api/v1/employees/update-data")
async def update_employee_data(
    request: Request,
    first_name: str = Form(None),
    last_name: str = Form(None),
    current_password: str = Form(...),
    uow: UnitOfWork = Depends(get_uow),
):
    return await employee_services.UpdateEmployeeDataService()(
        uow,
        request=request,
        first_name=first_name,
        last_name=last_name,
        current_password=current_password,
    )


@router.post("/api/v1/employees/rebind-email")
async def rebind_email(
    request: Request,
    new_email: str = Form(...),
    current_password: str = Form(...),
    uow: UnitOfWork = Depends(get_uow),
):
    return await employee_services.RebindEmailService()(
        uow,
        request=request,
        new_email=new_email,
        current_password=current_password,
    )


@router.get("/api/v1/employees/confirm-rebind-email")
async def confirm_rebind_email(token: str, uow: UnitOfWork = Depends(get_uow)):
    return await employee_services.ConfirmRebindEmailService()(uow, token=token)
