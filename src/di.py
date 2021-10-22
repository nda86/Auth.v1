from injector import Module, Binder
from flask_injector import request


from .services import UserService, AuthService, JWTService


class ServiceInjector(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=UserService, to=UserService, scope=request)
        binder.bind(interface=AuthService, to=AuthService, scope=request)
        binder.bind(interface=JWTService, to=JWTService, scope=request)
