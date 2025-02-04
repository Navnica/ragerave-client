# RageRave Client  
Простой асинхронный CLI-мессенджер для общения через сокеты с использованием asyncio 

[![Python 3.12.7](https://img.shields.io/badge/Python-3.12.7-000000?style=flat&logo=python&logoColor=FFFF00)](https://www.python.org/downloads/release/python-3127/)


## 🚀 Особенности  
- Создание чатов с автоматическим именованием  
- Подключение к нескольким чатам  
- Информация о чатах в реальном времени  
- Асинхронная обработка сообщений  
- Простое управление через CLI  
- Количество клиентов не ограничено

## 📦 Требования
- Запущенный [сервер](https://github.com/Navnica/ragerave-server.git)
- Python 3.12+  
- Установленные зависимости из `requirements.txt`  

## ⚙️ Установка  
```bash  
git clone https://github.com/Navnica/ragerave-client.git  
cd ragerave-client  
pip install -r requirements.txt  
```  

## 🔧 Настройка  
1. Отредактируйте `settings.py`:  
```python  
SERVER_IP = '127.0.0.1'  
SERVER_PORT = 8888  
```  

## 🖥 Использование  
### Основные команды  
```bash  
/create-chat [-n, --name] [имя]  
/connect [-n, --name] [имя]  
/info [-n, --name]  
/dconnect [-n, --name] [имя]  
```  

#### Пояснения
Такие команды как /create-chat, /info, /disconnect могут использоваться без аргумента --name, -n


## 🛠 Примеры  
```bash  
/create-chat -n МойЧат  
/connect --name МойЧат  
/info  
```  
[Python Version]: <https://www.python.org/downloads/release/python-3127/>
