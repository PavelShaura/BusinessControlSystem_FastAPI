from fastapi import APIRouter, Depends, Request, Form

from src.schemas.employee_schemas import (
    CreateEmployeeRequest,
    EmployeeResponse,
    UpdateEmployeeDataRequest,
    EmployeeRegistrationCompleteRequest,
    RebindEmailRequest,
    TokenSchema,
)
from src.services import employee_services
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["employees"])


@router.post("/api/v1/employees/create", response_model=EmployeeResponse)
async def create_employee(
    employee_data: CreateEmployeeRequest,
    request: Request,
    uow: UnitOfWork = Depends(get_uow),
    create_employee_service: employee_services.CreateEmployeeService = Depends(
        employee_services.CreateEmployeeService
    ),
):
    return await create_employee_service.create_employee(uow, employee_data, request)


@router.post("/api/v1/employees/{employee_id}/invite")
async def generate_employee_invite(
    employee_id: int,
    request: Request,
    uow: UnitOfWork = Depends(get_uow),
    generate_url_employee_invite_service: employee_services.GenerateURLEmployeeInviteService = Depends(
        employee_services.GenerateURLEmployeeInviteService
    ),
):
    return await generate_url_employee_invite_service.generate_url_employee_invite(
        uow, employee_id, request
    )


@router.get("/api/v1/employees/registration-complete")
async def show_registration_form(
    token: str,
    uow: UnitOfWork = Depends(get_uow),
    show_registration_form_service: employee_services.ShowRegistrationFormService = Depends(
        employee_services.ShowRegistrationFormService
    ),
):
    return await show_registration_form_service.show_form(uow, token)



@router.post("/api/v1/employees/registration-complete")
async def complete_employee_registration(
    token: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    uow: UnitOfWork = Depends(get_uow),
    complete_employee_registration_service: employee_services.EmployeeRegistrationCompleteService = Depends(
        employee_services.EmployeeRegistrationCompleteService
    ),
):
    form_data = EmployeeRegistrationCompleteRequest(token=token, password=password, password_confirm=password_confirm)
    return await complete_employee_registration_service.complete_registration(
        uow, form_data.token, form_data.password, form_data.password_confirm
    )


@router.patch("/api/v1/employees/update")
async def update_employee_data(
    employee_data: UpdateEmployeeDataRequest,
    request: Request,
    uow: UnitOfWork = Depends(get_uow),
    update_employee_service: employee_services.UpdateEmployeeDataService = Depends(
        employee_services.UpdateEmployeeDataService
    ),
):
    return await update_employee_service.update_employee(uow, employee_data, request)


@router.post("/api/v1/employees/rebind-email")
async def rebind_email(
    rebind_data: RebindEmailRequest,
    request: Request,
    uow: UnitOfWork = Depends(get_uow),
    rebind_email_service: employee_services.RebindEmailService = Depends(
        employee_services.RebindEmailService
    ),
):
    return await rebind_email_service.rebind_email(uow, rebind_data, request)


@router.get("/api/v1/employees/confirm-rebind-email")
async def confirm_rebind_email(
    token: TokenSchema,
    uow: UnitOfWork = Depends(get_uow),
    confirm_rebind_email_service: employee_services.ConfirmRebindEmailService = Depends(
        employee_services.ConfirmRebindEmailService
    ),
):
    return await confirm_rebind_email_service.confirm_rebind_email(uow, token)
