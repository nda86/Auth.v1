from src import create_app, db
from src.services.user_service import UserService
from src.models.user import User

app = create_app()


u1 = User(username="nda1", password="1", email="nda86@mail.ru")
u2 = User(username="nda1", password="1", email="nda86@mail.ru")


@app.shell_context_processor
def shell_ctx():
    return dict(us=UserService(), u1=u1, u2=u2, db=db)


if __name__ == "__main__":
    app.run(debug=True)
