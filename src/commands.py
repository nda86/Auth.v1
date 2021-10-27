import getpass

from flask import Flask

from core import db
from models import Role, User


def init_commands(app: Flask):
    @app.cli.command("create_admin")
    def create_admin():
        username = input("username:")
        password = getpass.getpass()
        role_admin = Role.query.filter_by(name="Admin").first() or Role(name="Admin")
        user_admin = User(username=username, password=password)
        user_admin.roles.append(role_admin)
        db.session.add(user_admin)
        db.session.commit()
        print("User Admin successfully created")
