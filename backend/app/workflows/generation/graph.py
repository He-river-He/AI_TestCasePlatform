from langgraph.graph import StateGraph,START,END
from app.workflows.generation.state import GenerationState
from app.workflows.generation.nodes import (
    load_task,
    prepare_feature,
    retrieve_knowledge,
    generate_core_cases,
    generate_specialist_cases,
    validate_cases,
    retry_feature,
    persist_feature_cases,
    detect_task_duplicates,
    run_task_judge,
    build_task_report,
    finalize_task,
    route_after_generation,
    route_after_validation,
    route_next_feature
)
from app.workflows.generation.control import wrap_node

def build_generation_graph(checkpointer=None):
    builder = StateGraph(GenerationState)

    builder.add_node("load_task",wrap_node(load_task,skip_pause_check=True))
    builder.add_node("prepare_feature",wrap_node(prepare_feature))
    builder.add_node("retrieve_knowledge",wrap_node(retrieve_knowledge))
    builder.add_node("generate_core_cases",wrap_node(generate_core_cases))
    builder.add_node("generate_specialist_cases",wrap_node(generate_specialist_cases))
    builder.add_node("validate_cases",wrap_node(validate_cases))
    builder.add_node("retry_feature",wrap_node(retry_feature))
    builder.add_node("persist_feature_cases",wrap_node(persist_feature_cases))
    builder.add_node("detect_duplicates",wrap_node(detect_task_duplicates))
    builder.add_node("run_judge",wrap_node(run_task_judge))
    builder.add_node("build_report",wrap_node(build_task_report))
    builder.add_node("finalize_task",wrap_node(finalize_task))

    builder.add_edge(START,"load_task")
    builder.add_edge("load_task","prepare_feature")
    builder.add_edge("prepare_feature","retrieve_knowledge")
    builder.add_edge("retrieve_knowledge","generate_core_cases")
    builder.add_conditional_edges(
        "generate_core_cases",
        route_after_generation,
        {
            "continue":"generate_specialist_cases",
            "retry":"retry_feature",
        }
    )
    builder.add_conditional_edges(
        "generate_specialist_cases",
        route_after_generation,
        {
            "continue":"validate_cases",
            "retry":"retry_feature",
        }
    )
    builder.add_conditional_edges(
        "validate_cases",
        route_after_validation,
        {
            "retry":"retry_feature",
            "persist":"persist_feature_cases",
        }
    )
    builder.add_edge("retry_feature","generate_core_cases")
    builder.add_conditional_edges(
        "persist_feature_cases",
        route_next_feature,
        {
            "next":"prepare_feature",
            "quality":"detect_duplicates",
        }
    )
    builder.add_edge("detect_duplicates","run_judge")
    builder.add_edge("run_judge","build_report")
    builder.add_edge("build_report","finalize_task")
    builder.add_edge("finalize_task",END)

    return builder.compile(checkpointer=checkpointer)
    
# graph = build_generation_graph()
# if __name__ == "__main__":
#     print(graph.get_graph().draw_mermaid())