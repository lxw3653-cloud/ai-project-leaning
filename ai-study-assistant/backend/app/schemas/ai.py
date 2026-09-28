"""AI 接口的请求与响应结构。"""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    """一轮对话消息。

    role 只允许 user / assistant：既符合真实对话的形态，
    也避免调用方塞进 system 消息把系统提示词覆盖掉。
    """

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    """AI 问答请求。"""

    question: str = Field(
        min_length=1,
        max_length=2000,
        description="用户的问题",
    )
    history: list[ChatMessage] = Field(
        default_factory=list,
        max_length=20,
        description="最近几轮对话，可选，用于让 AI 理解追问",
    )


class ChatResponse(BaseModel):
    """AI 问答响应。"""

    answer: str


class SummarizeRequest(BaseModel):
    """AI 笔记总结请求。"""

    content: str = Field(
        min_length=1,
        max_length=8000,
        description="需要总结的学习笔记，最长 8000 字",
    )

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str) -> str:
        """只有空白字符也算空，提前拦下来，顺便去掉首尾空白。"""
        stripped = value.strip()
        if not stripped:
            raise ValueError("笔记内容不能为空")
        return stripped


class SummarizeResponse(BaseModel):
    """AI 笔记总结响应。"""

    summary: str
    key_points: list[str]
