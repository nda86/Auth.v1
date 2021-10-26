from src import create_app, db
from src.models import User, Role

app = create_app()


u = User()
u.username = "test666"
u.password = "test666"


@app.shell_context_processor
def make_ctx():
    return dict(User=User, Role=Role, u=u, db=db)


if __name__ == "__main__":
    app.run(debug=True)
