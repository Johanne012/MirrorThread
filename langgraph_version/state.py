"""
MirrorThread LangGraph State Definition
"""

from typing import Annotated, List, Dict, Any, Optional, TypedDict
from operator import add
from datetime import datetime


class Entry(TypedDict):
    id: str
    date: str
    content: str
    created_at: str


class Thread(TypedDict):
    id: str
    theme: str
    occurrences: int
    first_seen: str
    last_seen: str
    strength: int
    avg_intensity: float
    trend: str  # rising | falling | stable
    samples: List[str]


class EmotionPattern(TypedDict):
    type: str
    name: str
    emotion: str
    frequency: int
    intensity: float
    description: str


class EmotionThemeLink(TypedDict):
    emotion: str
    theme: str
    strength: int
    insight: str


class LifeChapter(TypedDict):
    title: str
    start: str
    end: str
    entry_count: int
    dominant_themes: List[str]
    dominant_emotions: List[str]
    summary_hint: str


class FutureMessage(TypedDict):
    from_: str  # "from" is reserved
    based_on: str
    tone: str
    message: str


class ContinuityPoint(TypedDict):
    type: str
    theme: str
    advice: str


class MirrorState(TypedDict):
    """الحالة المشتركة للـGraph"""
    # المدخلات
    entries: List[Entry]
    
    # نتائج الوكلاء (تُملأ تدريجيًا)
    threads: Annotated[List[Thread], add]
    patterns: Annotated[List[EmotionPattern], add]
    emotion_theme_links: Annotated[List[EmotionThemeLink], add]
    life_chapters: Annotated[List[LifeChapter], add]
    future_messages: Annotated[List[FutureMessage], add]
    continuity_points: Annotated[List[ContinuityPoint], add]
    
    # بيانات مساعدة
    dominant_emotion: Optional[str]
    top_theme: Optional[str]
    llm_insight: Optional[str]
    
    # بيانات تشغيل
    current_step: str
    errors: Annotated[List[str], add]
    analyzed_at: Optional[str]
