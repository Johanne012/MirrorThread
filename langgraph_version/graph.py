"""
MirrorThread LangGraph — Orchestration Graph
============================================
Theme → Emotion → Narrative → FutureSelf → VisionTech → Finalize
رؤية مستقبلية تدمج التقنية + التطوير + الطاقة
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
        vision_tech_node,
        finalize_node,
    )
except ImportError:
    from state import MirrorState
    from nodes import (
        theme_node,
        emotion_node,
        narrative_node,
        future_self_node,
        vision_tech_node,
        finalize_node,
    )


def should_continue_after_theme(state: MirrorState) -> Literal["emotion", "end"]:
    entries = state.get("entries", [])
    if len(entries) < 2:
        return "end"
    return "emotion"


def build_mirror_graph(checkpointer=None):
    builder = StateGraph(MirrorState)

    builder.add_node("theme", theme_node)
    builder.add_node("emotion", emotion_node)
    builder.add_node("narrative", narrative_node)
    builder.add_node("future_self", future_self_node)
    builder.add_node("vision_tech", vision_tech_node)
    builder.add_node("finalize", finalize_node)

    builder.add_edge(START, "theme")
    builder.add_conditional_edges(
        "theme",
        should_continue_after_theme,
        {"emotion": "emotion", "end": END},
    )
    builder.add_edge("emotion", "narrative")
    builder.add_edge("narrative", "future_self")
    builder.add_edge("future_self", "vision_tech")
    builder.add_edge("vision_tech", "finalize")
    builder.add_edge("finalize", END)

    if checkpointer is None:
        checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)


def run_analysis(entries: list, thread_id: str = "default") -> dict:
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
    return graph.invoke(initial_state, config=config)
