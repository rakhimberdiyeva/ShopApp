from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import UserRegister, UserRead, ChangePasswordSchema


class AuthManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        pass

    async def login(
            self,
            username: str,
            password: str,
    ):
        """
        Метод для входа в учетную запись

        Проверяет наличие указанного юзернейма в бд

        Проверяет правильность указанного пароля

        :param username: имя пользователя
        :param password: пароль

        :raise Unauthorized: Ошибка авторизации

        :return: JWT токен
        """



    async def register(
            self,
            request: UserRegister
    ) -> UserRead:
        """
        Метод для регистрации пользователя

        Проверяет наличие юзернейма в бд

        Проверяет наличие почты в бд

        Хэширует пароль

        Создает пользователя в бд


        :param request: объект Pydantic модельки


        :return: моделька созданного пользователя
        """



    async def get_me(
            self,
            token: str
    ) -> UserRead:
        """
        Метод для получения информации пользователя

        Проверяет токен на валидность

        Достает информацию по ИД из бд

        :param token: JWT токен
        :return:  моделька токена
        """



    async def change_password(
            self,
            user_id: int,
            request: ChangePasswordSchema
    ) -> UserRead:
        """
        Метод изменения пароля

        Проверяет наличие пользователя

        Проверяет старый пароль пользователя

        Хэширует новый пароль

        Изменяет пароль в бд

        :param user_id: ИД пользователя
        :param request: объект Pydantic модельки
        :return: ничего
        """


    async def refresh_token(
            self,
            token: str
    ):
        """
        Метод для обновления токена

        Проверяет валидность токена

        Создает новую пару токенов

        :param token: JWT токен

        :return: JWT токен
        """


