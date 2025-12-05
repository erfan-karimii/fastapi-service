from sqladmin.authentication import AuthenticationBackend
from fastapi import Request


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        credential = await request.form()
        if credential["username"] != "admin" or credential["password"] != "admin":
            return False
        request.session.update({"token": "admin_token"})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token or token != "admin_token":
            return False

        return True
