from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from to_do_list.bot.models import TgUser


# Серилизатор TgUser


class TgUserSerializer(serializers.ModelSerializer):
    telegram_chat_id = serializers.SlugField(source='chat_id', read_only=True)

    class Meta:
        model = TgUser
        fields = ('chat_id', 'telegram_user_id', 'user', 'verification_code')
        read_only_fields = ('chat_id', 'telegram_user_id', 'user')

    def validate_verification_code(self, value: str) -> str:
        try:
            self.instance = TgUser.objects.get(verification_code=value)
        except TgUser.DoesNotExist:
            raise ValidationError('Code is incorrect')
        return value

    def update(self, instance, validated_data):
        self.instance.user = self.context['request'].user
        return super().update(instance, validated_data)

# class TgUserSerializer(serializers.ModelSerializer):

#
#     tg_id = serializers.IntegerField(source='chat_id', read_only=True)
#     username = serializers.CharField(source='user.username', read_only=True)
#
#     class Meta:
#         model = TgUser
#         fields = ('tg_id', 'username', 'verification_code', 'user_id')
#         read_only_fields = ('tg_id', 'username', 'user_id')
#
#     def validate_verification_code(self, code: str) -> str:
#         try:
#             self.tg_user = TgUser.objects.get(verification_code=code)
#         except TgUser.DoesNotExist:
#             raise ValidationError('Field is incorrect')
#         return code
#
#     def update(self, instance: TgUser, validated_data: dict):
#         return self.tg_user
