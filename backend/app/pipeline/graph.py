"""Construção do grafo LangGraph + roteamento condicional + interrupt (HITL)."""
from __future__ import annotations

from langgraph.graph import END, StateGraph

from .state import PipelineState
from .nodes.slug import definir_slug
from .nodes.prompt import gerar_prompt
from .nodes.imagem import gerar_imagem
from .nodes.objeto import gerar_objeto
from .nodes.validar import validar_objeto
from .nodes.atlas import atualizar_atlas
from .nodes.deploy import deploy, notificar_falha


def rotear_apos_validacao(state: PipelineState) -> str:
    """Coração da automação: ok → atlas; falha&<max → regenera; senão → falha."""
    if state.get("validacao_ok"):
        return "atualizar_atlas"
    if state.get("tentativas_correcao", 0) >= state.get("max_tentativas", 3):
        return "notificar_falha"
    return "gerar_objeto"


def build_graph(checkpointer):
    b = StateGraph(PipelineState)

    b.add_node("definir_slug", definir_slug)
    b.add_node("gerar_prompt", gerar_prompt)
    b.add_node("gerar_imagem", gerar_imagem)
    b.add_node("gerar_objeto", gerar_objeto)
    b.add_node("validar_objeto", validar_objeto)
    b.add_node("atualizar_atlas", atualizar_atlas)
    b.add_node("deploy", deploy)
    b.add_node("notificar_falha", notificar_falha)

    b.set_entry_point("definir_slug")
    b.add_edge("definir_slug", "gerar_prompt")
    b.add_edge("gerar_prompt", "gerar_imagem")
    b.add_edge("gerar_imagem", "gerar_objeto")
    b.add_edge("gerar_objeto", "validar_objeto")

    b.add_conditional_edges(
        "validar_objeto",
        rotear_apos_validacao,
        {
            "atualizar_atlas": "atualizar_atlas",
            "gerar_objeto": "gerar_objeto",
            "notificar_falha": "notificar_falha",
        },
    )

    b.add_edge("atualizar_atlas", "deploy")
    b.add_edge("deploy", END)
    b.add_edge("notificar_falha", END)

    # HITL: pausa ANTES de publicar; /approve retoma com ainvoke(None, config).
    return b.compile(checkpointer=checkpointer, interrupt_before=["deploy"])
