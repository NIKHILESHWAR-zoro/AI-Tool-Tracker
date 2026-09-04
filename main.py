import time
from fetch_tools import fetch_new_ai_tools
from database import init_db, is_new, save_tool
from summarize import summarize_tool
from telegram_notify import send_telegram_message


def run():
    init_db()
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
        send_telegram_message(message)
        new_count += 1
        time.sleep(1)  # be polite to the APIs

    print(f"Notified about {new_count} new tools")


if __name__ == "__main__":
    run()
