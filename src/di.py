from injector import Module, Binder, singleton
from flask_injector import request


from .services.user_service import UserService


class ServiceInjector(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=UserService, to=UserService, scope=request)
