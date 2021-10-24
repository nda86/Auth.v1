from abc import ABC, abstractmethod


class JWTStorage(ABC):
    """Абстрактный класс представляющий интерфейс для конкретных реализаций хранилищ токенов.
    Определяет методы , которые должны быть в реализации.
    """

    @abstractmethod
    def save_token(self, token_jti: str, user_id: str) -> None:
        """Метод для сохранения токена в хранилище. Хранить токен в разрезе user_id"""
        pass

    @abstractmethod
    def get_token(self, token_jti: str, user_id: str) -> str:
        """Метод для получения токена из хранилища, по переданным данным"""
        pass

    @abstractmethod
    def remove_token(self, token_jti: str, user_id: str) -> None:
        """Метод для удаления токена из хранилища """
        pass

    @abstractmethod
    def remove_all_token(self, user_id: str) -> None:
        """Метод для удаления всех токенов конкретного пользователя"""
        pass
