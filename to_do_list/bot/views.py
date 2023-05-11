
from django.conf import settings

from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from to_do_list.bot.serializers import TgUserSerializer
from to_do_list.bot.tg.client import TgClient


class VerificationView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TgUserSerializer

    def update(self, request, *args, **kwargs) -> Response:
        serializer: TgUserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer) -> None:
        tg_user = serializer.save()
        tg_client = TgClient(settings.BOT_TOKEN)
        tg_client.send_message(chat_id=tg_user.chat_id,
                               text='''Аккаунт успешно привязан!\n
    Доступные команды:\n"/goals" — получить список целей\n"/create" — создать новую цель''')


# class VerificationView(GenericAPIView):
#     # model = TgUser
#     permission_classes = [IsAuthenticated]
#     serializer_class = TgUserSerializer
#
#     def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         serializer: Serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         tg_user = self._get_tg_user(serializer.validated_data['verification_code'])
#
#         tg_user.user = request.user
#         tg_user.save()
#
#         TgClient(settings.BOT_TOKEN).send_message(tg_user.chat_id, 'Verification completed')
#
#         return Response(TgUserSerializer(tg_user).data)
#
#     @staticmethod
#     def _get_tg_user(verification_code: str) -> TgUser:
#         try:
#             return TgUser.objects.get(verification_code=verification_code)
#         except TgUser.DoesNotExist:
#             raise NotFound('Invalid verification code')
