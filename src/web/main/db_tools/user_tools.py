import exceptions

from main.db_tools.user_error_messages import DBUserErrorMessages
from main.models import UserData
from game_eng.game_model import GameModel
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.utils.encoding import force_bytes


class DBUserTools:
    """**Инструменты работы в БД с данными о пользователях**
    """

    @staticmethod
    def deleted_user_name() -> str:
        """**Особый логин/ник, обозначающий удалённого пользователя**
        """
        return "$_del"

    @staticmethod
    def try_register(login: str, password: str, team: int, request) -> (bool, str):
        """**Попытка регистрации пользователя**\n
        Пробует зарегистрировать пользователя.

        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises ArgumentValueException: |ArgumentValueException|
        :param login: Логин (1-64 символа)
        :type login: str
        :param password: Пароль (1-64 символа)
        :type password: str
        :param team: Номер фракции (0-2)
        :type team: int
        :param request: Запрос на регистрацию
        :type request: HttpRequest
        :return: (ok, error)
        :rtype: (bool, str) или (bool, None)
        """
        # vvv первичная проверка аргументов vvv
        if not (isinstance(login, str) and isinstance(password, str) and isinstance(team, int)):
            raise exceptions.ArgumentTypeException()
        if not ((0 < len(login) <= 64) and (0 < len(password) <= 64) and (0 <= team < 3)):
            raise exceptions.ArgumentValueException()
        del_name = DBUserTools.deleted_user_name()
        if login == del_name:
            raise exceptions.ArgumentValueException\
                (f"Логин не должен принимать значение '{del_name}'!")
        # vvv проверка согласованности аргументов с данными БД vvv
        if len(User.objects.filter(username=login)) > 0:
            return False, DBUserErrorMessages.login_is_already_in_use
        # vvv запись в БД vvv
        user = User(username=login, date_joined=timezone.now())
        user.set_password(password)
        user.save()
        user_data = UserData(user=user, team=team)
        user_data.activated = True
        user_data.save()
        return True, None

    @staticmethod
    def delete_user(user: User):
        """**Инструмент удаления пользователя из БД**\n
        :raises ArgumentTypeException: |ArgumentTypeException|
        :param user: Пользователь
        :type user: User
        """
        # vvv проверка аргумента vvv
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        # vvv удаление из БД vvv
        user_data = UserData.objects.filter(user=user)
        if len(user_data) > 0:
            user_data.delete()
        user.delete()

    @staticmethod
    def is_user_configuration_correct(user: User, return_user_data: bool = False):
        """**Инструмент проверки валидности пользовательских данных**\n
        Проверяет факт наличия в БД ровно одной записи типа :class:`main.models.UserData`.

        :raises ArgumentTypeException: |ArgumentTypeException|
        :param user: Пользователь
        :type user: User
        :param return_user_data: Факт возврата этим методом UserData
        :type return_user_data: bool
        :return: Факт валидности пользовательских данных
        :rtype: bool или (bool, UserData)
        """
        # vvv проверка аргумента vvv
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        # vvv проверка валидности vvv
        user_data = UserData.objects.filter(user=user)
        okay = len(user_data) == 1
        if return_user_data:
            return okay, (user_data[0] if okay else None)
        return okay

    @staticmethod
    def try_find_user_with_id(uid: int) -> (User, str):
        user = User.objects.filter(id=uid)
        if len(user) == 0:
            return None, DBUserErrorMessages.not_found
        return user[0], None

    @staticmethod
    def try_get_user_data(user) -> (UserData, str):
        user_data = UserData.objects.filter(user=user)
        if len(user_data) != 1:
            return None, DBUserErrorMessages.invalid_user_configuration
        return user_data[0], None

    @staticmethod
    def check_user_existence(login: str, password: str) -> bool:
        """**Инструмент проверки существования пары логин-пароль**\n
        :raises ArgumentTypeException: |ArgumentTypeException|
        :param login: Логин
        :type login: str
        :param password: Пароль
        :type password: str
        :return: Факт существования пары логин-пароль
        :rtype: bool
        """
        # vvv проверка аргументов vvv
        if not (isinstance(login, str) and isinstance(password, str)):
            raise exceptions.ArgumentTypeException()
        # vvv проверка данных по БД vvv
        user = User.objects.filter(username=login)
        if len(user) != 1:
            return False
        user = user[0]
        return user.check_password(password)

    @staticmethod
    def do_game_session_end_user_data_change(user_data: UserData, victory: bool):
        """**Инструмент изменения пользовательских данных по причине окончания игровой сессии**\n
        Увеличивает поле 'UserData.played_games_count' на 1. Если игрок победил,
        увеличивает поле 'UserData.victories_count' на 1 и даёт игроку level+1 единиц опыта.

        :raises ArgumentTypeException: |ArgumentTypeException|
        :param user_data: Пользовательских данные, которые требуется изменить
        :type user_data: UserData
        :param victory: Факт победы игрока
        :type victory: bool
        """
        if not (isinstance(user_data, UserData) and isinstance(victory, bool)):
            raise exceptions.ArgumentTypeException()
        user_data.played_games_count += 1
        if victory:
            user_data.victories_count += 1
            user_data.gain_exp(user_data.level + 1)
        user_data.save()

    @staticmethod
    def try_get_player_of_user_from_game_model(user: User, game_model: GameModel):
        if not (isinstance(user, User) and isinstance(game_model, GameModel)):
            raise exceptions.ArgumentTypeException()
        for team in game_model.teams:
            for player in team.players:
                if player.id == user.id:
                    return player
        return None
