# 🤖 AI Tool Tracker

An autonomous agent that discovers newly launched AI tools every day, uses an LLM to
explain what each one does, and pushes you a notification on your phone — with a
polished web dashboard to browse the full history.

## How it works

```
Hacker News (Show HN) --> filter for AI --> clean titles --> dedupe (SQLite)
        --> Gemini summarizes purpose + category
        --> Telegram bot notifies you --> Streamlit dashboard shows history
```

Runs automatically once a day via GitHub Actions — no server to maintain.

## Tech stack
- **Data source**: Hacker News Algolia API (free, no key)
- **LLM**: Google Gemini (`gemini-3.5-flash-lite`) — free tier, no credit card required
- **Storage**: SQLite
- **Notifications**: Telegram Bot API (this is your "mobile app")
- **Dashboard**: Streamlit, with a custom card-grid UI, search, and category filters
- **Automation**: GitHub Actions (cron)

## Setup

### 1. Get your API keys
- **Gemini API key**: [aistudio.google.com](https://aistudio.google.com) → sign in with a
  Google account → "Get API key" → "Create API key". No credit card needed, ever, for the
  free tier.
- **Telegram bot token**: message [@BotFather](https://t.me/BotFather) on Telegram,
  send `/newbot`, follow the prompts, copy the token it gives you
- **Telegram chat ID**: message your new bot anything, then visit
  `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser and copy
  the `"chat":{"id": ...}` number

### 2. Run locally
```bash
git clone <your-repo-url>
cd ai-tool-tracker
pip install -r requirements.txt
cp .env.example .env   # then fill in your keys
```
Load the env vars (PowerShell):
```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]*)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
    }
}
```
Or on Mac/Linux: `export $(cat .env | xargs)`

Then:
```bash
python main.py          # runs the tracker once, sends any Telegram notifications
streamlit run app.py    # opens the dashboard at localhost:8501
```

### 3. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: AI Tool Tracker"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### 4. Enable the daily automation
In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**,
add `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.
The workflow in `.github/workflows/daily_check.yml` will now run every day automatically
(and you can trigger it manually from the **Actions** tab anytime to test it).

### 5. Deploy the dashboard
Go to [share.streamlit.io](https://share.streamlit.io), connect your GitHub repo,
point it at `app.py`, add the same three secrets under the app's settings (TOML format:
`GEMINI_API_KEY = "..."`). You'll get a public URL that works great from your phone's
browser too.

### 6. Use it on mobile
- **Notifications**: open a chat with your bot in the Telegram app — you'll get pushed
  a message the moment a new AI tool is found
- **Dashboard**: open your Streamlit URL in your phone's browser and "Add to Home Screen"
  for an app-like icon

## Project structure
```
ai-tool-tracker/
├── fetch_tools.py       # pulls + filters new AI launches from Hacker News
├── utils.py             # title cleanup (strips "Show HN:" prefix)
├── summarize.py         # Gemini generates purpose summary + category
├── database.py          # SQLite storage + dedup tracking
├── telegram_notify.py   # sends the Telegram push
├── main.py              # orchestrates the full pipeline
├── app.py               # Streamlit dashboard (card grid, search, filters)
└── .github/workflows/daily_check.yml   # daily cron automation
```

## Resume bullet (edit as needed)
> Built and deployed an autonomous agent that monitors new AI tool launches daily,
> uses an LLM (Google Gemini) to generate purpose summaries and categorize each tool,
> and delivers real-time mobile notifications via Telegram; automated end-to-end with
> GitHub Actions and deployed a Streamlit dashboard with a custom UI.

## Possible extensions
- Add Product Hunt's GraphQL API as a second source
- Add a weekly digest summary instead of (or alongside) real-time pings
- Let users type a category in Telegram to get filtered summaries (adds an
  agentic "tool-use" loop)
- Swap SQLite for a hosted Postgres (e.g. Supabase) if you want the dashboard
  to always show fresh data without committing the DB file back to git