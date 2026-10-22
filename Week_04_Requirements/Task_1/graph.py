"""LangGraph wiring of the requirements-refinement network.

    load_corpus -> extract -> cluster -> coverage_check -> write -> review --(issues)--> cluster
                                                                         \--(approved / limit)--> render
"""

from langgraph.graph import END, START, StateGraph

from nodes import (GraphState, cluster, coverage_check, extract, load_corpus, render, review,
                   route_after_review, write)


def build_graph():
    g = StateGraph(GraphState)
    g.add_node("load_corpus", load_corpus)        # deterministic
    g.add_node("extract", extract)                # LLM
    g.add_node("cluster", cluster)                # LLM
    g.add_node("coverage_check", coverage_check)  # deterministic
    g.add_node("write", write)                    # LLM
    g.add_node("review", review)                  # LLM
    g.add_node("render", render)                  # deterministic

    g.add_edge(START, "load_corpus")
    g.add_edge("load_corpus", "extract")
    g.add_edge("extract", "cluster")
    g.add_edge("cluster", "coverage_check")
    g.add_edge("coverage_check", "write")
    g.add_edge("write", "review")
    g.add_conditional_edges("review", route_after_review, {"cluster": "cluster", "render": "render"})
    g.add_edge("render", END)
    return g.compile()
