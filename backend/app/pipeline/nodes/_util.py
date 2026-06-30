"""Helpers compartilhados pelos nós."""
from __future__ import annotations

from typing import Any

from ...events import bus


def thread_id(config: Any) -> str:
    return config["configurable"]["thread_id"]


async def emit(config: Any, node: str, status: str, message: str = "", payload: dict | None = None):
    await bus.emit(thread_id(config), node, status, message, payload)
