import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def summarize_tool(title, url):
    """Ask Gemini Flash-Lite to describe the tool's likely purpose and tag a category."""
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