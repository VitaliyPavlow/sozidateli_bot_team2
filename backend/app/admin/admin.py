from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin
from starlette_admin.i18n import I18nConfig

from app.core import Settings as settings
from app.domain.models import Meeting, User, Administration, Role
from app.domain.schemas import MeetingCreate, UserCreate
from app.domain.schemas.administrations import BaseAdministration
from app.domain.schemas.roles import BaseRole
from app.infrastructure.db import engine
from .administrations import AdministrationView
from .meetings import MeetingView
from .provider import UsernameAndPasswordProvider
from .roles import RoleView
from .users import UserView

admin = Admin(
    engine,
    title="Проект 'Созидатели'",
    i18n_config=I18nConfig(default_locale="ru"),
    middlewares=[
        Middleware(
            SessionMiddleware, secret_key=settings.admin_middleware_secret
        )
    ],
    auth_provider=UsernameAndPasswordProvider(),
)

admin.add_view(AdministrationView(Administration,
                                  pydantic_model=BaseAdministration,
                                  icon="fa fa-user"))
admin.add_view(RoleView(Role, pydantic_model=BaseRole, icon="fa fa-people-roof"))
admin.add_view(UserView(
    User, pydantic_model=UserCreate, icon="fa fa-school-circle-exclamation"
))

admin.add_view(
    MeetingView(Meeting, pydantic_model=MeetingCreate, icon="fa fa-calendar")
)
