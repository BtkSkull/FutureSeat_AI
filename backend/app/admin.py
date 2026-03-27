from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.config import settings
from app.models.college import College
from app.models.cutoff import Cutoff


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        if (form.get("username") == settings.ADMIN_USERNAME and
                form.get("password") == settings.ADMIN_PASSWORD):
            request.session.update({"admin_token": "ok"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin_token") == "ok"


class CollegeAdmin(ModelView, model=College):
    name        = "College"
    name_plural = "Colleges"
    icon        = "fa-solid fa-school"

    column_list = [
        "id", "name", "state", "type", "exam_type",
        "course", "fees_lpa", "seats", "naac_grade",
    ]
    column_searchable_list = ["name", "state", "exam_type"]
    column_sortable_list   = ["id", "name", "exam_type", "state"]
    page_size              = 50
    can_export             = True


class CutoffAdmin(ModelView, model=Cutoff):
    name        = "Cutoff"
    name_plural = "Cutoffs"
    icon        = "fa-solid fa-list-ol"

    column_list = [
        "id", "college_id", "quota", "category", "gender",
        "special", "opening_rank", "closing_rank", "year",
    ]
    column_sortable_list        = ["id", "college_id", "closing_rank"]
    column_details_exclude_list = ["college"]
    page_size                   = 100
    can_export                  = True


def setup_admin(app, engine) -> Admin:
    auth  = AdminAuth(secret_key=settings.ADMIN_SESSION_SECRET)
    admin = Admin(app, engine, authentication_backend=auth)
    admin.add_view(CollegeAdmin)
    admin.add_view(CutoffAdmin)
    return admin