from celery.result import AsyncResult

from worker.celery_tasks_factory.tasks_factory import TaskFactory, Task
from worker.tasks import (
    send_invite_email_task,
    send_rebind_email_task,
    send_employee_invite_email_task,
)


@TaskFactory.register("send_invite_email")
class SendInviteEmailTask(Task):
    async def execute(self, email, invite_token) -> AsyncResult:
        return send_invite_email_task.delay(email, invite_token)


@TaskFactory.register("send_rebind_email")
class RebindEmailTask(Task):
    async def execute(self, email, rebind_url) -> AsyncResult:
        return send_rebind_email_task.delay(email, rebind_url)


@TaskFactory.register("send_employee_invite_email")
class SendEmployeeInviteEmailTask(Task):
    async def execute(self, email, invite_url) -> AsyncResult:
        return send_employee_invite_email_task.delay(email, invite_url)
