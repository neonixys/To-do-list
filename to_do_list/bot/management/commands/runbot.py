import logging

from django.conf import settings
from django.core.management import BaseCommand

from to_do_list.bot.management._chat import Chat
from to_do_list.bot.tg.client import TgClient


class Command(BaseCommand):

    def __init__(self) -> None:
        super().__init__()
        self.tg_client: TgClient = TgClient(token=settings.BOT_TOKEN)
        self.logger = logging.getLogger(__name__)
        self.logger.info('Bot started')

    def handle(self, *args, **options) -> None:
        offset: int = 0
        while True:
            # Получение обновлений в бесконечном цикле.
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.logger.info(item.message)
                # Создание экземпляра класса чата и определение состояния.
                chat = Chat(message=item.message)
                chat.set_state(tg_client=self.tg_client)
                # Запуск исполнения команд, доступных юзеру каждого состояния.
                chat.state.run()






# class Command(BaseCommand):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.tg_client = TgClient(settings.BOT_TOKEN)
#
#     def handle(self, *args, **kwargs):
#         offset = 0
#
#         while True:
#             res = self.tg_client.get_updates(offset=offset)
#             for item in res.result:
#                 offset = item.update_id + 1
#                 self.handle_message(item.message)
#
#     def handle_message(self, msg: Message):
#         tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
#         if not tg_user.user:
#             # Пользователь телеграма НЕ привязан к пользователю приложения
#             self.tg_client.send_message(msg.chat.id, "Hello!")
#             verification_code = str(uuid4())
#             tg_user.verification_code = verification_code
#             tg_user.save(update_fields=['verification_code'])
#             self.tg_client.send_message(msg.chat.id, F"Verification Code: {verification_code}")
#         else:
#             # Пользователь телеграма привязан к пользователю приложения
#             self.handle_authorized_user(tg_user, msg)
#
#     def handle_authorized_user(self, tg_user: TgUser, msg: Message):
#         if msg.text.startswith('/'):
#             self.handle_command(tg_user, msg.text)
#         else:
#             ...
#
#     def handle_command(self, tg_user: TgUser, command: str):
#         match command:
#             case '/goals':
#                 goals = Goal.objects.select_related('user').filter(
#                     user=tg_user.user, category__is_deleted=False
#                 ).exclude(status=Goal.Status.archived)
#                 if not goals:
#                     self.tg_client.send_message(tg_user.chat_id, "There are no goals")
#                 else:
#                     resp = '\n'.join([goal.title for goal in goals])
#                     self.tg_client.send_message(tg_user.chat_id, resp)
