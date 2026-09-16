"""
MirrorThread LangGraph Nodes
كل Node = وكيل متخصص
VisionTech مدمج مع تطبيقات AI في الطاقة + أدوات مفتوحة المصدر + سيناريوهات عربية
"""

from collections import defaultdict
from datetime import datetime
from typing import Dict, Any, List
import hashlib
import random
import re

try:
    from .state import MirrorState
except ImportError:
    from state import MirrorState

EMOTION_KEYWORDS = {
    "فرح": ["سعيد", "فرحان", "مبسوط", "نجح", "فرحة", "ابتسامة", "حماس", "أمل", "متحمس", "مبتهج", "مسرور"],
    "حزن": ["حزين", "يائس", "تعبان", "مكتئب", "ألم", "دموع", "وحدة", "فقد", "خسارة", "حزن", "أسى"],
    "غضب": ["زعلان", "غاضب", "مستاء", "محبط", "ظلم", "غضب", "متضايق", "عصبي", "منزعج"],
    "قلق": ["قلقان", "خوف", "متوتر", "مضغوط", "قلق", "رهبة", "عدم استقرار", "خايف", "متخوف"],
    "امتنان": ["شكر", "ممتن", "الحمد", "نعمة", "تقدير", "ممتن", "شاكر"],
    "فضول": ["أتساءل", "فضولي", "اكتشاف", "تعلم", "جديد", "استكشاف", "مندهش"],
    "إرهاق": ["مرهق", "تعبان", "منهك", "إجهاد", "ضغط", "إرهاق", "مرهق جدًا"],
    "سلام": ["مرتاح", "هادئ", "سكينة", "سلام", "اطمئنان", "هدوء"],
}

THEME_KEYWORDS = {
    "عمل": ["شغل", "وظيفة", "مشروع", "اجتماع", "مدير", "زميل", "ترقية", "شركة", "عمل", "مكتب", "مهمة", "ديدلاين"],
    "علاقات": ["صديق", "حبيب", "عائلة", "أم", "أب", "أخ", "زوج", "علاقة", "ناس", "شريك", "رفقة"],
    "صحة": ["رياضة", "نوم", "أكل", "تعب", "صحة", "جيم", "مشي", "مرض", "دواء", "طبيب", "لياقة"],
    "نمو": ["تعلم", "كتاب", "دورة", "مهارة", "تطور", "هدف", "طموح", "خطة", "تطوير", "نمو"],
    "إبداع": ["كتابة", "رسم", "موسيقى", "فكرة", "إبداع", "فن", "تصميم", "ابتكار"],
    "روحانيات": ["صلاة", "تأمل", "معنى", "وجود", "سلام", "إيمان", "سكينة", "روح"],
    "مال": ["فلوس", "راتب", "مصروف", "ادخار", "دين", "استثمار", "ميزانية", "مال"],
    "وقت": ["وقت", "مشغول", "فراغ", "تأجيل", "تأخير", "استعجال", "جدول"],
    "تقنية": ["تقنية", "تكنولوجيا", "برمجة", "كود", "ذكاء اصطناعي", "AI", "آلة", "روبوت", "سحابة", "بيانات", "خوارزمية", "نظام", "تطبيق", "منصة", "API", "LLM", "وكيل", "أتمتة"],
    "تطوير": ["تطوير", "برمجيات", "هندسة", "ابتكار", "منتج", "نسخة", "إصدار", "تحديث", "تحسين", "بناء", "تصميم نظام", "معمارية", "مقياس", "نمو تقني"],
    "طاقة": ["طاقة", "كهرباء", "شمسية", "متجددة", "بطارية", "شبكة", "استدامة", "بيئة", "كربون", "كفاءة", "توليد", "تخزين", "طاقة نظيفة", "انتقال طاقي"],
    "مستقبل": ["مستقبل", "رؤية", "تحول", "ثورة", "جيل قادم", "2030", "2050", "ابتكار جذري", "نموذج جديد", "فرصة", "تحدي عالمي"],
}


def _detect_keywords(text: str, keyword_map: Dict[str, List[str]]) -> Dict[str, int]:
    text_lower = text.lower()
    scores = {}
    for label, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[label] = score
    return scores


def _detect_trend(scores: List[int]) -> str:
    if len(scores) < 3:
        return "stable"
    mid = len(scores) // 2
    first = sum(scores[:mid]) / max(1, mid)
    second = sum(scores[mid:]) / max(1, len(scores) - mid)
    if second > first * 1.4:
        return "rising"
    if second < first * 0.6:
        return "falling"
    return "stable"


def theme_node(state: MirrorState) -> Dict[str, Any]:
    entries = state.get("entries", [])
    if not entries:
        return {"current_step": "theme_done", "threads": []}
    sorted_entries = sorted(entries, key=lambda e: e.get("date", ""))
    theme_timeline = defaultdict(list)
    for entry in sorted_entries:
        themes = _detect_keywords(entry["content"], THEME_KEYWORDS)
        for theme, score in themes.items():
            theme_timeline[theme].append({"date": entry["date"], "score": score, "snippet": entry["content"][:120]})
    threads = []
    for theme, occurrences in theme_timeline.items():
        if len(occurrences) < 2:
            continue
        dates = [o["date"] for o in occurrences]
        scores = [o["score"] for o in occurrences]
        threads.append({
            "id": hashlib.md5(theme.encode()).hexdigest()[:8],
            "theme": theme,
            "occurrences": len(occurrences),
            "first_seen": min(dates),
            "last_seen": max(dates),
            "strength": sum(scores),
            "avg_intensity": round(sum(scores) / len(scores), 2),
            "trend": _detect_trend(scores),
            "samples": [o["snippet"] for o in occurrences[:4]],
        })
    threads.sort(key=lambda t: (t["strength"], t["occurrences"]), reverse=True)
    top = threads[0]["theme"] if threads else None
    return {"threads": threads, "top_theme": top, "current_step": "theme_done"}


def emotion_node(state: MirrorState) -> Dict[str, Any]:
    entries = state.get("entries", [])
    if not entries:
        return {"current_step": "emotion_done", "patterns": [], "emotion_theme_links": []}
    emotion_timeline = defaultdict(list)
    emotion_theme_pairs = defaultdict(int)
    for entry in entries:
        emotions = _detect_keywords(entry["content"], EMOTION_KEYWORDS)
        themes = _detect_keywords(entry["content"], THEME_KEYWORDS)
        for emotion, score in emotions.items():
            emotion_timeline[emotion].append({"date": entry["date"], "score": score})
            for theme in themes:
                emotion_theme_pairs[(emotion, theme)] += score
    patterns = []
    for emotion, occs in emotion_timeline.items():
        if len(occs) >= 2:
            scores = [o["score"] for o in occs]
            patterns.append({
                "type": "عاطفي",
                "name": f"نمط {emotion}",
                "emotion": emotion,
                "frequency": len(occs),
                "intensity": round(sum(scores) / len(scores), 2),
                "description": f"ظهر شعور «{emotion}» في {len(occs)} مناسبات. متوسط الشدة: {round(sum(scores)/len(scores),1)}",
            })
    links = []
    for (emotion, theme), score in sorted(emotion_theme_pairs.items(), key=lambda x: -x[1])[:6]:
        links.append({
            "emotion": emotion,
            "theme": theme,
            "strength": score,
            "insight": f"عندما يظهر موضوع «{theme}» غالبًا ما يكون مصحوبًا بشعور «{emotion}»",
        })
    dominant = max(emotion_timeline.keys(), key=lambda e: len(emotion_timeline[e])) if emotion_timeline else None
    return {"patterns": patterns, "emotion_theme_links": links, "dominant_emotion": dominant, "current_step": "emotion_done"}


def narrative_node(state: MirrorState) -> Dict[str, Any]:
    entries = state.get("entries", [])
    if not entries:
        return {"current_step": "narrative_done", "life_chapters": []}
    sorted_entries = sorted(entries, key=lambda e: e.get("date", ""))
    chapters = []
    chunk_size = 4
    for i in range(0, len(sorted_entries), chunk_size):
        chunk = sorted_entries[i:i + chunk_size]
        all_themes = defaultdict(int)
        all_emotions = defaultdict(int)
        for e in chunk:
            for t, s in _detect_keywords(e["content"], THEME_KEYWORDS).items():
                all_themes[t] += s
            for emo, s in _detect_keywords(e["content"], EMOTION_KEYWORDS).items():
                all_emotions[emo] += s
        dominant_themes = sorted(all_themes, key=all_themes.get, reverse=True)[:3]
        dominant_emotions = sorted(all_emotions, key=all_emotions.get, reverse=True)[:2]
        if dominant_themes and dominant_emotions:
            title = f"فصل {dominant_themes[0]} و{dominant_emotions[0]} — {chunk[0]['date']}"
        elif dominant_themes:
            title = f"فصل {dominant_themes[0]} — {chunk[0]['date']}"
        else:
            title = f"فصل {chunk[0]['date']}"
        chapters.append({
            "title": title,
            "start": chunk[0]["date"],
            "end": chunk[-1]["date"],
            "entry_count": len(chunk),
            "dominant_themes": dominant_themes,
            "dominant_emotions": dominant_emotions,
            "summary_hint": f"فترة يغلب عليها {', '.join(dominant_themes[:2]) if dominant_themes else 'تنوع'}",
        })
    return {"life_chapters": chapters, "current_step": "narrative_done"}


def future_self_node(state: MirrorState) -> Dict[str, Any]:
    threads = state.get("threads", [])
    patterns = state.get("patterns", [])
    links = state.get("emotion_theme_links", [])
    messages = []
    continuity_points = []
    if threads:
        top = threads[0]
        templates = [
            f"خيط «{top['theme']}» ظهر {top['occurrences']} مرات منذ {top['first_seen']}. هذا ليس ظرفًا عابرًا — إنه جزء من هويتك الحالية. اسأل نفسك: هل ما زلت تتعامل معه بنفس الطريقة؟",
            f"من موقعي في المستقبل أرى أن «{top['theme']}» كان محوريًا. الاتجاه الحالي: {top.get('trend', 'مستقر')}. استمر في مراقبته بصدق.",
            f"قوة خيط «{top['theme']}» = {top['strength']}. لو كنت مكانك الآن لجعلتُ منه موضوع تأمل أسبوعي قصير.",
        ]
        messages.append({"from_": "ذاتك المستقبلية", "based_on": top["theme"], "tone": "تأملي", "message": random.choice(templates)})
        if top.get("trend") == "rising":
            continuity_points.append({"type": "تصاعد", "theme": top["theme"], "advice": f"خيط «{top['theme']}» في تصاعد. خصص وقتًا واعيًا له كل أسبوع قبل أن يتحول إلى ضغط."})
        elif top.get("trend") == "falling":
            continuity_points.append({"type": "انحسار", "theme": top["theme"], "advice": f"خيط «{top['theme']}» يتراجع. هل هذا مقصود؟ أم أنك تتجاهل شيئًا مهمًا؟"})
    if len(threads) >= 2:
        names = " و ".join(t["theme"] for t in threads[:3])
        messages.append({"from_": "ذاتك المستقبلية", "based_on": "تداخل الخيوط", "tone": "استراتيجي", "message": f"حياتك ليست أحداثًا منفصلة. الخيوط المتداخلة ({names}) تتحدث مع بعضها. في المستقبل ستدرك أن هذه المواضيع كانت تشكل نظامًا واحدًا. حاول أن تكتب يومًا عن العلاقة الخفية بينها."})
    if links:
        strongest = links[0]
        messages.append({"from_": "ذاتك المستقبلية", "based_on": f"{strongest['emotion']} + {strongest['theme']}", "tone": "عاطفي", "message": f"لاحظتُ ارتباطًا متكررًا بين شعور «{strongest['emotion']}» وموضوع «{strongest['theme']}». في المستقبل، عندما يظهر أحدهما، تذكر أن الآخر قريب. الوعي بهذا الارتباط يمنحك حرية أكبر."})
    if patterns:
        continuity_points.append({"type": "نمط عاطفي", "theme": patterns[0].get("emotion", "عام"), "advice": f"نمط «{patterns[0]['name']}» متكرر. اكتب عنه بوعي في المرة القادمة بدل أن تمر عليه مرور الكرام."})
    return {"future_messages": messages, "continuity_points": continuity_points, "current_step": "future_done", "analyzed_at": datetime.now().isoformat()}


def vision_tech_node(state: MirrorState) -> Dict[str, Any]:
    """VisionTech Agent — يربط الأنماط الشخصية بتطبيقات AI الحقيقية في الطاقة + أدوات مفتوحة + سيناريوهات عربية."""
    threads = state.get("threads", [])
    patterns = state.get("patterns", [])
    top_theme = state.get("top_theme")
    dominant_emotion = state.get("dominant_emotion")
    theme_names = {t.get("theme") for t in threads}
    vision_messages = []
    continuity = list(state.get("continuity_points", []))

    if "طاقة" in theme_names or "تقنية" in theme_names or top_theme in ("طاقة", "تقنية", "تطوير"):
        vision_messages.append({
            "from_": "رؤية مستقبلية · AI في الطاقة",
            "based_on": top_theme or "طاقة + تقنية",
            "tone": "استشرافي-تطبيقي",
            "message": (
                "الأنماط التي تتكرر لديك تتقاطع مع أهم تطبيقات الذكاء الاصطناعي في قطاع الطاقة اليوم:\n"
                "• التنبؤ الدقيق بإنتاج الرياح والطاقة الشمسية (يزيد القيمة المالية للطاقة المتجددة بنسبة تصل إلى 20%).\n"
                "• تحسين تشغيل الشبكات الذكية وكشف الأعطال (يقلل مدة الانقطاع 30-50% ويفتح سعات إضافية دون بناء خطوط جديدة).\n"
                "• الصيانة التنبؤية للتوربينات والمحولات (خفض التوقف غير المخطط حتى 30% وتكاليف الصيانة حتى 40%).\n"
                "• وكلاء أذكياء يديرون التخزين والتداول في أسواق الكهرباء بدقة عالية.\n\n"
                "خيطك الحالي ليس مجرد اهتمام شخصي — إنه إشارة إلى أنك قد تكون جزءًا من الجيل الذي يبني هذه الأنظمة. "
                "ابدأ بمشروع صغير يربط بيانات أو تنبؤًا أو أتمتة بمجال الطاقة."
            ),
        })
    else:
        vision_messages.append({
            "from_": "رؤية مستقبلية · AI في الطاقة",
            "based_on": "إعادة توجيه",
            "tone": "تحفيزي",
            "message": (
                "حتى لو لم تظهر «طاقة» أو «تقنية» بقوة في مذكراتك بعد، فإن الوعي الذاتي الذي تبنيه هنا هو الأساس. "
                "قطاع الطاقة يحتاج مطورين ومهندسين يفهمون الأنماط البشرية والتقنية معًا. "
                "التطبيقات الأكثر تأثيرًا حاليًا تشمل: التنبؤ بالطلب والإنتاج، الصيانة التنبؤية، إدارة البطاريات والهيدروجين، "
                "والوكلاء الأذكياء التي تتداول وتوازن الشبكات. اسأل نفسك: أي مهارة من مهاراتي يمكن أن تخدم أحد هذه المجالات؟"
            ),
        })

    if dominant_emotion in ("قلق", "إرهاق"):
        vision_messages.append({
            "from_": "رؤية مستقبلية · طاقة بشرية + شبكات",
            "based_on": dominant_emotion,
            "tone": "توازني",
            "message": (
                f"شعور «{dominant_emotion}» المتكرر لديك يشبه ما تواجهه الشبكات الكهربائية مع تزايد مصادر الطاقة المتقطعة. "
                "الذكاء الاصطناعي يساعد الشبكات على التنبؤ والتكيف بدل الانهيار. "
                "بنفس المنطق: استخدم أدوات الوعي (مثل هذه المذكرات) للتنبؤ بحالات الإرهاق والتعامل معها مبكرًا. "
                "الطاقة النظيفة تحتاج بشرًا لديهم طاقة مستدامة، لا محترقين."
            ),
        })
    elif dominant_emotion in ("فضول", "فرح", "امتنان", "حماس"):
        vision_messages.append({
            "from_": "رؤية مستقبلية · فضول تقني-طاقي",
            "based_on": dominant_emotion,
            "tone": "تمكيني",
            "message": (
                f"شعور «{dominant_emotion}» هو الوقود الأندر في عالم التقنية والطاقة. "
                "الفضول دفع نماذج التنبؤ بالرياح والطاقة الشمسية إلى مستويات غير مسبوقة، ودفع اكتشاف مواد البطاريات بوتيرة أسرع بمئات الآلاف من المرات. "
                "حافظ على هذا الفضول ووجّهه نحو مشكلة حقيقية: تحسين تخزين الطاقة، أو جعل الشبكات أكثر مرونة، أو بناء أدوات مفتوحة المصدر للصيانة التنبؤية."
            ),
        })

    continuity.append({
        "type": "تطبيق عملي · AI في الطاقة",
        "theme": "مستقبل",
        "advice": (
            "اختر واحدًا هذا الشهر:\n"
            "1) بيانات مفتوحة: استخدم بيانات NASA POWER أو Open-Meteo أو بيانات شركات الكهرباء المفتوحة، وجرب نموذج تنبؤ بسيط (scikit-learn أو Prophet أو LSTM خفيف).\n"
            "2) أدوات مفتوحة: اطلع على مشاريع مثل Open Energy Dashboard، أو مكتبات التنبؤ بالطاقة المتجددة على GitHub، أو أدوات الصيانة التنبؤية مفتوحة المصدر.\n"
            "3) سياق عربي/إقليمي: ركز على تحديات المنطقة (وفرة الشمس، شبكات قيد التحديث، الحاجة لتخزين، وأمن الطاقة). اكتب كيف يمكن لمهاراتك أن تخدم مشروعًا شمسيًا أو شبكيًا في بلدك.\n"
            "الهدف: ربط خيطك الشخصي بتطبيق حقيقي قابل للتنفيذ."
        ),
    })

    continuity.append({
        "type": "سيناريو عربي · طاقة + تقنية",
        "theme": "إقليمي",
        "advice": (
            "سيناريو سريع للمنطقة العربية:\n"
            "• الشمس وفيرة → التنبؤ الدقيق بالإنتاج الشمسي + إدارة التخزين يضاعفان القيمة.\n"
            "• الشبكات تتحدث → الصيانة التنبؤية وكشف الأعطال يقللان الانقطاعات المكلفة.\n"
            "• الطلب ينمو مع الذكاء الاصطناعي ومراكز البيانات → الحاجة لوكلاء يوازنون الحمل والطاقة المتجددة.\n"
            "اسأل نفسك: أين يمكن أن أضع مهارة واحدة من مهاراتي داخل أحد هذه المحاور خلال 90 يومًا؟"
        ),
    })

    return {
        "future_messages": vision_messages,
        "continuity_points": continuity,
        "current_step": "vision_done",
    }


def finalize_node(state: MirrorState) -> Dict[str, Any]:
    return {"current_step": "completed", "analyzed_at": datetime.now().isoformat()}
