import streamlit as st
from database import init_db, get_all_tools
from utils import clean_title

st.set_page_config(page_title="AI Tool Tracker", page_icon="🤖", layout="wide")
init_db()

CATEGORY_STYLE = {
    "Coding":       {"emoji": "💻", "color": "#6366f1"},
    "Productivity": {"emoji": "⚡", "color": "#f59e0b"},
    "Marketing":    {"emoji": "📣", "color": "#ec4899"},
    "Writing":      {"emoji": "✍️", "color": "#10b981"},
    "Data":         {"emoji": "📊", "color": "#0ea5e9"},
    "Design":       {"emoji": "🎨", "color": "#a855f7"},
    "Voice":        {"emoji": "🎙️", "color": "#ef4444"},
    "Other":        {"emoji": "🔧", "color": "#64748b"},
}

st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .tool-card {
        background: #ffffff0d;
        border: 1px solid #ffffff1a;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 14px;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .tool-card:hover {
        transform: translateY(-2px);
        border-color: #ffffff40;
    }
    .tool-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .tool-summary {
        opacity: 0.85;
        font-size: 0.92rem;
        line-height: 1.4;
        margin-bottom: 10px;
    }
    .tool-meta {
        font-size: 0.78rem;
        opacity: 0.6;
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
        margin-bottom: 8px;
    }
    .hero {
        padding: 28px 32px;
        border-radius: 18px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        margin-bottom: 24px;
    }
    .hero h1 { color: white; margin: 0; font-size: 1.8rem; }
    .hero p { color: #ffffffd0; margin: 6px 0 0 0; font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

tools = get_all_tools()

st.markdown(f"""
<div class="hero">
    <h1>🤖 AI Tool Tracker</h1>
    <p>Autonomously discovered launches, summarized by Gemini — updated daily.</p>
</div>
""", unsafe_allow_html=True)

if not tools:
    st.info("No tools tracked yet. Run `python main.py` once, or wait for the daily GitHub Action.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Tools tracked", len(tools))
col2.metric("Categories", len(set(t["category"] for t in tools if t["category"])))
col3.metric("Latest", tools[0]["created_at"][:10] if tools else "—")

st.write("")

search_col, filter_col = st.columns([2, 3])
with search_col:
    search = st.text_input("🔍 Search", placeholder="Search by name...", label_visibility="collapsed")
with filter_col:
    categories = sorted(set(t["category"] for t in tools if t["category"]))
    chosen = st.multiselect("Filter by category", categories, label_visibility="collapsed",
                             placeholder="Filter by category")

filtered = tools
if search:
    filtered = [t for t in filtered if search.lower() in t["title"].lower()]
if chosen:
    filtered = [t for t in filtered if t["category"] in chosen]

st.write("")

if not filtered:
    st.warning("No tools match your search/filter.")
else:
    cols = st.columns(2)
    for i, t in enumerate(filtered):
        style = CATEGORY_STYLE.get(t["category"], CATEGORY_STYLE["Other"])
        title = clean_title(t["title"])
        with cols[i % 2]:
            st.markdown(f"""
            <div class="tool-card">
                <span class="badge" style="background:{style['color']}">
                    {style['emoji']} {t['category']}
                </span>
                <div class="tool-title">{title}</div>
                <div class="tool-summary">{t['summary']}</div>
                <div class="tool-meta">⭐ {t['points']} points · {t['created_at'][:10]}</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button("Visit tool →", t["url"], use_container_width=True)