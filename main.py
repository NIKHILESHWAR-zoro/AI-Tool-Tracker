import os
import time
from fetch_tools import fetch_new_ai_tools
from database import init_db, is_new, save_tool, add_subscriber
from summarize import summarize_tool
from telegram_notify import poll_new_subscribers, broadcast_message


def run():
    init_db()

    owner_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if owner_chat_id:
        add_subscriber(owner_chat_id, "owner")

    new_subs = poll_new_subscribers()
    if new_subs:
        print(f"Registered {new_subs} new subscriber(s)")

    tools = fetch_new_ai_tools(hours_back=24)
    print(f"Found {len(tools)} candidate launches")

    new_count = 0
    for tool in tools:
        if not is_new(tool["id"]):
            continue

        summary, category = summarize_tool(tool["title"], tool["url"])
        if summary is None:
            print(f"  Skipping '{tool['title']}' due to repeated API errors.")
            continue

        tool["summary"] = summary
        tool["category"] = category
        save_tool(tool)

        message = (
            f"🚀 *New AI Tool: {tool['title']}*\n\n"
            f"{summary}\n\n"
            f"Category: {category}\n"
            f"Link: {tool['url']}"
        )
        broadcast_message(message)
        new_count += 1
        time.sleep(1)

    print(f"Notified about {new_count} new tools (sent to all subscribers)")


if __name__ == "__main__":
    run()