# MirrorThread

**AI Temporal Narrative Weaver** — Multi-agent system that discovers long-term personal patterns from journal entries.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LangGraph](https://img.shields.io/badge/LangGraph-Ready-purple.svg)](https://github.com/langchain-ai/langgraph)

---

## What makes it unique?

Most AI systems react to the **present moment**.  
**MirrorThread** treats **time** as a first-class citizen.

You write journal entries (even months or years apart). The system:

1. Discovers **temporal threads** — recurring themes across time
2. Detects whether each thread is **rising / falling / stable**
3. Links emotions to themes (Emotion ↔ Theme correlations)
4. Builds automatic **life chapters**
5. Generates messages from your **future self** + practical continuity points
6. Optionally enriches everything with a real LLM

This is not a chatbot. It is personal temporal archaeology powered by agents.

---

## Two Editions

### 1. Classic (stdlib only)
Zero external dependencies. Fast local multi-agent engine + beautiful dark RTL web UI.

```bash
python3 server.py
# → http://localhost:8765
```

### 2. LangGraph Edition (recommended for production)
Full LangGraph graph with:
- Typed shared state
- Conditional edges
- Checkpointing (MemorySaver → ready for Postgres)
- Clear node separation (Theme → Emotion → Narrative → FutureSelf)

```bash
cd langgraph_version
python3 demo.py
```

---

## Multi-Agent Architecture

| Agent / Node | Responsibility |
|--------------|----------------|
| **ThemeAgent** | Temporal threads + trend detection (rising/falling/stable) |
| **EmotionAgent** | Emotional patterns + Emotion↔Theme links |
| **NarrativeAgent** | Automatic life-chapter construction |
| **FutureSelfAgent** | Future-self messages + continuity advice |
| **Orchestrator / Graph** | Coordinates the agents (classic) or LangGraph runtime |

---

## Features

- **Real LLM linking** — OpenAI-compatible (OpenAI, Groq, Together, Ollama…)
- **Improved pattern detection** — trends + intensity + correlations
- **Automation** — auto-analyze when enough new entries exist
- **Export** — clean Markdown report + JSON
- **LangGraph ready** — durable execution, checkpointing, human-in-the-loop path
- **Zero external dependencies** for the classic engine
- Beautiful dark RTL-ready web UI

---

## Quick Start (Classic)

```bash
git clone https://github.com/Johanne012/MirrorThread.git
cd MirrorThread
python3 server.py
```

Open → [http://localhost:8765](http://localhost:8765)

### Enable Real LLM (optional)

Edit `config.py`:

```python
LLM_API_KEY = "sk-..."
LLM_BASE_URL = "https://api.openai.com/v1"
LLM_MODEL = "gpt-4o-mini"
USE_REAL_LLM = True
```

---

## LangGraph Edition

```bash
pip install langgraph
cd langgraph_version
python3 demo.py
```

The graph flow:

```
START → theme → (conditional) → emotion → narrative → future_self → finalize → END
```

Checkpointing is enabled by default (`MemorySaver`). Swap to `PostgresSaver` for production durability.

---

## Project Structure

```
MirrorThread/
├── server.py                 # Classic HTTP server + web UI
├── agents.py                 # Classic multi-agent engine
├── llm_connector.py          # Real LLM integration
├── export.py                 # Markdown + JSON export
├── config.py                 # Configuration
├── langgraph_version/        # ★ Production-oriented LangGraph edition
│   ├── state.py
│   ├── nodes.py
│   ├── graph.py
│   ├── demo.py
│   └── __init__.py
├── data/                     # Journal storage (auto-created)
└── exports/                  # Generated reports
```

---

## Arabic Summary / ملخص عربي

**MirrorThread** نظام وكلاء متعدد يكتشف الخيوط الزمنية في مذكراتك الشخصية، يبني فصول حياة، ويرسل لك رسائل من "ذاتك المستقبلية".

- إصدار كلاسيكي (بدون مكتبات خارجية) + واجهة ويب
- إصدار **LangGraph** للإنتاج (checkpointing + توجيه شرطي + حالة مشتركة)
- ربط حقيقي بأي LLM متوافق مع OpenAI API
- أتمتة + تصدير Markdown/JSON

---

## License

MIT
