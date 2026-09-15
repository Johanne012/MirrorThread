"""
MirrorThread Multi-Agent System
================================
وكلاء متخصصون يعملون معًا لاكتشاف الأنماط الزمنية.
"""

from collections import defaultdict
from datetime import datetime
import re
import hashlib
import random
from typing import List, Dict, Any

# ====================== Keyword Knowledge ======================
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
}


class BaseAgent:
    """الوكيل الأساسي"""
    name = "BaseAgent"

    def run(self, entries: List[Dict], context: Dict = None) -> Dict:
        raise NotImplementedError


class ThemeAgent(BaseAgent):
    """وكيل اكتشاف المواضيع والخيوط الزمنية"""
    name = "ThemeAgent"

    def run(self, entries: List[Dict], context: Dict = None) -> Dict:
        if not entries:
            return {"threads": [], "theme_evolution": {}}

        sorted_entries = sorted(entries, key=lambda e: e.get("date", ""))
        theme_timeline = defaultdict(list)

        for entry in sorted_entries:
            themes = self._detect(entry["content"])
            entry["themes"] = themes
            for theme, score in themes.items():
                theme_timeline[theme].append({
                    "date": entry["date"],
                    "score": score,
                    "snippet": entry["content"][:120],
                    "entry_id": entry.get("id")
                })

        threads = []
        for theme, occurrences in theme_timeline.items():
            if len(occurrences) < 2:
                continue
            dates = [o["date"] for o in occurrences]
            scores = [o["score"] for o in occurrences]
            # Trend detection
            trend = self._detect_trend(scores)
            threads.append({
                "id": hashlib.md5(theme.encode()).hexdigest()[:8],
                "theme": theme,
                "occurrences": len(occurrences),
                "first_seen": min(dates),
                "last_seen": max(dates),
                "strength": sum(scores),
                "avg_intensity": round(sum(scores) / len(scores), 2),
                "trend": trend,  # rising / falling / stable
                "samples": [o["snippet"] for o in occurrences[:4]]
            })

        threads.sort(key=lambda t: (t["strength"], t["occurrences"]), reverse=True)

        # Evolution map
        evolution = {t["theme"]: t["trend"] for t in threads}

        return {
            "threads": threads,
            "theme_evolution": evolution,
            "top_theme": threads[0]["theme"] if threads else None
        }

    def _detect(self, text: str) -> Dict[str, int]:
        text_lower = text.lower()
        scores = {}
        for theme, keywords in THEME_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[theme] = score
        return scores

    def _detect_trend(self, scores: List[int]) -> str:
        if len(scores) < 3:
            return "stable"
        first_half = sum(scores[:len(scores)//2]) / max(1, len(scores)//2)
        second_half = sum(scores[len(scores)//2:]) / max(1, len(scores) - len(scores)//2)
        if second_half > first_half * 1.4:
            return "rising"
        if second_half < first_half * 0.6:
            return "falling"
        return "stable"


class EmotionAgent(BaseAgent):
    """وكيل التحليل العاطفي والأنماط الشعورية"""
    name = "EmotionAgent"

    def run(self, entries: List[Dict], context: Dict = None) -> Dict:
        if not entries:
            return {"patterns": [], "emotion_theme_links": [], "dominant_emotion": None}

        emotion_timeline = defaultdict(list)
        emotion_theme_pairs = defaultdict(int)

        for entry in entries:
            emotions = self._detect(entry["content"])
            entry["emotions"] = emotions
            themes = entry.get("themes", {})

            for emotion, score in emotions.items():
                emotion_timeline[emotion].append({
                    "date": entry["date"],
                    "score": score
                })
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
                    "description": f"ظهر شعور «{emotion}» في {len(occs)} مناسبات. متوسط الشدة: {round(sum(scores)/len(scores),1)}"
                })

        # أقوى الروابط بين العاطفة والموضوع
        links = []
        for (emotion, theme), score in sorted(emotion_theme_pairs.items(), key=lambda x: -x[1])[:6]:
            links.append({
                "emotion": emotion,
                "theme": theme,
                "strength": score,
                "insight": f"عندما يظهر موضوع «{theme}» غالبًا ما يكون مصحوبًا بشعور «{emotion}»"
            })

        dominant = max(emotion_timeline.keys(), key=lambda e: len(emotion_timeline[e])) if emotion_timeline else None

        return {
            "patterns": patterns,
            "emotion_theme_links": links,
            "dominant_emotion": dominant
        }

    def _detect(self, text: str) -> Dict[str, int]:
        text_lower = text.lower()
        scores = {}
        for emotion, keywords in EMOTION_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[emotion] = score
        return scores


class NarrativeAgent(BaseAgent):
    """وكيل بناء فصول الحياة والسرد"""
    name = "NarrativeAgent"

    def run(self, entries: List[Dict], context: Dict = None) -> Dict:
        if not entries:
            return {"life_chapters": []}

        sorted_entries = sorted(entries, key=lambda e: e.get("date", ""))
        chapters = []
        chunk_size = 4

        for i in range(0, len(sorted_entries), chunk_size):
            chunk = sorted_entries[i:i + chunk_size]
            all_themes = defaultdict(int)
            all_emotions = defaultdict(int)

            for e in chunk:
                for t, s in e.get("themes", {}).items():
                    all_themes[t] += s
                for emo, s in e.get("emotions", {}).items():
                    all_emotions[emo] += s

            dominant_themes = sorted(all_themes, key=all_themes.get, reverse=True)[:3]
            dominant_emotions = sorted(all_emotions, key=all_emotions.get, reverse=True)[:2]

            title = self._make_title(dominant_themes, dominant_emotions, chunk[0]["date"])

            chapters.append({
                "title": title,
                "start": chunk[0]["date"],
                "end": chunk[-1]["date"],
                "entry_count": len(chunk),
                "dominant_themes": dominant_themes,
                "dominant_emotions": dominant_emotions,
                "summary_hint": f"فترة يغلب عليها {', '.join(dominant_themes[:2]) if dominant_themes else 'تنوع'}"
            })

        return {"life_chapters": chapters}

    def _make_title(self, themes, emotions, start_date):
        if themes and emotions:
            return f"فصل {themes[0]} و{emotions[0]} — {start_date}"
        if themes:
            return f"فصل {themes[0]} — {start_date}"
        return f"فصل {start_date}"


class FutureSelfAgent(BaseAgent):
    """وكيل توليد رسائل من الذات المستقبلية + نقاط الاستمرارية"""
    name = "FutureSelfAgent"

    def run(self, entries: List[Dict], context: Dict = None) -> Dict:
        threads = (context or {}).get("threads", [])
        patterns = (context or {}).get("patterns", [])
        links = (context or {}).get("emotion_theme_links", [])

        messages = []
        continuity_points = []

        if threads:
            top = threads[0]
            messages.append({
                "from": "ذاتك المستقبلية",
                "based_on": top["theme"],
                "tone": "تأملي",
                "message": self._msg_for_thread(top)
            })

            if top.get("trend") == "rising":
                continuity_points.append({
                    "type": "تصاعد",
                    "theme": top["theme"],
                    "advice": f"خيط «{top['theme']}» في تصاعد. خصص وقتًا واعيًا له كل أسبوع قبل أن يتحول إلى ضغط."
                })
            elif top.get("trend") == "falling":
                continuity_points.append({
                    "type": "انحسار",
                    "theme": top["theme"],
                    "advice": f"خيط «{top['theme']}» يتراجع. هل هذا مقصود؟ أم أنك تتجاهل شيئًا مهمًا؟"
                })

        if len(threads) >= 2:
            messages.append({
                "from": "ذاتك المستقبلية",
                "based_on": "تداخل الخيوط",
                "tone": "استراتيجي",
                "message": self._cross_thread_msg(threads[:3])
            })

        if links:
            strongest = links[0]
            messages.append({
                "from": "ذاتك المستقبلية",
                "based_on": f"{strongest['emotion']} + {strongest['theme']}",
                "tone": "عاطفي",
                "message": f"لاحظتُ ارتباطًا متكررًا بين شعور «{strongest['emotion']}» وموضوع «{strongest['theme']}». "
                           f"في المستقبل، عندما يظهر أحدهما، تذكر أن الآخر قريب. الوعي بهذا الارتباط يمنحك حرية أكبر."
            })

        # نقطة استمرارية عامة
        if patterns:
            continuity_points.append({
                "type": "نمط عاطفي",
                "theme": patterns[0].get("emotion", "عام"),
                "advice": f"نمط «{patterns[0]['name']}» متكرر. اكتب عنه بوعي في المرة القادمة بدل أن تمر عليه مرور الكرام."
            })

        return {
            "future_messages": messages,
            "continuity_points": continuity_points
        }

    def _msg_for_thread(self, thread):
        templates = [
            f"خيط «{thread['theme']}» ظهر {thread['occurrences']} مرات منذ {thread['first_seen']}. "
            f"هذا ليس ظرفًا عابرًا — إنه جزء من هويتك الحالية. اسأل نفسك: هل ما زلت تتعامل معه بنفس الطريقة؟",

            f"من موقعي في المستقبل أرى أن «{thread['theme']}» كان محوريًا. "
            f"الاتجاه الحالي: {thread.get('trend', 'مستقر')}. استمر في مراقبته بصدق.",

            f"قوة خيط «{thread['theme']}» = {thread['strength']}. "
            f"لو كنت مكانك الآن لجعلتُ منه موضوع تأمل أسبوعي قصير."
        ]
        return random.choice(templates)

    def _cross_thread_msg(self, threads):
        names = " و ".join(t["theme"] for t in threads)
        return (
            f"حياتك ليست أحداثًا منفصلة. الخيوط المتداخلة ({names}) تتحدث مع بعضها. "
            f"في المستقبل ستدرك أن هذه المواضيع كانت تشكل نظامًا واحدًا. "
            f"حاول أن تكتب يومًا عن العلاقة الخفية بينها."
        )


class Orchestrator:
    """المنسق — يشغّل كل الوكلاء بالترتيب ويجمع النتائج"""

    def __init__(self):
        self.theme_agent = ThemeAgent()
        self.emotion_agent = EmotionAgent()
        self.narrative_agent = NarrativeAgent()
        self.future_agent = FutureSelfAgent()

    def run_full_analysis(self, entries: List[Dict]) -> Dict:
        if not entries:
            return {
                "threads": [],
                "patterns": [],
                "emotion_theme_links": [],
                "life_chapters": [],
                "future_messages": [],
                "continuity_points": [],
                "meta": {"agents_used": [], "entries_analyzed": 0}
            }

        # 1. Theme
        theme_result = self.theme_agent.run(entries)

        # 2. Emotion (يعتمد على themes التي أضافها ThemeAgent)
        emotion_result = self.emotion_agent.run(entries)

        # 3. Narrative
        narrative_result = self.narrative_agent.run(entries)

        # 4. Future Self (يحتاج نتائج السابقين)
        context = {
            "threads": theme_result["threads"],
            "patterns": emotion_result["patterns"],
            "emotion_theme_links": emotion_result["emotion_theme_links"]
        }
        future_result = self.future_agent.run(entries, context)

        return {
            "threads": theme_result["threads"],
            "theme_evolution": theme_result.get("theme_evolution", {}),
            "patterns": emotion_result["patterns"],
            "emotion_theme_links": emotion_result["emotion_theme_links"],
            "dominant_emotion": emotion_result.get("dominant_emotion"),
            "life_chapters": narrative_result["life_chapters"],
            "future_messages": future_result["future_messages"],
            "continuity_points": future_result["continuity_points"],
            "meta": {
                "agents_used": ["ThemeAgent", "EmotionAgent", "NarrativeAgent", "FutureSelfAgent"],
                "entries_analyzed": len(entries),
                "top_theme": theme_result.get("top_theme"),
                "analyzed_at": datetime.now().isoformat()
            }
        }
