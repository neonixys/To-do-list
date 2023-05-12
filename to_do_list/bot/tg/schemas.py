from pydantic.main import BaseModel


class Chat(BaseModel):
    id: int
    first_name: str | None = None
    username: str | None


class Message(BaseModel):
    chat: Chat
    text: str | None = None


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj]