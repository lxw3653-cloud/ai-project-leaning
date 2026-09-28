"""AI 业务逻辑：组装消息、调用模型、返回结果。

路由层只负责收参数和返回响应，具体怎么问、问几轮历史都在这里决定。
"""

import json
import re

from app.ai.client import chat_completion
from app.ai.prompts import build_chat_messages, build_summary_messages

# 最多带上最近 10 条历史消息。上下文越长越贵越慢，还可能超出模型的上下文上限
MAX_HISTORY_MESSAGES = 10

# 有些模型会在 JSON 外面多说一句「好的，以下是结果：」，用它兜底
_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)


def _trim_history(history: list[dict[str, str]]) -> list[dict[str, str]]:
    """只保留最近几轮对话，避免上下文无限增长。"""
    return history[-MAX_HISTORY_MESSAGES:]


async def answer_question(question: str, history: list[dict[str, str]]) -> str:
    """回答一个学习问题，返回模型给出的文本。"""
    messages = build_chat_messages(question, _trim_history(history))
    return await chat_completion(messages)


def _parse_summary(raw: str) -> tuple[str, list[str]]:
    """把模型返回的文本解析成 (总结, 知识点列表)。

    模型不一定严格只输出 JSON，所以这里逐级降级：
    直接解析 → 从文本里抠出 JSON 块解析 → 都不行就把原文当总结。
    这样即使模型不听话，页面上也一定有内容可看，不会白屏。
    """
    data: object = None

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        matched = _JSON_BLOCK.search(raw)
        if matched:
            try:
                data = json.loads(matched.group(0))
            except json.JSONDecodeError:
                data = None

    if not isinstance(data, dict):
        return raw.strip(), []

    summary = data.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        summary = raw

    key_points: list[str] = []
    raw_points = data.get("key_points")
    if isinstance(raw_points, list):
        key_points = [
            item.strip() for item in raw_points if isinstance(item, str) and item.strip()
        ]
    elif isinstance(raw_points, str):
        # 模型偶尔会把数组写成一段带换行的文字
        key_points = [line.strip() for line in raw_points.splitlines() if line.strip()]

    return summary.strip(), key_points


async def summarize_notes(content: str) -> tuple[str, list[str]]:
    """把一段学习笔记整理成「简洁总结 + 核心知识点」。"""
    messages = build_summary_messages(content)
    raw = await chat_completion(messages)
    return _parse_summary(raw)
