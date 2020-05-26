import exceptions

from net_connection.participation_status_ids import ParticipationStatusIDs
from main.models import UserParticipation, GameSession
from django.contrib.auth.models import User
from .user_tools import DBUserTools
from .user_error_messages import DBUserErrorMessages


class DBUSerParticipationTools:
    @staticmethod
    def get_user_participation(user: User) -> UserParticipation:
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        participation = UserParticipation.objects.get(user=user)
        return None if len(participation) == 0 else participation[0]

    @staticmethod
    def get_participation_status(user: User) -> ParticipationStatusIDs:
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        participation = DBUSerParticipationTools.get_user_participation(user)
        if participation is None:
            return ParticipationStatusIDs.NO_PARTICIPATION
        phase = participation.game_session.phase
        return ParticipationStatusIDs.WAITING_FOR_BEGINNING if phase == 0 else ParticipationStatusIDs.PLAYING_GAME

    @staticmethod
    def try_sign_user_up_for_session(user, game_session) -> (bool, str):
        if not (isinstance(user, User) and isinstance(game_session, GameSession)):
            raise exceptions.ArgumentTypeException()
        ok, user_data = DBUserTools.is_user_configuration_correct(user, True)
        if not ok:
            return False, DBUserErrorMessages.invalid_user_configuration
        if not user_data.activated:
            return False, DBUserErrorMessages.not_activated
        from .game_session_tools import DBGameSessionTools
        ok, error = DBGameSessionTools.can_user_take_part_in_session(user, user_data, game_session)
        if not ok:
            return False, error
        participation = UserParticipation(user_data=user_data, game_session=game_session)
        participation.save()
        return True, None

    @staticmethod
    def search_sessions_for_user_participation(user) -> (set, str):
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        ok, user_data = DBUserTools.is_user_configuration_correct(user, True)
        if not ok:
            return False, DBUserErrorMessages.invalid_user_configuration
        if not user_data.activated:
            return False, DBUserErrorMessages.not_activated
        level = user_data.level
        raw = GameSession.objects.filter(user_lowest_level__lte=level, user_highest_level__gte=level, phase=0)
        from .game_session_tools import DBGameSessionTools
        sessions = set()
        for session in raw:
            if DBGameSessionTools.can_user_take_part_in_session(user, user_data, session)[0]:
                sessions.add(session)
        return sessions, None
