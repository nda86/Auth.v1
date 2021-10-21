from src import create_app
from .services.user_service import UserService

app = create_app()


@app.shell_context_processor
def shell_ctx():
    return dict(us=UserService())


if __name__ == "__main__":
    app.run(debug=True)
