import asyncio
from src.client.core_client import CoreClient
from settings import *


if __name__ == '__main__':
    client: CoreClient = CoreClient(
        host=host,
        port=port,
        nickname=nickname,
        client_id=client_id
    )

    try:
        asyncio.run(client.start_client_cli())
    except (Exception, ImportError, asyncio.CancelledError) as e:
        e.__traceback__ = e.__traceback__