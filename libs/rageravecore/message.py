import pickle


class Message:
    text: str | None
    author: str
    client_id: int
    message_type: str
    service_type: str | None
    chat_info: dict | None

    def __init__(
            self, client_id: int,
            author: str,
            text: str | None = None,
            message_type: str = "text",
            service_type: str | None = None,
            chat_info: dict | None = None
    ) -> None:
        self.text = text
        self.author = author
        self.message_type = message_type
        self.client_id = client_id
        self.chat_info = chat_info
        self.service_type = service_type

    def encode(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def decode(encoded_bytes: bytes) -> 'Message':
        return pickle.loads(encoded_bytes)
