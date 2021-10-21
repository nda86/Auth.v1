from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .user import User


user_pydantic = sqlalchemy_to_pydantic(User)
print(user_pydantic)
