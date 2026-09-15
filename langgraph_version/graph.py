"""
MirrorThread LangGraph — Orchestration Graph
============================================
Theme → Emotion → Narrative → FutureSelf → Finalize
مع إمكانية التفرع الشرطي لاحقًا.
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

try:
    from .state import MirrorState
    from .nodes import (
        theme_node,
        emotion_node,
        narrative_node,
        future_self_node,
        finalize_node,
    )
except ImportError:
    from state import MirrorState
    from nodes import (
        theme_node,
        emotion_node,
        narrative_node,
        future_self_node,
        finalize_node,
    )


def should_continue_after_theme(state: MirrorState) -> Literal["emotion", "end"]:
    """توجيه شرطي: إذا لم توجد مذكرات كافية نتوقف"""
    entries = state.get("entries", [])
    if len(entries) < 2:
        return "end"
    return "emotion"


def build_mirror_graph(checkpointer=None):
    """بناء الـGraph مع إمكانية إضافة checkpointer للـpersistence"""
    
    builder = StateGraph(MirrorState)

    # Nodes
    builder.add_node("theme", theme_node)
    builder.add_node("emotion", emotion_node)
    builder.add_node("narrative", narrative_node)
    builder.add_node("future_self", future_self_node)
    builder.add_node("finalize", finalize_node)

    # Edges
    builder.add_edge(START, "theme")
    
    # Conditional after theme
    builder.add_conditional_edges(
        "theme",
        should_continue_after_theme,
        {
            "emotion": "emotion",
            "end": END,
        }
    )
    
    builder.add_edge("emotion", "narrative")
    builder.add_edge("narrative", "future_self")
    builder.add_edge("future_self", "finalize")
    builder.add_edge("finalize", END)

    # Compile with optional checkpointer (enables resume / human-in-the-loop later)
    if checkpointer is None:
        checkpointer = MemorySaver()
    
    graph = builder.compile(checkpointer=checkpointer)
    return graph


def run_analysis(entries: list, thread_id: str = "default") -> dict:
    """تشغيل التحليل الكامل"""
    graph = build_mirror_graph()
    
    initial_state = {
        "entries": entries,
        "threads": [],
        "patterns": [],
        "emotion_theme_links": [],
        "life_chapters": [],
        "future_messages": [],
        "continuity_points": [],
        "dominant_emotion": None,
        "top_theme": None,
        "llm_insight": None,
        "current_step": "start",
        "errors": [],
        "analyzed_at": None,
    }
    
    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke(initial_state, config=config)
    return result
