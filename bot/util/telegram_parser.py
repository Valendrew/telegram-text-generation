import json


def read_telegram_file(filename: str, specific_ids: list[int] = []) -> list:
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        chats = data["chats"]["list"]
        if len(specific_ids) > 0:
            return [v["messages"] for v in chats if v["id"] in specific_ids]
        else:
            return chats
    except:
        return list()


# for each message: 'type'=='message' and retrieve 'text'
def parse_telegram_file(data: list, message_type: list[str] = ["message"]) -> list[str]:
    raw_data = [
        msg["text"]
        for chat in data
        for msg in chat
        if (msg["type"] in message_type and isinstance(msg["text"], str) and len(msg["text"])> 0)
    ]
    return raw_data
