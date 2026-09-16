#!/usr/bin/env python3
"""
Demo: MirrorThread × LangGraph
توليد الأفكار والرؤى والحلول — طاقة × ذكاء اصطناعي × بنية تحتية × سياسات × تمويل
"""

from graph import run_analysis

SAMPLE_ENTRIES = [
    {
        "id": "1",
        "date": "2025-01-12",
        "content": "أفكر كثيرًا في كيف يمكن للذكاء الاصطناعي أن يغيّر طريقة تمويل مشاريع الطاقة المتجددة، وليس فقط تشغيلها. أشعر بفضول كبير تجاه المؤسسات المالية والصناديق السيادية.",
        "created_at": "2025-01-12T10:00:00",
    },
    {
        "id": "2",
        "date": "2025-03-20",
        "content": "البنية التحتية للشبكات في منطقتنا تحتاج تفكيرًا جديدًا. القلق من الانقطاعات والتكاليف يجعلني أتساءل عن سياسات أفضل وحوافز للمرونة.",
        "created_at": "2025-03-20T10:00:00",
    },
    {
        "id": "3",
        "date": "2025-05-08",
        "content": "قرأت عن صناديق الضمان ومشاريع التجميع (Aggregation). فكرة تحويل المشاريع الصغيرة إلى أصل قابل للتمويل تبدو واعدة جدًا للمنطقة العربية.",
        "created_at": "2025-05-08T10:00:00",
    },
    {
        "id": "4",
        "date": "2025-07-15",
        "content": "أريد أن أساهم في حلول تربط مراكز البيانات بالطاقة المتجددة. النمو في الطلب على الحوسبة يجب أن يتحول إلى فرصة للشبكات المرنة لا عبئًا.",
        "created_at": "2025-07-15T10:00:00",
    },
    {
        "id": "5",
        "date": "2025-09-10",
        "content": "ما زلت قلقان أحيانًا من بطء السياسات، لكن الفضول أقوى. أؤمن أن الجامعات والصناديق والبنوك يمكنها إطلاق نوافذ جديدة للطاقة الرقمية.",
        "created_at": "2025-09-10T10:00:00",
    },
]


def main():
    print("=" * 64)
    print("  MirrorThread × LangGraph")
    print("  توليد الأفكار والرؤى والحلول")
    print("  طاقة · ذكاء اصطناعي · بنية تحتية · سياسات · تمويل")
    print("=" * 64)

    result = run_analysis(SAMPLE_ENTRIES, thread_id="solutions-demo")

    print("\n🧵 الخيوط الزمنية:")
    for t in result.get("threads", []):
        trend = {"rising": "تصاعد ↗", "falling": "انحسار ↘", "stable": "مستقر →"}.get(t["trend"], t["trend"])
        print(f"  • {t['theme']} ({t['occurrences']}×) — {trend}")

    print("\n✦ الرؤى والحلول المولَّدة:")
    for msg in result.get("future_messages", []):
        print(f"\n  [{msg.get('from_', '')}]")
        print(f"  {msg['message']}")

    print("\n📌 نقاط الاستمرارية:")
    for cp in result.get("continuity_points", []):
        print(f"\n  • ({cp['type']})")
        print(f"    {cp['advice']}")

    print(f"\n✅ اكتمل — الخطوة: {result.get('current_step')}")


if __name__ == "__main__":
    main()
