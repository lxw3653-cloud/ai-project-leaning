"""提示词模板。

想调整 AI 的回答风格或要求时改这里，不用动业务代码。
"""

SYSTEM_PROMPT = (
    "你是一位耐心的学习助手，面向正在自学的学生。回答要求：\n"
    "1. 用中文回答；\n"
    "2. 先给出结论，再解释原因和关键细节；\n"
    "3. 遇到抽象概念时，补一个生活中的类比帮助理解；\n"
    "4. 不确定的内容要明确说明，不要编造。"
)


def build_chat_messages(
    question: str,
    history: list[dict[str, str]],
) -> list[dict[str, str]]:
    """把系统提示词、历史对话和当前问题拼成模型需要的消息列表。"""
    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": question})
    return messages


SUMMARY_SYSTEM_PROMPT = (
    "你是一位帮学生整理笔记的助教。请把用户给出的学习笔记整理成便于复习的内容。\n"
    "要求：\n"
    "1. 用中文；\n"
    "2. summary 用 2 到 4 句话概括这段笔记在讲什么，突出主线，不要照抄原文；\n"
    "3. key_points 提炼 3 到 6 个核心知识点，每条一句话，适合考前快速回顾；\n"
    "4. 只输出 JSON，不要输出任何多余的文字或代码块标记，格式为：\n"
    '{"summary": "总结内容", "key_points": ["重点1", "重点2"]}'
)


def build_summary_messages(content: str) -> list[dict[str, str]]:
    """把用户粘贴的笔记包装成总结任务的消息列表。"""
    return [
        {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
        {"role": "user", "content": f"请整理下面这段学习笔记：\n\n{content}"},
    ]
