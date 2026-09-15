# MirrorThread

**AI Temporal Narrative Weaver** — Multi-agent system that discovers long-term personal patterns from journal entries.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

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

## Multi-Agent Architecture

| Agent | Responsibility |
|-------|----------------|
| **ThemeAgent** | Temporal threads + trend detection (rising/falling/stable) |
| **EmotionAgent** | Emotional patterns + Emotion↔Theme links |
| **NarrativeAgent** | Automatic life-chapter construction |
| **FutureSelfAgent** | Future-self messages + continuity advice |
| **Orchestrator** | Coordinates the agents in sequence |

---

## Features

- **Real LLM linking** — OpenAI-compatible (OpenAI, Groq, Together, Ollama…)
- **Improved pattern detection** — trends + intensity + correlations
- **Automation** — auto-analyze when enough new entries exist
- **Export** — clean Markdown report + JSON
- **Zero external dependencies** for the local engine (stdlib only)
- Beautiful dark RTL-ready web UI

---

## Quick Start

```bash
git clone https://github.com/Johanne012/MirrorThread.git
cd MirrorThread
python3 server.py
```

Open → [http://localhost:8765](http://localhost:8765)

---

## Enable Real LLM (optional)

Edit `config.py`:

```python
LLM_API_KEY = "sk-..."
LLM_BASE_URL = "https://api.openai.com/v1"   # or Groq / Together / Ollama
LLM_MODEL = "gpt-4o-mini"
USE_REAL_LLM = True
```

---

## Project Structure

```
MirrorThread/
├── server.py           # HTTP server + web UI
├── agents.py           # Theme / Emotion / Narrative / FutureSelf agents
├── llm_connector.py    # Real LLM integration
├── export.py           # Markdown + JSON export
├── config.py           # Configuration
├── data/               # Journal storage (auto-created)
└── exports/            # Generated reports (auto-created)
```

---

## Arabic Summary / ملخص عربي

**MirrorThread** نظام وكلاء متعدد يكتشف الخيوط الزمنية في مذكراتك الشخصية، يبني فصول حياة، ويرسل لك رسائل من "ذاتك المستقبلية".

- وكلاء متخصصون (Theme, Emotion, Narrative, FutureSelf)
- ربط حقيقي بأي LLM متوافق مع OpenAI API
- أتمتة + تصدير Markdown/JSON
- واجهة ويب عربية بالكامل

---

## License

MIT
