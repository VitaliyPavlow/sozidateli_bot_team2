from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed

from app.application.repositories import AdministrationRepository
from app.core.password import verify_password


class UsernameAndPasswordProvider(AuthProvider):
    """Авторизация/идентификация/аутентификация."""

    async def login(
            self,
            username: str,
            password: str,
            remember_me: bool,
            request: Request,
            response: Response,
    ) -> Response:
        """Аутентификация пользователя."""
        administration = AdministrationRepository(request.state.session)
        user = await administration.find_one(username=username)
        if not user:
            raise LoginFailed("Неправильные логин или пароль.")
        if username == user.username and verify_password(password, user.password):
            request.session.update({"username": username})
            return response
        raise LoginFailed("Неправильные логин или пароль.")

    async def is_authenticated(self, request) -> bool:
        """Аутентификация."""
        if not request.session.get("username"):
            return False

        administration = AdministrationRepository(request.state.session)
        user = await administration.find_one(username=request.session["username"])

        if not user:
            return False

        data = {"name": user.name,
                "roles": [role.name for role in user.roles]}
        request.state.user = data
        return True

    def get_admin_config(self, request: Request) -> AdminConfig:
        """Получение конфигурации для администратора."""
        user = request.state.user
        custom_app_title = "Привет " + user["name"] + "!"
        custom_logo_url = None
        if user.get("company_logo_url", None):
            custom_logo_url = request.url_for(
                "static", path=user["company_logo_url"]
            )
        return AdminConfig(
            app_title=custom_app_title,
            logo_url=custom_logo_url,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        """Получение администратора."""
        user = request.state.user
        return AdminUser(username=user["name"])

    async def logout(self, request: Request, response: Response) -> Response:
        """Разлогинивание."""
        request.session.clear()
        return response
