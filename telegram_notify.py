import os
import requests
from database import add_subscriber, get_all_subscribers, get_meta, set_meta

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def poll_new_subscribers():
    """
    Check for anyone who has messaged the bot since the last check, and register
    them as a subscriber. Sends each brand-new subscriber a welcome message.
    Returns the number of new subscribers found.
    """
    offset = get_meta("telegram_update_offset")
    params = {"timeout": 0}
    if offset:
        params["offset"] = int(offset)

    resp = requests.get(f"{API_URL}/getUpdates", params=params, timeout=15)
    resp.raise_for_status()
    updates = resp.json().get("result", [])

    new_subscriber_count = 0
    highest_update_id = None

    for update in updates:
        highest_update_id = update["update_id"]
        message = update.get("message")
        if not message:
            continue

        chat = message.get("chat", {})
        chat_id = chat.get("id")
        username = chat.get("username") or chat.get("first_name") or "unknown"
        if chat_id is None:
            continue

        is_new = add_subscriber(chat_id, username)
        if is_new:
            new_subscriber_count += 1
            _send_to_one(
                chat_id,
                "👋 You're subscribed to AI Tool Tracker! I'll message you here "
                "whenever a new AI tool launches, with a quick summary of what it does."
            )

    if highest_update_id is not None:
        set_meta("telegram_update_offset", highest_update_id + 1)

    return new_subscriber_count


def _send_to_one(chat_id, text):
    try:
        resp = requests.post(f"{API_URL}/sendMessage", data={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False,
        }, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"  Failed to notify {chat_id}: {e}")


def broadcast_message(text):
    """Send a message to every registered subscriber."""
    for chat_id in get_all_subscribers():
        _send_to_one(chat_id, text)