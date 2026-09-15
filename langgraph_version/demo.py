#!/usr/bin/env python3
"""
Demo: تشغيل MirrorThread على LangGraph
"""

from graph import run_analysis
import json

SAMPLE_ENTRIES = [
    {
        "id": "1",
        "date": "2025-01-10",
        "content": "اليوم كنت سعيد جدا بنجاح المشروع في الشغل. شعرت بالامتنان والحماس.",
        "created_at": "2025-01-10T10:00:00",
    },
    {
        "id": "2",
        "date": "2025-03-15",
        "content": "العمل أصبح مرهقا. أشعر بالقلق والتوتر من الاجتماعات الكثيرة.",
        "created_at": "2025-03-15T10:00:00",
    },
    {
        "id": "3",
        "date": "2025-05-01",
        "content": "قررت أركز على صحتي. بدأت أمشي كل يوم وأشعر بتحسن وسلام داخلي.",
        "created_at": "2025-05-01T10:00:00",
    },
    {
        "id": "4",
        "date": "2025-07-20",
        "content": "المشروع الجديد في الشغل يثير حماسي جدا. أريد أتعلم مهارات جديدة وأنمو.",
        "created_at": "2025-07-20T10:00:00",
    },
    {
        "id": "5",
        "date": "2025-09-05",
        "content": "ما زلت قلقان من المستقبل المهني، لكن الرياضة والمشي بيساعدوني كثيرا على الهدوء.",
        "created_at": "2025-09-05T10:00:00",
    },
]


def main():
    print("=" * 60)
    print("  MirrorThread × LangGraph Demo")
    print("  Theme → Emotion → Narrative → FutureSelf")
    print("=" * 60)

    result = run_analysis(SAMPLE_ENTRIES, thread_id="demo-1")

    print("\n🧵 الخيوط الزمنية:")
    for t in result.get("threads", []):
        print(f"  • {t['theme']} ({t['occurrences']}×) — {t['trend']} — قوة {t['strength']}")

    print("\n💫 الأنماط العاطفية:")
    for p in result.get("patterns", []):
        print(f"  • {p['name']}: {p['description']}")

    print("\n🔗 روابط العاطفة ↔ الموضوع:")
    for link in result.get("emotion_theme_links", [])[:3]:
        print(f"  • {link['insight']}")

    print("\n✦ رسائل الذات المستقبلية:")
    for msg in result.get("future_messages", []):
        print(f"  [{msg['based_on']}] {msg['message'][:100]}...")

    print("\n📌 نقاط الاستمرارية:")
    for cp in result.get("continuity_points", []):
        print(f"  • {cp['type']}: {cp['advice'][:80]}...")

    print("\n📖 فصول الحياة:")
    for ch in result.get("life_chapters", []):
        print(f"  • {ch['title']} ({ch['entry_count']} ملاحظات)")

    print(f"\n✅ اكتمل التحليل في: {result.get('analyzed_at')}")
    print(f"   الخطوة الحالية: {result.get('current_step')}")


if __name__ == "__main__":
    main()
