# MirrorThread

**AI Temporal Narrative Weaver** with a forward-looking vision toward **Technology · Development · Energy**.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LangGraph](https://img.shields.io/badge/LangGraph-Ready-purple.svg)](https://github.com/langchain-ai/langgraph)

---

## Core Idea

Most AI systems react to the present moment.  
**MirrorThread** treats **time** as a first-class citizen and projects personal patterns into a larger future of technology, software development, and energy transition.

You write journal entries. The system:

1. Discovers **temporal threads** (work, health, growth, tech, energy…)
2. Detects whether each thread is **rising / falling / stable**
3. Links emotions to themes
4. Builds automatic **life chapters**
5. Generates messages from your **future self**
6. Adds a **VisionTech** layer that connects your personal patterns to the worlds of **AI, software development, and clean energy**

This is personal temporal archaeology aimed at builders of the next decade.

---

## Two Editions

### Classic (stdlib only)
```bash
python3 server.py
# → http://localhost:8765
```

### LangGraph Edition (recommended)
Full production-oriented graph:

```
START → theme → emotion → narrative → future_self → vision_tech → finalize → END
```

```bash
pip install langgraph
cd langgraph_version
python3 demo.py
```

---

## Vision Layer (Tech · Development · Energy)

The new `vision_tech_node` reads your dominant threads and emotions and produces forward-looking messages such as:

- How your recurring themes intersect with AI and the energy transition
- How curiosity or anxiety can become fuel for responsible building
- Practical continuity points that link personal life to systemic challenges

Themes now include: **تقنية · تطوير · طاقة · مستقبل** in addition to the classic personal themes.

---

## Architecture

| Node / Agent | Role |
|--------------|------|
| ThemeAgent | Temporal threads + trend detection |
| EmotionAgent | Emotional patterns + Emotion↔Theme links |
| NarrativeAgent | Life chapters |
| FutureSelfAgent | Personal future-self messages |
| **VisionTechAgent** | Links personal patterns to technology, development & energy futures |
| Orchestrator / Graph | LangGraph runtime with checkpointing |

---

## Quick Start

```bash
git clone https://github.com/Johanne012/MirrorThread.git
cd MirrorThread

# Classic UI
python3 server.py

# LangGraph vision demo
cd langgraph_version
python3 demo.py
```

---

## Project Structure

```
MirrorThread/
├── server.py / agents.py / ...     # Classic edition
├── langgraph_version/
│   ├── state.py
│   ├── nodes.py          # includes VisionTech
│   ├── graph.py
│   └── demo.py           # Tech + Energy oriented sample
└── README.md
```

---

## Arabic Summary

**MirrorThread** يكتشف الخيوط الزمنية في مذكراتك ويربطها برؤية مستقبلية في **التقنية والتطوير والطاقة**.

- إصدار كلاسيكي + واجهة ويب
- إصدار LangGraph مع عقدة **VisionTech**
- رسائل من الذات المستقبلية + إسقاطات على عالم الذكاء الاصطناعي والانتقال الطاقي

---

## License

MIT
