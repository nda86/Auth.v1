"""
Применяем здесь подход dependency inversion.
Чтобы исключить жёсткую связь классов, в данном случае сервиса для работы с jwt и хранилища токенов.
Сервис будет зависеть от абстрактного класса, а работать будет с конкретной реализацией.
"""

from abc import ABC, abstractmethod


class JWTStorage(ABC):
    """Абстрактный класс представляющий интерфейс для конкретных реализаций хранилищ токенов.
    Определяет методы , которые должны быть в реализации.
    Для наших целей мы будем хранить в базе не весь рефреш токен, а только его идентификатор - jti
    """

    @abstractmethod
    def save_token(self, token: str, user_id: str) -> None:
        """Метод для сохранения токена в хранилище. Хранить токен в разрезе user_id"""
        pass

    @abstractmethod
    def get_token_by_jti(self, token_jti: str, user_id: str) -> str:
        """Метод для получения токена из хранилища, по переданным данным"""
        pass

    @abstractmethod
    def remove_token_by_jti(self, token_jti: str, user_id: str) -> None:
        """Метод для удаления токена из хранилища """
        pass

    @abstractmethod
    def remove_all_user_tokens(self, user_id: str) -> None:
        """Метод для удаления всех токенов конкретного пользователя"""
        pass
