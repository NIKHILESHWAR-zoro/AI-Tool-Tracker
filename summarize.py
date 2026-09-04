import os
import time
from google import genai
from google.genai import errors

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def summarize_tool(title, url, max_retries=3):
    """Ask Gemini Flash-Lite to describe the tool's likely purpose and tag a category.
    Retries with backoff on transient server errors (e.g. 503 UNAVAILABLE)."""
    prompt = f"""A new tool was just launched. Here's what we know:

Title: {title}
Link: {url}

In 2 short sentences, describe what this tool most likely does and who it's for,
based on the title. Then on a new line, give ONE category word
(e.g. "Coding", "Productivity", "Marketing", "Writing", "Data", "Design", "Voice", "Other").

Respond in EXACTLY this format, nothing else:
Summary: <2 sentences>
Category: <one word>
"""
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )
            text = resp.text
            summary, category = "", "Other"
            for line in text.splitlines():
                if line.startswith("Summary:"):
                    summary = line.replace("Summary:", "").strip()
                elif line.startswith("Category:"):
                    category = line.replace("Category:", "").strip()
            return summary, category
        except errors.ServerError as e:
            print(f"  Gemini server error on attempt {attempt}/{max_retries}: {e}")
            if attempt == max_retries:
                print(f"  Giving up on '{title}' after {max_retries} attempts.")
                return None, None
            time.sleep(5 * attempt)  # 5s, then 10s backoff before retrying