"""
Real LLM Connector for MirrorThread
====================================
يدعم أي endpoint متوافق مع OpenAI API (OpenAI, Groq, Together, Ollama, Fireworks...)
"""

import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
import config

SYSTEM_PROMPT = """أنت محلل أنماط زمنية متخصص في المذكرات الشخصية.
مهمتك: استخراج رؤى عميقة وغير سطحية من مذكرات المستخدم عبر الزمن.
أجب دائمًا بالعربية الفصحى الواضحة.
كن صادقًا ومباشرًا، وتجنب المجاملات الفارغة.
"""

def call_llm(user_prompt: str, system: str = SYSTEM_PROMPT, temperature: float = 0.7) -> Optional[str]:
    """استدعاء LLM حقيقي. يعيد None إذا فشل أو لم يكن مفعّلًا."""
    if not config.USE_REAL_LLM or not config.LLM_API_KEY:
        return None

    payload = {
        "model": config.LLM_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": 1200
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{config.LLM_BASE_URL.rstrip('/')}/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.LLM_API_KEY}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[LLM Error] {e}")
        return None


def enrich_with_llm(analysis: Dict[str, Any], entries: list) -> Dict[str, Any]:
    """
    يثري نتائج الوكلاء المحليين برؤى من LLM حقيقي إن وُجد.
    """
    if not config.USE_REAL_LLM or not config.LLM_API_KEY:
        analysis["llm_enriched"] = False
        analysis["llm_insight"] = None
        return analysis

    # بناء ملخص موجز للمذكرات
    summary_lines = []
    for e in sorted(entries, key=lambda x: x.get("date", ""))[-12:]:  # آخر 12 فقط
        summary_lines.append(f"[{e['date']}] {e['content'][:180]}")

    threads_summary = ", ".join(
        f"{t['theme']}({t['occurrences']}×, {t.get('trend','?')})"
        for t in analysis.get("threads", [])[:5]
    )

    prompt = f"""هذه ملخصات مذكرات المستخدم عبر الزمن:

{chr(10).join(summary_lines)}

الخيوط الزمنية المكتشفة محليًا: {threads_summary or 'لا يوجد بعد'}

المطلوب منك (أجب بشكل منظم):
1. أبرز نمط خفي لم يُذكر صراحة.
2. رسالة قصيرة وقوية من \"الذات المستقبلية\" (3-5 جمل).
3. نصيحة عملية واحدة قابلة للتنفيذ هذا الأسبوع.
"""

    insight = call_llm(prompt)
    analysis["llm_enriched"] = insight is not None
    analysis["llm_insight"] = insight
    return analysis
