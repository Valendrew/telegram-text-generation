# N-Gram Text Generation

## Run the bot

Place the **json** with chats in the main folder and run:

```bash
python -m textgen
```

## Configuration file

- Create a **config.ini** file
- Retrieve your api id and hash from <https://my.telegram.org/>
- Add your bot name and bot token, which you can retrieve by writing to @BotFather on Telegram
- TELEGRAM_CHAT.ids is a string of space separated chat ids

```ini
[TELEGRAM_CHAT]
ids = 

[BOT]
name = 
id = 
hash = 
token = 
```
