import asyncio
from pickle import UnpicklingError
from prompt_toolkit import print_formatted_text, HTML, PromptSession
from libs.rageravecore.message import Message


class CoreClient:
    host: str
    port: int
    nickname: str
    client_id: int

    try_reconnect: bool = True

    __reconnect_delay: int = 1
    __reconnect_tries: int = 5
    __reconnect_iter: int = 0

    __server_closed: bool = False
    __input_task: asyncio.Task = None
    __prompt_session: PromptSession = None

    def __init__(self, host: str, port: int, nickname: str, client_id: int, try_reconnect: bool = True) -> None:
        self.writer = None
        self.reader = None
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client_id = client_id
        self.try_reconnect = try_reconnect
        self.__prompt_session = PromptSession()

    async def start_client_cli(self) -> None:
        await self.connect()

    async def connect(self) -> None:
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            print_formatted_text(
                HTML('<style fg="green">Успешное подключение к серверу</style>')
            )

            self.__server_closed = False
            self.__reconnect_iter = 0

            await self.send_message("ping")

            self.__input_task = asyncio.create_task(self.input_messages())
            await asyncio.create_task(self.receive_messages())

            await self.on_server_connected()

        except Exception as e:
            e.__cause__ = e

            print_formatted_text(
                HTML(f'<style fg="red">Подключение не удалось</style>')
            )
            self.__server_closed = True

    async def send_message(self, message: str) -> None:
        try:
            encoded_message: bytes = Message(
                text=message,
                author=self.nickname,
                message_type='command' if message.startswith('/') else 'text',
                client_id=self.client_id
            ).encode()

            self.writer.write(encoded_message)
            await self.writer.drain()
        except Exception as e:
            print_formatted_text(
                HTML(f'<style fg="red">Ошибка отправки: {e}</style>')
            )

    async def input_messages(self) -> None:
        try:
            while not self.__server_closed:
                try:
                    message: str = await self.__prompt_session.prompt_async(HTML('<style fg="yellow">> </style>'))
                    if not message.strip():
                        continue

                    if message.lower() == '/exit':
                        print_formatted_text(
                            HTML('<style fg="yellow">Соединение закрыто</style>')
                        )
                        self.try_reconnect = False
                        self.__server_closed = True
                        self.writer.close()
                        await self.writer.wait_closed()

                        break

                    await self.send_message(message)
                except asyncio.CancelledError:
                    break

        except Exception as e:
            print_formatted_text(
                HTML(f'<style fg="red">Ошибка ввода сообщений: {e}</style>')
            )

    async def receive_messages(self) -> None:
        try:
            data_buffer: bytes = b''
            while True:
                data = await self.reader.read(1024)
                data_buffer += data
                if not data:
                    await self.on_server_close_connection()
                    return

                try:
                    await self.__on_new_message(Message.decode(data_buffer))
                    data_buffer = b''
                except UnpicklingError:
                    continue
                except UnicodeDecodeError as e:
                    print_formatted_text(
                        HTML(f'<style fg="red">Ошибка декодирования данных: {e}</style>')
                    )

        except (ValueError, asyncio.CancelledError, AttributeError, WindowsError) as e:
            print(e)
        except Exception as e:
            print_formatted_text(
                HTML(f'<style fg="red">Ошибка получения сообщений: {e}</style>')
            )

    async def __on_new_message(self, message: Message) -> None:
        if message.client_id == self.client_id:
            return

        print_formatted_text(
            HTML(
                f'<style fg="{"yellow" if message.message_type == "service" else "blue"}">'
                f'{message.author}: {message.text}</style>'
            )
        )

        if message.message_type == "service" and message.service_type == 'chat_connected':
            match message.service_type:
                case 'chat_connected':
                    await self.__on_chat_connected(message)

        await self.on_new_message(message)

    async def __on_chat_connected(self, message: Message) -> None:
        await self.on_chat_connected(message)

    async def on_chat_connected(self, message: Message) -> None:
        pass

    async def on_new_message(self, message: Message) -> None:
        pass

    async def on_server_connected(self) -> None:
        pass

    async def on_server_disconnected(self) -> None:
        pass

    async def reconnect(self) -> None:
        while self.__server_closed and self.__reconnect_iter != self.__reconnect_tries:
            await asyncio.sleep(self.__reconnect_delay)

            self.__reconnect_iter += 1

            print_formatted_text(
                HTML(
                    f'<style fg="yellow">Попытка переподключения {self.__reconnect_iter}/{self.__reconnect_tries}. Следующая попытка через {self.__reconnect_delay} секунд</style>'
                )
            )
            await self.connect()

        else:
            print_formatted_text(
                HTML(
                    f'<style color="orange">Клиент завершил работу</style>'
                )
            )
            return

    async def on_server_close_connection(self) -> None:
        self.__server_closed = True
        if self.__input_task:
            self.__input_task.cancel()
        try:
            self.__prompt_session.app.exit()
        except Exception as e:
            e.__cause__ = e

        print_formatted_text(
            HTML('<style fg="red">Сервер закрыл соединение</style>')
        )

        if self.try_reconnect:
            print_formatted_text(
                HTML(
                    f'<style fg="yellow">Сервер настроен на попытку переподключения при потере соединения. Первая попытка начнется через {self.__reconnect_delay} секунд </style>')
            )

            await self.reconnect()
        else:
            await self.on_server_disconnected()
            exit()
