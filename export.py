"""
Export utilities for MirrorThread
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
import config

os.makedirs(config.EXPORT_DIR, exist_ok=True)


def export_json(data: Dict, entries: List[Dict], filename: str = None) -> str:
    if not filename:
        filename = f"mirrorthread_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(config.EXPORT_DIR, filename)
    payload = {
        "exported_at": datetime.now().isoformat(),
        "entries_count": len(entries),
        "entries": entries,
        "analysis": data
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def export_markdown(data: Dict, entries: List[Dict], filename: str = None) -> str:
    if not filename:
        filename = f"mirrorthread_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    path = os.path.join(config.EXPORT_DIR, filename)

    lines = [
        "# MirrorThread — تقرير السرد الزمني",
        f"**تاريخ التصدير:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**عدد المذكرات:** {len(entries)}",
        "",
        "---",
        "",
        "## 🧵 الخيوط الزمنية",
        ""
    ]

    for t in data.get("threads", []):
        trend_ar = {"rising": "تصاعد ↗", "falling": "انحسار ↘", "stable": "مستقر →"}.get(t.get("trend"), "?")
        lines.append(f"### {t['theme']}")
        lines.append(f"- الظهور: **{t['occurrences']}** مرة")
        lines.append(f"- من {t['first_seen']} إلى {t['last_seen']}")
        lines.append(f"- القوة: {t['strength']} | الاتجاه: {trend_ar}")
        if t.get("samples"):
            lines.append("- عينات:")
            for s in t["samples"][:3]:
                lines.append(f"  - «{s}»")
        lines.append("")

    lines += ["## 💫 الأنماط العاطفية", ""]
    for p in data.get("patterns", []):
        lines.append(f"- **{p['name']}**: {p['description']}")
    lines.append("")

    if data.get("emotion_theme_links"):
        lines += ["## 🔗 روابط العاطفة ↔ الموضوع", ""]
        for link in data["emotion_theme_links"][:5]:
            lines.append(f"- {link['insight']}")
        lines.append("")

    lines += ["## ✦ رسائل من الذات المستقبلية", ""]
    for msg in data.get("future_messages", []):
        lines.append(f"**{msg['from']}** (بناءً على: {msg['based_on']})")
        lines.append(f"> {msg['message']}")
        lines.append("")

    if data.get("continuity_points"):
        lines += ["## 📌 نقاط الاستمرارية", ""]
        for cp in data["continuity_points"]:
            lines.append(f"- **{cp['type']}** ({cp['theme']}): {cp['advice']}")
        lines.append("")

    if data.get("life_chapters"):
        lines += ["## 📖 فصول الحياة", ""]
        for ch in data["life_chapters"]:
            lines.append(f"### {ch['title']}")
            lines.append(f"{ch['start']} → {ch['end']} | {ch['entry_count']} ملاحظات")
            lines.append("")

    if data.get("llm_insight"):
        lines += ["## 🧠 رؤية الـLLM الإضافية", "", data["llm_insight"], ""]

    lines += ["---", "", "## المذكرات الأصلية", ""]
    for e in sorted(entries, key=lambda x: x.get("date", "")):
        lines.append(f"### {e['date']}")
        lines.append(e["content"])
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path
