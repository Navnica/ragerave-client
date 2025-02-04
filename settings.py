from random import randint


host: str = '192.168.1.207'
port: int = 8080

nickname: str = f"Client {randint(0, 1000)}"
client_id: int = randint(100000, 999999)