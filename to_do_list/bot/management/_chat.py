from to_do_list.bot.management._state import BaseTgUserState, NewUserState, UnverifiedUserState, VerifiedUserState
from to_do_list.bot.models import TgUser
from to_do_list.bot.tg.client import TgClient
from to_do_list.bot.tg.schemas import Message


class Chat:
    """Класс чата с пользователем для изменения состояния"""
    def __init__(self, message: Message):
        self.message = message
        self.__state: BaseTgUserState | None = None

    @property
    def state(self) -> BaseTgUserState | None:
        if self.__state:
            return self.__state
        else:
            raise RuntimeError('''State doesn't exist.''')

    def set_state(self, tg_client: TgClient) -> None:
        # Проверка юзера на наличие в базе / создание нового.
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=self.message.chat.id,
            defaults={
                'telegram_user_id': self.message.from_.id
            }
        )
        if created:
            self.__state = NewUserState(tg_client=tg_client, tg_user=tg_user)
        elif not tg_user.user:
            self.__state = UnverifiedUserState(tg_client=tg_client, tg_user=tg_user)
        else:
            self.__state = VerifiedUserState(tg_client=tg_client, tg_user=tg_user, message=self.message)