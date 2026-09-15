#!/usr/bin/env python3
"""
Demo: MirrorThread × LangGraph
رؤية مستقبلية تدمج التقنية + التطوير + الطاقة
"""

from graph import run_analysis

SAMPLE_ENTRIES = [
    {
        "id": "1",
        "date": "2025-01-12",
        "content": "بدأت أتعلم أساسيات الذكاء الاصطناعي والطاقة المتجددة. أشعر بفضول كبير تجاه كيف يمكن للتقنية أن تسرّع الانتقال الطاقي.",
        "created_at": "2025-01-12T10:00:00",
    },
    {
        "id": "2",
        "date": "2025-03-20",
        "content": "العمل في مشروع أتمتة أنظمة المراقبة للطاقة الشمسية مرهق لكنه مثير. أشعر بالقلق من سرعة التطور وضرورة مواكبته.",
        "created_at": "2025-03-20T10:00:00",
    },
    {
        "id": "3",
        "date": "2025-05-08",
        "content": "قرأت عن بطاريات الجيل القادم وتخزين الطاقة. فكرت كيف يمكنني المساهمة في بناء أدوات مفتوحة المصدر لهذا المجال.",
        "created_at": "2025-05-08T10:00:00",
    },
    {
        "id": "4",
        "date": "2025-07-15",
        "content": "المشروع الجديد يربط بيانات الاستهلاك مع نماذج تنبؤية. أشعر بالحماس والنمو. أريد أتعلم المزيد عن الوكلاء الأذكياء والأنظمة الموزعة.",
        "created_at": "2025-07-15T10:00:00",
    },
    {
        "id": "5",
        "date": "2025-09-10",
        "content": "ما زلت قلقان أحيانًا من مستقبل الطاقة والذكاء الاصطناعي، لكن الرياضة والتأمل بيساعدوني. أؤمن أن التقنية النظيفة تحتاج مطورين يشعرون بالمسؤولية.",
        "created_at": "2025-09-10T10:00:00",
    },
]


def main():
    print("=" * 64)
    print("  MirrorThread × LangGraph")
    print("  رؤية مستقبلية: تقنية · تطوير · طاقة")
    print("  Theme → Emotion → Narrative → FutureSelf → VisionTech")
    print("=" * 64)

    result = run_analysis(SAMPLE_ENTRIES, thread_id="vision-demo")

    print("\n🧵 الخيوط الزمنية:")
    for t in result.get("threads", []):
        trend = {"rising": "تصاعد ↗", "falling": "انحسار ↘", "stable": "مستقر →"}.get(t["trend"], t["trend"])
        print(f"  • {t['theme']} ({t['occurrences']}×) — {trend} — قوة {t['strength']}")

    print("\n💫 الأنماط العاطفية:")
    for p in result.get("patterns", []):
        print(f"  • {p['name']}: {p['description']}")

    print("\n🔗 روابط العاطفة ↔ الموضوع:")
    for link in result.get("emotion_theme_links", [])[:4]:
        print(f"  • {link['insight']}")

    print("\n✦ رسائل الذات المستقبلية + الرؤية التقنية-الطاقية:")
    for msg in result.get("future_messages", []):
        print(f"\n  [{msg.get('from_', msg.get('based_on'))}]")
        print(f"  {msg['message']}")

    print("\n📌 نقاط الاستمرارية:")
    for cp in result.get("continuity_points", []):
        print(f"  • ({cp['type']}) {cp['advice'][:110]}...")

    print("\n📖 فصول الحياة:")
    for ch in result.get("life_chapters", []):
        print(f"  • {ch['title']} ({ch['entry_count']} ملاحظات)")

    print(f"\n✅ اكتمل التحليل — الخطوة: {result.get('current_step')}")
    print(f"   الوقت: {result.get('analyzed_at')}")


if __name__ == "__main__":
    main()
